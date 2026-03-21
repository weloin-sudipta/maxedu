frappe.ui.form.on('Form Field', {
    field_label: function(frm) {
        if (!frm.doc.field_name && frm.doc.field_label) {
            
            let fieldname = frm.doc.field_label
                .toLowerCase()
                .replace(/[^a-z0-9 ]/g, '')   // remove special chars
                .replace(/\s+/g, '_');       // spaces → underscore

            frm.set_value('field_name', fieldname);
        }
    }
});