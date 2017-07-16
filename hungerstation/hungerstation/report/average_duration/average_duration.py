# Copyright (c) 2013, Accurate Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
                          nowdate, get_datetime_str, get_datetime,
                          now_datetime)


def execute(filters=None):
    columns = [{
        "fieldname": "email",
        "label": "Email",
        "fieldtype": "Data",
        "option": "User",
        "width": 200
    }, {
        "fieldname": "task",
        "label": "Task Duration",
        "fieldtype": "Data",
        "option": "User",
        "width": 100
    }]
    data = get_Duration(filters)
    return columns, data


@frappe.whitelist()
def get_Duration(filters):
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

    tasks = frappe.get_list(
        "ToDo",
        filters={
            "reference_type": "Task",
            "owner": ("in", emp_list),
            "creation": (">=", filters.get("from")),
            "closing_date": ("<=", filters.get("to"))
        },
        fields=["*"],
        order_by='name')

    for emp in emp_list:
        task_sum = 0
        task_diff_total = 0
        average = 0
        print "employee = {}".format(emp)
        # for todo in tasks :
        # print "todo = {}".format(todo.name)
        expectedResult = [d for d in tasks if d['owner'] in emp]
        # print "owner = {} description
        # ={}".format(expectedResult["owner"],expectedResult["description"])
        for x in expectedResult:
            task_sum = task_sum + 1
            task_diff_total = task_diff_total + date_diff(x.closing_date,
                                                          x.creation)
            # print "owner = {} task = {} start = {} end = {} diff =
            # {}".format(x.owner,x.description,x.creation,x.closing_date,date_diff(x.closing_date,x.creation))
        if task_diff_total != 0 or task_sum != 0:
            average = task_diff_total / task_sum
        # print "////////////////////////////////// task_sum = {}
        # task_diff_total = {} average
        # ={}".format(task_sum,task_diff_total,average)
        val = {"email": emp, "task": average}
        out.append(val)
    # print "////////////////// out = {}".format(out)
    return out
