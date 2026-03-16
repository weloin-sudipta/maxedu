import frappe


@frappe.whitelist()
def get_all_faculty_data():
    
    # Fetch all instructors
    instructors = frappe.get_all(
        "Instructor",
        fields="*"
    )
    print(instructors)
    # Prepare list with logs

    result = []

    for inst in instructors:
        logs = frappe.get_all(
            "Instructor Log",
            filters={"parent": inst.name}, 
            fields="*",
            order_by="creation desc"
        )
        result.append({
            "instructor": inst,
            "logs": logs
        })

    return result
