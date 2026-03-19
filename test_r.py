import frappe

def run():
    # Find an active issued book
    issues = frappe.get_all("Book Issue", filters={"status": "Issued"}, limit=1)
    if issues:
        issue_name = issues[0].name
        issue_doc = frappe.get_doc("Book Issue", issue_name)
        print(f"Testing Return for Issue: {issue_doc.name}, Book Copy: {issue_doc.book_copy}")
        
        copy_doc = frappe.get_doc("Book Copy", issue_doc.book_copy)
        print(f"Status before: {copy_doc.status}")
        
        issue_doc.status = "Returned"
        issue_doc.save()
        
        copy_doc.reload()
        print(f"Status after: {copy_doc.status}")
        
        inv = frappe.get_all("Book Inventory", filters={"book": issue_doc.book}, fields=["available_copies"])
        print(f"Inventory Available Copies: {inv}")
    else:
        print("No issued books found to test.")
