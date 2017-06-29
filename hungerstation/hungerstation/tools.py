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
