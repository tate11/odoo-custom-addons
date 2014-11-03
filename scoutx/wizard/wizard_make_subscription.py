from openerp import api, fields, models



class scoutx_make_subscription_wizard(models.TransientModel):

    _name = 'scoutx.make.subscription.wizard'


    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    wizard_line_ids = fields.One2many('scoutx.make.subscription.line.wizard', 'wizard_id', string='Inscriptinos',
        help="List of inscriptions")
    role_id = fields.Many2one('scoutx.role', string='Function', domain=[('is_section_function','=',True)],
        help="Function of the person, during the period")
    section_id = fields.Many2one('scoutx.section', string='Section', required=True,
        help="The section of the inscription")
    period_id = fields.Many2one('scoutx.period', string='Scout Period', required=True,
        help="The scout period the person got the role in the section")


    @api.onchange('section_id')
    def _onchange_section_id(self):
        # Control the age and the gender of the partner with the section
        for line in self.wizard_line_ids:
            if self.section_id:
                if line.partner_gender != self.section_id.gender and self.section_id.gender != 'mixte':
                    line.error = 'error_gender'
                else:
                    if self.section_id.start_age and self.section_id.end_age:
                        if not (self.section_id.start_age <= line.partner_age and line.partner_age <= self.section_id.end_age):
                            line.error = 'error_age'
                        else:
                            line.error = 'ok'
                    else:
                        line.error = 'ok'



    # --------------------------------------------------
    # METHODS
    # --------------------------------------------------
    @api.model
    def default_get(self, fields):
        """ create the lines on the wizard """
        res = super(scoutx_make_subscription_wizard, self).default_get(fields)

        active_ids = self._context.get('active_ids', [])

        # create order lines
        if active_ids:
            lines = []
            for partner in self.env['res.partner'].browse(active_ids):
                lines.append((0, 0, {
                    'partner_id': partner.id,
                    'partner_name': partner.name,
                    'partner_gender' : partner.gender,
                    'partner_age' : partner.age,
                }))
            res['wizard_line_ids'] = lines
        return res


    @api.multi
    def action_apply(self):
        Inscription = self.env['scoutx.inscription']
        for wizard in self:
            for line in wizard.wizard_line_ids:
                Inscription.create({
                    'partner_id' : line.partner_id.id,
                    'role_id' : wizard.role_id.id,
                    'section_id' : wizard.section_id.id,
                    'period_id' : wizard.period_id.id,
                })
        return {'type': 'ir.actions.act_window_close'}



class scoutx_make_subscription_line_wizard(models.TransientModel):

    _name = 'scoutx.make.subscription.line.wizard'

   
    # --------------------------------------------------
    # MODEL FIELDS
    # --------------------------------------------------
    wizard_id = fields.Many2one('scoutx.make.subscription.wizard', 'Wizard')

    partner_id = fields.Many2one('res.partner', string='Partner')
    partner_name = fields.Char(strng='Name')
    partner_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', required=True)
    partner_age = fields.Float(string='Age')
    error = fields.Selection([('ok', 'OK'), ('error_age', 'Too young or to old'), ('error_gender', 'Not correct gender')], string='Error')
    

