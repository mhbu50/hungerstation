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
from frappe.core.doctype.role.role import get_emails_from_role
from frappe.frappeclient import FrappeClient
from frappe.utils import get_url
from frappe.desk.form.assign_to import add
from frappe.utils import formatdate,  \
    get_url_to_form


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
    def get_restaurant(customer):
        print "list opp = {} for customer = {} $".format(
            frappe.get_list(
                "Opportunity", filters={"title": customer}, fields=["name"]),
            customer)
        opportunity = (frappe.get_list(
            "Opportunity", filters={"title": customer}, fields=["name"]) or
                       [None])[0]
        if opportunity:
            restaurant_opp = frappe.get_list(
                "Restaurant Opp",
                filters={"parent": ("=", opportunity.name)},
                fields=["*"])
            return restaurant_opp

    if doc.customer_type == "Company":
        project = frappe.get_doc({
            "doctype": "Project",
            "project_name": doc.name,
            "status": "Open",
            "customer": doc.name
        })

        project.insert()

        t0 = frappe.get_doc({
            "doctype": "Task",
            "name": doc.name + " - Documents Submission",
            "subject": doc.name + " - Documents Submission",
            "status": "Open",
            "restaurant": get_restaurant(project.name),
            "project": project.name
        })
        t0.insert()

        depend1 = frappe.get_doc({
            "doctype":
            "Task Depends On",
            "task":
            t0.name,
            "subject":
            doc.name + " - Documents Submission",
            "project":
            project.name
        })
        t1 = frappe.get_doc({
            "doctype": "Task",
            "name": doc.name + " - Data Entry",
            "subject": doc.name + " - Data Entry",
            "status": "Open",
            "restaurant": get_restaurant(project.name),
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
            "restaurant": get_restaurant(project.name),
            "project": project.name
        })
        # t2.append("depends_on", depend2)
        t2.insert()

        if doc.area == "AAA":
            aaa = frappe.get_doc({
                "doctype": "Task",
                "subject": doc.name + " - AAA Reviewer",
                "status": "Open",
                "restaurant": get_restaurant(project.name),
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
                    "restaurant":
                    get_restaurant(project.name),
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
            "restaurant": get_restaurant(project.name),
            "project": project.name
        })
        # t3.append("depends_on", depend3)
        t3.insert()

        print "project.name = {} doc.name  = {}".format(project.name, doc.name)

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
            "restaurant": get_restaurant(project.name),
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
            "restaurant": get_restaurant(project.name),
            "project": project.name
        })
        # t5.append("depends_on", depend5)
        t5.insert()


@frappe.whitelist()
def is_od(restaurant):
    opportunity = (frappe.get_all(
        "Opportunity", filters={"title": restaurant}, fields=["name"]) or
                   [None])[0]
    print "opportunity = {}".format(opportunity)
    print "///////////////////////"
    restaurant_opp = frappe.get_all(
        "Restaurant Opp",
        filters={"parent": ("=", opportunity.name)},
        fields=["parent,type"])
    print "restaurant_opp = {}".format(restaurant_opp)
    print "///////////////////////"
    boolean = False
    for ro in restaurant_opp:
        print "ro.type = {}".format(ro)
        if ro.type == "OD":
            boolean = True
    print "boolean = {}".format(boolean)
    return boolean


@frappe.whitelist()
def close_documents_submission(self, d):
    # TODO: move task depend to loop
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
    # TODO: if all tasks are closed then close project
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
    doc.name = doc.subject


def add_multiple_assignee(doc, method):
    def assign_to_role(role, reviewer=False):
        print "role = {}".format(role)
        emails = get_emails_from_role(role)
        print "####### emails = {}".format(emails)
        name = ""

        for email in emails:
            if email == "admin@example.com":
                continue
            print "email = {}".format(email)
            print "role[-2] = {}".format(role[:-2])
            if (reviewer):
                name = role
            else:
                name = role[:-2]
            add({
                "assign_to":
                email,
                "doctype":
                "Task",
                "name":
                doc.project + " - " + name,
                "description":
                "New Task : " + doc.project + " - " + name + "<br><br>" +
                "<a href='" + get_url_to_form("Task", doc.project + " - " +
                                              name) +
                "' target='_self'>&nbsp; Click Hear To open Task</a>"
            })

    def check_arae(state):
        if (doc.area == "AAA"):
            assign_to_role(state + " A")
        if (doc.area == "Central"):
            assign_to_role(state + " C")
        if (doc.area == "Eastern"):
            assign_to_role(state + " E")
        if (doc.area == "Western"):
            assign_to_role(state + " W")
        if (doc.area == "Northern"):
            assign_to_role(state + " N")
        if (doc.area == "Bahrain"):
            assign_to_role(state + " B")

    if (doc.status == "Closed"):
        print "doc name = {}".format(doc.name)
        if ("Documents Submission" in doc.name):
            print "in Documents Submission"
            frappe.get_doc({
                "doctype":
                "ToDo",
                "description":
                "Please Assign Task : " + doc.project + " - Data Entry" +
                "<br><br> <a href='" + get_url_to_form("Task", doc.project +
                                                       " - Data Entry") +
                "' target='_self'>&nbsp; Click Hear To open Task</a>",
                "owner":
                "heba.nabil@otlob.com"
            }).insert(ignore_permissions=True)
            # TODO:create sitting screen for defult email

        elif ("Data Entry" in doc.name):
            print "in Data Entry"
            frappe.get_doc({
                "doctype":
                "ToDo",
                "description":
                "Please Assign Task : " + doc.project + " - QA" + "<br><br>" +
                "<a href='" + get_url_to_form("Task", doc.project + " - QA") +
                "' target='_self'>&nbsp; Click Hear To open Task</a>",
                "owner":
                "heba.nabil@otlob.com"
            }).insert(ignore_permissions=True)
        elif (" - QA" in doc.name):
            # print "in QA"
            if (doc.area == "AAA"):
                assign_to_role("AAA Reviewer", True)
            elif (is_od(doc.project)):
                assign_to_role("Delivery Approval", True)
            else:
                check_arae("Control")
        elif ("AAA Reviewer" in doc.name):
            # print "in AAA Reviewer"
            if (is_od(doc.project)):
                assign_to_role("Delivery Approval", True)
            else:
                check_arae("Control")
        elif ("Delivery Approval" in doc.name):
            check_arae("Control")
        elif ("- Control" in doc.name):
            # print "in Control"
            check_arae("Printer")
        elif ("Printer" in doc.name):
            # print " in Printer"
            check_arae("Finance")
        else:  # set project status as cpmpleted
            pass
