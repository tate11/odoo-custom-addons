
import datetime

from datetime import date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api
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
    age = fields.Float(string='Age', digits=(10,2), compute='_compute_age', store=False,
        help="Computed age")
    role_id = fields.Many2one('scoutx.role', string='Status',
        help="Status of the person")
    section_id = fields.Many2one('scoutx.section', string='Section',
        help="Section of the person")

    inscription_ids = fields.One2many('scoutx.inscription', 'partner_id', string='Inscriptinos',
        help="List of inscriptions")

    #status = fields.Many2one('scoutx.status', 'Status', default=_get_status)
    #section_id = fields.Many2one('scoutx.section', string='Section', default=False,
    #    help="The current section of the person") # todo, must be a functionnal field computed with the participation ?
