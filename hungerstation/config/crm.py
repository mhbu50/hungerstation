from frappe import _


def get_data():
    return [{
        "label":
        _("Reports"),
        "icon":
        "fa fa-list",
        "items": [
            {
                "type": "report",
                "is_query_report": True,
                "name": "Date Entry Time",
                "doctype": "Task"
            },
            {
                "type": "report",
                "is_query_report": True,
                "name": "QA Time",
                "doctype": "Task"
            },
            {
                "type": "report",
                "is_query_report": True,
                "name": "Tasks Per User",
                "doctype": "Task"
            },
            {
                "type": "report",
                "is_query_report": True,
                "name": "Project KPI",
                "doctype": "Task"
            },

            {
                "type": "report",
                "name": "Accounts By User",
                "doctype": "Customer",
                "is_query_report": True
            },
            # {
            # 	"type": "report",
            # 	"is_query_report": True,
            # 	"name": "Customer Addresses And Contacts",
            # 	"doctype": "Contact"
            # },
            # {
            # 	"type": "report",
            # 	"is_query_report": True,
            # 	"name": "Inactive Customers",
            # 	"doctype": "Sales Order"
            # },
            # {
            # 	"type": "report",
            # 	"is_query_report": True,
            # 	"name": "Campaign Efficiency",
            # 	"doctype": "Lead"
            # },
            # {
            # 	"type": "report",
            # 	"is_query_report": True,
            # 	"name": "Lead Owner Efficiency",
            # 	"doctype": "Lead"
            # }
        ]
    }]
