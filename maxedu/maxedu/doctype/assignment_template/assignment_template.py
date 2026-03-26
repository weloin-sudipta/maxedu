import frappe
from frappe.model.document import Document

class AssignmentTemplate(Document):
	def before_save(self):
		# Get instructor linked to current user using full_name
		full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
		instructor = frappe.db.get_value("Instructor", {"name": full_name}, "name")
		
		if not instructor:
			frappe.throw("You must be an Instructor to create assignments")
		
		self.instructor = instructor
		
		# Verify instructor teaches this course using Course Schedule
		teaches = frappe.db.exists("Course Schedule", {
			"course": self.course,
			"instructor": self.instructor
		})
		
		if not teaches and "System Manager" not in frappe.get_roles():
			frappe.throw(f"You ({self.instructor}) are not scheduled as an instructor for the course {self.course}")
