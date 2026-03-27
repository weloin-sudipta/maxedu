# User & Role Management

The User & Role Management module ensures that every individual in the system has appropriate access levels.

## Role Definition
Every user is assigned to one of the following roles:
- **Student**: Can browse books, request items, view their borrowings, and see recommendations.
- **Teacher**: Can access academic materials, manage their teaching resources, and track student reading patterns by subject.
- **Library Staff**: Can approve requests, issue books, handle returns, and monitor library statistics.
- **Librarian (Admin)**: Full administrative access to library configuration and inventory.

## Member Profiles
- **Profile Data**: Every user has a `Library Member` profile that stores their contact details, current borrowings, lifetime history, and outstanding fines.
- **Authentication**: All users are authenticated via Frappe's secure session management.

## Access Control
- **DocType Permissions**: Permissions are enforced at the DocType level, ensuring that students cannot see or modify staff-only records.
- **Role-Based Views**: The frontend UI dynamically adjusts based on the user's role, presenting the most relevant information and actions.
