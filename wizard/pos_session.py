# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosDetails(models.TransientModel):
    _name = 'pos.details.wizard.custom'
    _description = 'Point of Sale Session Details Report'

    # def _default_start_date(self):
    #     """ Find the earliest start_date of the latests sessions """
    #     # restrict to configs available to the user
    #     config_ids = self.env['pos.config'].search([]).ids
    #     # exclude configs has not been opened for 2 days
    #     self.env.cr.execute("""
    #         SELECT
    #         max(start_at) as start,
    #         config_id
    #         FROM pos_session
    #         WHERE config_id = ANY(%s)
    #         AND start_at > (NOW() - INTERVAL '2 DAYS')
    #         GROUP BY config_id
    #     """, (config_ids,))
    #     latest_start_dates = [res['start'] for res in self.env.cr.dictfetchall()]
    #     # earliest of the latest sessions
    #     return latest_start_dates and min(latest_start_dates) or fields.Datetime.now()

    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime(required=True)
    pos_session_ids = fields.Many2many('pos.session',
        default=lambda s: s.env['pos.session'].search([]))
    pos_branch_ids = fields.Many2many('pos.config',string="Point of Sale")

    def generate_session_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'config_ids': self.pos_branch_ids.ids}
        return self.env.ref('zts_pos_session_report.sr_pos_session_report').report_action([], data=data)


# 