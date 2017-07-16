// Copyright (c) 2016, Accurate Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Average Duration"] = {
	"filters": [
		{
								"fieldname":"from",
								"label": __("From"),
								"fieldtype": "Date",
								"default": frappe.sys_defaults.year_start_date,

						},
						{
												"fieldname":"to",
												"label": __("To"),
												"fieldtype": "Date",
												"default": frappe.datetime.get_today()
										},
	]
}
