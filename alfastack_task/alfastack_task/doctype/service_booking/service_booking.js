// Copyright (c) 2025, Alaa Jaraa and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Booking", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Trigger Webhook'), function() {
                trigger_webhook_manually(frm);
            });
        }
    },
});

function trigger_webhook_manually(frm) {
    frappe.call({
        method: 'alfastack_task.api.trigger_webhook',
        args: {
            booking_name: frm.doc.name
        },
        callback: function(r) {
            if (r.message && r.message.status === 'success') {
                frappe.show_alert({
                    message: r.message.message,
                    indicator: 'green'
                });
            } else {
                frappe.show_alert({
                        message: r.message ? r.message.message : 'Error triggering webhook',
                    indicator: 'red'
                });
            }
        }
    });
}