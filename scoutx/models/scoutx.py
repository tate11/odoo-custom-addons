import openerp
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning



class scoutx_role(models.Model):

    _name = 'scoutx.role'
    _description = 'Status of a person'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    is_section_function = fields.Boolean('Is a function', default=False,
        help="Check this if the role is a status in a group section. (i.e. : section chief, responsible, ...)")




class scoutx_period(models.Model):

    _name = 'scoutx.period'
    _description = 'Scout Year'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    start_date = fields.Date(string='Start Date',
        help="Keep empty to use the current date")
    end_date = fields.Date(string='End Date',
        help="Keep empty to use the current date")


    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_closing_date(self):
        if self.end_date < self.start_date:
            raise Warning(_('Closing Date cannot be set before Beginning Date.'))

    @api.returns('self')
    def find_period(self, date=None, redirect=False):
        """ return the period record for the given date. If not given, get the one for the current date. 
            :param date : the date of the period wanted
            :param redirect : if True, will redirect to the period tree view if no period is found for the given date.
            :return period record if period found for the given date
                    False otherwise (if redirect=False, else redirect to tree view)
        """
        if not date:
            date = fields.Datetime.now()
        domain = [('start_date', '<=', date), ('end_date', '>=', date)]
        result = self.search(domain, limit=1)
        if not result:
            if redirect:
                model, action_id = self.env['ir.model.data'].get_object_reference('scoutx', 'action_scoutx_period')
                msg = _('There is no period defined for this date: %s.\nPlease go to Configuration > Periods.') % date
                raise openerp.exceptions.RedirectWarning(msg, action_id, _('Go to the configuration panel'))
            else:
                return False
        return result



class scoutx_section(models.Model):

    _name = 'scoutx.section'
    _description = 'Group of animated'
    _rec_name = 'name'

    @api.model
    def _get_gender(self):
        return [('male', 'Male'), ('female', 'Female'), ('mixte', 'Mixte')]

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



class scoutx_group(models.Model):

    _name = 'scoutx.group'
    _description = 'Scout Group'

    name = fields.Char(string='Name', required=True, 
        help='The name of the group')
    section_id = fields.Many2one('scoutx.section', string='Section', required=True,
        help="The section of the group")
    partner_ids = fields.One2many('res.partner', 'group_id', string='Members')
    #TODO fields : code federation, ...


class scoutx_inscription(models.Model):

    _name = 'scoutx.inscription'
    _description = 'Insciption of a person in a group.'


    role_id = fields.Many2one('scoutx.role', string='Function', domain=[('is_section_function', '=', True)],
        help="Function of the person, during the period")
    partner_id = fields.Many2one('res.partner', string='Person', required=True,
        help="Person participating", ondelete="cascade")
    group_id = fields.Many2one('scoutx.group', string='Group', required=True,
        help="The section of the inscription")
    section_id = fields.Many2one('scoutx.section', string='Section', related='group_id.section_id', store=True, readonly=True,
        help="Section of the group")
    period_id = fields.Many2one('scoutx.period', string='Scout Period', required=True,
        help="The scout period the person got the role in the section")


    @api.one
    @api.constrains('period_id', 'partner_id')
    def _check_unique_period_partner(self):
        inscriptions = self.search([('partner_id', '=', self.partner_id.id), ('period_id', '=', self.period_id.id)])
        if len(inscriptions) > 1:
            raise Warning(_('The member %s already have an inscription for the period %s.') % (self.partner_id.name, self.period_id.name))

    # @api.one
    # @api.constrains('section_id', 'partner_id')
    # def _check_gender_compatibility(self):
    #     if self.partner_id.gender != self.section_id.gender and self.section_id.gender != 'mixte':
    #         raise Warning(_('The member %s can not be in the section %s, because the gender of this one is %s') % (self.partner_id.name, self.section_id.name, self.section_id.gender))


