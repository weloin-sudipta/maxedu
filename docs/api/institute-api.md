# Institute API

The Institute API provides endpoints for administrative and operational oversight of the library.

## `get_library_statistics()`
Returns high-level library metrics and trends.
- **Output**:
  - `total_books`: Total books in the catalog.
  - `total_issues`: Lifetime total of book issues.
  - `total_members`: Total registered library members.
  - `active_borrowers`: Number of members with currently issued books.
  - `average_borrow_days`: Average lending period.
  - `most_borrowed_categories`: Top 10 categories by borrow count.
- **Access**: Staff, Admin.

## `get_available_book_copies(txt)`
Search endpoint for librarians to find available physical book copies by title or ISBN.
- **Input**: `txt` (search string).
- **Output**: List of `[isbn, book_title]` for available copies.
- **Usage**: Used in the staff issuance portal.

## `get_book_inventory_details(isbn)`
Retrieves detailed information about a specific book copy.
- **Input**: `isbn` (copy identifier).
- **Output**: `title`, `copy_type`, `available_copies`, `borrow_period_days`, `total_copies`.
- **Validation**: Throws an error if the copy is already issued.
