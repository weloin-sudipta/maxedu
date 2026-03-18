import frappe
from .student import get_student_group
from frappe.model.workflow import apply_workflow


@frappe.whitelist()
def apply_leave(from_date=None, to_date=None, reason=None, attendance_based_on=None, mark_as_present=0):
    try:
        user = frappe.session.user
        student = frappe.get_doc("Student", {"user": user})
        student_id = student.name
        student_group = get_student_group()

        doc = frappe.new_doc("Student Leave Application")

        doc.student = student_id
        doc.student_name = student.student_name
        doc.from_date = from_date
        doc.to_date = to_date
        doc.student_group = student_group[0].parent
        doc.reason = reason
        doc.attendance_based_on = attendance_based_on
        doc.mark_as_present = mark_as_present
        doc.flags.ignore_validate = True
        doc.insert(ignore_permissions=True)


        # ── Auto submit workflow right after insert ────────────────────
        apply_workflow(doc, "Submit")
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "name": doc.name,
            "student_name": student.student_name,
            "student_group": student_group,
            "student_id": student_id,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Apply Leave Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def submit_leave(docname):
    try:
        from frappe.model.workflow import apply_workflow

        doc = frappe.get_doc("Student Leave Application", docname)

        # Make sure this belongs to the logged-in student
        user    = frappe.session.user
        student = frappe.get_doc("Student", {"user": user})
        if doc.student != student.name:
            frappe.throw("Not authorized to submit this application")

        apply_workflow(doc, "Submit")
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status":         "success",
            "message":        "Leave application submitted for approval",
            "docname":        doc.name,
            "workflow_state": doc.workflow_state,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Submit Leave Error")
        return {
            "status":  "error",
            "message": str(e),
        }


@frappe.whitelist()
def get_my_applications():
    try:
        user    = frappe.session.user
        student = frappe.get_doc("Student", {"user": user})

        applications = frappe.get_all(
            "Student Leave Application",
            filters={"student": student.name},
            fields=[
                "name", "student", "student_name",
                "from_date", "to_date", "total_leave_days",
                "attendance_based_on", "student_group",
                "reason", "mark_as_present", "workflow_state"
            ],
            order_by="creation desc"
        )

        return {
            "status":       "success",
            "applications": applications,
            "student_name": student.student_name,
            "student_id":   student.name,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Applications Error")
        return {
            "status":  "error",
            "message": str(e),
        }