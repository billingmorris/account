from odoo import models, fields, api


class FinancialDiagnostic(models.Model):
    _name = 'financial.diagnostic'
    _description = 'Financial Diagnostic'
    _order = 'analysis_id desc, severity, name'

    name = fields.Char('Diagnostic Title', required=True)
    analysis_id = fields.Many2one('financial.analysis', 'Analysis', required=True, ondelete='cascade')

    category = fields.Selection([
        ('profitability', 'Profitability'),
        ('liquidity', 'Liquidity'),
        ('leverage', 'Leverage'),
        ('efficiency', 'Efficiency'),
        ('solvency', 'Solvency'),
        ('growth', 'Growth'),
    ], string='Category', required=True)

    severity = fields.Selection([
        ('info', 'Informational'),
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('critical', 'Critical'),
    ], string='Severity Level', required=True)

    description = fields.Text('Description', required=True)

    # Métricas relacionadas
    metric_name = fields.Char('Related Metric')
    metric_value = fields.Float('Current Value')
    metric_target = fields.Float('Target Value')
    metric_variance = fields.Float('Variance %')

    # Estado
    status = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ], string='Status', default='new')

    # Seguimiento
    owner_id = fields.Many2one('res.users', 'Assigned To')
    deadline = fields.Date('Action Deadline')
    action_notes = fields.Text('Action Notes')

    # Auditoría
    created_date = fields.Datetime('Created', default=fields.Datetime.now, readonly=True)

    @api.model
    def create(self, vals):
        """Hook para crear diagnósticos"""
        record = super().create(vals)
        # Aquí se pueden agregar acciones adicionales
        return record

    def action_acknowledge(self):
        """Marca diagnóstico como reconocido"""
        self.status = 'acknowledged'

    def action_start_resolution(self):
        """Marca como en progreso"""
        self.ensure_one()
        self.status = 'in_progress'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Status Updated',
                'message': f'Diagnostic "{self.name}" marked as in progress.',
                'type': 'info',
                'sticky': False,
            }
        }

    def action_mark_resolved(self):
        """Marca diagnóstico como resuelto"""
        self.ensure_one()
        if not self.action_notes:
            raise UserError('Please add action notes before marking as resolved.')

        self.status = 'resolved'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Diagnostic "{self.name}" marked as resolved.',
                'type': 'success',
                'sticky': False,
            }
        }
