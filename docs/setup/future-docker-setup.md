# Future Docker Setup

Maxedu is planned to support Dockerized deployments for improved scalability and simplified orchestration.

## Dockerized Architecture
- **Frontend (Nuxt)**: A lightweight Node.js base image to serve the frontend application.
- **Backend (Frappe)**: A Frappe-specific image for the application server and background workers.
- **Database (MariaDB)**: A standard MariaDB container for persistent storage.
- **Cache (Redis)**: Dedicated containers for caching and queuing.

## Docker Compose
A `docker-compose.yml` file is planned to orchestrate these services, allowing for a single-command setup:
- **`docker-compose up -d`**: Launch the entire Maxedu stack in the background.

## Benefits
- **Consistent Environment**: Ensure that development, staging, and production environments are identical.
- **Simplified Scaling**: Easily scale specific services, like the frontend or background workers, based on load.
- **Isolation**: Prevent dependency conflicts between the host system and the application.

Dockerized deployment is a key milestone on the Maxedu roadmap.
