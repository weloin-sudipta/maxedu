import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, today, getdate


class BookIssue(Document):

    def validate(self):
        # Auto-set status to Returned when return_date is set
        if self.return_date and self.status == "Issued":
            self.status = "Returned"

        # Calculate overdue and fine if returned or currently overdue
        if self.due_date:
            check_date = getdate(self.return_date) if self.return_date else getdate(today())
            overdue_days = date_diff(check_date, getdate(self.due_date))

            if overdue_days > 0:
                if not self.return_date:
                    self.status = "Overdue"
                self.days_overdue = overdue_days
                fine_rate = self.fine_per_day or 0
                self.total_fine = overdue_days * fine_rate
            else:
                self.days_overdue = 0
                self.total_fine = 0

    def on_update(self):
        if self.status == "Returned" and self.return_date:
            self.process_return()

    def process_return(self):
        # Guard: only process once (when inventory is still marked issued)
        if self.book_isbn:
            is_issued = frappe.db.get_value("Library Book Inventory", self.book_isbn, "is_issued")
            if is_issued:
                frappe.db.set_value("Library Book Inventory", self.book_isbn, "is_issued", 0)

                # Increment available copies with fresh DB read
                current_available = frappe.db.get_value(
                    "Library Book Inventory", self.book_isbn, "available_copies"
                ) or 0
                frappe.db.set_value(
                    "Library Book Inventory", self.book_isbn,
                    "available_copies", current_available + 1
                )

                # Check if any reservations exist for this book and notify
                self.notify_next_reservation()

        # Update linked Book Request status to Returned
        if self.book_request:
            frappe.db.set_value("Book Request", self.book_request, "status", "Returned")

        # Fine notification
        if (self.total_fine or 0) > 0 and not self.fine_paid:
            frappe.msgprint(
                f"Book returned late. Total fine: {frappe.utils.fmt_money(self.total_fine)}. "
                f"Please collect the fine before closing.",
                title="Fine Due",
                indicator="orange"
            )
        else:
            frappe.msgprint("Book returned successfully.", alert=True)

    def notify_next_reservation(self):
        """Notify the next member in the reservation queue for this book."""
        reservation = frappe.db.get_value(
            "Book Request",
            {"book": self.book, "status": "Reserved", "request_type": "Reservation"},
            ["name", "member", "member_name"],
            as_dict=True,
            order_by="request_date asc"
        )
        if reservation:
            frappe.msgprint(
                f"Heads up: Member {reservation.member_name} has a reservation for this book. "
                f"Book Request: {reservation.name}",
                title="Reservation Pending",
                indicator="blue"
            )

@frappe.whitelist()
def get_book_isbns(book):
    # Find the Physical copy inventory for this book
    inventory = frappe.db.sql("SELECT name FROM `tabLibrary Book Inventory` WHERE book = %s AND copy_type = %s", (book, "Physical"), as_dict=True)
    if not inventory:
        return []

    # Get all ISBNs tagged in that inventory's child table
    isbns = frappe.get_all(
        "Library Book ISBN",
        filters={"parent": inventory[0].name, "parenttype": "Library Book Inventory"},
        pluck="book_isbn"
    )
    return isbns