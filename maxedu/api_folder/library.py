import frappe
from frappe.utils import getdate, today, date_diff
from datetime import timedelta
from collections import defaultdict


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_book_copies(doctype, txt, searchfield, start, page_len, filters):
    """
    Search endpoint for librarians to find available physical book copies by book name.
    Returns: List of [isbn, book_title] for books with at least one available copy
    """
    return frappe.db.sql(
        """
        SELECT 
            lbi.name,
            CONCAT(lb.title, ' (ISBN: ', lbi.isbn, ')')
        FROM `tabLibrary Book Inventory` lbi
        INNER JOIN `tabLibrary Book` lb 
            ON lbi.book = lb.name
        WHERE 
            lbi.copy_type = 'Physical'
            AND lbi.is_issued = 0
            AND (lb.title LIKE %(txt)s OR lbi.isbn LIKE %(txt)s)
        ORDER BY lb.title, lbi.isbn
        LIMIT %(page_len)s OFFSET %(start)s
        """,
        {
            "txt": f"%{txt}%",
            "page_len": page_len,
            "start": start
        },
    )


@frappe.whitelist()
def get_book_inventory_details(isbn):
    """
    Get details of a specific book inventory copy.
    Used by librarians when issuing to confirm borrow period.
    """
    if not isbn:
        frappe.throw("ISBN is required")
    
    inv = frappe.db.get_value(
        "Library Book Inventory",
        isbn,
        ["isbn", "book", "copy_type", "is_issued", "available_copies", "borrow_period_days", "total_copies"]
    )
    
    if not inv:
        frappe.throw(f"Book copy {isbn} not found")
    
    isbn_val, book, copy_type, is_issued, available, period, total = inv
    
    if is_issued:
        frappe.throw(f"This book copy is already issued. Status changed, please refresh.")
    
    book_title = frappe.db.get_value("Library Book", book, "title")
    
    return {
        "isbn": isbn_val,
        "book": book,
        "book_title": book_title,
        "copy_type": copy_type,
        "available_copies": available,
        "total_copies": total,
        "borrow_period_days": period
    }


