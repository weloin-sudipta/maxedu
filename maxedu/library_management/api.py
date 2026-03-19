import frappe
from frappe.utils import getdate, today, date_diff, add_days
from datetime import datetime

def get_member_for_user(user, library=None):
    filters1 = {"user": user}
    filters2 = {"email": user}
    if library:
        filters1["library"] = library
        filters2["library"] = library
        
    member = frappe.db.get_value("Library Member", filters1, "name")
    if not member:
        member = frappe.db.get_value("Library Member", filters2, "name")
    return member

@frappe.whitelist()
def get_catalog():
    """
    Get all books combined with their active total and available copies from Book Inventory.
    """
    books = frappe.db.sql(
        """
        SELECT 
            b.name,
            b.title,
            b.author,
            b.category,
            b.book_type as copy_type,
            b.isbn,
            b.library,
            b.cover_image,
            COALESCE(bi.total_copies, 0) as total_copies,
            COALESCE(bi.available_copies, 0) as available_copies
        FROM `tabBook` b
        LEFT JOIN `tabBook Inventory` bi ON bi.book = b.name
        ORDER BY b.title ASC
        """,
        as_dict=True
    )
    return books


@frappe.whitelist()
def get_my_issues():
    """
    Return all Book Issue records for the logged-in user.
    """
    user = frappe.session.user
    
    # Get Member ID for user
    member_name = get_member_for_user(user)
    
    if not member_name:
        return []
        
    issues = frappe.get_list(
        "Book Issue",
        filters={"member": member_name, "status": ["in", ["Issued", "Overdue"]]},
        fields=[
            "name", "book", "book_copy", 
            "issue_date", "due_date", "return_date",
            "status", "fine_amount", "library",
            "renew_requested", "renewal_count"
        ],
        order_by="issue_date desc"
    )
    
    # Enrichment
    current_date = getdate(today())
    for issue in issues:
        book_title, book_isbn = frappe.db.get_value("Book", issue["book"], ["title", "isbn"])
        issue["book_title"] = book_title
        issue["book_isbn"] = book_isbn
        
        due_date = getdate(issue["due_date"])
        days_diff = date_diff(due_date, current_date)
        
        issue["is_overdue"] = issue["status"] == "Issued" and days_diff < 0
        issue["days_left"] = max(0, days_diff) if issue["status"] == "Issued" else 0
        issue["days_overdue"] = max(0, abs(days_diff)) if issue["is_overdue"] else 0

    return issues


@frappe.whitelist()
def get_my_requests():
    """
    Return all active Book Requests for the logged-in user.
    """
    user = frappe.session.user
    member_name = get_member_for_user(user)
    
    if not member_name:
        return []
        
    requests = frappe.get_list(
        "Book Request",
        filters={"member": member_name},
        fields=[
            "*"
        ],
        order_by="creation desc"
    )
    
    for req in requests:
        book_title = frappe.db.get_value("Book", req["book"], "title")
        req["book_title"] = book_title
        req["request_date"] = req["request_date"]
        
    return requests


@frappe.whitelist()
def request_book(book, library):
    """
    Create a new book request. Prevent duplicate requests/active issues.
    Assign a strict priority queue number.
    """
    user = frappe.session.user
    
    if not library:
        frappe.throw("This book has not been assigned to a Library! Please update the Book record in the Frappe backend first.")
        
    member_name = get_member_for_user(user, library=library)
    
    if not member_name:
        frappe.throw("You must be a registered member of this library to request a book.")
        
    # Validation 1: User cannot request if they already have an active Pending or Approved request for this book.
    existing_req = frappe.db.exists("Book Request", {
        "member": member_name,
        "book": book,
        "status": ["in", ["Pending", "Approved"]]
    })
    
    if existing_req:
        frappe.throw("You already have an active request for this book.")
        
    # Validation 2: User cannot request if they currently possess an active issued copy of this book.
    existing_issue = frappe.db.exists("Book Issue", {
        "member": member_name,
        "book": book,
        "status": "Issued"
    })
    
    if existing_issue:
        frappe.throw("You already have a physical copy of this book currently issued to you. Please return it before requesting another copy.")
        
    # Determine Priority - Count of Pending requests for this exact book and library
    pending_count = frappe.db.count("Book Request", filters={
        "book": book,
        "library": library,
        "status": "Pending"
    })
    
    priority_num = pending_count + 1
    
    req_doc = frappe.get_doc({
        "doctype": "Book Request",
        "library": library,
        "member": member_name,
        "book": book,
        "date": today(),
        "status": "Pending",
        "priority": priority_num
    })
    
    req_doc.insert(ignore_permissions=True)
    
    return {
        "success": True, 
        "request_id": req_doc.name, 
        "queue_position": priority_num
    }


