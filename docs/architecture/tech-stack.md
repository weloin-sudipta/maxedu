# Tech Stack

Maxedu leverages a robust and scalable tech stack tailored for educational institutions.

## Frontend
- **Framework**: [Nuxt.js](https://nuxt.com/) (Vue 3)
- **Styling**: Vanilla CSS, TailwindCSS (for some components).
- **State Management**: Vue Composition API (Refs, Reactives).
- **Communication**: Axios, Frappe's `frappe.call()`.
- **UI Components**: Custom-built Vue components.

## Backend
- **Framework**: [Frappe](https://frappeframework.com/) (Python-based)
- **Language**: Python 3.x
- **ORM**: Frappe DocType engine.
- **Task Scheduling**: RQ (Redis Queue) for background jobs.
- **Email/Notifications**: Frappe's built-in email and notification system.

## Database
- **Database Engine**: MariaDB
- **Key Storage**: Redis (for caching and background jobs).

## Deployment & Hosting
- **Application Server**: Gunicorn/Bench.
- **Reverse Proxy**: Nginx.
- **Environment**: Linux (Ubuntu recommended for production).
