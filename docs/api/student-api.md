# Student API

The Student API provides endpoints for students to manage their library interactions.

## `get_user_borrowed_books()`
Retrieves all currently issued books for the logged-in user.
- **Output**:
  - `books`: List of `[name, book_title, book_isbn, issue_date, due_date, days_left, is_overdue, has_reservation]`.
  - `total`: Count of current borrowings.
- **Usage**: Used to populate the "Issued Books" tab in the library.

## `request_renewal(book_issue_name)`
Allows a student to request a renewal for an issued book.
- **Input**: `book_issue_name` (name of the Book Issue record).
- **Validation**:
  - Checks if the book is currently `Issued`.
  - Blocks renewal if there is a pending `Reservation` for the book.
- **Effect**:
  - Extends `due_date` by the standard borrow period.
  - Increments `renewal_count`.

## `get_new_books()`
Retrieves books added to the library catalog within the last 3 days.
- **Output**:
  - `books`: List of `[name, title, author, category, cover_image]`.
  - `total`: Count of new arrivals.
- **Usage**: Highlighted in the library catalog as "New Arrivals".
