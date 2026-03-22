import frappe

def get_policy(form, institute=None):
    filters = {"form": form, "is_active": 1}
    if institute:
        filters["institute"] = institute
    policy_name = frappe.db.get_value("Approval Policy", filters)
    if not policy_name:
        frappe.throw(f"No active Approval Policy found for Form: {form}")
    return frappe.get_doc("Approval Policy", policy_name)

def get_step(application, current_step_order):
    institute = application.get("institute")
    policy = get_policy(application.form, institute)
    for step in policy.steps:
        if step.order == current_step_order:
            return step
    frappe.throw(f"Step {current_step_order} not found in policy.")

def submit_application(doc):
    # doc.institute might not exist on Application strictly per schema, so use .get()
    policy = get_policy(doc.form, doc.get("institute"))

    for step in policy.steps:
        users = set()

        if step.approved_by == "User" and step.get("user"):
            users.add(step.user)
        elif step.approved_by == "Role" and step.get("role"):
            role_users = frappe.get_all("Has Role",
                filters={"role": step.role},
                fields=["parent"]
            )
            for ru in role_users:
                users.add(ru.parent)

        if not users:
            if step.get("fallback_user"):
                users.add(step.fallback_user)
            elif step.get("fallback_role"):
                fallback_users = frappe.get_all("Has Role",
                    filters={"role": step.fallback_role},
                    fields=["parent"]
                )
                for fu in fallback_users:
                    users.add(fu.parent)

        for user in users:
            frappe.get_doc({
                "doctype": "Application Approval Log",
                "application": doc.name,
                "approver": user,
                "role": step.get("role"),
                "status": "Pending",
                "order": step.order,
                "is_active": 1 if step.order == 1 else 0
            }).insert(ignore_permissions=True)

    doc.status = "Pending"
    doc.current_step = 1
    doc.save(ignore_permissions=True)

def approve_step(application_name, user):
    application = frappe.get_doc("Application", application_name)

    logs = frappe.get_all(
        "Application Approval Log",
        filters={
            "application": application_name,
            "order": application.current_step,
            "is_active": 1
        },
        fields=["name", "approver"]
    )

    current_log = next((l for l in logs if l.approver == user), None)

    if not current_log:
        frappe.throw("Not authorized")

    log_doc = frappe.get_doc("Application Approval Log", current_log.name)
    log_doc.status = "Approved"
    log_doc.save(ignore_permissions=True)

    step = get_step(application, application.current_step)

    if step.approval_mode == "Any One":
        # deactivate others
        for l in logs:
            if l.name != log_doc.name:
                frappe.db.set_value("Application Approval Log", l.name, "is_active", 0)
        activate_next_step(application)

    elif step.approval_mode == "All":
        pending = frappe.db.count("Application Approval Log", {
            "application": application_name,
            "order": application.current_step,
            "status": "Pending"
        })
        if pending == 0:
            activate_next_step(application)

def activate_next_step(application):
    next_step = application.current_step + 1

    logs = frappe.get_all(
        "Application Approval Log",
        filters={
            "application": application.name,
            "order": next_step
        }
    )

    if not logs:
        application.status = "Approved"
        application.save(ignore_permissions=True)
        return

    for log in logs:
        frappe.db.set_value("Application Approval Log", log.name, "is_active", 1)

    application.current_step = next_step
    application.save(ignore_permissions=True)

def reject_step(application_name, user):
    log = frappe.get_doc(
        "Application Approval Log",
        {"application": application_name, "status": "Pending", "is_active": 1, "approver": user}
    )
    if not log:
        frappe.throw("Not authorized to reject at this step.")

    log.status = "Rejected"
    log.approver = user
    log.save(ignore_permissions=True)

    application = frappe.get_doc("Application", application_name)
    application.status = "Rejected"
    application.save(ignore_permissions=True)
