# Database Tables

Maxedu's library module is supported by a set of dedicated MariaDB tables.

## 1. `tabBook Issue`
- **Purpose**: Primary record for all book borrowing transactions.
- **Key Columns**:
  - `name`: Unique ID (BOI-XXXX).
  - `member`: Link to `Library Member`.
  - `book_isbn`: Link to `Library Book Inventory` (tracked by ISBN).
  - `issue_date`: Date book was issued.
  - `due_date`: Scheduled return date.
  - `return_date`: Actual return date (nullable).
  - `renewal_count`: Number of times the book was renewed.
  - `status`: `Issued`, `Returned`, `Overdue`.
  - `total_fine`: Auto-calculated based on days overdue and per-day rate.

## 2. `tabBook Request`
- **Purpose**: Manages the approval and reservation workflow.
- **Key Columns**:
  - `name`: Unique ID (BR-XXXX).
  - `member`: Link to `Library Member`.
  - `book`: Link to `Library Book`.
  - `status`: `Pending`, `Approved`, `Issued`, `Reserved`, `Cancelled`.

## 3. `tabLibrary Book Inventory`
- **Purpose**: Tracks individual physical copies of books.
- **Key Columns**:
  - `isbn`: Unique ISBN for each copy.
  - `book`: Link to the parent `Library Book`.
  - `is_issued`: Boolean (0/1) for availability.
  - `shelf_location`: Physical location within the library.
  - `borrow_period_days`: Standard lending duration.

## 4. `tabLibrary Member`
- **Purpose**: Stores student, teacher, and staff profile for library use.
- **Key Columns**:
  - `user`: Link to Frappe User.
  - `member_type`: `Student`, `Teacher`, `Staff`.
  - `current_books`: Auto-updated count of currently borrowed books.
  - `total_fine`: Total outstanding fine amount.

These tables form the persistent data layer for the Maxedu Library Management System.
