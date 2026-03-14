import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_books(doctype, txt, searchfield, start, page_len, filters):
    """Return unique Library Books that have at least one available physical copy."""

    return frappe.db.sql(
        """
        SELECT 
            lb.name,
            lb.title
        FROM `tabLibrary Book` lb
        INNER JOIN `tabLibrary Book Inventory` lbi 
            ON lbi.book = lb.name
        WHERE 
            lbi.copy_type = 'Physical'
            AND lbi.available_copies > 0
            AND (lb.title LIKE %(txt)s OR lb.name LIKE %(txt)s)
        GROUP BY lb.name
        ORDER BY lb.title
        LIMIT %(page_len)s OFFSET %(start)s
        """,
        {
            "txt": f"%{txt}%",
            "page_len": page_len,
            "start": start
        },
    )


class BookRequest(Document):

    def before_insert(self):
        """Automatically link member from logged-in user"""
        if not self.member:
            member = frappe.db.get_value(
                "Library Member",
                {"user": frappe.session.user},
                "name"
            )

            if not member:
                frappe.throw("No Library Member linked with this User.")

            self.member = member


    def validate(self):
        """Handle approval workflow"""

        if self.status == "Approved":
            if self.request_type == "Issue":
                self._handle_issue_approval()

            elif self.request_type == "Reservation":
                self._handle_reservation()


    def _handle_issue_approval(self):
        """Issue book after approval"""

        inventory = frappe.db.get_value(
            "Library Book Inventory",
            {"book": self.book, "copy_type": "Physical"},
            ["available_copies", "borrow_period_days"],
            as_dict=True
        )

        if not inventory or inventory.available_copies <= 0:
            frappe.throw(
                "No available physical copies for the selected book."
            )

        # Borrow period
        borrow_days = inventory.borrow_period_days or 14
        self.borrow_period_days = borrow_days

        # Create Book Issue
        book_issue = frappe.new_doc("Book Issue")
        book_issue.book_request = self.name
        book_issue.member = self.member
        book_issue.book = self.book
        book_issue.issue_date = today()
        book_issue.due_date = add_days(today(), borrow_days)
        book_issue.status = "Issued"

        book_issue.insert(ignore_permissions=True)

        # Reduce available copies
        frappe.db.set_value(
            "Library Book Inventory",
            {"book": self.book, "copy_type": "Physical"},
            "available_copies",
            inventory.available_copies - 1
        )

        # Update request status
        self.status = "Issued"


    def _handle_reservation(self):
        """Handle book reservation"""

        existing = frappe.db.exists(
            "Book Request",
            {
                "member": self.member,
                "book": self.book,
                "request_type": "Reservation",
                "status": ["in", ["Pending", "Approved", "Reserved"]]
            }
        )

        if existing and existing != self.name:
            frappe.throw(
                "You already have an active reservation for this book."
            )

        self.status = "Reserved"