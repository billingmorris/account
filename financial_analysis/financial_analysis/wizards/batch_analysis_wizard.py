from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


class BatchAnalysisWizard(models.TransientModel):
    _name = 'batch.analysis.wizard'
    _description = 'Batch Financial Analysis Generator'

    period_type = fields.Selection([
        ('monthly', 'Monthly Analysis (All months of year)'),
        ('quarterly', 'Quarterly Analysis (All quarters of year)'),
        ('semiannual', 'Semi-annual Analysis (Both semesters of year)'),
        ('annual', 'Annual Analysis (Year only)'),
    ], string='Period Type', required=True, default='monthly')

    year = fields.Integer('Year', required=True, default=lambda self: datetime.now().year)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)

    include_budget_comparison = fields.Boolean('Include Budget Comparison', default=True)
    include_previous_period = fields.Boolean('Include Previous Period Comparison', default=True)
    generate_reports = fields.Boolean('Generate Reports', default=False)

    @api.constrains('year')
    def _check_year(self):
        """Valida que el año sea válido"""
        for record in self:
            if record.year < 2000 or record.year > datetime.now().year + 10:
                raise UserError('Please enter a valid year between 2000 and current year + 10')

    def action_generate_analyses(self):
        """Genera análisis en lote según el tipo de período"""
        self.ensure_one()

        analyses = []

        try:
            if self.period_type == 'monthly':
                analyses = self._generate_monthly_analyses()
            elif self.period_type == 'quarterly':
                analyses = self._generate_quarterly_analyses()
            elif self.period_type == 'semiannual':
                analyses = self._generate_semiannual_analyses()
            elif self.period_type == 'annual':
                analyses = self._generate_annual_analysis()

            if not analyses:
                raise UserError('No analyses were created. Please check your settings.')

            # Mostrar resumen
            message = f'Successfully created {len(analyses)} financial analysis/analyses:\n\n'
            for analysis in analyses:
                message += f'- {analysis.name}\n'

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Batch Analysis Created',
                    'message': message,
                    'type': 'success',
                    'sticky': True,
                }
            }

        except Exception as e:
            raise UserError(f'Error generating analyses: {str(e)}')

    def _generate_monthly_analyses(self):
        """Genera análisis para cada mes del año"""
        analyses = []

        for month in range(1, 13):
            start_date = datetime(self.year, month, 1).date()
            # Último día del mes
            last_day = calendar.monthrange(self.year, month)[1]
            end_date = datetime(self.year, month, last_day).date()

            month_name = datetime(self.year, month, 1).strftime('%B')
            name = f'Monthly Analysis - {month_name} {self.year}'

            analysis = self.env['financial.analysis'].create({
                'name': name,
                'company_id': self.company_id.id,
                'analysis_type': 'monthly',
                'start_date': start_date,
                'end_date': end_date,
                'analysis_date': fields.Date.today(),
            })

            # Ejecutar análisis
            try:
                analysis.action_analyze()
            except:
                pass  # Continuar si hay error en análisis individual

            analyses.append(analysis)

        return analyses

    def _generate_quarterly_analyses(self):
        """Genera análisis para cada trimestre del año"""
        analyses = []
        quarters = [
            (1, 3, 'Q1'),
            (4, 6, 'Q2'),
            (7, 9, 'Q3'),
            (10, 12, 'Q4'),
        ]

        for start_month, end_month, quarter in quarters:
            start_date = datetime(self.year, start_month, 1).date()
            last_day = calendar.monthrange(self.year, end_month)[1]
            end_date = datetime(self.year, end_month, last_day).date()

            name = f'Quarterly Analysis - {quarter} {self.year}'

            analysis = self.env['financial.analysis'].create({
                'name': name,
                'company_id': self.company_id.id,
                'analysis_type': 'quarterly',
                'start_date': start_date,
                'end_date': end_date,
                'analysis_date': fields.Date.today(),
            })

            try:
                analysis.action_analyze()
            except:
                pass

            analyses.append(analysis)

        return analyses

    def _generate_semiannual_analyses(self):
        """Genera análisis para cada semestre del año"""
        analyses = []
        semesters = [
            (1, 6, 'H1'),
            (7, 12, 'H2'),
        ]

        for start_month, end_month, semester in semesters:
            start_date = datetime(self.year, start_month, 1).date()
            last_day = calendar.monthrange(self.year, end_month)[1]
            end_date = datetime(self.year, end_month, last_day).date()

            name = f'Semi-annual Analysis - {semester} {self.year}'

            analysis = self.env['financial.analysis'].create({
                'name': name,
                'company_id': self.company_id.id,
                'analysis_type': 'semiannual',
                'start_date': start_date,
                'end_date': end_date,
                'analysis_date': fields.Date.today(),
            })

            try:
                analysis.action_analyze()
            except:
                pass

            analyses.append(analysis)

        return analyses

    def _generate_annual_analysis(self):
        """Genera análisis para el año completo"""
        analyses = []

        start_date = datetime(self.year, 1, 1).date()
        end_date = datetime(self.year, 12, 31).date()
        name = f'Annual Analysis - {self.year}'

        analysis = self.env['financial.analysis'].create({
            'name': name,
            'company_id': self.company_id.id,
            'analysis_type': 'annual',
            'start_date': start_date,
            'end_date': end_date,
            'analysis_date': fields.Date.today(),
        })

        try:
            analysis.action_analyze()
        except:
            pass

        analyses.append(analysis)

        return analyses
