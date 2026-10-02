from odoo import models, fields, api


class BudgetComparison(models.Model):
    _name = 'budget.comparison'
    _description = 'Budget vs Actual Comparison'
    _order = 'analysis_id desc, line_type, account_name'

    analysis_id = fields.Many2one('financial.analysis', 'Analysis', required=True, ondelete='cascade')

    account_name = fields.Char('Account', required=True)
    account_code = fields.Char('Account Code')

    line_type = fields.Selection([
        ('revenue', 'Revenue'),
        ('cost', 'Cost'),
        ('expense', 'Expense'),
        ('investment', 'Investment'),
    ], string='Type', required=True)

    # Datos presupuestados
    budget_amount = fields.Float('Budgeted Amount')

    # Datos reales
    actual_amount = fields.Float('Actual Amount')

    # Análisis
    variance = fields.Float('Variance', compute='_compute_variance', store=True)
    variance_pct = fields.Float('Variance %', compute='_compute_variance', store=True)

    status = fields.Selection([
        ('on_target', 'On Target'),
        ('favorable', 'Favorable'),
        ('unfavorable', 'Unfavorable'),
    ], string='Status', compute='_compute_status', store=True)

    notes = fields.Text('Notes')

    @api.depends('budget_amount', 'actual_amount', 'line_type')
    def _compute_variance(self):
        """Calcula varianza presupuestaria"""
        for record in self:
            record.variance = record.actual_amount - record.budget_amount

            if record.budget_amount != 0:
                record.variance_pct = (record.variance / record.budget_amount) * 100
            else:
                record.variance_pct = 0

    @api.depends('variance', 'variance_pct', 'line_type')
    def _compute_status(self):
        """Determina estado de presupuesto"""
        for record in self:
            # Para ingresos: más alto es mejor (favorable = variance positivo)
            # Para gastos: más bajo es mejor (favorable = variance negativo)

            if record.line_type == 'revenue':
                if abs(record.variance_pct) <= 5:
                    record.status = 'on_target'
                elif record.variance > 0:
                    record.status = 'favorable'
                else:
                    record.status = 'unfavorable'

            else:  # cost, expense, investment
                if abs(record.variance_pct) <= 5:
                    record.status = 'on_target'
                elif record.variance < 0:
                    record.status = 'favorable'
                else:
                    record.status = 'unfavorable'
