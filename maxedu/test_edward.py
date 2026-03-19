import frappe

def test_request():
    frappe.set_user("edward.thomas@example.com")
    
    # Check library members
    members = frappe.db.get_all("Library Member", {"user": "edward.thomas@example.com"}, ["name", "library", "email"])
    print("Members for Edward:", members)
    
    # Try requesting a specific book. We don't know the exact book id Edward used, let's get any available.
    books = frappe.db.get_all("Book", limit=5)
    
    for book in books:
        library = frappe.db.get_value("Book", book.name, "library")
        try:
            from maxedu.library_management.api import request_book
            res = request_book(book.name, library)
            print("Success for", book.name, res)
        except Exception as e:
            print("Failed for", book.name, str(e))
