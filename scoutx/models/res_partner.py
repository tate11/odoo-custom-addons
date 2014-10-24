
from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning


class res_partner(models.Model):

    _inherit = 'res.partner'

    @api.model
    def _get_status(self):
        status = self.env['ir.model.data'].get_object('scoutx', 'function_animated')
        return status.id

    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    mother_id = fields.Many2one('res.partner', 'Mother', domain=[('status', '!=', 'kids')],
        help="Mother of the current person.")
    father_id = fields.Many2one('res.partner', 'Father', domain=[('status', '!=', 'kids')],
        help="Father of the current person.")

    totem = fields.Char(string='Totem')
    birthday = fields.Date(string='Birthdate',
        help="Date of the birth of the person.")

    inscription_ids = fields.One2many('scoutx.inscription', 'partner_id', string='Inscriptinos',
        help="List of inscriptions")

    #status = fields.Many2one('scoutx.status', 'Status', default=_get_status)
    #section_id = fields.Many2one('scoutx.section', string='Section', default=False,
    #    help="The current section of the person") # todo, must be a functionnal field computed with the participation ?
