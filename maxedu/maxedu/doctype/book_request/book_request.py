import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, date_diff


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_books(doctype, txt, searchfield, start, page_len, filters):
    """Return Library Books that have at least one available physical copy."""
    return frappe.db.sql(
        """
        SELECT DISTINCT lb.name, lb.title, lb.author
        FROM `tabLibrary Book` lb
        INNER JOIN `tabLibrary Book Inventory` lbi ON lbi.book = lb.name
        WHERE lbi.copy_type = 'Physical'
          AND lbi.is_issued = 0
          AND (lb.title LIKE %(txt)s OR lb.name LIKE %(txt)s)
        ORDER BY lb.title
        LIMIT %(page_len)s OFFSET %(start)s
        """,
        {"txt": f"%{txt}%", "page_len": page_len, "start": start}
    )


class BookRequest(Document):

    def before_save(self):
        # Auto-generate request ID if not set
        if not self.request_id:
            self.request_id = frappe.generate_hash(length=8).upper()

    def validate(self):
        # Validate that the requested book has available copies (for Issue requests)
        if self.request_type == "Issue" and self.book:
            available = frappe.db.count(
                "Library Book Inventory",
                {"book": self.book, "is_issued": 0, "copy_type": "Physical"}
            )
            if not available and self.status == "Pending":
                frappe.msgprint(
                    "No physical copies available. Consider changing Request Type to 'Reservation'.",
                    alert=True
                )

    def on_update(self):
        if self.status == "Approved":
            if self.request_type == "Issue":
                self.create_book_issue()
            else:
                self.create_reservation()
        elif self.status == "Rejected":
            self.notify_rejection()

    def create_book_issue(self):
        # Validate that an ISBN copy has been selected
        if not self.book_isbn:
            frappe.throw("Please select a Book ISBN (Copy) before approving the request.")

        # Check if a Book Issue already exists for this request
        existing = frappe.db.exists("Book Issue", {"book_request": self.name})
        if existing:
            return

        # Validate the selected copy is available
        inventory = frappe.get_doc("Library Book Inventory", self.book_isbn)
        if inventory.is_issued:
            frappe.throw(f"The selected copy (ISBN: {inventory.isbn}) is already issued.")
        if inventory.copy_type != "Physical":
            frappe.throw("Only physical copies can be issued.")

        # Get borrow period from inventory or default to 14 days
        borrow_days = inventory.borrow_period_days or 14

        # Create the Book Issue document
        issue = frappe.get_doc({
            "doctype": "Book Issue",
            "book_request": self.name,
            "member": self.member,
            "book": self.book,
            "book_isbn": self.book_isbn,
            "issue_date": today(),
            "due_date": add_days(today(), borrow_days),
            "fine_per_day": inventory.fine_per_day or 0,
            "status": "Issued"
        })
        issue.insert(ignore_permissions=True)

        # Mark inventory copy as issued
        frappe.db.set_value("Library Book Inventory", self.book_isbn, "is_issued", 1)

        # Decrement available copies (safe: reload to get fresh value)
        current_available = frappe.db.get_value(
            "Library Book Inventory", self.book_isbn, "available_copies"
        ) or 0
        if current_available > 0:
            frappe.db.set_value(
                "Library Book Inventory", self.book_isbn,
                "available_copies", current_available - 1
            )

        # Update request status to Issued
        frappe.db.set_value("Book Request", self.name, "status", "Issued")

        frappe.msgprint(f"Book Issue created: {issue.name}", alert=True)

    def create_reservation(self):
        # For reservations, just mark the request as Reserved
        existing = frappe.db.exists("Book Request", {
            "book": self.book,
            "member": self.member,
            "status": "Reserved",
            "name": ["!=", self.name]
        })
        if existing:
            frappe.throw("Member already has an active reservation for this book.")

        frappe.db.set_value("Book Request", self.name, "status", "Reserved")
        frappe.msgprint(
            f"Book reserved for {self.member_name}. They will be notified when a copy becomes available.",
            alert=True
        )

    def notify_rejection(self):
        frappe.msgprint(
            f"Book Request {self.name} has been rejected.", alert=True
        )
