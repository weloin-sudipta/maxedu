frappe.ui.form.on("Book Inventory", {
    refresh(frm) {
        frm.set_query("managed_by", function() {
            return {
                query: "frappe.core.doctype.user.user.user_query",
                filters: {
                    role: "Librarian"
                }
            };
        });
    }
});