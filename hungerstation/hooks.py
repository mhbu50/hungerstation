# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hungerstation"
app_title = "HungerStation"
app_publisher = "Accurate Systems"
app_description = "HungerStation"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mohammed.r@accuratesystems.com.sa"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hungerstation/css/hungerstation.css"
app_include_js = "assets/js/hungerstation.js"
website_context = {
    "favicon": "/assets/hungerstation/images/hungerstation-android.png",
    "splash_image": "/assets/hungerstation/images/hungerstation-android.png"
}

# include js, css files in header of web template
# web_include_css = "/assets/hungerstation/css/hungerstation.css"
# web_include_js = "/assets/hungerstation/js/hungerstation.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "Lead": "public/js/Lead.js",
    "Project": "public/js/Project.js",
    "Opportunity": "public/js/Opportunity.js",
    "Customer": "public/js/Customer.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hungerstation.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hungerstation.install.before_install"
# after_install = "hungerstation.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hungerstation.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Customer": {
        "after_insert":
        "hungerstation.hungerstation.tools.after_insert_customer",
    },
    "Task": {
        "autoname": "hungerstation.hungerstation.tools.set_autoname",
        "before_insert": "hungerstation.hungerstation.tools.set_autoname",
        "validate":
        "hungerstation.hungerstation.tools.close_documents_submission",
    },
    "ToDo": {
        "validate": "hungerstation.hungerstation.tools.on_change_status_todo"
    },
    "Lead": {
        "on_update": "hungerstation.hungerstation.tools.on_update_lead"
    },
    "Bank": {
        "on_trash": "hungerstation.hungerstation.tools.on_delete_bank"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"hungerstation.tasks.all"
# 	],
# 	"daily": [
# 		"hungerstation.tasks.daily"
# 	],
# 	"hourly": [
# 		"hungerstation.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hungerstation.tasks.weekly"
# 	]
# 	"monthly": [
# 		"hungerstation.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "hungerstation.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hungerstation.event.get_events"
# }
