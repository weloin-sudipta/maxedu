import frappe
from frappe.model.document import Document

class BookCopy(Document):
    def on_update(self):
        self.sync_inventory()

    def on_trash(self):
        self.sync_inventory(is_trash=True)

    def sync_inventory(self, is_trash=False):
        if not self.book:
            return

        book_doc = frappe.get_doc("Book", self.book)
        library = book_doc.library
        if not library:
            return

        total = frappe.db.count("Book Copy", filters={"book": self.book})
        available = frappe.db.count("Book Copy", filters={"book": self.book, "status": "Available"})

        if is_trash:
            total -= 1
            if self.status == "Available":
                available -= 1

        total = max(0, total)
        available = max(0, available)

        inventory_name = frappe.db.get_value("Book Inventory", {"book": self.book, "library": library}, "name")

        if not inventory_name:
            if total > 0 or available > 0:
                inv = frappe.get_doc({
                    "doctype": "Book Inventory",
                    "library": library,
                    "book": self.book,
                    "total_copies": total,
                    "available_copies": available
                })
                inv.insert(ignore_permissions=True)
        else:
            frappe.db.set_value("Book Inventory", inventory_name, {
                "total_copies": total,
                "available_copies": available
            })