import frappe
from frappe.model.document import Document


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
            AND lbi.is_issued = 0
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

        member = frappe.db.get_value(
            "Library Member",
            {"user": frappe.session.user},
            "name"
        )

        if not member:
            frappe.throw("No Library Member linked with this User.")

        self.member = member