import frappe

@frappe.whitelist()
def get_all_events():
    student = frappe.db.get_value(
        "Student",
        {"student_email_id": frappe.session.user},
        "name"
    )

    if not student:
        return []

    events = frappe.db.sql(
        """
        SELECT ce.*
        FROM `tabCalendar event` ce
        JOIN `tabCalendar Student Group` csg ON csg.parent = ce.name
        JOIN `tabStudent Group Student` sgs ON sgs.parent = csg.student_group
        WHERE sgs.student = %s
        """,
        student,
        as_dict=True
    )

    return events or []

@frappe.whitelist()
def get_all_event_tags():
    return frappe.get_all("Calendar event", fields=["*"])