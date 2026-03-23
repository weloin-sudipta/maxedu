import frappe
from frappe.utils import getdate

def create_class_12_science_data():
    frappe.init(site="dev.localhost")
    frappe.connect()

    frappe.set_user("Administrator")

    # Ensure Term and Program exist
    institutes = frappe.db.get_all("Institute")
    institute = institutes[0].name if institutes else None
    
    if not institute:
        institute = "MH"
        if not frappe.db.exists("Institute", institute):
            frappe.get_doc({"doctype": "Institute", "institute_name": "MaxEdu High School", "institute_code": "MH"}).insert(ignore_permissions=True)
            
    program = "Higher Secondary"
    if not frappe.db.exists("Program", program):
        frappe.get_doc({
            "doctype": "Program", 
            "program_name": program, 
            "program_abbreviation": "HS",
            "institute": institute
        }).insert(ignore_permissions=True)

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

    # Instructors and Courses
    instructors = [("SC-T1", "Dr. Smith"), ("SC-T2", "Prof. Johnson"), ("SC-T3", "Mr. Davis"), ("SC-T4", "Mr. Brown")]
    for code, name in instructors:
        if not frappe.db.exists("Instructor", name):
            frappe.get_doc({
                "doctype": "Instructor",
                "instructor_name": name,
                "first_name": name.split()[0],
                "last_name": name.split()[-1],
                "naming_series": "INS-"
            }).insert(ignore_permissions=True)

    courses = ["Physics", "Chemistry", "Biology", "Maths For Science", "English SC"]
    for c in courses:
        if not frappe.db.exists("Course", c):
            frappe.get_doc({"doctype": "Course", "course_name": c, "course_code": f"C-{c}"}).insert(ignore_permissions=True)

    # Student Group
    group_name = "Class 12 Science"
    if not frappe.db.exists("Student Group", group_name):
        frappe.get_doc({
            "doctype": "Student Group",
            "student_group_name": group_name,
            "group_based_on": "Program",
            "program": program,
            "academic_year": "2026-2027",
            "academic_term": academic_term_id,
            "max_students": 100
        }).insert(ignore_permissions=True)

    # Assign student Edward Thomas to the group
    edward = frappe.db.get_value("Student", {"student_email_id": "edward.thomas@example.com"}, "name")
    if edward:
        if not frappe.db.exists("Student Group Student", {"parent": group_name, "student": edward}):
            doc = frappe.get_doc("Student Group", group_name)
            doc.append("students", {"student": edward, "student_name": "Edward Thomas", "active": 1})
            doc.save(ignore_permissions=True)

    # Create Routine Generator
    gen = frappe.new_doc("Routine Generator")
    gen.academic_term = academic_term_id
    gen.max_classes_per_instructor_per_day = 2
    gen.max_classes_per_subject_per_day = 2
    gen.min_classes_per_instructor_per_week = 5
    gen.max_classes_per_instructor_per_week = 20
    
    # Days and periods
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    for d in days:
        gen.append("days", {"day": d})
        
    for p in range(1, 6): # 5 periods
        gen.append("periods", {"period": p, "start_time": f"{8+p:02d}:00:00", "end_time": f"{9+p:02d}:00:00"})
        
    gen.append("student_groups", {"student_group": group_name})
    
    # Instructor Mapping
    mappings = [
        ("Dr. Smith", "Physics"),
        ("Prof. Johnson", "Chemistry"),
        ("Mr. Davis", "Biology"),
        ("Mr. Brown", "Maths For Science"),
        ("Mr. Davis", "English SC")
    ]
    for t, c in mappings:
        gen.append("instructor_map", {"instructor": t, "course": c})

    gen.insert(ignore_permissions=True)
    
    print(f"Generated Routine Config: {gen.name}")
    import maxedu.api
    print(maxedu.api.generate_routine(gen.name))
    
    frappe.db.commit()

create_class_12_science_data()
