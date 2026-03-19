// Copyright (c) 2024, weloin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Issue", {
	setup: function(frm) {
		frm.set_query("member", function() {
			if (frm.doc.library) {
				return {
					filters: {
						library: frm.doc.library
					}
				};
			}
		});
	},
    refresh: function(frm) {
        if (frm.doc.renew_requested && frm.doc.status === "Issued") {
            frm.add_custom_button(__("Approve Renewal"), function() {
                frappe.call({
                    method: "maxedu.library_management.api.approve_renewal",
                    args: { issue_name: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__("Renewal Approved successfully. Due date has been extended."));
                            frm.reload_doc();
                        }
                    }
                });
            }).addClass("btn-primary");
        }
    }
});