@frappe.whitelist()
def get_book_recommendations():
    """
    Get personalized book recommendations for the current user based on:
    - Program match (+5)
    - Subject match (+4)
    - Previously borrowed category (+2)
    - Similar users borrowed (+4)
    - New book bonus (+1)
    
    Returns:
    - List of recommendation sections with books grouped by reason
    """
    
    user_email = frappe.session.user
    
    # Get the Library Member linked to the current user
    member = frappe.db.get_value(
        "Library Member",
        {"user": user_email},
        ["name", "member_type", "student"]
    )
    
    if not member:
        frappe.throw("No Library Member linked to your account")
    
    member_name, member_type, student = member
    
    # Initialize scoring structure
    book_scores = defaultdict(lambda: {
        "score": 0,
        "reasons": [],
        "title": "",
        "author": "",
        "category": "",
        "tags": ""
    })
    
    # Get all available books
    all_books = frappe.get_list(
        "Library Book",
        fields=["name", "title", "author", "category", "tags", "creation"]
    )
    
    if not all_books:
        return {"sections": []}
    
    # 1. Get student's program enrollment
    program_subjects = set()
    student_program = None
    
    if member_type == "Student" and student:
        program_data = frappe.db.get_value("Student", student, "program")
        if program_data:
            student_program = program_data
            
            # Get program enrollment details
            program_courses = frappe.db.get_list(
                "Program Course",
                filters={"parent": program_data},
                fields=["course"]
            )
            program_subjects = {course.get("course") for course in program_courses}
    
    # 2. Get student's enrolled courses (for subject matching)
    enrolled_courses = set()
    if member_type == "Student" and student:
        course_enrollments = frappe.db.get_list(
            "Course Enrollment",
            filters={"student": student, "status": "Active"},
            fields=["course"]
        )
        enrolled_courses = {ce.get("course") for ce in course_enrollments}
    
    # 3. Get student's previously borrowed categories
    borrowed_categories = set()
    previous_issues = frappe.db.get_list(
        "Book Issue",
        filters={"member": member_name},
        fields=["book"]
    )
    
    if previous_issues:
        borrowed_book_ids = [issue.get("book") for issue in previous_issues]
        previous_books = frappe.db.get_list(
            "Library Book",
            filters={"name": ["in", borrowed_book_ids]},
            fields=["category"]
        )
        borrowed_categories = {book.get("category") for book in previous_books if book.get("category")}
    
    # 4. Get books borrowed by similar users (same program)
    similar_users_books = set()
    if student_program:
        similar_students = frappe.db.get_list(
            "Student",
            filters={"program": student_program},
            fields=["name"]
        )
        similar_student_ids = [s.get("name") for s in similar_students]
        
        if similar_student_ids:
            similar_issues = frappe.db.get_list(
                "Book Issue",
                filters={"member": ["in", [frappe.db.get_value("Library Member", {"student": s}, "name") for s in similar_student_ids]]},
                fields=["book"]
            )
            similar_users_books = {issue.get("book") for issue in similar_issues if issue.get("book")}
    
    # Calculate scores for each book
    ninety_days_ago = getdate(today()) - timedelta(days=90)
    
    for book in all_books:
        book_id = book.get("name")
        book_info = book_scores[book_id]
        book_info["title"] = book.get("title")
        book_info["author"] = book.get("author")
        book_info["category"] = book.get("category")
        book_info["tags"] = book.get("tags", "")
        
        # Score: Program match (+5)
        if book.get("category") and book.get("category") in program_subjects:
            book_info["score"] += 5
            book_info["reasons"].append("Program Core")
        
        # Score: Subject match (+4)
        book_tags = set(book.get("tags", "").split(",")) if book.get("tags") else set()
        if book_tags & enrolled_courses:
            book_info["score"] += 4
            book_info["reasons"].append("Subject Match")
        
        # Score: Previously borrowed category (+2)
        if book.get("category") in borrowed_categories:
            book_info["score"] += 2
            book_info["reasons"].append("Past Borrowing")
        
        # Score: Similar users borrowed (+4)
        if book_id in similar_users_books:
            book_info["score"] += 4
            book_info["reasons"].append("Popular Among Peers")
        
        # Score: New book bonus (+1)
        if book.get("creation") and getdate(book.get("creation")) >= ninety_days_ago:
            book_info["score"] += 1
            book_info["reasons"].append("New Arrival")
    
    # Sort books by score and organize into sections
    sorted_books = sorted(
        book_scores.items(),
        key=lambda x: (-x[1]["score"], x[0])
    )
    
    # Group books by primary reason
    sections_dict = defaultdict(list)
    
    for book_id, book_data in sorted_books:
        if book_data["score"] > 0:  # Only include books with positive score
            book_entry = {
                "id": book_id,
                "title": book_data["title"],
                "author": book_data["author"],
                "category": book_data["category"],
                "score": book_data["score"],
                "reasons": book_data["reasons"]
            }
            
            # Categorize by main reason
            if "Program Core" in book_data["reasons"]:
                sections_dict["Program Core Essentials"].append(book_entry)
            elif "Past Borrowing" in book_data["reasons"]:
                sections_dict["Based on Past Borrowing"].append(book_entry)
            elif "Popular Among Peers" in book_data["reasons"]:
                sections_dict["Popular Among Peers"].append(book_entry)
            elif "New Arrival" in book_data["reasons"]:
                sections_dict["New Arrivals"].append(book_entry)
            else:
                sections_dict["Recommended for You"].append(book_entry)
    
    # Format output
    sections = []
    section_metadata = {
        "Program Core Essentials": {
            "subtitle": "Required reading for your major",
            "badge": "Major Match",
            "icon": "fa fa-university"
        },
        "Based on Past Borrowing": {
            "subtitle": "Because you've shown interest in this subject",
            "badge": "Interests",
            "icon": "fa fa-history"
        },
        "Popular Among Peers": {
            "subtitle": "Borrowed by students in your program",
            "badge": "Popular",
            "icon": "fa fa-heart"
        },
        "New Arrivals": {
            "subtitle": "Recently added to the library",
            "badge": "New",
            "icon": "fa fa-star"
        },
        "Recommended for You": {
            "subtitle": "Based on your interests",
            "badge": "Curated",
            "icon": "fa fa-magic"
        }
    }
    
    for section_name, books in sections_dict.items():
        if books:  # Only include non-empty sections
            section = {
                "title": section_name,
                "subtitle": section_metadata[section_name]["subtitle"],
                "badge": section_metadata[section_name]["badge"],
                "icon": section_metadata[section_name]["icon"],
                "books": books[:12]  # Limit to 12 books per section
            }
            sections.append(section)
    
    return {
        "sections": sections,
        "total_recommendations": sum(len(books) for books in sections_dict.values())
    }


