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
*   **Servidor WSGI:** Gunicorn con trabajadores Uvicorn (Optimizado para Render)
*   **ORM:** SQLAlchemy 2.0
*   **Migraciones:** Alembic
*   **Base de Datos:** PostgreSQL (Alojada en Clever Cloud)
*   **Validación:** Pydantic V2
*   **Seguridad:** JWT (JSON Web Tokens) y Passlib (BCrypt)

### Frontend
*   **Framework:** Vue 3 (Composition API)
*   **Build Tool:** Vite
*   **Estado Global:** Pinia
*   **Enrutado:** Vue Router
*   **Estilos:** Tailwind CSS v4 (Configuración vía @theme en CSS)
*   **Cliente HTTP:** Axios
*   **Despliegue:** Vercel

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

## 5. Despliegue y Ambientes

La aplicación está configurada para operar en dos ambientes: **Develop** y **Producción**.

### Infraestructura
*   **Frontend:** Vercel (con `vercel.json` para soporte de SPA routing).
*   **Backend:** Render (PaaS).
*   **Base de Datos:** Clever Cloud (Instancias PostgreSQL independientes para Dev y Prod).

### Configuración de CORS
El backend está configurado para aceptar peticiones desde dominios específicos de Vercel (incluyendo dominios de preview y producción). La variable `CORS_ALLOWED_ORIGINS` gestiona esta lista.

### Optimización para Base de Datos Gratuita
Para evitar el error `FATAL: too many connections` en planes gratuitos, el backend utiliza:
*   **Pool Limiting:** `pool_size=2` y `max_overflow=0` en la configuración de SQLAlchemy.
*   **Single Worker:** Despliegue en Render con un solo worker de Gunicorn (`-w 1`) para minimizar el consumo de conexiones.

---

## 6. Estructura del Repositorio

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
│   │   ├── stores/         # Estados globales (Pinia)
│   │   └── views/          # Páginas principales
│   ├── vercel.json         # Configuración de despliegue Vercel
│   └── src/styles.css      # Tema de Tailwind v4 y estilos globales
└── README.md               # Documentación principal del proyecto
```

---

## 7. Reglas de Dominio e Integridad

*   **Propiedad de los datos:** Un usuario solo puede acceder a la información de los bebés que ha registrado personalmente.
*   **Contexto de Bebé Activo:** La UI opera siempre bajo el contexto de un "Bebé Activo".
*   **Validación de Ownership:** Cada petición al backend verifica rigurosamente que el recurso pertenezca al usuario autenticado.
*   **Integridad de Enums:** Los tipos de eventos (feeding, sleep, medication, etc.) están sincronizados entre Python y PostgreSQL. Al añadir nuevos tipos, se debe ejecutar `ALTER TYPE event_types ADD VALUE 'nuevo_valor'` en la base de datos.

---

## 8. Instalación y Configuración Local

### Requisitos Previos
*   Python 3.12+
*   Node.js 18+
*   PostgreSQL 15+

### Configuración del Backend
1.  Navegar a `backend/`, crear entorno virtual e instalar: `pip install -r requirements.txt`.
2.  Configurar `.env`:
    ```env
    DATABASE_URL=postgresql://usuario:password@localhost:5432/creciendo_db
    SECRET_KEY=tu_clave_secreta
    CORS_ALLOWED_ORIGINS=http://localhost:5173
    ```

### Configuración del Frontend
1.  Navegar a `frontend/` e instalar: `npm install`.
2.  Iniciar desarrollo: `npm run dev`.

---

## 9. Base de Datos y Migraciones
*   **Aplicar migraciones:** `alembic upgrade head`.
*   **Nota sobre Producción:** El comando de inicio en Render incluye la ejecución automática de migraciones: `alembic upgrade head && gunicorn...`

---

## 10. Estado Actual y Siguientes Pasos
El MVP está **totalmente operativo y desplegado**.

**Próximas mejoras:**
*   Implementación de gráficas de crecimiento (OMS).
*   Exportación de reportes mensuales en PDF.
*   Optimización de carga de imágenes de perfil.
