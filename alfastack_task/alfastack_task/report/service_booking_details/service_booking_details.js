frappe.query_reports["Service Booking Details"] = {
    "filters": [
        {
            "fieldname": "service_type",
            "label": __("Service Type"),
            "fieldtype": "Select",
            "options": "\nTherapy\nSpa\nOthers",
            "default": "",
            "reqd": 0,
            "width": "200px"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nRequested\nApproved\nCompleted",
            "default": "",
            "reqd": 0,
            "width": "200px"
        }
    ],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "status" && data && data.status == "Requested") {
			value = "<span style='color:blue'>" + value + "</span>";
		}
		else if (column.fieldname == "status" && data && data.status == "Approved") {
			value = "<span style='color:green'>" + value + "</span>";
		}
		else if (column.fieldname == "status" && data && data.status == "Completed") {
			value = "<span style='color:red'>" + value + "</span>";
		}
		return value;
	},
    "onload": function(report) {
		report.set_filter_value('status', '');
    }
};
