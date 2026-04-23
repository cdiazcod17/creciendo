# Creciendo

**Creciendo** es una aplicación web diseñada para el seguimiento integral de bebés desde su nacimiento hasta aproximadamente los 2 años de edad. Este proyecto es un MVP (Producto Mínimo Viable) orientado a un producto real, enfocado en ofrecer a los padres y cuidadores una herramienta robusta y segura para registrar rutinas, hitos de crecimiento y salud.

---

## 1. Objetivo del Producto
Facilitar la gestión de la información del desarrollo infantil en un entorno multi-bebé, permitiendo centralizar registros de alimentación, sueño, higiene, citas médicas y parámetros de crecimiento bajo una arquitectura segura que garantiza la privacidad y la integridad de los datos.

## 2. Características del MVP
*   **Gestión Multi-perfil:** Registro y administración de uno o más bebés bajo una misma cuenta de usuario.
*   **Bebé Activo:** Sistema de contexto global que permite cambiar entre perfiles de bebés manteniendo la persistencia en toda la interfaz.
*   **Registro de Eventos:** Seguimiento detallado de rutinas diarias (sueño, alimentación, pañales, medicinas y notas).
*   **Agenda Médica:** Gestión de citas y consultas médicas.
*   **Control de Crecimiento:** Registro de peso, talla y perímetro cefálico.
*   **Panel de Control (Dashboard):** Vista resumida del estado actual, últimos eventos y próximas actividades del bebé seleccionado.

## 3. Stack Tecnológico

### Backend
*   **Framework:** FastAPI (Python 3.12+)
*   **ORM:** SQLAlchemy 2.0
*   **Migraciones:** Alembic
*   **Base de Datos:** PostgreSQL
*   **Validación:** Pydantic V2
*   **Seguridad:** JWT (JSON Web Tokens) y Passlib (BCrypt)

### Frontend
*   **Framework:** Vue 3 (Composition API)
*   **Build Tool:** Vite
*   **Estado Global:** Pinia
*   **Enrutado:** Vue Router
*   **Estilos:** Tailwind CSS
*   **Cliente HTTP:** Axios
*   **Componentes UI:** Vue Toastification, Font Awesome

---

## 4. Arquitectura General

El proyecto sigue una separación clara de responsabilidades para facilitar el mantenimiento y la escalabilidad.

### Backend: Arquitectura por Capas
1.  **Routers:** Definición de endpoints y manejo de peticiones HTTP.
2.  **Services:** Contienen la lógica de negocio y coordinación de tareas.
3.  **Repositories:** Encapsulan el acceso a datos y consultas a la base de datos.
4.  **Schemas:** Modelos Pydantic para validación de entrada/salida (DTOs).
5.  **Models:** Definición de entidades de base de datos (SQLAlchemy).

### Frontend: Flujo de Datos
1.  **Views:** Componentes de página que interactúan exclusivamente con los stores.
2.  **Stores (Pinia):** Gestión del estado global y lógica de sincronización con el backend.
3.  **Services:** Clientes HTTP que realizan las llamadas a la API mediante Axios.

---

## 5. Estructura del Repositorio

```bash
creciendo-app/
├── backend/                # API y lógica del servidor
│   ├── app/
│   │   ├── api/            # Rutas y dependencias de FastAPI
│   │   ├── core/           # Configuración, seguridad y enums
│   │   ├── db/             # Sesión y conexión a base de datos
│   │   ├── models/         # Entidades de SQLAlchemy
│   │   ├── repositories/   # Capa de persistencia
│   │   ├── schemas/        # Modelos de validación (Pydantic)
│   │   └── services/       # Lógica de negocio
│   ├── alembic/            # Migraciones de base de datos
│   ├── tests/              # Pruebas unitarias y de integración
│   └── main.py             # Punto de entrada de la aplicación
├── frontend/               # Aplicación Vue.js
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── composables/    # Lógica reactiva extraída
│   │   ├── router/         # Configuración de Vue Router
│   │   ├── services/       # Llamadas a la API (Axios)
│   │   ├── stores/         # Estados globales (Pinia)
│   │   └── views/          # Páginas principales
│   └── tailwind.config.js  # Configuración de estilos
└── README.md               # Documentación principal del proyecto
```

---

## 6. Reglas de Dominio e Integridad

*   **Propiedad de los datos:** Un usuario solo puede acceder a la información de los bebés que ha registrado personalmente.
*   **Contexto de Bebé Activo:** La UI opera siempre bajo el contexto de un "Bebé Activo". Si un usuario no tiene bebés, el sistema le guiará para crear el primero.
*   **Validación de Ownership:** Cada petición al backend que involucre un `baby_id` o recursos asociados (eventos, citas) verifica rigurosamente que el recurso pertenezca al usuario autenticado.
*   **Persistencia de Selección:** El bebé activo seleccionado persiste entre sesiones y a través de la navegación entre los diferentes módulos.

---

## 7. Instalación y Configuración Local

### Requisitos Previos
*   Python 3.12+
*   Node.js 18+
*   PostgreSQL 15+

### Configuración del Backend

1.  Navegar a la carpeta de backend:
    ```bash
    cd backend
    ```
2.  Crear y activar entorno virtual:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/macOS:
    source .venv/bin/activate
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configurar variables de entorno (archivo `.env`):
    ```env
    SECRET_KEY=tu_clave_secreta_aqui
    DATABASE_URL=postgresql://usuario:password@localhost:5432/creciendo_db
    ```

### Configuración del Frontend

1.  Navegar a la carpeta de frontend:
    ```bash
    cd frontend
    ```
2.  Instalar dependencias:
    ```bash
    npm install
    ```

---

## 8. Ejecución del Proyecto

### Iniciar Backend
Desde la carpeta `backend`:
```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

### Iniciar Frontend
Desde la carpeta `frontend`:
```bash
npm run dev
```
La aplicación estará disponible en `http://localhost:5173`.

---

## 9. Base de Datos y Migraciones
El proyecto utiliza **Alembic** para gestionar el esquema de la base de datos de forma evolutiva.

*   **Crear una nueva migración:**
    ```bash
    alembic revision --autogenerate -m "descripción del cambio"
    ```
*   **Aplicar migraciones:**
    ```bash
    alembic upgrade head
    ```

## 10. Testing
Se incluyen pruebas automatizadas para el backend utilizando `pytest`, con especial énfasis en seguridad y validación de propiedad.

*   **Ejecutar pruebas:**
    ```bash
    cd backend
    pytest
    ```
*   **Cobertura actual:** Autenticación de usuarios, validación de pertenencia de recursos (Ownership) y sincronización del bebé activo.

---

## 11. Estado Actual y Siguientes Pasos
El proyecto se encuentra en una fase avanzada de su MVP. Los módulos de **Autenticación**, **Dashboard**, **Bebés**, **Citas** y **Eventos** están operativos y sincronizados.

**Próximas mejoras:**
*   Implementación de gráficas de crecimiento basadas en estándares de la OMS.
*   Módulo extendido de notas de salud e historial de vacunas.
*   Exportación de reportes mensuales en formato PDF.
*   Optimización del sistema de gestión de imágenes de perfil.
*   Módulo de Hitos del desarrollo.

---

## 12. Contribución
Para mantener la integridad y calidad del código:
1.  Crear ramas descriptivas: `feature/nombre-funcionalidad` o `fix/descripcion-error`.
2.  Validar que `npm run lint` no devuelva errores antes de realizar un Commit.
3.  Asegurarse de que las nuevas funcionalidades respeten el flujo `router -> service -> repository`.

