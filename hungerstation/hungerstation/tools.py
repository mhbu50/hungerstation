from __future__ import unicode_literals
import frappe
import json

from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import cstr, flt, getdate, comma_and, cint, nowdate, add_days

@frappe.whitelist()
def make_customer(doc):
	doc = json.loads(doc)
	customer = frappe.get_doc({
	"doctype": "Customer",
	"customer_name":doc["customer_name"],
	"customer_type":"Company",
	"lead_name": doc["lead"] ,
	"opportunity": doc["name"],
	"territory":"Saudi Arabia",
	"Area":doc['area']
	})
	customer.insert()

	for r in doc['restaurant_opp']:
		print "Restaurant {}".format(r['name1'])
		customer2 = frappe.get_doc({
		"doctype": "Customer",
		"customer_name":r['name1'],
		"customer_type":"Restaurant",
		"lead_name": doc["lead"] ,
		"opportunity": doc["name"],
		"territory":"Saudi Arabia",
		"Area":doc['area']
		})
		customer2.insert()
	return doc["lead"]

@frappe.whitelist()
def after_insert_customer(doc, method):
 project = frappe.get_doc({
  "doctype": "Project",
  "project_name": doc.name,
  "status": "New",
  "customer":doc.name
  })

 project.insert()
 t0 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Documents submission","status":"Open","project":project.name})
 t0.insert()

 depend1 = frappe.get_doc({"doctype": "Task Depends On", "task": t0.name,"subject": doc.name + " - Documents submission","project":project.name})
 t1 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Data Entry","status":"Open","project":project.name})
 # t1.append("depends_on", depend1)
 t1.insert()

 depend2 = frappe.get_doc({"doctype": "Task Depends On", "task": t1.name,"subject": doc.name + " - Data Entry","project":project.name})
 t2 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - QA","status":"Open","project":project.name})
 # t2.append("depends_on", depend2)
 t2.insert()

 depend3 = frappe.get_doc({"doctype": "Task Depends On", "task": t2.name,"subject": doc.name + " - QA","project":project.name})
 t3 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Control","status":"Open","project":project.name})
 # t3.append("depends_on", depend3)
 t3.insert()

 depend4 = frappe.get_doc({"doctype": "Task Depends On", "task": t3.name,"subject": doc.name + " - Control","project":project.name})
 t4 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Printer","status":"Open","project":project.name})
 # t4.append("depends_on", depend4)
 t4.insert()

 depend5 = frappe.get_doc({"doctype": "Task Depends On", "task": t4.name,"subject": doc.name + " - Printer","project":project.name})
 t5 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Finance","status":"Open","project":project.name})
 # t5.append("depends_on", depend5)
 t5.insert()

@frappe.whitelist()
def close_documents_submission(self ,d):
# to DO // move task depend to loop
	if self.status == "Closed" and  " - Documents submission" in self.subject:
		tasks = frappe.get_list("Task", filters={"project": self.project,"status":"Open"},fields=["name"])

		for t in tasks:
			print "task = {}".format(t.name)
			ts =  frappe.get_doc("Task", t.name)
			print "exp_start_date = {}".format(ts.exp_start_date)
			ts.exp_start_date = nowdate()
			print "exp_start_date = {}".format(ts.exp_start_date)
			ts.exp_end_date = add_days(nowdate(),5)
			ts.update({ts.exp_start_date: nowdate(),ts.exp_end_date:add_days(nowdate(),5)})
			ts.save()
