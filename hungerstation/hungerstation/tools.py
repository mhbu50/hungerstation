from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document
from frappe.utils import cstr, flt, getdate, comma_and, cint

@frappe.whitelist()
def make_customer(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.territory = "Saudi Arabia"
		target.customer_type = "Company"


	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Customer",
			"field_map": {
				"customer_name": "customer_name",
                "Area":"Area",
                "territory":"Saudi Arabia"
			}
		}#,
		# "Opportunity Item": {
		# 	"doctype": "Supplier Quotation Item",
		# 	"field_map": {
		# 		"uom": "stock_uom"
		# 	}
		# }
	}, target_doc, set_missing_values)

	return doclist

@frappe.whitelist()
def after_insert_customer(doc, method):
 project = frappe.get_doc({
  "doctype": "Project",
  "project_name": doc.name,
  "status": "New",
  "customer":doc.name
  })

 project.insert()

 t1 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Data Entry","status":"Open","project":project.name})
 t1.insert()

 depend2 = frappe.get_doc({"doctype": "Task Depends On", "task": t1.name,"subject": doc.name + " - Data Entry","project":project.name})
 t2 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - QA","status":"Open","project":project.name})
 t2.append("depends_on", depend2)
 t2.insert()

 depend3 = frappe.get_doc({"doctype": "Task Depends On", "task": t2.name,"subject": doc.name + " - QA","project":project.name})
 t3 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Control","status":"Open","project":project.name})
 t3.append("depends_on", depend3)
 t3.insert()

 depend4 = frappe.get_doc({"doctype": "Task Depends On", "task": t2.name,"subject": doc.name + " - Control","project":project.name})
 t4 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Printer","status":"Open","project":project.name})
 t4.append("depends_on", depend4)
 t4.insert()

 depend5 = frappe.get_doc({"doctype": "Task Depends On", "task": t2.name,"subject": doc.name + " - Printer","project":project.name})
 t5 = frappe.get_doc({"doctype": "Task", "subject": doc.name + " - Finance","status":"Open","project":project.name})
 t5.append("depends_on", depend5)
 t5.insert()
