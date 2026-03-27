# Folder Structure

Maxedu's folder structure is organized to separate backend logic from frontend presentation.

## Root Directory
- **`maxedu/`**: The core Frappe application.
  - **`maxedu/api_folder/`**: Whitelisted API endpoints (e.g., `library.py`).
  - **`maxedu/doctype/`**: DocType definitions and logic.
- **`frontend/`**: The Nuxt.js frontend application.
  - **`frontend/pages/`**: Application pages (e.g., `/library`, `/library/statistics`).
  - **`frontend/components/`**: Reusable Vue components.
  - **`frontend/composables/`**: Shared logic and API wrappers (`useLibraryBooks.js`).
  - **`frontend/assets/`**: Static assets like images and CSS.
- **`docs/`**: Technical documentation (this directory).
- **`ARCHITECTURE_MAP.md`**: High-level system overview.
- **`IMPLEMENTATION_SUMMARY.md`**: Recent implementation details and status.

## Key Files
- **`pyproject.toml`**: Python project configuration and dependencies.
- **`package.json`**: Frontend dependencies and scripts.
- **`README.md`**: Project overview and quick start.

This structured approach ensures that both backend and frontend code are easy to locate and maintain.
