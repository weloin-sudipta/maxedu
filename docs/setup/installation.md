# Installation Guide

Maxedu requires both a Frappe backend and a Nuxt frontend to be installed and configured.

## Prerequisites
- **Python**: 3.10 or higher.
- **Node.js**: 18.x or higher.
- **MariaDB**: 10.6 or higher.
- **Redis**: For Frappe background jobs and caching.
- **Frappe Bench**: Installed globally (`pip install frappe-bench`).

## 1. Backend Setup (Frappe)
1. **Create Site**: `bench new-site maxedu.local`.
2. **Install App**: `bench get-app maxedu` and `bench --site maxedu.local install-app maxedu`.
3. **Migrate**: `bench --site maxedu.local migrate`.
4. **Start Bench**: `bench start`.

## 2. Frontend Setup (Nuxt)
1. **Navigate**: `cd frontend`.
2. **Install Dependencies**: `npm install`.
3. **Configure Environment**: Create a `.env` file (see [Environment Setup](./environment-setup.md)).
4. **Development Server**: `npm run dev`.

## 3. Verification
- **Backend Admin**: Access `http://localhost:8000/desk`.
- **Frontend App**: Access `http://localhost:3000/library`.

Following these steps will provide a functional development environment for Maxedu.
