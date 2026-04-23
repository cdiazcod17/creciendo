✦ Creciendo

  Creciendo es una aplicación web diseñada para el seguimiento integral de bebés desde su nacimiento hasta aproximadamente los 2 años de edad. Esta orientado a un
  producto real, enfocado en ofrecer a los padres y cuidadores una herramienta robusta y segura para registrar rutinas, hitos de crecimiento y salud.

  ---

  1. Objetivo del Producto
  Facilitar la gestión de la información del desarrollo infantil en un entorno multi-bebé, permitiendo centralizar registros de alimentación, sueño, higiene, citas médicas y parámetros de crecimiento bajo una
  arquitectura segura que garantiza la privacidad y la integridad de los datos.

  2. Características del Producto
   * Gestión Multi-perfil: Registro y administración de uno o más bebés bajo una misma cuenta de usuario.
   * Bebé Activo: Sistema de contexto global que permite cambiar entre perfiles de bebés manteniendo la persistencia en toda la interfaz.
   * Registro de Eventos: Seguimiento detallado de rutinas diarias (sueño, alimentación, pañales, medicinas y notas).
   * Agenda Médica: Gestión de citas y consultas pendientes.
   * Control de Crecimiento: Registro de peso, talla y perímetro cefálico.
   * Panel de Control (Dashboard): Vista resumida del estado actual, últimos eventos y próximas actividades del bebé seleccionado.

  3. Stack Tecnológico

  Backend
   * Framework: FastAPI (Python 3.12+)
   * ORM: SQLAlchemy 2.0
   * Migraciones: Alembic
   * Base de Datos: PostgreSQL
   * Validación: Pydantic V2
   * Seguridad: JWT (JSON Web Tokens) y Passlib (BCrypt)

  Frontend
   * Framework: Vue 3 (Composition API)
   * Build Tool: Vite
   * Estado Global: Pinia
   * Enrutado: Vue Router
   * Estilos: Tailwind CSS
   * Cliente HTTP: Axios
   * Componentes UI: Vue Toastification, Font Awesome

  ---

  4. Arquitectura General

  El proyecto sigue una separación clara de responsabilidades para facilitar el mantenimiento y la escalabilidad.

  Backend: Arquitectura por Capas
   1. Routers: Definición de endpoints y manejo de peticiones HTTP.
   2. Services: Contienen la lógica de negocio y coordinación de tareas.
   3. Repositories: Encapsulan el acceso a datos y consultas a la base de datos.
   4. Schemas: Modelos Pydantic para validación de entrada/salida (DTOs).
   5. Models: Definición de entidades de SQLAlchemy.

  Frontend: Flujo de Datos
   1. Views: Componentes de página que interactúan con los stores.
   2. Stores (Pinia): Gestión del estado global y lógica de sincronización.
   3. Services: Clientes HTTP que realizan las llamadas a la API mediante Axios.

  ---


  5. Estructura del Repositorio
    1 creciendo-app/
    2 ├── backend/                # API y lógica de servidor
    3 │   ├── app/
    4 │   │   ├── api/            # Rutas y dependencias de FastAPI
    5 │   │   ├── core/           # Configuración, seguridad y enums
    6 │   │   ├── db/             # Sesión y base de datos
    7 │   │   ├── models/         # Entidades de SQLAlchemy
    8 │   │   ├── repositories/   # Capa de persistencia
    9 │   │   ├── schemas/        # Modelos de validación (Pydantic)
   10 │   │   └── services/       # Lógica de negocio
   11 │   ├── alembic/            # Migraciones de base de datos
   12 │   ├── tests/              # Pruebas unitarias y de integración
   13 │   └── main.py             # Punto de entrada de la aplicación
   14 ├── frontend/               # Aplicación Vue.js
   15 │   ├── src/
   16 │   │   ├── components/     # Componentes reutilizables
   17 │   │   ├── composables/    # Lógica reactiva extraída
   18 │   │   ├── router/         # Configuración de Vue Router
   19 │   │   ├── services/       # Llamadas a la API
   20 │   │   ├── stores/         # Estados globales (Pinia)
   21 │   │   └── views/          # Páginas principales
   22 │   └── tailwind.config.js  # Configuración de estilos
  ---

  6. Reglas de Dominio e Integridad

   * Propiedad de los datos: Un usuario solo puede acceder a la información de los bebés que ha registrado.
   * Contexto de Bebé Activo: La UI debe operar siempre bajo el contexto de un "Bebé Activo". Si un usuario no tiene bebés, el sistema debe guiarlo a crear el primero.
   * Validación de Ownership: Cada petición al backend que involucre un baby_id o recursos asociados (eventos, citas) debe verificar que el recurso pertenece al usuario autenticado.
   * Persistencia de Selección: El bebé activo seleccionado por el usuario debe persistir entre sesiones y navegación de módulos.

  ---

  7. Instalación y Configuración Local

  Requisitos Previos
   * Python 3.12+
   * Node.js 18+
   * PostgreSQL 15+

  Configuración del Backend

   1. Navegar a la carpeta de backend:
   1     cd backend
   2. Crear y activar entorno virtual:

   1     python -m venv .venv
   2     # Windows:
   3     .venv\Scripts\activate
   4     # Linux/macOS:
   5     source .venv/bin/activate
   3. Instalar dependencias:

   1     pip install -r requirements.txt
   4. Configurar variables de entorno (.env):

   1     SECRET_KEY=tu_clave_secreta_aqui
   2     DATABASE_URL=postgresql://usuario:password@localhost:5432/creciendo_db

  Configuración del Frontend

   1. Navegar a la carpeta de frontend:
   1     cd frontend
   2. Instalar dependencias:
   1     npm install

  ---

  8. Ejecución del Proyecto

  Iniciar Backend
  Desde la carpeta backend:

   1 uvicorn app.main:app --reload
  La API estará disponible en http://localhost:8000 y la documentación interactiva en /docs.

  Iniciar Frontend
  Desde la carpeta frontend:
   1 npm run dev
  La aplicación estará disponible en http://localhost:5173.

  ---

  9. Base de Datos y Migraciones
  El proyecto utiliza Alembic para gestionar el esquema de la base de datos de forma evolutiva.

   * Crear una nueva migración:

   1     alembic revision --autogenerate -m "descripción del cambio"
   * Aplicar migraciones:

   1     alembic upgrade head

  10. Testing
  Se incluyen pruebas automatizadas para el backend utilizando pytest. El enfoque principal es la validación de seguridad y ownership.

   * Ejecutar pruebas:

   1     cd backend
   2     pytest
   * Cobertura actual: Autenticación de usuarios, validación de pertenencia de recursos (Ownership) y sincronización del bebé activo.

  ---

  11. Estado Actual y Siguientes Pasos
  El proyecto se encuentra en una fase avanzada de su MVP, con los módulos de Autenticación, Dashboard, Bebés, Citas y Eventos operativos.

  Próximas mejoras:
   * Implementación de gráficas de crecimiento (curvas de la OMS).
   * Módulo extendido de notas de salud.
   * Exportación de reportes en PDF para pediatras.
   * Optimización de carga de imágenes para fotos de perfil.
   * Modulo Hitos de bebe

  ---

  12. Contribución
  Para mantener la calidad del código, se recomienda:
   1. Crear ramas descriptivas (feature/nombre-funcionalidad o fix/descripcion-error).
   2. Asegurarse de que npm run lint no devuelva errores antes de enviar un PR.
   3. Asegurarse de que todos los servicios y stores sigan el patrón de diseño establecido.

  ---
