# Coding Standards

Maxedu follows industry-standard coding practices to ensure high-quality, maintainable code.

## 1. Python (Frappe)
- **Linting**: Follow [PEP 8](https://pep8.org/) for Python code.
- **Type Hinting**: Use Python type hints where appropriate to improve code clarity and IDE support.
- **Docstrings**: All whitelisted functions and complex logic should include descriptive docstrings.
- **Error Handling**: Use `frappe.throw()` for user-facing errors and log internal exceptions for debugging.

## 2. JavaScript (Nuxt)
- **Linting**: Follow [ESLint](https://eslint.org/) recommended rules.
- **Vue Composition API**: Use `<script setup>` with the Composition API for all new components.
- **Reactivity**: Prefer `ref()` and `reactive()` over the Options API's `data()`.
- **Naming**: Use PascalCase for component filenames and camelCase for variables and functions.

## 3. General
- **Formatting**: Use [Prettier](https://prettier.io/) for consistent code formatting across all file types.
- **Comments**: Write clear, concise comments to explain "why" instead of "what" for complex logic.
- **DRY Principle**: Avoid code duplication by creating reusable components and utilities.

Maintaining these standards is essential for the long-term health of the Maxedu codebase.