@frappe.whitelist()
def get_new_books():
    """
    Get books added in the last 3 days (New Arrivals).
    These are highlighted in the library catalog.
    """
    three_days_ago = getdate(today()) - timedelta(days=3)
    
    new_books = frappe.get_list(
        "Library Book",
        filters={"creation": [">=", three_days_ago]},
        fields=["name", "title", "author", "category", "cover_image"],
        order_by="creation desc"
    )
    
    return {
        "books": new_books,
        "total": len(new_books),
        "highlight_period_days": 3
    }


@frappe.whitelist()
def get_library_statistics():
    """
    Get library statistics:
    - Most borrowed book types/categories
    - Total books borrowed
    - Average borrow period
    - Member statistics
    """
    
    # Most borrowed categories
    most_borrowed = frappe.db.sql(
        """
        SELECT 
            lb.category,
            COUNT(bi.name) as borrow_count,
            COUNT(DISTINCT bi.member) as member_count
        FROM `tabBook Issue` bi
        INNER JOIN `tabLibrary Book` lb ON bi.book = lb.name
        WHERE bi.status IN ('Issued', 'Returned', 'Overdue')
        GROUP BY lb.category
        ORDER BY borrow_count DESC
        LIMIT 10
        """,
        as_dict=True
    )
    
    # Total statistics
    total_books = frappe.db.count("Library Book")
    total_issues = frappe.db.count("Book Issue", {"status": ["!=", "Draft"]})
    total_members = frappe.db.count("Library Member")
    active_borrowers = frappe.db.count("Book Issue", {"status": "Issued"})
    
    # Average borrow period
    avg_period = frappe.db.get_value(
        "Library Book Inventory",
        {},
        "avg(borrow_period_days)"
    ) or 14
    
    return {
        "total_books": total_books,
        "total_issues": total_issues,
        "total_members": total_members,
        "active_borrowers": active_borrowers,
        "average_borrow_days": int(avg_period),
        "most_borrowed_categories": most_borrowed
    }


@frappe.whitelist()
def request_renewal(book_issue_name):
    """
    Request renewal for an issued book.
    Checks if book has pending reservations before allowing renewal.
    Returns: {"success": bool, "message": str, "new_due_date": date or null}
    """
    if not book_issue_name:
        frappe.throw("Book Issue ID is required")
    
    # Get current issue details
    issue = frappe.get_doc("Book Issue", book_issue_name)
    
    if issue.status != "Issued":
        frappe.throw(f"Cannot renew. Current status: {issue.status}")
    
    # Check for pending reservations on this book
    reservation = frappe.db.get_value(
        "Book Request",
        {
            "book": issue.book,
            "status": "Reserved",
            "request_type": "Reservation"
        },
        "name"
    )
    
    if reservation:
        frappe.throw(
            f"Cannot renew this book. There is a pending reservation. "
            f"Please return this book to fulfill the reservation."
        )
    
    # Calculate new due date (add borrow_period_days from today)
    borrow_period = frappe.db.get_value(
        "Library Book Inventory",
        issue.book_isbn,
        "borrow_period_days"
    ) or 14
    
    old_due_date = issue.due_date
    new_due_date = getdate(today()) + timedelta(days=int(borrow_period))
    
    # Update the issue
    issue.due_date = new_due_date
    issue.renewal_count = (issue.renewal_count or 0) + 1
    issue.save(ignore_permissions=True)
    
    frappe.msgprint(
        f"Book renewed successfully. New due date: {new_due_date}",
        alert=True
    )
    
    return {
        "success": True,
        "message": f"Renewal successful. New due date: {new_due_date}",
        "old_due_date": old_due_date,
        "new_due_date": new_due_date
    }


