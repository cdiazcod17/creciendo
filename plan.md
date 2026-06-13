# Plan de Mejoras Técnicas — Creciendo App

> Análisis completo realizado el 2026-06-13. Mejoras organizadas por impacto y esfuerzo.

---

## Resumen ejecutivo

| Área | Problemas encontrados | Prioridad |
|------|-----------------------|-----------|
| Seguridad | 6 vulnerabilidades (rate limiting, logout real, token rotation, headers HTTP, echo SQL, stores sin reset) | CRÍTICA |
| Backend | 5 mejoras (paginación, N+1 query, query estilo antiguo, reintentos email, validador duplicado) | ALTA |
| Frontend | 6 mejoras (errores duplicados, lazy loading, ConfirmModal sin usar, imágenes, magic strings, estados error) | ALTA |
| Infraestructura | 4 mejoras (.env.example, GitHub Actions, ruff linting, .env en gitignore) | MEDIA |
| Testing | Cobertura baja, faltan tests de features críticas | MEDIA |

---

## BLOQUE 1 — SEGURIDAD

### 1.1 Rate Limiting en endpoints de autenticación

**Problema:** Login, register, forgot-password y reset-password no tienen protección contra fuerza bruta. Un atacante puede intentar miles de contraseñas sin restricción.

**Archivos a modificar:**
- `backend/app/main.py` — registrar el limiter
- `backend/app/api/routes/auth.py` — añadir decoradores

**Implementación:**
```python
# requirements.txt: añadir slowapi
pip install slowapi

# main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# auth.py — en cada endpoint sensible
@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    ...

@router.post("/register")
@limiter.limit("3/minute")
async def register(request: Request, ...):
    ...

@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(request: Request, ...):
    ...
```

---

### 1.2 Activar token_version en JWT (revocación de sesiones)

**Problema:** El campo `token_version` existe en el modelo `User` pero nunca se incluye en el JWT ni se valida. No hay forma de invalidar tokens emitidos.

**Archivos a modificar:**
- `backend/app/core/security.py` — incluir `token_version` en los claims
- `backend/app/api/deps/auth.py` — validar `token_version` al decodificar

**Implementación:**
```python
# security.py — al crear el access token
def create_access_token(data: dict, ...) -> str:
    to_encode = data.copy()
    # data debe incluir: {"sub": user.email, "token_version": user.token_version}
    ...

# deps/auth.py — al validar el token
payload = decode_token(token)
token_version = payload.get("token_version")
if token_version != user.token_version:
    raise credentials_exception  # Token fue invalidado
```

---

### 1.3 Logout real (invalidar token mediante token_version)

**Problema:** `POST /auth/logout` devuelve `{"msg": "Logout exitoso"}` sin invalidar el token. El token sigue siendo válido hasta que expira.

**Archivo a modificar:** `backend/app/api/routes/auth.py`

**Implementación:**
```python
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_active_user),
    user_repo: UserRepository = Depends(get_user_repository),
):
    current_user.token_version += 1
    user_repo.update(current_user)
    return {"msg": "Logout exitoso"}
```

---

### 1.4 Refresh token rotation

**Problema:** El refresh token nunca se rota. Si se filtra, puede usarse indefinidamente durante 7 días.

**Archivo a modificar:** `backend/app/services/auth_service.py` (método `refresh_token`)

**Implementación:**
```python
def refresh_token(self, refresh_token: str) -> dict:
    payload = decode_token(refresh_token)
    # ... validar tipo "refresh" ...

    user = self.user_repo.get_by_email(payload["sub"])
    user.token_version += 1  # Invalidar token anterior
    self.user_repo.update(user)

    new_access = create_access_token({"sub": user.email, "token_version": user.token_version})
    new_refresh = create_refresh_token({"sub": user.email, "token_version": user.token_version})
    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}
```

---

### 1.5 Headers de seguridad HTTP

