# User Registration & Management API (GraphQL)

¡Bienvenido!  
¿Quieres ver la demo en vivo? Visita [http://35.192.42.29:8000/](http://35.192.42.29:8000/) para el formulario de registro y [http://35.192.42.29:8000/graphql/](http://35.192.42.29:8000/graphql/) para interactuar con la API GraphQL.

## Descripción

Este proyecto es una API REST (GraphQL) desarrollada en Django que permite el registro y la gestión de usuarios. Se utilizan Graphene-Django para implementar el esquema GraphQL, y se incluye un formulario (HTML/CSS/JS) para interactuar con la API. El proyecto está dockerizado para facilitar su despliegue y ejecución.

## Tecnologías

- **Backend:**  
  - Django (versión >= 4.2)  
  - Graphene-Django (para la API GraphQL)  
  - bcrypt (para el hash de contraseñas)  
- **Frontend:**  
  - HTML, CSS (Bootstrap 5) y JavaScript (vanilla)  
- **Contenedorización:**  
  - Docker y Docker Compose (para ejecutar la aplicación en un entorno aislado)  
- **Base de datos:**  
  - SQLite (por defecto, aunque se puede adaptar a PostgreSQL u otra DB)  

## Estructura del Proyecto

El proyecto se organiza de la siguiente manera:

- **core/**  
  - **manage.py:** Script de administración de Django.  
  - **core/:**  
    - **settings.py:** Configuración del proyecto (base de datos, middleware, etc.).  
    - **urls.py:** Rutas (endpoints) de la API (por ejemplo, `/graphql`).  
    - **wsgi.py** y **asgi.py:** Configuración para WSGI/ASGI (despliegue).  
  - **User/:**  
    - **models.py:** Define los modelos (UserApp_TB, UserDocument_TB, TypeDocument_TB, Country_TB, ContactInfo_TB, etc.).  
    - **schema.py:** Implementa los tipos GraphQL (DjangoObjectType) y las mutaciones (por ejemplo, para crear o actualizar usuarios). Aca se implementa el corazon de la API con graphQL.  
    - **templates/User/:**  
      - **formulario.html:** Interfaz de usuario (HTML) que se conecta a la API.  
      - **formulario.css:** Estilos (CSS) para el formulario.  
      - **formulario.js:** Script (JS) que maneja la interacción (por ejemplo, validación de campos numéricos, toggle de contraseña, etc.).  
- **requirements.txt:** Lista de dependencias (Django, graphene-django, bcrypt, etc.).  
- **Dockerfile:** Instrucciones para construir la imagen Docker (basada en Python 3.11-slim).  
- **docker-compose.yml:** Configuración para levantar el contenedor (volúmenes, puertos, etc.).  

## Schemas GraphQL

El archivo `core/User/schema.py` define los tipos y mutaciones de GraphQL. Por ejemplo:

- **Tipos:**  
  - Se utilizan `DjangoObjectType` para exponer los modelos (UserApp_TB, UserDocument_TB, etc.) como tipos GraphQL.  
- **Mutations:**  
  - Se implementan mutaciones (por ejemplo, `CreateUser`, `UpdateUser`, etc.) que permiten crear, actualizar o eliminar registros.  
- **Autenticación:**  
  - Se utiliza bcrypt para el hash de contraseñas y se manejan errores (por ejemplo, con `GraphQLError`) en caso de datos inválidos.  

## Ejemplos de Peticiones GraphQL

A continuación se muestran algunos ejemplos de peticiones que puedes realizar en el endpoint [http://35.192.42.29:8000/graphql/](http://35.192.42.29:8000/graphql/) (o en tu entorno local si lo ejecutas con runserver o Docker):

### 1. Crear un Usuario (CreateUser)

```graphql
mutation {
  createUser(input: {
    username: "johndoe",
    password: "secret",
    email: "johndoe@example.com",
    firstName: "John",
    lastName: "Doe",
    military: true,
    temporal: false,
    documentNumber: "123456",
    documentType: 1,
    placeOfExpedition: "Ciudad",
    dateOfExpedition: "2023-01-01",
    phone: "123456789",
    cellPhone: "987654321",
    address: "Calle 1",
    city: "Ciudad",
    country: 1,
    emergencyName: "Jane Doe",
    emergencyPhone: "555555555"
  }) {
    user {
      id
      username
      email
    }
    ok
    error
  }
}
```

### 2. Listar Usuarios (Query: allUsers)

```graphql
query {
  allUsers {
    id
    username
    email
    firstName
    lastName
    military
    temporal
    documentNumber
    documentType {
      id
      name
    }
    country {
      id
      name
    }
    contactInfo {
      phone
      cellPhone
      address
      city
      emergencyName
      emergencyPhone
    }
  }
}
```

### 3. Listar Países (Query: allCountries)

```graphql
query {
  allCountries {
    id
    name
  }
}
```

### 4. Listar Tipos de Documentos (Query: allTypeDocuments)

```graphql
query {
  allTypeDocuments {
    id
    name
  }
}
```

### 5. Actualizar un Usuario (UpdateUser)

```graphql
mutation {
  updateUser(input: {
    id: 1,
    email: "johndoe_updated@example.com",
    firstName: "Johnny",
    lastName: "Doe Updated"
  }) {
    user {
      id
      username
      email
      firstName
      lastName
    }
    ok
    error
  }
}
```

### 6. Eliminar un Usuario (DeleteUser)

```graphql
mutation {
  deleteUser(input: { id: 1 }) {
    ok
    error
  }
}
```

---

## Ejecución del Proyecto

### Opción 1: Usando el Servidor de Desarrollo (runserver)

1. Asegúrate de tener Python (3.11 o superior) y pip instalados.  
2. (Opcional) Crea un entorno virtual (por ejemplo, con `python -m venv venv` y actívalo).  
3. Instala las dependencias:  
   ```bash
   cd core
   pip install -r requirements.txt
   ```
4. Ejecuta las migraciones (si es necesario):  
   ```bash
   python manage.py migrate
   ```
5. Inicia el servidor de desarrollo:  
   ```bash
   python manage.py runserver
   ```
6. Abre tu navegador en `http://localhost:8000` (o la ruta donde se sirve el formulario) y accede a la interfaz de usuario.  
7. Para consultar la API GraphQL, visita (por ejemplo) `http://localhost:8000/graphql`.

### Opción 2: Usando Docker

1. Asegúrate de tener Docker y Docker Compose instalados.  
2. En la raíz del proyecto (donde se encuentra el `Dockerfile` y `docker-compose.yml`), ejecuta:  
   ```bash
   docker-compose build
   docker-compose up
   ```
3. El contenedor se construye, recolecta los archivos estáticos, ejecuta las migraciones y levanta el servidor en `http://localhost:8000`.  
4. Para consultar la API GraphQL, visita (por ejemplo) `http://localhost:8000/graphql`.

## Notas Adicionales

- **Base de Datos:**  
  - Por defecto se usa SQLite. Si se requiere cambiar a PostgreSQL (u otra DB), actualiza `settings.py` y el `Dockerfile` (por ejemplo, instalando `psycopg2`).  


---

¡Gracias por revisar el proyecto! Si tienes dudas o sugerencias, no dudes en abrir un issue o contactar al equipo.

 