# Frappe Setup

Maxedu's backend is powered by Frappe, which provides a robust platform for managing business logic and data persistence.

## 1. Bench Commands
- **`bench get-app maxedu`**: Download the Maxedu application from the repository.
- **`bench --site maxedu.local install-app maxedu`**: Install Maxedu on a specific Frappe site.
- **`bench build`**: Bundle and compile static assets.
- **`bench watch`**: Automatically recompile assets when changes occur.

## 2. DocType Management
- **`bench --site maxedu.local migrate`**: Synchronize the MariaDB schema with the DocType JSON definitions.
- **`bench --site maxedu.local clear-cache`**: Refresh the application-level cache.

## 3. Worker Status
- **`bench worker`**: Ensure that background workers are running to perform tasks like email notifications and long-running recommendations.

Frappe provides the necessary tools to maintain and scale the Maxedu backend efficiently.
