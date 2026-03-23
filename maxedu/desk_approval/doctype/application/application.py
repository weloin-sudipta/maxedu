import frappe
from frappe.model.document import Document

class Application(Document):
    pass

@frappe.whitelist()
def get_user_applications():
    user = frappe.session.user
    
    apps = frappe.get_all("Application", filters={"applicant": user}, fields=["name", "form", "status", "creation", "current_step"], order_by="creation desc")
    
    result = []
    import json
    for app in apps:
        app_doc = frappe.get_doc("Application", app.name)
        
        # Get form name from Form Doctype
        form_name = frappe.db.get_value("Form", app.form, "form_name") or app.form
        
        data = {}
        if app_doc.data:
            try:
                data = json.loads(app_doc.data)
            except Exception:
                pass
        
        subject = data.get("leave_type") or data.get("reason") or f"{form_name} Request"
        if "leave_type" in data and "reason" in data:
            subject = f"{data['leave_type']} - {data['reason']}"
        
        # Get Approval Policy Steps
        policy = frappe.db.get_value("Approval Policy", {"form": app.form}, "name")
        workflow = []
        if policy:
            policy_doc = frappe.get_doc("Approval Policy", policy)
            # Find logs
            logs = frappe.get_all("Application Approval Log", filters={"application": app.name}, fields=["role", "status", "order"])
            log_map = {log.order: log for log in logs}
            
            # Application applicant is the "initiator" step
            workflow.append({
                "role": "Student" if "Student" in frappe.get_roles(user) else "User",
                "icon": "fa fa-user",
                "state": "approved"
            })
            
            for step in policy_doc.steps:
                log = log_map.get(step.order)
                state = "waiting"
                if log:
                    state = log.status.lower()
                elif app.current_step == step.order:
                    state = "pending"
                
                step_role = step.role or step.user or "Unknown Approver"
                icon = "fa fa-user-tie" if "Instructor" in step_role else "fa fa-building"
                
                workflow.append({
                    "role": step_role,
                    "icon": icon,
                    "state": state
                })
                
        result.append({
            "id": app.name,
            "type": form_name,
            "subject": subject,
            "date": frappe.utils.formatdate(app.creation, "MMM dd, yyyy"),
            "status": app.status,
            "workflow": workflow
        })
        
    return result

@frappe.whitelist()
def get_active_forms():
    forms = frappe.get_all("Form", filters={"is_active": 1}, fields=["name", "form_name"])
    
    result = []
    for f in forms:
        form_doc = frappe.get_doc("Form", f.name)
        fields = []
        for field in form_doc.fields:
            if not field.field: continue
            form_field = frappe.get_doc("Form Field", field.field)
            fields.append({
                "field_name": form_field.field_name,
                "field_label": form_field.field_label,
                "field_type": form_field.field_type,
                "options": form_field.options,
                "is_required": field.is_required,
                "placeholder": field.placeholder,
                "order": field.order or 0
            })
        fields = sorted(fields, key=lambda x: x["order"])
        
        # Determine icon based on form name
        icon = "fa fa-file-alt"
        if "leave" in f.form_name.lower(): icon = "fa fa-calendar-minus"
        elif "improv" in f.form_name.lower(): icon = "fa fa-lightbulb"
        elif "complain" in f.form_name.lower(): icon = "fa fa-exclamation-triangle"
        elif "resource" in f.form_name.lower(): icon = "fa fa-book"
        
        result.append({
            "id": f.name,
            "label": f.form_name,
            "icon": icon,
            "fields": fields
        })
        
    return result

@frappe.whitelist()
def submit_application(form, data):
    import json
    user = frappe.session.user
    
    doc = frappe.get_doc({
        "doctype": "Application",
        "form": form,
        "applicant": user,
        "status": "Pending",
        "current_step": 1,
        "data": data
    })
    doc.insert(ignore_permissions=True)
    
    return {
        "status": "success",
        "name": doc.name,
        "message": "Application submitted successfully"
    }

@frappe.whitelist()
def approve_application(application_name):
    user = frappe.session.user
    doc = frappe.get_doc("Application", application_name)
    
    if doc.status != "Pending":
        frappe.throw("Application is already " + doc.status)
        
    # Get current step
    policy = frappe.db.get_value("Approval Policy", {"form": doc.form}, "name")
    if not policy:
        # Auto approve if no policy (or just one step)
        doc.status = "Approved"
        doc.approved_by = user
        doc.save(ignore_permissions=True)
        return
        
    policy_doc = frappe.get_doc("Approval Policy", policy)
    current_step_order = doc.current_step or 1
    
    # Identify the current step setup
    step_doc = None
    for s in policy_doc.steps:
        if s.order == current_step_order:
            step_doc = s
            break
            
    if not step_doc:
        frappe.throw("Configuration Error: Missing Approval Policy Step for order " + str(current_step_order))
    
    user_roles = frappe.get_roles(user)
    has_permission = ("System Manager" in user_roles) or (step_doc.role and step_doc.role in user_roles) or (step_doc.user == user)
    
    if not has_permission:
        frappe.throw(f"You do not have the required Role ({step_doc.role}) to approve this step.")
        
    # Log approval
    log = frappe.get_doc({
        "doctype": "Application Approval Log",
        "application": doc.name,
        "approver": user,
        "role": step_doc.role,
        "status": "Approved",
        "order": current_step_order
    })
    log.insert(ignore_permissions=True)
    
    # Check if there's another step
    next_step = None
    for s in policy_doc.steps:
        if s.order > current_step_order:
            if not next_step or s.order < next_step.order:
                next_step = s
                
    if next_step:
        doc.current_step = next_step.order
    else:
        doc.status = "Approved"
        doc.approved_by = user
        
    doc.save(ignore_permissions=True)
    frappe.db.commit()

@frappe.whitelist()
def reject_application(application_name):
    user = frappe.session.user
    doc = frappe.get_doc("Application", application_name)
    
    if doc.status != "Pending":
        frappe.throw("Application is already " + doc.status)
    
    policy = frappe.db.get_value("Approval Policy", {"form": doc.form}, "name")
    current_step_order = doc.current_step or 1
    
    role = "System Manager"
    if policy:
        policy_doc = frappe.get_doc("Approval Policy", policy)
        for s in policy_doc.steps:
            if s.order == current_step_order:
                role = s.role
                break

    log = frappe.get_doc({
        "doctype": "Application Approval Log",
        "application": doc.name,
        "approver": user,
        "role": role,
        "status": "Rejected",
        "order": current_step_order
    })
    log.insert(ignore_permissions=True)
    
    doc.status = "Rejected"
    doc.save(ignore_permissions=True)
    frappe.db.commit()
