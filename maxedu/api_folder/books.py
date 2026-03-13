import frappe
from frappe.query_builder import DocType

@frappe.whitelist()
def all_available_book():

    Book = DocType("Library Book")
    Inventory = DocType("Library Book Inventory")

    books = (
        frappe.qb.from_(Book)
        .left_join(Inventory)
        .on(Book.name == Inventory.book)
        .select(
            Book.star,
            Inventory.status,
            Inventory.copy_type
        )
    ).run(as_dict=True)

    return books


@frappe.whitelist()
def all_borrowed_books():

    BookIssue = DocType("Book Issue")
    LibraryMember = DocType("Library Member")

    # Single query: join Library Member, filter by logged-in user and status "Issued"
    books = (
        frappe.qb.from_(BookIssue)
        .join(LibraryMember)
        .on(BookIssue.member == LibraryMember.name)
        .select(BookIssue.star)
        .where(
            (LibraryMember.email == frappe.session.user) &
            (BookIssue.status == "Issued")
        )
    ).run(as_dict=True)

    return books


@frappe.whitelist()
def book_tracking():

    LibraryMember = DocType("Library Member")
    BookRequest = DocType("Book Request")

    # Single query: join Library Member with Book Request
    requests = (
        frappe.qb.from_(BookRequest)
        .join(LibraryMember)
        .on(BookRequest.member == LibraryMember.name)
        .select(BookRequest.star)
        .where(LibraryMember.email == frappe.session.user)
    ).run(as_dict=True)

    return requests or []