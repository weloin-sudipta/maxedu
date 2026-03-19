// Copyright (c) 2024, weloin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Member", {
	// refresh(frm) {

	// },
	user: function(frm) {
		if (frm.doc.user) {
			frappe.db.get_doc('User', frm.doc.user).then(user_doc => {
				// Only overwrite the field if it is currently blank
				if (!frm.doc.member_name) {
					frm.set_value('member_name', user_doc.full_name);
				}
				if (!frm.doc.email) {
					frm.set_value('email', user_doc.email);
				}
				if (!frm.doc.phone) {
					frm.set_value('phone', user_doc.phone || user_doc.mobile_no);
				}
			});
		}
	}
});
