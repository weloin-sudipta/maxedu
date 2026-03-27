# Database Design

Maxedu's database is structured to balance data integrity with high performance for frequent library transactions.

## Core Schema
The system uses several key MariaDB tables managed via Frappe DocTypes:

### 1. `book_issue`
- **Primary Transaction Log**: Tracks every book borrowing instance.
- **Key Columns**: `member`, `book_isbn`, `issue_date`, `due_date`, `return_date`, `renewal_count`, `fine_per_day`, `total_fine`.
- **Relationship**: Links to `Internal Member` and `Library Book`.

### 2. `book_request`
- **Workflow Audit**: Manages the approval process for book requests.
- **Key Columns**: `member`, `book`, `request_date`, `request_type`, `status`.
- **Status Flow**: `Pending → Approved → Issued → Returned`.

### 3. `library_book_inventory`
- **Copy Tracking**: Manages individual physical book copies.
- **Key Columns**: `book_isbn`, `isbn`, `shelf_location`, `is_issued`.
- **Usage**: Used to ensure availability before issuance.

### 4. `library_member`
- **User Profiles**: Tracks library usage metrics per user.
- **Key Columns**: `user`, `member_type`, `current_books`, `total_borrowed`, `total_fine`.

## Indexing & Performance
- **Indexed Fields**: `member`, `book_isbn`, `status`, `due_date`, `is_issued`.
- **Fast Lookups**: Optimized O(log n) performance for identifying a user's borrowed books and finding available copies.
- **Caching**: Recommendation and statistics data are cached to reduce database load.

This schema ensures that the library operations are both traceable and responsive under load.
