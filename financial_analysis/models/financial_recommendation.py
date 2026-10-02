from odoo import models, fields, api


class FinancialRecommendation(models.Model):
    _name = 'financial.recommendation'
    _description = 'Financial Recommendation'
    _order = 'analysis_id desc, priority, name'

    name = fields.Char('Recommendation', required=True)
    analysis_id = fields.Many2one('financial.analysis', 'Analysis', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', 'Company', related='analysis_id.company_id', store=True, readonly=True)

    category = fields.Selection([
        ('profitability', 'Improve Profitability'),
        ('liquidity', 'Improve Liquidity'),
        ('leverage', 'Optimize Leverage'),
        ('efficiency', 'Operational Efficiency'),
        ('margin', 'Margin Improvement'),
        ('growth', 'Revenue Growth'),
        ('cost', 'Cost Reduction'),
        ('other', 'Other'),
    ], string='Category', required=True)

    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Priority', required=True, default='medium')

    description = fields.Text('Description', required=True)

    # Impacto esperado
    expected_impact = fields.Text('Expected Impact')
    estimated_benefit = fields.Monetary('Estimated Benefit', currency_field='company_currency_id')
    implementation_cost = fields.Monetary('Implementation Cost', currency_field='company_currency_id')
    roi = fields.Float('Expected ROI %', compute='_compute_roi', store=True)

    # Currency field reference
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, readonly=True)

    # Timeline
    estimated_days = fields.Integer('Estimated Days to Implement')

    # Acciones
    action_steps = fields.Text('Action Steps')
    owner_id = fields.Many2one('res.users', 'Owner')
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], string='Status', default='not_started')

    # Seguimiento
    start_date = fields.Date('Start Date')
    completion_date = fields.Date('Completion Date')
    actual_benefit = fields.Monetary('Actual Benefit Realized', currency_field='company_currency_id')
    notes = fields.Text('Notes')

    # Auditoría
    created_date = fields.Datetime('Created', default=fields.Datetime.now, readonly=True)

    @api.depends('estimated_benefit', 'implementation_cost')
    def _compute_roi(self):
        """Calcula ROI esperado"""
        for record in self:
            if record.implementation_cost and record.implementation_cost > 0:
                record.roi = ((record.estimated_benefit - record.implementation_cost) / record.implementation_cost) * 100
            else:
                record.roi = 0

    def action_start_implementation(self):
        """Inicia implementación de recomendación"""
        self.ensure_one()
        self.status = 'in_progress'
        if not self.start_date:
            self.start_date = fields.Date.today()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Implementation Started',
                'message': f'Recommendation "{self.name}" implementation started.',
                'type': 'info',
                'sticky': False,
            }
        }

    def action_mark_completed(self):
        """Marca recomendación como completada"""
        self.ensure_one()
        self.status = 'completed'
        if not self.completion_date:
            self.completion_date = fields.Date.today()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Recommendation "{self.name}" marked as completed.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_hold(self):
        """Pone recomendación en espera"""
        self.ensure_one()
        self.status = 'on_hold'

    def action_resume(self):
        """Reanuda recomendación"""
        self.ensure_one()
        self.status = 'in_progress'
