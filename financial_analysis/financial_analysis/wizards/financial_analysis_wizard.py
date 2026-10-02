from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class FinancialAnalysisWizard(models.TransientModel):
    _name = 'financial.analysis.wizard'
    _description = 'Quick Financial Analysis Wizard'

    analysis_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
    ], string='Analysis Type', required=True, default='monthly')

    period_selection = fields.Selection([
        ('current', 'Current Period'),
        ('previous', 'Previous Period'),
        ('custom', 'Custom Date Range'),
    ], string='Period Selection', required=True, default='current')

    custom_start_date = fields.Date('Start Date')
    custom_end_date = fields.Date('End Date')

    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    include_budget_comparison = fields.Boolean('Include Budget Comparison', default=True)
    include_previous_period = fields.Boolean('Include Previous Period Comparison', default=True)
    generate_report = fields.Boolean('Generate Report', default=True)

    @api.onchange('analysis_type', 'period_selection')
    def _onchange_dates(self):
        """Actualiza fechas según tipo de análisis"""
        today = fields.Date.today()

        if self.period_selection == 'current':
            if self.analysis_type == 'monthly':
                self.custom_start_date = today.replace(day=1)
                # Último día del mes
                next_month = today.replace(day=28) + timedelta(days=4)
                self.custom_end_date = next_month - timedelta(days=next_month.day)

            elif self.analysis_type == 'quarterly':
                quarter = (today.month - 1) // 3
                self.custom_start_date = today.replace(month=quarter*3+1, day=1)
                next_quarter = today.replace(month=quarter*3+4, day=1)
                self.custom_end_date = next_quarter - timedelta(days=1)

            elif self.analysis_type == 'annual':
                self.custom_start_date = today.replace(month=1, day=1)
                self.custom_end_date = today.replace(month=12, day=31)

        elif self.period_selection == 'previous':
            if self.analysis_type == 'monthly':
                # Mes anterior
                first_day = today.replace(day=1)
                last_month = first_day - timedelta(days=1)
                self.custom_start_date = last_month.replace(day=1)
                self.custom_end_date = last_month

            elif self.analysis_type == 'quarterly':
                # Trimestre anterior
                quarter = (today.month - 1) // 3 - 1
                if quarter < 0:
                    quarter = 3
                self.custom_start_date = today.replace(month=quarter*3+1, day=1)
                next_quarter = today.replace(month=quarter*3+4, day=1)
                self.custom_end_date = next_quarter - timedelta(days=1)

            elif self.analysis_type == 'annual':
                # Año anterior
                self.custom_start_date = today.replace(year=today.year-1, month=1, day=1)
                self.custom_end_date = today.replace(year=today.year-1, month=12, day=31)

    def action_create_analysis(self):
        """Crea análisis financiero con los parámetros seleccionados"""
        self.ensure_one()

        if not self.custom_start_date or not self.custom_end_date:
            raise UserError('Please specify the period dates.')

        if self.custom_start_date > self.custom_end_date:
            raise UserError('Start date cannot be after end date.')

        try:
            # Crear nombre del análisis
            name = f"{self.get_analysis_type_display()} Analysis - {self.custom_start_date} to {self.custom_end_date}"

            # Buscar análisis anterior si se requiere
            previous_analysis = None
            if self.include_previous_period:
                if self.analysis_type == 'monthly':
                    prev_start = self.custom_start_date.replace(day=1)
                    prev_end = (self.custom_start_date - timedelta(days=1))
                    prev_start = prev_end.replace(day=1)

                elif self.analysis_type == 'quarterly':
                    quarter = (self.custom_start_date.month - 1) // 3 - 1
                    if quarter < 0:
                        quarter = 3
                    prev_start = self.custom_start_date.replace(month=quarter*3+1, day=1)
                    next_quarter = self.custom_start_date.replace(month=quarter*3+4, day=1)
                    prev_end = next_quarter - timedelta(days=1)

                else:  # annual
                    prev_start = self.custom_start_date.replace(year=self.custom_start_date.year-1)
                    prev_end = self.custom_end_date.replace(year=self.custom_end_date.year-1)

                previous_analysis = self.env['financial.analysis'].search([
                    ('company_id', '=', self.company_id.id),
                    ('start_date', '=', prev_start),
                    ('end_date', '=', prev_end),
                    ('state', '!=', 'draft'),
                ], limit=1)

            # Crear análisis
            analysis = self.env['financial.analysis'].create({
                'name': name,
                'company_id': self.company_id.id,
                'analysis_type': self.analysis_type,
                'start_date': self.custom_start_date,
                'end_date': self.custom_end_date,
                'analysis_date': fields.Date.today(),
                'previous_analysis_id': previous_analysis.id if previous_analysis else None,
            })

            # Ejecutar análisis automáticamente
            analysis.action_analyze()

            # Abrir el análisis creado
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'financial.analysis',
                'res_id': analysis.id,
                'view_mode': 'form',
                'view_id': False,
            }

        except Exception as e:
            raise UserError(f'Error creating analysis: {str(e)}')
