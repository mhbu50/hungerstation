# Copyright (c) 2013, Accurate Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import date_diff

def execute(filters=None):
	columns = [{
		"fieldname": "kpi",
		"label": "Project KPI",
		"fieldtype": "Data",
		"width": 200
	}]

	data = get_project(filters)
	return columns, data

def get_project(filters):
	val = {}
	out = []
	tasks =  frappe.get_list("Task", filters=[["ifnull(exp_start_date, '')","!=", ""], ["ifnull(closing_date, '')","!=", ""],["exp_start_date",">=", filters.get("from")],["closing_date","<=", filters.get("to")]],fields=["project,exp_start_date,closing_date"], order_by='name')
	project_list = []
	diff_sum = 0
	for ts in tasks:
		# print "project = {} start date = {} closing date = {} diff= {} ".format(ts.project,ts.exp_start_date, ts.closing_date ,date_diff(ts.closing_date,ts.exp_start_date) )
		diff_sum = diff_sum + date_diff(ts.closing_date,ts.exp_start_date)
		if ts.project not in project_list:
			project_list.append( ts.project );
	# for pro in project_list:
		# print "list = {}".format(pro)
	# print "project length = {} diff_sum ={}".format(len(project_list),diff_sum)
	val = dict({"kpi":diff_sum/len(project_list)})
	out.append(val)
	# print "////////////////// out = {}".format(out)
	return out
