import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    """
    Defines the columns for the Service Bookings Overview report.
    """
    return [
        {"fieldname": "name", "label": _("Booking ID"), "fieldtype": "Link", "options": "Service Booking", "width": 120},
        {"fieldname": "customer_name", "label": _("Customer Name"), "fieldtype": "Data", "width": 180},
        {"fieldname": "service_type", "label": _("Service Type"), "fieldtype": "Data", "width": 150},
        {"fieldname": "preferred_datetime", "label": _("Preferred Date/Time"), "fieldtype": "Datetime", "width": 200},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "creation", "label": _("Created On"), "fieldtype": "Datetime", "width": 180},
    ]

def get_data(filters):
    conditions = ""
    values = {}

    if filters:
        if filters.get("service_type"):
            conditions += " AND service_type = %(service_type)s"
            values["service_type"] = filters["service_type"]
        if filters.get("status"):
            conditions += " AND status = %(status)s"
            values["status"] = filters["status"]
    data = frappe.db.sql(f"""
        SELECT
            name,
            customer_name,
            service_type,
            preferred_datetime,
            status,
            creation
        FROM
            `tabService Booking`
        WHERE
            1=1 {conditions}
        ORDER BY
            creation DESC
    """, values=values, as_dict=False)

    return data
