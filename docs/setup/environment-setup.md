# Environment Setup

Maxedu requires environment variables for seamless integration.

## Nuxt Frontend (`frontend/.env`)
- **`NUXT_PUBLIC_API_URL`**: URL of the Frappe backend (e.g., `http://localhost:8000`).
- **`NUXT_PUBLIC_SITE_NAME`**: Current Frappe site name (e.g., `maxedu.local`).
- **`NUXT_PUBLIC_RELOAD_INTERVAL`**: Rate of polling for real-time updates (default: `5000`ms).

## Frappe Backend (`common_site_config.json` or Site-Specific `site_config.json`)
- **`db_password`**: Password for MariaDB access.
- **`redis_cache`**: Endpoint and port for Redis caching.
- **`redis_queue`**: Endpoint and port for Redis task queuing.
- **`redis_socketio`**: Endpoint and port for Redis WebSocket communication.

## Optional Tooling
- **Git**: Configuration for standard development workflow.
- **VS Code Extensions**: Recommended extensions for Nuxt and Python development.

Proper environment configuration is critical for both development and production deployments.
