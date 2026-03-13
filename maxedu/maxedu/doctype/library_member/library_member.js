frappe.ui.form.on("Library Member", {

    student: function(frm) {
        if (frm.doc.student) {
            frappe.db.get_doc("Student", frm.doc.student).then(doc => {
                frm.set_value("full_name", doc.student_name);
                frm.set_value("email", doc.student_email_id);
                frm.set_value("phone", doc.student_mobile_number);
            });
        }
    },

    instructor: function(frm) {
        if (frm.doc.instructor) {
            frappe.db.get_doc("Instructor", frm.doc.instructor).then(doc => {
                frm.set_value("full_name", doc.instructor_name);
                frm.set_value("email", doc.instructor_name + "@example.com"); // Assuming email is not available in Instructor doctype
                frm.set_value("phone", "1234567890"); // Assuming phone is not available in Instructor doctype
            });
        }
    },

    // staff: function(frm) {
    //     if (frm.doc.staff) {
    //         frappe.db.get_doc("Employee", frm.doc.employee).then(doc => {
    //             frm.set_value("full_name", doc.full_name);
    //             frm.set_value("email", doc.email);
    //             frm.set_value("phone", doc.phone);
    //         });
    //     }
    // }

});