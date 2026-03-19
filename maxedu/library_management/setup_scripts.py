import frappe

def execute():
    # Force sync of Book Tag to create the missing table
    print("Reloading Book Tag...")
    frappe.reload_doc('library_management', 'doctype', 'book_tag', force=True)
    
    # Just in case the python file is missing
    from frappe.model.document import Document
    print("Sync complete.")