**Problema:** El backend no envía headers de seguridad críticos (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`).

**Archivo a modificar:** `backend/app/main.py`

**Implementación:**
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

---

### 1.6 Corregir echo=True en sesión de base de datos

**Problema:** `backend/app/db/session.py` tiene `echo=True` — loguea TODAS las queries SQL en producción, incluyendo datos sensibles.

**Archivo a modificar:** `backend/app/db/session.py`

**Implementación:**
```python
# Cambiar:
engine = create_engine(DATABASE_URL, echo=True)

# Por:
engine = create_engine(DATABASE_URL, echo=settings.DEBUG)  # False en producción
```

---

### 1.7 Resetear todos los stores al hacer logout (Frontend)

**Problema:** `auth.js` solo limpia su propio estado al hacer logout. Los datos de bebés, eventos, citas y crecimiento permanecen en memoria.

**Archivo a modificar:** `frontend/src/components/AppNavbar.vue` (función `handleLogout`)

**Implementación:**
```javascript
async function handleLogout() {
  closeMobileMenu();
  await authStore.logout();

  // Limpiar todos los stores
  useBabiesStore().$reset();
  useEventsStore().$reset();
  useAppointmentsStore().$reset();
  useGrowthStore().$reset();

  router.push({ name: 'login' });
}
```

---

## BLOQUE 2 — BACKEND

### 2.1 Paginación consistente en todos los listados

**Problema:** `/babies`, `/growth-records` y `/appointments` devuelven todos los registros sin límite. Solo `/events` y `/health-notes` tienen paginación. Referencia del patrón correcto: `backend/app/api/routes/event.py`.

**Archivos a modificar:**
- `backend/app/api/routes/babies.py`
- `backend/app/api/routes/growth_record.py`
- `backend/app/api/routes/appointment.py`
- Sus respectivos services y repositories

**Implementación (patrón a replicar):**
```python
@router.get("/", response_model=list[BabyRead])
def list_babies(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    service: BabyService = Depends(get_baby_service),
):
    return service.list_babies(current_user.id, limit=limit, offset=offset)
```

---

### 2.2 Eliminar N+1 query en Dashboard

**Problema:** `dashboard_service.py` hace 1 query por bebé para obtener el último evento. Con N bebés → N+1 queries.

**Archivos a modificar:**
- `backend/app/repositories/event_repository.py` — nuevo método batch
- `backend/app/services/dashboard_service.py` — usar el nuevo método

**Implementación:**
```python
# event_repository.py — nuevo método
def get_latest_events_by_baby_ids(self, baby_ids: list[UUID]) -> dict[UUID, Event]:
    subq = (
        select(Event.baby_id, func.max(Event.occurred_at).label("latest"))
        .where(Event.baby_id.in_(baby_ids))
        .group_by(Event.baby_id)
        .subquery()
    )
    results = self.session.execute(
        select(Event)
        .join(subq, and_(Event.baby_id == subq.c.baby_id, Event.occurred_at == subq.c.latest))
    ).scalars().all()
    return {e.baby_id: e for e in results}

# dashboard_service.py — reemplazar el bucle
baby_ids = [b.id for b in babies]
latest_events = self.event_repo.get_latest_events_by_baby_ids(baby_ids)
# Usar: latest_events.get(baby.id) en lugar del bucle anterior
```

---

### 2.3 Migrar session.query() a select() (SQLAlchemy 2.0)

**Problema:** `baby_service.py` usa sintaxis deprecada de SQLAlchemy 1.x.

**Archivo a modificar:** `backend/app/services/baby_service.py`

**Implementación:**
```python
# Cambiar:
replacement_baby = (
    self.session.query(Baby)
    .filter(Baby.user_id == current_user.id, Baby.id != baby.id)
    .order_by(Baby.created_at.asc())
    .first()
)

# Por:
replacement_baby = self.session.execute(
    select(Baby)
    .where(Baby.user_id == current_user.id, Baby.id != baby.id)
    .order_by(Baby.created_at.asc())
    .limit(1)
).scalar_one_or_none()
```

---

### 2.4 Reintentos en email_service

**Problema:** Si Resend falla temporalmente, el reset de contraseña falla sin reintentos.

**Archivo a modificar:** `backend/app/services/email_service.py`

**Implementación:**
```python
# requirements.txt: añadir tenacity
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _send_via_resend(self, params: dict) -> None:
    resend.Emails.send(params)

def send_password_reset_email(self, email: str, token: str) -> None:
    params = { ... }
    self._send_via_resend(params)
```

---

### 2.5 Validador de contraseña reutilizable

**Problema:** La lógica de validación de contraseña está duplicada en `UserRegister` y `ResetPasswordRequest`.

**Archivo a modificar:** `backend/app/schemas/user.py`

**Implementación:**
```python
def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not any(c.isupper() for c in password):
        raise ValueError("La contraseña debe contener al menos una mayúscula")
    if not any(c.islower() for c in password):
        raise ValueError("La contraseña debe contener al menos una minúscula")
    if not any(c.isdigit() for c in password):
        raise ValueError("La contraseña debe contener al menos un número")
    return password

class UserRegister(BaseModel):
    password: Annotated[str, AfterValidator(validate_password_strength)]

class ResetPasswordRequest(BaseModel):
    new_password: Annotated[str, AfterValidator(validate_password_strength)]
```

---

## BLOQUE 3 — FRONTEND

### 3.1 Composable centralizado de manejo de errores

**Problema:** `normalizeApiError()` o `normalizeError()` está duplicada con variaciones en los 5 stores.

**Archivo a crear:** `frontend/src/composables/useErrorHandler.js`

**Implementación:**
```javascript
// frontend/src/composables/useErrorHandler.js
export function useErrorHandler() {
  function normalizeError(err, fallback = "Ha ocurrido un error inesperado") {
    const detail = err?.response?.data?.detail;
    if (Array.isArray(detail)) {
      return detail.map(d => d.msg).join(", ");
    }
    return detail || err?.message || fallback;
  }

  return { normalizeError };
}

// En cada store (reemplazar la función local):
import { useErrorHandler } from '@/composables/useErrorHandler';
const { normalizeError } = useErrorHandler();
```

---

### 3.2 Lazy loading de rutas estáticas

**Problema:** `LoginView`, `RegisterView`, `HomeView` y `NotFoundView` se importan estáticamente aumentando el bundle inicial.

**Archivo a modificar:** `frontend/src/router/index.js`

**Implementación:**
```javascript
// Cambiar imports estáticos:
import LoginView from '../views/LoginView.vue'        // ❌
import RegisterView from '../views/RegisterView.vue'  // ❌
import HomeView from '@/views/HomeView.vue'            // ❌
import NotFoundView from '@/views/NotFoundView.vue'   // ❌

// Por imports dinámicos:
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const HomeView = () => import('@/views/HomeView.vue')
const NotFoundView = () => import('@/views/NotFoundView.vue')
```

---

### 3.3 Usar ConfirmModal en lugar de window.confirm()

**Problema:** Se usa `window.confirm()` en 4 vistas para confirmar borrados. El componente `ConfirmModal.vue` ya existe pero no se usa.

**Archivos a modificar:**
- `frontend/src/views/DashboardView.vue`
- `frontend/src/views/BabyDetailsView.vue`
- `frontend/src/views/EventsView.vue`
- `frontend/src/views/GrowthView.vue`

**Implementación (patrón a aplicar en cada vista):**
```vue
<script setup>
import ConfirmModal from '@/components/ConfirmModal.vue';
const showConfirm = ref(false);
const pendingDeleteId = ref(null);

function requestDelete(id) {
  pendingDeleteId.value = id;
  showConfirm.value = true;
}

async function confirmDelete() {
  await store.deleteItem(pendingDeleteId.value);
  showConfirm.value = false;
}
</script>

<template>
  <ConfirmModal
    :open="showConfirm"
    title="Confirmar eliminación"
    message="Esta acción no se puede deshacer."
    @confirm="confirmDelete"
    @cancel="showConfirm = false"
  />
</template>
```

---

### 3.4 Optimizar imágenes de bebés

**Problema:** Las fotos no tienen `loading="lazy"`, ni dimensiones definidas (causa Cumulative Layout Shift), ni fallback si la imagen falla.

**Archivos a modificar:** `frontend/src/views/DashboardView.vue`, `frontend/src/views/BabiesView.vue`

**Implementación:**
```vue
<img
  v-if="baby.photo_url"
  :src="baby.photo_url"
  :alt="baby.name"
  loading="lazy"
  width="56"
  height="56"
  class="h-14 w-14 object-cover rounded-full"
  @error="(e) => e.target.style.display = 'none'"
/>
<div v-else class="h-14 w-14 rounded-full bg-leaf/20 flex items-center justify-center">
  <span class="text-leaf font-bold text-xl">{{ baby.name[0] }}</span>
</div>
```

---

### 3.5 Constantes para magic strings

**Problema:** Keys de localStorage (`"access_token"`, `"refresh_token"`, `"user"`) y números (`15`, `10000`) están hardcodeados en múltiples archivos.

**Archivo a crear:** `frontend/src/constants/index.js`

**Implementación:**
```javascript
export const STORAGE_KEYS = {
  ACCESS_TOKEN: "access_token",
  REFRESH_TOKEN: "refresh_token",
  USER: "user",
};

export const API_LIMITS = {
  EVENTS_BATCH: 15,
  PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
};

export const TIMEOUT_MS = {
  REQUEST: 10_000,
  TOAST_INFO: 2_800,
  TOAST_ERROR: 4_200,
};
```

---

### 3.6 Estado de error en DashboardView

**Problema:** `DashboardView.vue` muestra spinner de carga pero no tiene bloque `v-else-if` para errores. Si la API falla, muestra pantalla vacía sin feedback. `EventsView.vue` tiene el patrón correcto.

**Archivo a modificar:** `frontend/src/views/DashboardView.vue`

**Implementación (siguiendo el patrón de EventsView.vue):**
```vue
<div v-if="babiesStore.isLoading" class="flex justify-center py-12">
  <!-- spinner actual -->
</div>

<div v-else-if="babiesStore.error" class="rounded-3xl border border-red-200 bg-red-50 p-6 text-center">
  <p class="text-red-600">{{ babiesStore.error }}</p>
  <button @click="babiesStore.fetchBabies()" class="mt-4 text-sm text-red-500 underline">
    Reintentar
  </button>
</div>

<div v-else>
  <!-- contenido actual -->
</div>
```

---

## BLOQUE 4 — INFRAESTRUCTURA

### 4.1 Crear .env.example para backend

**Problema:** No hay template de variables de entorno. Un desarrollador nuevo no sabe qué configurar.

**Archivo a crear:** `backend/.env.example`

```bash
# Seguridad
SECRET_KEY=your-secret-key-here-min-32-chars

# Base de datos
DATABASE_URL=postgresql://user:password@host:5432/dbname

# CORS — URLs separadas por coma
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://tu-app.vercel.app

# Email (Resend)
RESEND_API_KEY=re_xxxxxxxxxxxx
MAIL_FROM=noreply@tudominio.com

# Frontend
FRONTEND_URL=http://localhost:5173

# Desarrollo
DEBUG=false
```

---

### 4.2 GitHub Actions — CI básico

**Problema:** No hay CI/CD. Los tests no se ejecutan automáticamente en PRs.

**Archivo a crear:** `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
        working-directory: backend
      - name: Run tests
        run: pytest tests/ -v
        working-directory: backend

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - name: Install dependencies
        run: npm ci
        working-directory: frontend
      - name: Lint
        run: npm run lint
        working-directory: frontend
```

---

### 4.3 Configurar ruff para linting Python

**Problema:** No hay linter Python configurado. Inconsistencias de estilo no se detectan.

**Archivo a crear:** `backend/pyproject.toml`

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

**Agregar a `requirements.txt`:**
```
ruff>=0.4.0
```

---

### 4.4 Sacar .env del frontend de git

**Problema:** `frontend/.env` está siendo trackeado por git.

**Cambios:**
1. Añadir a `.gitignore`: `frontend/.env`
2. Crear `frontend/.env.example`:
```bash
# URL del backend
VITE_API_BASE_URL=http://localhost:8000
```
3. Ejecutar: `git rm --cached frontend/.env`

---

## BLOQUE 5 — TESTING

**Estado actual:** 4 archivos de test (auth, ownership, active_baby, password_reset). Solo happy paths.

**Tests prioritarios a añadir:**

| Archivo | Casos a cubrir |
|---------|---------------|
| `tests/test_events.py` | CRUD eventos, filtro por tipo, paginación, ownership |
| `tests/test_growth.py` | Crear/listar registros, validación campos numéricos |
| `tests/test_health_notes.py` | Soft delete funciona, notas borradas no aparecen |
| `tests/test_appointments.py` | Endpoint next appointment, cambio de status |
| `tests/test_dashboard.py` | Respuesta correcta con múltiples bebés |

**Herramientas a añadir:**
```bash
# requirements.txt
pytest-cov>=5.0.0

# Ejecutar con cobertura
pytest --cov=app --cov-report=html tests/
# Target: >70% cobertura
```

---

## Orden de implementación recomendado

| # | Mejora | Esfuerzo | Impacto |
|---|--------|----------|---------|
| 1 | 1.6 echo=False en BD | 1 línea | Crítico |
| 2 | 1.3 Logout real | ~10 líneas | Alto |
| 3 | 1.2 Activar token_version | ~15 líneas | Alto |
| 4 | 1.7 Reset stores al logout | ~10 líneas | Alto |
| 5 | 4.1 Crear .env.example | 5 min | Medio |
| 6 | 4.4 Sacar .env de git | 5 min | Medio |
| 7 | 3.6 Estado error Dashboard | ~15 líneas | Medio |
| 8 | 3.3 ConfirmModal en vistas | ~20 líneas x4 | Medio |
| 9 | 3.1 Composable errores | ~30 líneas | Medio |
| 10 | 3.2 Lazy loading rutas | 4 líneas | Bajo-Medio |
| 11 | 2.1 Paginación consistente | ~30 líneas x3 | Alto |
| 12 | 1.1 Rate limiting | ~20 líneas | Crítico |
| 13 | 2.2 N+1 query dashboard | ~25 líneas | Medio |
| 14 | 4.2 GitHub Actions | ~40 líneas yaml | Medio |
| 15 | 2.4 Reintentos email | ~10 líneas | Bajo |
| 16 | 1.4 Refresh token rotation | ~20 líneas | Alto |
| 17 | 1.5 Security headers | ~10 líneas | Medio |
| 18 | 5.x Tests adicionales | ~200 líneas | Medio |

---

## Verificación final

```bash
# Backend
cd backend
pytest --cov=app --cov-report=term-missing tests/

# Frontend  
cd frontend
npm run lint
npm run build  # Verificar que no hay errores de build

# Test de flujo completo (manual)
# 1. Registro de nuevo usuario
# 2. Login → verificar tokens en localStorage
# 3. Crear bebé → verificar ownership
# 4. Registrar evento → verificar paginación
# 5. Logout → verificar que tokens se invalidan
# 6. Intentar usar token anterior → debe devolver 401
```
