# System Architecture

Maxedu is built on a modern, distributed architecture combining a powerful backend framework with a dynamic frontend.

## Overview
The system consists of three main layers:

### 1. Frontend Layer (Nuxt.js)
- **Framework**: Nuxt.js (Vue 3)
- **Navigation**: Centered around the `/library` hub.
- **Components**: Modular Vue components (e.g., `IssuedBooks`, `AllBooks`, `StaffIssuance`).
- **Composables**: Reusable logic for API communication (`useLibraryBooks`).

### 2. API Layer (Frappe)
- **Framework**: Frappe (Python)
- **Interface**: RESTful APIs whitelisted via `@frappe.whitelist()`.
- **Logic**: Backend business rules for issuance, returns, and recommendations.

### 3. Data Layer (MariaDB & Frappe ORM)
- **Database**: MariaDB
- **ORM**: Frappe DocTypes.
- **Key Entities**: Book Issue, Book Request, Library Book, Member.

## Component Interaction
1. **User Action**: Student requests a book on the Nuxt frontend.
2. **API Call**: Frontend calls a whitelisted Frappe API endpoint.
3. **Backend Logic**: API validates the request against existing database records.
4. **Data Persistence**: Changes are saved to the database via the Frappe ORM.
5. **UI Update**: Frontend updates the view in real-time based on the API response.
