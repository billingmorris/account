from odoo import models, fields, api


class FinancialIndicator(models.Model):
    _name = 'financial.indicator'
    _description = 'Financial Indicator'
    _order = 'analysis_id desc, category, name'

    name = fields.Char('Indicator Name', required=True)
    analysis_id = fields.Many2one('financial.analysis', 'Analysis', required=True, ondelete='cascade')

    category = fields.Selection([
        ('profitability', 'Profitability'),
        ('liquidity', 'Liquidity'),
        ('leverage', 'Leverage'),
        ('efficiency', 'Efficiency'),
        ('growth', 'Growth'),
    ], string='Category', required=True)

    value = fields.Float('Value', required=True)
    unit = fields.Char('Unit', help='%, ratio, days, etc.')

    benchmark = fields.Float('Benchmark Value', help='Industry standard or historical comparison')
    variance = fields.Float('Variance %', compute='_compute_variance', store=True)

    status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], string='Status', compute='_compute_status', store=True)

    description = fields.Text('Description')
    notes = fields.Text('Notes')

    # Leyenda del indicador
    legend_id = fields.Many2one(
        'indicator.legend',
        string='Leyenda del Indicador',
        compute='_compute_legend',
        store=True,
        help='Definición, fórmula y rangos de interpretación para este indicador'
    )
    legend_formula = fields.Text(
        string='Fórmula',
        related='legend_id.formula'
    )
    legend_description = fields.Text(
        string='Qué Mide',
        related='legend_id.description'
    )
    legend_interpretation = fields.Text(
        string='Interpretación',
        compute='_compute_legend_interpretation',
        help='Interpretación específica del valor actual'
    )
    legend_improvement = fields.Text(
        string='Cómo Mejorar',
        related='legend_id.improvement_tips'
    )

    @api.depends('value', 'benchmark')
    def _compute_variance(self):
        """Calcula varianza respecto al benchmark"""
        for record in self:
            if record.benchmark and record.benchmark != 0:
                record.variance = ((record.value - record.benchmark) / record.benchmark) * 100
            else:
                record.variance = 0

    @api.depends('name')
    def _compute_legend(self):
        """Busca la leyenda correspondiente al indicador"""
        for record in self:
            legend = self.env['indicator.legend'].search([
                ('name', 'ilike', record.name)
            ], limit=1)
            record.legend_id = legend.id if legend else False

    @api.depends('legend_id', 'value')
    def _compute_legend_interpretation(self):
        """Genera interpretación basada en la leyenda y el valor"""
        for record in self:
            if not record.legend_id:
                record.legend_interpretation = 'No hay leyenda disponible para este indicador'
                continue

            legend = record.legend_id
            value = record.value
            interpretation = ""

            if value >= legend.excellent_min and value <= legend.excellent_max:
                interpretation = f"🟢 EXCELENTE: {legend.excellent_description}"
            elif value >= legend.good_min and value <= legend.good_max:
                interpretation = f"🟡 BUENO: {legend.good_description}"
            elif value >= legend.fair_min and value <= legend.fair_max:
                interpretation = f"🟠 REGULAR: {legend.fair_description}"
            elif value >= legend.poor_min and value <= legend.poor_max:
                interpretation = f"🔴 DEFICIENTE: {legend.poor_description}"
            else:
                interpretation = "⚫ FUERA DE RANGO: Revisar cálculo del indicador"

            record.legend_interpretation = interpretation

    @api.depends('value', 'category', 'benchmark')
    def _compute_status(self):
        """Determina estado del indicador"""
        for record in self:
            status = 'fair'

            if record.category == 'profitability':
                if record.value > 15:
                    status = 'excellent'
                elif record.value > 10:
                    status = 'good'
                elif record.value > 5:
                    status = 'fair'
                else:
                    status = 'poor'

            elif record.category == 'liquidity':
                if 1.5 <= record.value <= 3:
                    status = 'excellent'
                elif 1.2 <= record.value < 1.5 or 3 < record.value <= 5:
                    status = 'good'
                elif 1 <= record.value < 1.2 or 0.8 <= record.value < 1:
                    status = 'fair'
                else:
                    status = 'poor'

            elif record.category == 'leverage':
                if record.value < 0.5:
                    status = 'excellent'
                elif record.value < 1:
                    status = 'good'
                elif record.value < 1.5:
                    status = 'fair'
                else:
                    status = 'poor'

            elif record.category == 'efficiency':
                if record.value > 2:
                    status = 'excellent'
                elif record.value > 1.5:
                    status = 'good'
                elif record.value > 1:
                    status = 'fair'
                else:
                    status = 'poor'

            elif record.category == 'growth':
                if record.value > 10:
                    status = 'excellent'
                elif record.value > 5:
                    status = 'good'
                elif record.value > 0:
                    status = 'fair'
                else:
                    status = 'poor'

            record.status = status
