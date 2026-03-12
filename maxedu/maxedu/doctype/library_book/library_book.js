frappe.ui.form.on('Library Book', {
    refresh(frm) {
        frm.set_query("tags", function() {
            return {
                filters: {}
            };
        });
    }
});