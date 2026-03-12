import frappe
from frappe.query_builder import DocType

@frappe.whitelist()
def all_available_book():

    Book = DocType("Library Book")
    Inventory = DocType("Library Book Inventory")

    books = (
        frappe.qb.from_(Book)
        .left_join(Inventory)
        .on(Book.name == Inventory.book)
        .select(
            Book.star,
            Inventory.status
        )
    ).run(as_dict=True)

    return books