# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class InfsConfigRedirect(http.Controller):

    @http.route('/infs_config/goto/todo', type='http', auth='user')
    def goto_todo(self):
        """Full-page redirect to the To-do app with correct menu context."""
        menu = request.env.ref('project_todo.menu_todo_todos')
        return request.redirect('/web#menu_id=%d' % menu.id)

    @http.route('/infs_config/goto/timesheets', type='http', auth='user')
    def goto_timesheets(self):
        """Full-page redirect to My Timesheets with correct menu context."""
        menu = request.env.ref('hr_timesheet.timesheet_menu_activity_user')
        return request.redirect('/web#menu_id=%d' % menu.id)

