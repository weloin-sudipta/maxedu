import sys
import os
sys.path.insert(0, ".")
import frappe

def create_test_data():
    frappe.init(site='dev.localhost')
    frappe.connect()

    subjects = ["Math", "Physics", "English", "Chemistry"]
    for s in subjects:
        if not frappe.db.exists("Course", s):
            frappe.get_doc({
                "doctype": "Course",
                "course_name": s
            }).insert(ignore_permissions=True)
            
    if not frappe.db.exists("Academic Year", "2026-2027"):
        frappe.get_doc({
            "doctype": "Academic Year",
            "academic_year_name": "2026-2027"
        }).insert(ignore_permissions=True)
        
    classes = ["class6", "class10", "class12"]
    for c in classes:
        if not frappe.db.exists("Student Group", c):
            frappe.get_doc({
                "doctype": "Student Group",
                "student_group_name": c,
                "group_based_on": "Course",
                "course": "Math",
                "academic_year": "2026-2027"
            }).insert(ignore_permissions=True)

    teacher_subject_map = {
        "T1": ["Math"], "T2": ["Physics"], "T3": ["English"], "T4": ["Chemistry"],
        "T5": ["Math","Physics"], "T6": ["English","Chemistry"],
        "T7": ["Math","Physics","English","Chemistry"],
        "T8": ["Math","Physics","English","Chemistry"],
        "T9": ["Math","Physics","English","Chemistry"]
    }

    for t, subs in teacher_subject_map.items():
        if not frappe.db.exists("Instructor", t):
            frappe.get_doc({
                "doctype": "Instructor",
                "instructor_name": t
            }).insert(ignore_permissions=True)

    # Academic Term
    term_name = "2026 Term 1"
    try:
        term = frappe.get_doc({
            "doctype": "Academic Term",
            "term_name": term_name,
            "title": term_name,
            "term_start_date": "2026-03-01",
            "term_end_date": "2026-06-30",
            "academic_year": "2026-2027"
        }).insert(ignore_permissions=True)
        academic_term_id = term.name
    except Exception:
        academic_term_id = frappe.db.get_value("Academic Term", {"term_name": term_name}, "name")

    # Create Routine Generator
    if frappe.db.exists("DocType", "Routine Generator"):
        gen = frappe.new_doc("Routine Generator")
        gen.academic_term = academic_term_id
        gen.max_classes_per_instructor_per_day = 2
        gen.max_classes_per_subject_per_day = 2
        gen.min_classes_per_instructor_per_week = 8
        gen.max_classes_per_instructor_per_week = 12

        # Days
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for d in days:
            gen.append("days", {"day": d})
            
        # Periods
        for p in range(1, 7):
            gen.append("periods", {"period": p})
            
        # Classes
        for c in classes:
            gen.append("student_groups", {"student_group": c})
            
        # Teachers
        for t, subs in teacher_subject_map.items():
            for s in subs:
                gen.append("instructor_map", {"instructor": t, "course": s})
                
        # Hard locks
        gen.append("hard_locks", {
            "student_group": "class10", "day": "Mon", "period": 1, "instructor": "T1", "course": "Math"
        })
        
        # Soft preferences
        gen.append("preferences", {
            "instructor": "T1", "student_group": "class12", "weight": 5
        })
        gen.append("preferences", {
            "instructor": "T2", "student_group": "class10", "weight": 3
        })
        gen.append("preferences", {
            "instructor": "T3", "student_group": "class6", "weight": 3
        })

        gen.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Generated Test Routine config:", gen.name)

if __name__ == '__main__':
    create_test_data()