@frappe.whitelist()
def cancel_request(request_name):
    """
    Cancel an active request. Must be 'Pending'. 
    Reorganizes priority of remaining queue.
    """
    req_doc = frappe.get_doc("Book Request", request_name)
    user = frappe.session.user
    member_name = get_member_for_user(user)
    
    if req_doc.member != member_name:
        frappe.throw("You can only cancel your own requests.")
        
    if req_doc.status != "Pending":
        frappe.throw(f"You can only cancel Pending requests. This request is currently {req_doc.status}.")
        
    book = req_doc.book
    library = req_doc.library
    canceled_priority = req_doc.priority
    
    req_doc.status = "Cancelled"
    req_doc.priority = 0
    req_doc.save(ignore_permissions=True)
    
    # Priority auto-shift for remaining queued items
    frappe.db.sql(
        """
        UPDATE `tabBook Request`
        SET priority = priority - 1
        WHERE book = %s 
          AND library = %s 
          AND status = 'Pending' 
          AND priority > %s
        """,
        (book, library, canceled_priority)
    )
    
    return {"success": True, "message": "Request cancelled successfully."}


@frappe.whitelist()
def renew_book(issue_name):
    """
    Renew a book. Allowed only if no active reservations (Pending Requests) exist in the queue for the book.
    """
    issue_doc = frappe.get_doc("Book Issue", issue_name)
    user = frappe.session.user
    member_name = get_member_for_user(user)
    
    if issue_doc.member != member_name:
        frappe.throw("You can only renew your own issued books.")
        
    if issue_doc.status != "Issued":
        frappe.throw("You can only renew books currently marked as Issued.")
        
    # Check constraints: Are there any Pending requests waiting for this book?
    waiting_requests = frappe.db.count("Book Request", {
        "book": issue_doc.book,
        "library": issue_doc.library,
        "status": "Pending"
    })
    
    if waiting_requests > 0:
        frappe.throw(f"This book cannot be renewed because {waiting_requests} other member(s) are currently waiting for it.")
        
    issue_doc.db_set("renew_requested", 1)
    
    return {
        "success": True,
        "message": "Renewal requested successfully"
    }

@frappe.whitelist()
def approve_renewal(issue_name):
    """
    Approve a pending renewal request to extend the due date.
    """
    roles = frappe.get_roles()
    if "Librarian" not in roles and "System Manager" not in roles:
        frappe.throw("Not permitted to approve renewals.")

    issue_doc = frappe.get_doc("Book Issue", issue_name)
    
    if not issue_doc.renew_requested:
        frappe.throw("No renewal request found for this issue.")
        
    library_doc = frappe.get_doc("Library", issue_doc.library)
    duration = library_doc.issue_duration_days or 14
    
    new_due_date = add_days(issue_doc.due_date, duration)
    issue_doc.due_date = new_due_date
    issue_doc.renew_requested = 0
    issue_doc.renewal_count = (issue_doc.renewal_count or 0) + 1
    issue_doc.save(ignore_permissions=True)
    
    return {
        "success": True,
        "new_due_date": new_due_date
    }
