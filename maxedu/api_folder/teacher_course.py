import frappe
from .teacher_greading import get_my_courses


@frappe.whitelist()
def get_course_topics():
    teacherdata = get_my_courses()

    if not teacherdata or teacherdata.get("error"):
        return teacherdata

    instructor_log = teacherdata.get("instructor_log", [])

    # Extract course names
    course_names = [
        log.get("course")
        for log in instructor_log
        if log.get("course")
    ]

    # Remove duplicates
    course_names = list(set(course_names))

    courses = []

    for course_name in course_names:
        try:
            course_doc = frappe.get_doc("Course", course_name)

            # Convert to dict so it's JSON serializable
            course_dict = course_doc.as_dict()

            # Optional: keep only topics cleanly
            course_dict["topics"] = course_doc.get("topics")

            courses.append(course_dict)

        except frappe.DoesNotExistError:
            continue

    return courses

@frappe.whitelist()
def get_teacher_details():
    return frappe.get_doc("Instructor","Mr. Davis")


# maxedu/api_folder/study_materials.py
import frappe
from frappe.utils import nowdate
from frappe import _


@frappe.whitelist()
def create_study_material():
    try:
        title = frappe.form_dict.get('title')
        course = frappe.form_dict.get('course')
        topic = frappe.form_dict.get('topic')
        category = frappe.form_dict.get('category')
        upload_date = frappe.form_dict.get('upload_date')
        description = frappe.form_dict.get('description')

        # ✅ Files come from frappe.request.files, NOT frappe.form_dict
        uploaded_file = frappe.request.files.get('file')

        print("Received data:", {
            "title": title,
            "course": course,
            "topic": topic,
            "category": category,
            "upload_date": upload_date,
            "description": description,
            "file": uploaded_file.filename if uploaded_file else None
        })

        if not title:
            return {"success": False, "message": "Title is required"}

        if not course:
            return {"success": False, "message": "Course is required"}

        if not uploaded_file:
            return {"success": False, "message": "File is required"}

        if not frappe.db.exists("Course", course):
            return {"success": False, "message": f"Course '{course}' does not exist"}

        if topic and not frappe.db.exists("Topic", topic):
            return {"success": False, "message": f"Topic '{topic}' does not exist"}

        study_material = frappe.get_doc({
            "doctype": "Study Material",
            "title": title.strip(),
            "course": course,
            "topic": topic if topic else None,
            "category": category if category else None,
            "upload_date": upload_date if upload_date else nowdate(),
            "description": description if description else "",
            "status": "Active"
        })
        study_material.insert()

        file_url = None
        file_name = None
        file_size = None

        try:
            # FileStorage object from Werkzeug — use .read() and .filename
            file_content = uploaded_file.read()
            file_name = uploaded_file.filename or f"{title}.file"

            file_size_bytes = len(file_content)
            if file_size_bytes < 1024:
                file_size = f"{file_size_bytes} B"
            elif file_size_bytes < 1024 * 1024:
                file_size = f"{file_size_bytes / 1024:.1f} KB"
            elif file_size_bytes < 1024 * 1024 * 1024:
                file_size = f"{file_size_bytes / (1024 * 1024):.1f} MB"
            else:
                file_size = f"{file_size_bytes / (1024 * 1024 * 1024):.1f} GB"

            file_doc = frappe.get_doc({
                "doctype": "File",
                "file_name": file_name,
                "attached_to_doctype": "Study Material",
                "attached_to_name": study_material.name,
                "folder": "Home/Attachments/Study Materials",
                "is_private": 0,
                "content": file_content
            })
            file_doc.insert()

            file_url = file_doc.file_url
            study_material.file = file_url
            study_material.file_name = file_name
            study_material.file_size = file_size
            study_material.save()

        except Exception as file_error:
            frappe.log_error(f"File upload error: {str(file_error)}", "Study Material File Error")
            file_url = None

        frappe.db.commit()

        response_data = {
            "name": study_material.name,
            "title": study_material.title,
            "course": study_material.course,
            "topic": study_material.topic,
            "category": study_material.category,
            "file": file_url,
            "file_name": file_name,
            "file_size": file_size,
            "upload_date": str(study_material.upload_date) if study_material.upload_date else None,
            "description": study_material.description,
            "status": study_material.status,
            "created_at": str(study_material.creation)
        }

        if study_material.course:
            course_name = frappe.db.get_value("Course", study_material.course, "course_name")
            response_data["course_name"] = course_name or study_material.course

        if study_material.topic:
            topic_name = frappe.db.get_value("Topic", study_material.topic, "topic_name")
            response_data["topic_name"] = topic_name or study_material.topic

        return {
            "success": True,
            "message": "Study Material created successfully",
            "data": response_data
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating study material: {str(e)}", "Study Material API Error")
        return {"success": False, "message": f"Error creating study material: {str(e)}"}