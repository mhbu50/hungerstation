# -*- coding: utf-8 -*-
# Copyright (c) 2013, Accurate Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def execute(filters=None):
    columns = [{
        "fieldname": "email",
        "label": "Email",
        "fieldtype": "Link",
        "options": "User",
        "width": 200
    }, {
        "fieldname": "total",
        "label": "Total",
        "fieldtype": "Data",
        "width": 100
    }, {
        "fieldname": "restaurant",
        "label": "Restaurant",
        "fieldtype": "Data",
        "width": 100
    }, {
        "fieldname": "branch",
        "label": "Branch",
        "fieldtype": "Data",
        "width": 100
    }, {
        "fieldname": "lead",
        "label": "Lead",
        "fieldtype": "Data",
        "width": 100
    }, {
        "fieldname": "opportunity",
        "label": "Opportunity",
        "fieldtype": "Data",
        "width": 100
    }]
    data = get_accounts(filters)
    return columns, data


@frappe.whitelist()
def get_accounts(filters):
    emp_list = []
    out = []
    print("from ={}").format(filters.get("from"))
    print("to ={}").format(filters.get("to"))

    # get role of sales employee
    user_role = frappe.db.sql(
        "SELECT DISTINCT parent FROM `tabHas Role` WHERE role=%s and parenttype = 'User'",
        ("Sales User", ),
        as_dict=True)
    for t in user_role:
        if t.parent != "Administrator":
            print "email = {}".format(t.parent)
            emp_list.append(t.parent)

    for emp in emp_list:
        customer_sum = 0
        branch_sum = 0
        lead_sum = 0
        opportunity_sum = 0
        total = 0
        print "employee = {}".format(emp)

        customer_filters = {
            "customer_type": "Restaurant",
            "creation": (">=", filters.get("from")),
            "creation": ("<=", filters.get("to")),
            "owner": emp
        }
        branch_filters = {
            "creation": (">=", filters.get("from")),
            "creation": ("<=", filters.get("to")),
            "owner": emp
        }
        if filters.get("area") != None:
            customer_filters.update({"area": filters.get("area")})
            branch_filters.update({"area": filters.get("area")})
        #customer = {}
        customer = frappe.get_list(
            "Customer",
            filters=customer_filters,
            fields=["*"],
            order_by='name')
        # print "customer = {}".format(customer)

        for c in customer:
            customer_sum = customer_sum + 1
            #print "customer ={} owner={}  ".format(c.name, c.owner)
            branch = frappe.get_list(
                "Rest Branches", filters=branch_filters, fields=["*"])
            for b in branch:
                branch_sum = branch_sum + 1
        lead_filters = {
            "status": "Converted",
            "converted_date": (">=", filters.get("from")),
            "converted_date": ("<=", filters.get("to")),
            "owner": emp
        }
        if filters.get("area") != None:
            lead_filters.update({"area": filters.get("area")})

        lead = frappe.get_list("Lead", filters=lead_filters, fields=["*"])

        for ll in lead:
            lead_sum = lead_sum + 1

        opp_filters = {
            "status": "Converted",
            "converted_date": (">=", filters.get("from")),
            "converted_date": ("<=", filters.get("to")),
            "owner": emp
        }
        if filters.get("area") != None:
            opp_filters.update({"area": filters.get("area")})

        opp = frappe.get_list("Opportunity", filters=opp_filters, fields=["*"])

        for ol in opp:
            opportunity_sum = opportunity_sum + 1
        total = customer_sum + lead_sum + opportunity_sum
        print "emp = {} total = {} restaurant ={} branch = {} lead = {}  opportunity ={} ".format(
            emp, total, customer_sum, branch_sum, lead_sum, opportunity_sum)
        val = {
            "email": emp,
            "total": total,
            "restaurant": customer_sum,
            "branch": branch_sum,
            "lead": lead_sum,
            "opportunity": opportunity_sum
        }
        out.append(val)
    #     val = {"email":emp,"task":average}
    #     out.append(val)
    print "////////////////// out = {}".format(out)
    return out
