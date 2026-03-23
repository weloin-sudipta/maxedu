frappe.ui.form.on('Application', {
    refresh: function(frm) {
        if (frm.doc.status === "Pending") {
            frm.add_custom_button(__('Approve'), function() {
                frappe.call({
                    method: "maxedu.desk_approval.doctype.application.application.approve_application",
                    args: {
                        application_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                            frappe.show_alert({message:__("Application Approved successfully."), indicator:'green'});
                        }
                    }
                });
            }, __('Actions')).addClass('btn-primary');

            frm.add_custom_button(__('Reject'), function() {
                frappe.call({
                    method: "maxedu.desk_approval.doctype.application.application.reject_application",
                    args: {
                        application_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                            frappe.show_alert({message:__("Application Rejected."), indicator:'red'});
                        }
                    }
                });
            }, __('Actions'));
        }
    }
});
