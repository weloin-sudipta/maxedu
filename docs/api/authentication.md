# Authentication API

Maxedu uses Frappe's built-in authentication system to ensure secure access to library resources.

## Mechanisms
- **Session-Based Authentication**: For regular users (Students, Teachers, Staff) logged in via the browser.
- **REST API Authentication**: For external integrations or mobile apps using API Key and Secret.

## Key Concepts
- **`frappe.session.user`**: The unique identifier of the currently logged-in user.
- **Role-Based Permissions**: Every API call is validated against the user's roles to prevent unauthorized access.
- **CSRF Protection**: All POST requests are protected by Frappe's CSRF token mechanism.

## Common Operations
- **Login**: Handled by Frappe's `/api/method/login` endpoint.
- **Logout**: Handled by `/api/method/logout`.
- **Session Check**: Verifying the user's current session status.

Authentication is the first step for all Maxedu library interactions.
