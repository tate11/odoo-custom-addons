
from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning



class scoutx_role(models.Model):

    _name = 'scoutx.role'
    _description = 'Status of a person'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    is_section_function = fields.Boolean('Is a function', default=False,
        help="True means this role is a function a person can have in a section. (e.i. : section chief, responsible, ...)")




class scoutx_period(models.Model):

    _name = 'scoutx.period'
    _description = 'Scout Year'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date',
        help="Keep empty to use the current date")
    end_date = fields.Date(string='End Date',
        help="Keep empty to use the current date")




class scoutx_section(models.Model):

    _name = 'scoutx.section'
    _description = 'Group of animated'
    _rec_name = 'name'

    @api.model
    def _get_gender(self):
        return [('male', 'Male'), ('female', 'Female'), ('mixte', 'Mixte')]

    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    name = fields.Char(string='Name', required=True,
        help="The name of the section.")
    description = fields.Text(string='Description',
        help="The description of the section.")
    start_age = fields.Integer(string='Start Age',
        help="The minimum age to be in the section.")
    end_age = fields.Integer(string='End Age',
        help="The maximum age to be in the section.")
    gender = fields.Selection('_get_gender', string='Gender',
        required=True, default='mixte')
    #TODO : add image field logo



class scoutx_inscription(models.Model):

    _name = 'scoutx.inscription'
    _description = 'Insciption of a person in a section.'


    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    role_id = fields.Many2one('scoutx.role', string='Function', domain=[('is_section_function','=',True)],
        help="Function of the person, during the period")
    partner_id = fields.Many2one('res.partner', string='Person', required=True,
        help="Person participating")
    section_id = fields.Many2one('scoutx.section', string='Section', required=True,
        help="The section of the inscription")
    period_id = fields.Many2one('scoutx.period', string='Scout Period', required=True,
        help="The scout period the person got the role in the section")
