frappe.ui.form.on("Institute", {
    refresh(frm) {
        frm.set_query("listed_by", function () {
            return {
                query: "frappe.core.doctype.user.user.user_query",
            };
        });

        if (!frm.doc.listed_by) {
            frm.set_value("listed_by", frappe.session.user);
        }
    }
});