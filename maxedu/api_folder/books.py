import frappe
from frappe.query_builder import DocType
from datetime import datetime

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


@frappe.whitelist()
def get_user_requests():
    """Get all non-cancelled book requests for the logged-in user"""
    try:
        user = frappe.session.user
        
        # Query Book Request documents for the current user
        book_requests = frappe.get_list(
            'Book Request',
            filters={
                'member': user,
                'status': ['!=', 'Cancelled']
            },
            fields=['name', 'book', 'status', 'request_date', 'request_type'],
            order_by='request_date desc'
        )
        
        return book_requests.as_dict() if book_requests else []
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'get_user_requests')
        return []


@frappe.whitelist()
def request_book(book, request_type='Issue'):
    """Create a new book request for the logged-in user"""
    try:
        user = frappe.session.user
        
        # Get Library Member for the current user
        library_member = frappe.db.get_value('Library Member', {'email': user}, 'name')
        
        if not library_member:
            frappe.throw('You are not registered as a Library Member')
        
        # Check if book already requested by user
        existing_request = frappe.db.get_value(
            'Book Request',
            {
                'member': library_member,
                'book': book,
                'status': ['!=', 'Cancelled']
            },
            'name'
        )
        
        if existing_request:
            frappe.throw(f'You already have an active request for this book')
        
        # Create new Book Request
        book_request = frappe.get_doc({
            'doctype': 'Book Request',
            'member': library_member,
            'book': book,
            'request_type': request_type,
            'request_date': datetime.now().date(),
            'status': 'Pending',
            'remarks': ''
        })
        
        book_request.insert(ignore_permissions=False)
        frappe.db.commit()
        
        return {
            'name': book_request.name,
            'status': book_request.status,
            'request_date': book_request.request_date.isoformat() if hasattr(book_request.request_date, 'isoformat') else str(book_request.request_date)
        }
    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), 'request_book - Validation Error')
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'request_book')
        frappe.throw(str(e))


@frappe.whitelist()
def cancel_request(request_id):
    """Cancel a book request for the logged-in user"""
    try:
        user = frappe.session.user
        
        # Get Library Member for the current user
        library_member = frappe.db.get_value('Library Member', {'email': user}, 'name')
        
        if not library_member:
            frappe.throw('You are not registered as a Library Member')
        
        # Verify ownership and get the request
        book_request = frappe.get_doc('Book Request', request_id)
        
        if book_request.member != library_member:
            frappe.throw('You can only cancel your own book requests')
        
        if book_request.status == 'Cancelled':
            frappe.throw('This request is already cancelled')
        
        # Update status to Cancelled
        book_request.status = 'Cancelled'
        book_request.save(ignore_permissions=False)
        frappe.db.commit()
        
        return {
            'name': book_request.name,
            'status': book_request.status
        }
    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), 'cancel_request - Validation Error')
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'cancel_request')
        frappe.throw(str(e))
        
@frappe.whitelist()
def all_borrowed_books():
    """
    Returns Book Issue records for the logged-in user where status = 'Issued'.
    The `book` field identifies which Library Book is currently held by the user,
    so the frontend can hide those books from the catalog.
    """
    BookIssue = DocType("Book Issue")
    LibraryMember = DocType("Library Member")

    books = (
        frappe.qb.from_(BookIssue)
        .join(LibraryMember)
        .on(BookIssue.member == LibraryMember.name)
        # ── Explicitly select `book` so the frontend Set works correctly ──────
        .select(
            BookIssue.name,
            BookIssue.book,       # ← the Library Book ID
            BookIssue.status,
            BookIssue.member,
        )
        .where(
            (LibraryMember.email == frappe.session.user) &
            (BookIssue.status == "Issued")
        )
    ).run(as_dict=True)

    return books     

@frappe.whitelist()
def get_all_pending_requests():
    """
    Get all PENDING book requests for the logged-in user.
    Returns both the flat list (request_book) the frontend Set needs,
    and a details list (requests) so the caller has the request doc name
    available for cancel operations — avoiding a second round-trip.
    """
    BookRequest = DocType("Book Request")
    LibraryMember = DocType("Library Member")

    requests = (
        frappe.qb.from_(BookRequest)
        .join(LibraryMember)
        .on(BookRequest.member == LibraryMember.name)
        .select(
            BookRequest.name,           # request doc ID — needed for cancel
            BookRequest.book,
            BookRequest.status,
            BookRequest.request_type,
            BookRequest.request_date,
        )
        .where(
            (LibraryMember.email == frappe.session.user) &
            (BookRequest.status == "Pending")
        )
    ).run(as_dict=True)

    return {
        # Flat list of book IDs — used to build the frontend Set quickly
        "request_book": [r.get("book") for r in requests] if requests else [],
        # Full rows — so the frontend can build bookRequestMap without a second call
        "requests": requests or [],
    }