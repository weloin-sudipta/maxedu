# Database Relationships

Maxedu's library module relies on clear relationships between its core entities to maintain data integrity and enable complex queries.

## 1. Member to Transactions
- **One-to-Many**: One `Library Member` can have multiple `Book Request` records.
- **One-to-Many**: One `Library Member` can have multiple `Book Issue` records.
- **Goal**: Track borrowing history and outstanding fines for each member.

## 2. Book to Catalog
- **One-to-Many**: One `Library Book` title can have multiple `Library Book Inventory` copies (physical books).
- **One-to-Many**: One `Library Book` can be linked to multiple `Book Request` and `Book Issue` records.
- **Goal**: Maintain a central catalog while tracking individual physical item status.

## 3. Request to Issue
- **One-to-One**: A successful `Book Request` leads to a single `Book Issue`.
- **Linked By**: The `Book Issue` record stores the `book_request` ID.
- **Goal**: Audit the entire lifecycle from request initiation to book issuance.

## 4. Category to Book
- **One-to-Many**: One `Library Category` can contain multiple `Library Book` records.
- **Goal**: Group books for search, statistics, and recommendation scoring.

These relationships ensure that the library's data remains consistent and supportive of all operational and analytical needs.
