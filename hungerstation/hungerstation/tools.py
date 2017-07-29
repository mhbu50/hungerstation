from __future__ import unicode_literals
import frappe
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import cstr, flt, getdate, comma_and, cint, nowdate, add_days


@frappe.whitelist()
def make_customer(doc):
    doc = json.loads(doc)
    customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": doc["customer_name"],
        "customer_type": "Company",
        "lead_name": doc["lead"],
        "opportunity": doc["name"],
        "territory": "Saudi Arabia",
        "area": doc['area']
    })
    customer.insert()

    for r in doc['restaurant_opp']:
        print "Restaurant {}".format(r['name1'])
        customer2 = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": r['name1'],
            "vendor_comany": doc["customer_name"],
            "customer_type": "Restaurant",
            "lead_name": doc["lead"],
            "opportunity": doc["name"],
            "territory": "Saudi Arabia",
            "area": doc['area']
        })
        customer2.insert()
    frappe.db.set_value(
        'Lead',
        doc["lead"],
        'converted_date',
        nowdate(),
        update_modified=False)
    return doc["lead"]


@frappe.whitelist()
def after_insert_customer(doc, method):
    if doc.customer_type == "Company":
        project = frappe.get_doc({
            "doctype": "Project",
            "project_name": doc.name,
            "status": "New",
            "customer": doc.name
        })

        project.insert()

        t0 = frappe.get_doc({
            "doctype": "Task",
            "name": doc.name + " - Documents submission",
            "subject": doc.name + " - Documents submission",
            "status": "Open",
            "project": project.name
        })
        t0.insert()

        depend1 = frappe.get_doc({
            "doctype":
            "Task Depends On",
            "task":
            t0.name,
            "subject":
            doc.name + " - Documents submission",
            "project":
            project.name
        })
        t1 = frappe.get_doc({
            "doctype": "Task",
            "name": doc.name + " - Data Entry",
            "subject": doc.name + " - Data Entry",
            "status": "Open",
            "project": project.name
        })
        # t1.append("depends_on", depend1)
        t1.insert()

        depend2 = frappe.get_doc({
            "doctype": "Task Depends On",
            "task": t1.name,
            "subject": doc.name + " - Data Entry",
            "project": project.name
        })
        t2 = frappe.get_doc({
            "doctype": "Task",
            "subject": doc.name + " - QA",
            "status": "Open",
            "project": project.name
        })
        # t2.append("depends_on", depend2)
        t2.insert()

        if doc.area == "AAA":
            aaa = frappe.get_doc({
                "doctype": "Task",
                "subject": doc.name + " - AAA Reviewer",
                "status": "Open",
                "project": project.name
            })
            # t2.append("depends_on", depend2)
            aaa.insert()

        # check if Restaurant has OD
        restaurant_opp = frappe.get_list(
            "Restaurant Opp",
            filters={"parent": doc.opportunity},
            fields=["*"])

        delivery_type = ""
        for ro in restaurant_opp:
            print "rest type = {}".format(ro.type)
            if ro.type == "OD":

                da = frappe.get_doc({
                    "doctype":
                    "Task",
                    "subject":
                    doc.name + " - Delivery Approval",
                    "status":
                    "Open",
                    "project":
                    project.name
                })
                da.insert()
                break

        depend3 = frappe.get_doc({
            "doctype": "Task Depends On",
            "task": t2.name,
            "subject": doc.name + " - QA",
            "project": project.name
        })

        t3 = frappe.get_doc({
            "doctype": "Task",
            "subject": doc.name + " - Control",
            "status": "Open",
            "project": project.name
        })
        # t3.append("depends_on", depend3)
        t3.insert()

        depend4 = frappe.get_doc({
            "doctype": "Task Depends On",
            "task": t3.name,
            "subject": doc.name + " - Control",
            "project": project.name
        })
        t4 = frappe.get_doc({
            "doctype": "Task",
            "subject": doc.name + " - Printer",
            "status": "Open",
            "project": project.name
        })
        # t4.append("depends_on", depend4)
        t4.insert()

        depend5 = frappe.get_doc({
            "doctype": "Task Depends On",
            "task": t4.name,
            "subject": doc.name + " - Printer",
            "project": project.name
        })
        t5 = frappe.get_doc({
            "doctype": "Task",
            "subject": doc.name + " - Finance",
            "status": "Open",
            "project": project.name
        })
        # t5.append("depends_on", depend5)
        t5.insert()


@frappe.whitelist()
def close_documents_submission(self, d):
    # print "$$$$$$$$$$$$$$$$$"
    # to DO // move task depend to loop
    if self.status == "Closed" and self.closing_date is None:
        self.closing_date = nowdate()
    if self.status == "Closed" and " - Documents Submission" in self.subject:
        tasks = frappe.get_list(
            "Task",
            filters={"project": self.project,
                     "status": "Open"},
            fields=["name"])

        for t in tasks:
            ts = frappe.get_doc("Task", t.name)
            if ts.exp_start_date is None and ts.exp_end_date is None:
                ts.exp_start_date = nowdate()
                ts.exp_end_date = add_days(nowdate(), 5)
                ts.update({
                    ts.exp_start_date: nowdate(),
                    ts.exp_end_date: add_days(nowdate(), 5)
                })
                ts.save()


@frappe.whitelist()
def on_change_status_todo(doc, method):
    if doc.status == "Closed":
        if doc.closing_date == None:
            doc.closing_date = nowdate()
        if doc.reference_type == "Task":
            frappe.db.set_value("Task", doc.reference_name, "status", "Closed")
            frappe.db.set_value("Task", doc.reference_name, "closing_date",
                                nowdate())
    else:
        if doc.closing_date != None:
            doc.closing_date = None


@frappe.whitelist()
def on_update_lead(doc, method):
    if doc.status == "Converted" and doc.converted_date == None:
        doc.converted_date = nowdate()


@frappe.whitelist()
def set_autoname(doc, method):
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print "befor doc.name = {}".format(doc.name)
    doc.name = doc.subject
    print "after doc.name = {}".format(doc.name)


@frappe.whitelist()
def on_delete_bank(doc, method):
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "on_delete_bank doc.name = {}".format(doc.name)
