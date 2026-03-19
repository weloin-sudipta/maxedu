import frappe
import json
import os

def run():
    json_path = os.path.join(frappe.get_app_path("maxedu"), "library_management", "doctype", "book_issue", "book_issue.json")
    
    with open(json_path, "r") as f:
        data = json.load(f)
        
    # Check if fields exist
    fieldnames = [field.get("fieldname") for field in data.get("fields", [])]
    
    if "renew_requested" not in fieldnames:
        data["fields"].append({
            "fieldname": "renew_requested",
            "fieldtype": "Check",
            "label": "Renew Requested",
            "default": "0",
            "read_only": 1
        })
        
    if "renewal_count" not in fieldnames:
        data["fields"].append({
            "fieldname": "renewal_count",
            "fieldtype": "Int",
            "label": "Renewal Count",
            "default": "0",
            "read_only": 1
        })
        
    with open(json_path, "w") as f:
        json.dump(data, f, indent=1)
        
    print("Successfully patched book_issue.json!")
