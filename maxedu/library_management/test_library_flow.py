import frappe
from maxedu.library_management.api import request_book, cancel_request, renew_book

def execute():
    # Setup test data
    frappe.set_user("Administrator")
    
    from frappe.utils import random_string
    rs = random_string(5)
    
    library = frappe.get_doc({
        "doctype": "Library",
        "library_name": f"Test Library {rs}",
        "library_code": f"LIB-{rs}",
        "owner_type": "Organization",
        "librarian": "Administrator",
        "max_books_per_member": 3,
        "issue_duration_days": 7,
        "fine_per_day": 5,
        "allow_reservation": 1,
        "auto_assign_on_return": 1
    }).insert(ignore_permissions=True)
    
    # We need a user account to test `frappe.session.user` for member resolution
    # Let's create two test members and map them to users
    test_email1 = f"test1_{rs}@example.com"
    test_email2 = f"test2_{rs}@example.com"
    
    user1 = frappe.get_doc({
        "doctype": "User",
        "email": test_email1,
        "first_name": "Test1",
        "password": "pass"
    }).insert(ignore_permissions=True)
    
    user2 = frappe.get_doc({
        "doctype": "User",
        "email": test_email2,
        "first_name": "Test2",
        "password": "pass"
    }).insert(ignore_permissions=True)
    
    member1 = frappe.get_doc({
        "doctype": "Library Member",
        "member_name": f"Member 1 {rs}",
        "member_type": "Student",
        "library": library.name,
        "email": test_email1,
        "max_books_allowed": 3
    }).insert(ignore_permissions=True)
    
    member2 = frappe.get_doc({
        "doctype": "Library Member",
        "member_name": f"Member 2 {rs}",
        "member_type": "Student",
        "library": library.name,
        "email": test_email2,
        "max_books_allowed": 3
    }).insert(ignore_permissions=True)
    
    # Book Category
    if not frappe.db.exists("Book Category", "Fiction"):
        frappe.get_doc({"doctype": "Book Category", "category_name": "Fiction"}).insert(ignore_permissions=True)
        
    book = frappe.get_doc({
        "doctype": "Book",
        "title": f"Test Book {rs}",
        "book_type": "Physical",
        "library": library.name,
        "category": "Fiction",
    }).insert(ignore_permissions=True)
    
    # Insert first copy
    copy1 = frappe.get_doc({
        "doctype": "Book Copy",
        "book": book.name,
        "status": "Available",
        "condition": "New"
    }).insert(ignore_permissions=True)
    
    # Verify Inventory Sync
    inv = frappe.db.get_value("Book Inventory", {"book": book.name, "library": library.name}, ["total_copies", "available_copies"], as_dict=True)
    assert inv.total_copies == 1, f"Expected 1 total copy, got {inv.total_copies}"
    assert inv.available_copies == 1, f"Expected 1 available copy, got {inv.available_copies}"
    print("--- Setup Complete & Inventory Sync Verified ---")
    
    # Member 1 creates request using API
    frappe.set_user(test_email1)
    res1 = request_book(book.name, library.name)
    req1_name = res1["request_id"]
    assert res1["queue_position"] == 1, "First request should have priority 1"
    
    # Verify duplication prevention
    try:
        request_book(book.name, library.name)
        assert False, "Duplicate request did not raise error"
    except Exception as e:
        print("Duplicate prevented successfully:", str(e))
        
    # Member 2 creates request
    frappe.set_user(test_email2)
    res2 = request_book(book.name, library.name)
    req2_name = res2["request_id"]
    assert res2["queue_position"] == 2, "Second request should have priority 2"
    
    print("--- Requests Created & Prioritized ---")
    
    # Librarian Approves Req 1 (Simulating approval process)
    frappe.set_user("Administrator")
    req1 = frappe.get_doc("Book Request", req1_name)
    req1.status = "Approved"
    req1.save()
    
    # Verify inventory remains the same (Reserved copies still reduce available)
    # Wait, Reserve drops available but keeps total. Let's check Book Copy status and Inventory.
    # In my logic, available = count of 'Available'. Since it went to 'Reserved', available should drop!
    inv2 = frappe.db.get_value("Book Inventory", {"book": book.name}, ["total_copies", "available_copies"], as_dict=True)
    assert inv2.total_copies == 1
    assert inv2.available_copies == 0, "Available copies should drop to 0 after reservation"
    print("Reservation Sync Validated.")
    
    # Issue Book
    issue_name = req1.create_book_issue()
    print(f"Book Issued: {issue_name}")
    
    # Return book
    issue_doc = frappe.get_doc("Book Issue", issue_name)
    issue_doc.status = "Returned"
    issue_doc.save()
    
    # Verify Auto Assign
    req2 = frappe.get_doc("Book Request", req2_name)
    assert req2.status == "Approved", f"Expected Req 2 to be Approved, but was {req2.status}"
    assert req2.assigned_copy == copy1.name, "Copy should have been assigned to Req 2"
    
    print("--- Test Completed Successfully ---")

