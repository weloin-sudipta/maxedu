# Naming Conventions

Consistent naming is key to a readable and maintainable codebase.

## 1. Files & Directories
- **Vue Components**: PascalCase (e.g., `IssuedBooks.vue`).
- **JavaScript/TypeScript Files**: camelCase (e.g., `useLibraryBooks.js`).
- **Python Files**: snake_case (e.g., `library.py`).
- **Directories**: kebab-case or snake_case (e.g., `api-folder` or `api_folder`).

## 2. Variables & Functions
- **JavaScript**: camelCase (e.g., `fetchData`, `isLoading`).
- **Python**: snake_case (e.g., `get_user_borrowed_books`, `issue_date`).
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RENEWAL_COUNT`).

## 3. DocTypes & Database
- **DocType Names**: Pascal Case with spaces (e.g., `Book Issue`).
- **Field Names**: snake_case (e.g., `borrow_period_days`).
- **Table Names**: `tab` + Snake Case (e.g., `tabBook Issue`).

Adhering to these conventions ensures that every developer can navigate the codebase with ease.
