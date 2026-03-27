# Multi-tenant Design

Maxedu is specifically designed to support multiple institutions within a single deployment, leveraging Frappe's multi-tenancy capabilities.

## Architecture
Each institution (tenant) has its own database and configuration, ensuring data isolation and security.

### 1. Database Isolation
- **Tenant Databases**: For each institute, a unique MariaDB database is created.
- **Shared Application Code**: All tenants share the same application code but operate on their isolated data.
- **Tenant-Specific Data**: Book inventories, member profiles, and transaction logs are stored within the tenant's database.

### 2. Branding & Configuration
- **Custom Branding**: Institutes can configure their logos, colors, and site names.
- **Policy Tuning**: Borrowing periods, fine rates, and renewal limits can be set per institute.
- **Role-Based Access**: Multi-tenant RBAC ensures that staff from one institute cannot access another institute's data.

### 3. Scaling
- **Scalable Infrastructure**: The system supports horizontal scaling of application servers while maintaining data integrity through individual databases.
- **Resource Management**: Background jobs are handled per tenant via dedicated queues.

This multi-tenant approach allows Maxedu to serve as a SaaS platform for a diverse range of educational institutions.