@frappe.whitelist()
def get_user_borrowed_books():
    """
    Get all currently issued (borrowed) books for the logged-in user.
    Includes status and days remaining until due date.
    """
    user_email = frappe.session.user
    
    # Get Library Member for current user
    member = frappe.db.get_value(
        "Library Member",
        {"email": user_email},
        "name"
    )
    
    if not member:
        return {"books": []}
    
    # Get all issued books for this member
    issues = frappe.get_list(
        "Book Issue",
        filters={"member": member, "status": "Issued"},
        fields=[
            "name",
            "book",
            "book_title",
            "book_isbn",
            "issue_date",
            "due_date",
            "fine_per_day"
        ],
        order_by="due_date asc"
    )
    
    # Add calculated fields
    for issue in issues:
        days_left = date_diff(getdate(issue["due_date"]), getdate(today()))
        issue["days_left"] = max(0, days_left)
        issue["is_overdue"] = days_left < 0
        issue["days_overdue"] = max(0, abs(days_left)) if days_left < 0 else 0
        # Check for pending reservations
        issue["has_reservation"] = bool(
            frappe.db.get_value(
                "Book Request",
                {"book": issue["book"], "status": "Reserved", "request_type": "Reservation"},
                "name"
            )
        )
    
    return {"books": issues, "total": len(issues)}


@frappe.whitelist()
def issue_book_to_member(book_request_id, isbn):
    """
    Issue a book to a member (called by library staff).
    Creates a Book Issue document and updates inventory.
    """
    if not book_request_id or not isbn:
        frappe.throw("Book Request ID and ISBN are required")
    
    # Get book request details
    book_request = frappe.get_doc("Book Request", book_request_id)
    
    # Verify book inventory
    inventory = frappe.db.get_value(
        "Library Book Inventory",
        isbn,
        ["name", "book", "copy_type", "is_issued", "available_copies", "borrow_period_days", "total_copies"]
    )
    
    if not inventory:
        frappe.throw(f"Book copy with ISBN {isbn} not found in inventory")
    
    inv_name, book, copy_type, is_issued, available, period, total = inventory
    
    if is_issued == 1:
        frappe.throw("This copy is already issued to another member")
    
    if available <= 0 and copy_type == "Physical":
        frappe.throw("No available copies of this book")
    
    # Calculate due date
    due_date = getdate(today()) + timedelta(days=int(period or 14))
    
    # Create Book Issue document
    issue = frappe.new_doc("Book Issue")
    issue.book_request = book_request_id
    issue.member = book_request.member
    issue.book = book
    issue.book_isbn = isbn
    issue.issue_date = today()
    issue.due_date = due_date
    issue.status = "Issued"
    
    # Get fine per day from inventory
    fine_per_day = frappe.db.get_value("Library Book Inventory", isbn, "fine_per_day") or 0
    issue.fine_per_day = fine_per_day
    
    issue.insert(ignore_permissions=True)
    
    # Update inventory - mark as issued and decrement available copies
    if copy_type == "Physical":
        frappe.db.set_value("Library Book Inventory", isbn, "is_issued", 1)
        frappe.db.set_value("Library Book Inventory", isbn, "available_copies", max(0, available - 1))
    
    # Update Book Request status
    frappe.db.set_value("Book Request", book_request_id, "status", "Issued")
    
    # Notify member
    frappe.msgprint(
        f"Book '{book_request.book_title}' issued successfully. Due date: {due_date}",
        alert=True
    )
    
    return {
        "success": True,
        "issue_name": issue.name,
        "due_date": due_date,
        "borrow_period_days": period
    }


@frappe.whitelist()
def return_book(book_issue_id, return_date=None):
    """
    Record book return (called by library staff).
    Updates issue status to 'Returned' and frees inventory.
    """
    if not book_issue_id:
        frappe.throw("Book Issue ID is required")
    
    if not return_date:
        return_date = today()
    
    # Get Book Issue
    issue = frappe.get_doc("Book Issue", book_issue_id)
    
    if issue.status == "Returned":
        frappe.throw("This book has already been returned")
    
    # Set return date and status
    issue.return_date = return_date
    issue.status = "Returned"
    issue.save(ignore_permissions=True)
    
    # The on_update hook in Document will handle inventory updates
    
    return {
        "success": True,
        "message": f"Book returned successfully",
        "return_date": return_date,
        "fine": issue.total_fine or 0
    }
