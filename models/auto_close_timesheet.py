# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AutoCloseTimesheet(models.Model):
    _inherit = 'res.users'

    @api.model
    def _cron_auto_close_timesheet(self):
        """Cron: runs weekdays at 18:00.

        For every infs_crm.group_admin_config user with is_auto_close_timesheet=True:
        - Find any running timesheet timer for today.
        - Sum all timesheet hours logged today (saved + currently elapsed).
        - If total < 8 h: stop the running timer and fill the running
          timesheet so that the day total equals exactly 8 h.
        """
        group = self.env.ref('infs_crm.group_admin_config', raise_if_not_found=False)
        if not group:
            _logger.warning('infs_config: group infs_crm.group_admin_config not found, skipping cron.')
            return

        users = self.env['res.users'].search([
            ('groups_id', 'in', group.ids),
            ('is_auto_close_timesheet', '=', True),
            ('active', '=', True),
        ])

        today = fields.Date.today()
        AnalyticLine = self.env['account.analytic.line']
        TimerTimer = self.env['timer.timer']

        for user in users:
            # Find running timer for this user on account.analytic.line
            running_timer = TimerTimer.sudo().search([
                ('user_id', '=', user.id),
                ('res_model', '=', 'account.analytic.line'),
                ('timer_start', '!=', False),
                ('timer_pause', '=', False),
            ], limit=1)

            if not running_timer:
                continue  # no active timer for this user

            # The timesheet record the timer belongs to
            running_timesheet = AnalyticLine.sudo().browse(running_timer.res_id)
            if not running_timesheet.exists() or running_timesheet.date != today:
                continue

            # Elapsed hours currently ticking (unsaved portion)
            elapsed_hours = (fields.Datetime.now() - running_timer.timer_start).total_seconds() / 3600.0

            # Sum all saved timesheet amounts for this user today
            today_timesheets = AnalyticLine.sudo().search([
                ('user_id', '=', user.id),
                ('date', '=', today),
                ('project_id', '!=', False),
            ])
            saved_hours = sum(today_timesheets.mapped('unit_amount'))

            # Total = saved amounts + unsaved elapsed time on the running timer
            total_hours = saved_hours + elapsed_hours

            if total_hours >= 8.0:
                continue  # already at or above 8 h, nothing to do

            # Stop the timer (clears timer_start; does NOT write unit_amount)
            running_timer.sudo().action_timer_stop()

            # New amount for the running timesheet:
            # current saved amount + elapsed + shortfall to reach 8 h
            shortfall = 8.0 - total_hours
            new_running_amount = running_timesheet.unit_amount + elapsed_hours + shortfall

            # Write the filled amount so the day total reaches exactly 8 h
            running_timesheet.sudo().write({'unit_amount': new_running_amount})

            _logger.info(
                'Auto-close timesheet: user %s – total was %.2f h, filled to 8 h '
                '(running timesheet id=%d set to %.4f h)',
                user.name, total_hours, running_timesheet.id, new_running_amount,
            )
