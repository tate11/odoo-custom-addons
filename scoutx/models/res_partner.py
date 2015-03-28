
import datetime

from datetime import date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class res_partner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def _get_status(self):
        status = self.env['ir.model.data'].get_object('scoutx', 'function_animated')
        return status.id

    @api.one
    def _compute_age(self):
        if self.birthday:
            date_end = datetime.date.today()
            date_start = datetime.datetime.strptime(self.birthday, DEFAULT_SERVER_DATE_FORMAT).date()
            delta = (date_end-date_start)
            self.age = float(delta.days) /float(365)

    @api.one
    @api.depends('inscription_ids')
    def _compute_section_id(self):
        period = self.env['scoutx.period'].find_period()
        if period:
            inscriptions = self.env['scoutx.inscription'].search([('period_id', '=', period.id), ('partner_id', '=', self.id)])
            if inscriptions:
                self.section_id = inscriptions[0].section_id.id
            else:
                self.section_id = False
        else:
            self.section_id = False

    @api.one
    @api.constrains('section_id', 'role_id')
    def _check_section_role(self):
        if self.section_id:
            if self.role_id:
                if not self.role_id.is_section_function:
                    raise Warning(_('The status/role must be a section function since a section is selected for the member.'))


    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    mother_id = fields.Many2one('res.partner', 'Mother', 
        help="Mother of the current person.")
    father_id = fields.Many2one('res.partner', 'Father', 
        help="Father of the current person.")

    totem = fields.Char(string='Totem')
    birthday = fields.Date(string='Birthdate',
        help="Date of the birth of the person.")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender',
        required=True)
    age = fields.Float(string='Age', digits=(10, 2), compute='_compute_age', store=False,
        help="Computed age")
    contact_person = fields.Selection([('parents_only', 'Parents Only'), ('person_only', 'Member Only'), ('parents_and_person', 'Both')], string='Contact Person', required=True, default='parents_only',
        help="Contact person for news relative to the member")
    role_id = fields.Many2one('scoutx.role', string='Status', default=_get_status, 
        help="Status of the person")
    

    group_id = fields.Many2one('scoutx.group', string='Group',
        help="Current group of the person")
    section_id = fields.Many2one('scoutx.section', string='Section', related='group_id.section_id', store=True, readonly=True,
        help="Current section of the person")

    inscription_ids = fields.One2many('scoutx.inscription', 'partner_id', string='Inscriptinos',
        help="List of inscriptions")

    #status = fields.Many2one('scoutx.status', 'Status', default=_get_status)
    #section_id = fields.Many2one('scoutx.section', string='Section', default=False,
    #    help="The current section of the person") # todo, must be a functionnal field computed with the participation ?
