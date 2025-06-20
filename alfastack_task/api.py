
import frappe
import json
from frappe import _
from frappe.model.document import Document

@frappe.whitelist(allow_guest=False)
def trigger_webhook(booking_name):
    try:
        from alfastack_task.alfastack_task.doctype.service_booking.service_booking import send_to_webhook
        
        doc = frappe.get_doc('Service Booking', booking_name)
        send_to_webhook(doc, 'manual_trigger')
        
        return {
            'status': 'success',
            'message': f'Webhook triggered for Service Booking {booking_name}'
        }
        
    except Exception as e:
        frappe.log_error(f"API Error - trigger_webhook: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
