# Copyright (c) 2025, Alaa Jaraa and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from frappe.model.document import Document
from frappe import _

class ServiceBooking(Document):
    def validate(self):
        pass

    def on_update(self):
        if self.has_value_changed('status') and self.status == 'Approved':
            send_to_webhook(self, 'update')

@frappe.whitelist()
def send_to_webhook(doc, method=None):
    try:
        webhook_url = 'https://webhook.site/5a4401ef-26be-4795-8fe5-bef7041a914f'
        
        
        if isinstance(doc, str):
            doc = frappe.get_doc('Service Booking', doc)
        
        payload = {
            'event_type': method or 'update',
            'booking_id': doc.name,
            'customer_name': doc.customer_name,
            'service_type': doc.service_type,
            'preferred_date_time': str(doc.preferred_datetime) if doc.preferred_datetime else None,
            'status': doc.status,
            'creation': str(doc.creation),
            'modified': str(doc.modified),
            'site_name': frappe.utils.get_url(),
            'timestamp': frappe.utils.now()
        }
        
        if frappe.db.exists('Customer', doc.customer_name):
            customer = frappe.get_doc('Customer', doc.customer_name)
            payload['customer_details'] = {
                'customer_code': customer.name,
                'customer_group': customer.customer_group,
                'territory': customer.territory
            }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'ERPNext-ServiceBooking/{frappe.__version__}'
        }
        
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        if response.status_code == 200:
            frappe.logger().info(f"Webhook sent successfully for Service Booking {doc.name}")
            
        else:
            frappe.logger().error(f"Webhook failed for Service Booking {doc.name}: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        frappe.logger().error(f"Webhook request failed for Service Booking {doc.name}: {str(e)}")
        
    except Exception as e:
        frappe.logger().error(f"Unexpected error in webhook for Service Booking {doc.name}: {str(e)}")
        frappe.log_error(f"Service Booking Webhook Error: {str(e)}")


