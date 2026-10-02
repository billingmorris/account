from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class FinancialAnalysis(models.Model):
    _name = 'financial.analysis'
    _description = 'Financial Analysis & Diagnostics'
    _order = 'analysis_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Campos básicos
    name = fields.Char('Analysis Name', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    analysis_date = fields.Date('Analysis Date', required=True, default=fields.Date.context_today)
    analysis_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semiannual', 'Semi-annual'),
        ('annual', 'Annual'),
        ('custom', 'Custom'),
    ], string='Analysis Type', required=True, default='monthly')

    start_date = fields.Date('Period Start Date', required=True)
    end_date = fields.Date('Period End Date', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
    ], string='State', default='draft', readonly=True)

    # Relaciones
    diagnostic_ids = fields.One2many('financial.diagnostic', 'analysis_id', 'Diagnostics')
    indicator_ids = fields.One2many('financial.indicator', 'analysis_id', 'Financial Indicators')
    recommendation_ids = fields.One2many('financial.recommendation', 'analysis_id', 'Recommendations')
    budget_comparison_ids = fields.One2many('budget.comparison', 'analysis_id', 'Budget Comparisons')

    # Datos financieros base (calculados)
    total_revenue = fields.Float('Total Revenue', compute='_compute_financial_data', store=True)
    cost_of_goods_sold = fields.Float('Cost of Goods Sold', compute='_compute_financial_data', store=True)
    gross_profit = fields.Float('Gross Profit', compute='_compute_financial_data', store=True)
    operating_expenses = fields.Float('Operating Expenses', compute='_compute_financial_data', store=True)
    operating_profit = fields.Float('Operating Profit', compute='_compute_financial_data', store=True)
    net_income = fields.Float('Net Income', compute='_compute_financial_data', store=True)

    # Balance Sheet Items
    total_assets = fields.Float('Total Assets', compute='_compute_balance_sheet', store=True)
    current_assets = fields.Float('Current Assets', compute='_compute_balance_sheet', store=True)
    fixed_assets = fields.Float('Fixed Assets', compute='_compute_balance_sheet', store=True)

    total_liabilities = fields.Float('Total Liabilities', compute='_compute_balance_sheet', store=True)
    current_liabilities = fields.Float('Current Liabilities', compute='_compute_balance_sheet', store=True)
    long_term_liabilities = fields.Float('Long Term Liabilities', compute='_compute_balance_sheet', store=True)

    total_equity = fields.Float('Total Equity', compute='_compute_balance_sheet', store=True)

    # Cash Flow
    operating_cash_flow = fields.Float('Operating Cash Flow', compute='_compute_cash_flow', store=True)
    investing_cash_flow = fields.Float('Investing Cash Flow', compute='_compute_cash_flow', store=True)
    financing_cash_flow = fields.Float('Financing Cash Flow', compute='_compute_cash_flow', store=True)

    # KPIs principales
    gross_margin = fields.Float('Gross Margin %', compute='_compute_kpis', store=True)
    operating_margin = fields.Float('Operating Margin %', compute='_compute_kpis', store=True)
    net_margin = fields.Float('Net Margin %', compute='_compute_kpis', store=True)
    roe = fields.Float('ROE %', compute='_compute_kpis', store=True)
    roa = fields.Float('ROA %', compute='_compute_kpis', store=True)

    current_ratio = fields.Float('Current Ratio', compute='_compute_kpis', store=True)
    quick_ratio = fields.Float('Quick Ratio', compute='_compute_kpis', store=True)

    debt_to_equity = fields.Float('Debt to Equity', compute='_compute_kpis', store=True)
    interest_coverage = fields.Float('Interest Coverage', compute='_compute_kpis', store=True)

    asset_turnover = fields.Float('Asset Turnover', compute='_compute_kpis', store=True)

    # Análisis comparativo
    previous_analysis_id = fields.Many2one('financial.analysis', 'Previous Analysis (Comparison)')
    revenue_growth = fields.Float('Revenue Growth %', compute='_compute_comparisons', store=True)
    profit_growth = fields.Float('Profit Growth %', compute='_compute_comparisons', store=True)

    # Resumen ejecutivo
    overall_health = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ], string='Overall Financial Health', compute='_compute_overall_health', store=True)

    health_score = fields.Float('Health Score (0-100)', compute='_compute_overall_health', store=True)
    summary_text = fields.Text('Executive Summary', compute='_compute_summary')

    # Notas y observaciones
    notes = fields.Text('Notes and Observations')

    # Auditoría
    created_by = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user, readonly=True)
    created_date = fields.Datetime('Creation Date', default=fields.Datetime.now, readonly=True)
    reviewed_by = fields.Many2one('res.users', 'Reviewed By', readonly=True)
    reviewed_date = fields.Datetime('Review Date', readonly=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise UserError('Start date cannot be after end date.')

    @api.depends('start_date', 'end_date', 'company_id')
    def _compute_financial_data(self):
        """Calcula datos financieros desde asientos contables"""
        for record in self:
            if not record.start_date or not record.end_date:
                record.total_revenue = 0
                record.cost_of_goods_sold = 0
                record.gross_profit = 0
                record.operating_expenses = 0
                record.operating_profit = 0
                record.net_income = 0
                continue

            try:
                # Obtener asientos contables del período
                moves = self.env['account.move'].search([
                    ('company_id', '=', record.company_id.id),
                    ('date', '>=', record.start_date),
                    ('date', '<=', record.end_date),
                    ('state', '=', 'posted'),
                ])

                # Calcular ingresos (cuentas 4xxx)
                revenue_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '4%'),
                    ('internal_group', '=', 'income'),
                ])

                revenue_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', revenue_accounts.ids),
                ])
                record.total_revenue = abs(sum(revenue_lines.mapped('balance')))

                # Calcular COGS (cuentas 61xx)
                cogs_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '61%'),
                ])

                cogs_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', cogs_accounts.ids),
                ])
                record.cost_of_goods_sold = sum(cogs_lines.mapped('balance'))

                record.gross_profit = record.total_revenue - record.cost_of_goods_sold

                # Calcular gastos operacionales (cuentas 51xx, 52xx)
                opex_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '5%'),
                    ('code', '!=ilike', '61%'),
                ])

                opex_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', opex_accounts.ids),
                ])
                record.operating_expenses = sum(opex_lines.mapped('balance'))

                record.operating_profit = record.gross_profit - record.operating_expenses

                # Calcular ingresos netos (flujos financieros)
                financial_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '3%'),
                ])

                financial_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', financial_accounts.ids),
                ])
                financial_result = sum(financial_lines.mapped('balance'))

                record.net_income = record.operating_profit + financial_result

            except Exception as e:
                _logger.warning(f"Error computing financial data: {e}")
                record.total_revenue = 0
                record.cost_of_goods_sold = 0
                record.gross_profit = 0
                record.operating_expenses = 0
                record.operating_profit = 0
                record.net_income = 0

    @api.depends('end_date', 'company_id')
    def _compute_balance_sheet(self):
        """Calcula balance sheet al final del período"""
        for record in self:
            if not record.end_date:
                record.total_assets = 0
                record.current_assets = 0
                record.fixed_assets = 0
                record.total_liabilities = 0
                record.current_liabilities = 0
                record.long_term_liabilities = 0
                record.total_equity = 0
                continue

            try:
                # Activos circulantes (cuentas 11xx)
                current_asset_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '11%'),
                    ('internal_group', '=', 'asset'),
                ])

                current_asset_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', current_asset_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.current_assets = sum(current_asset_lines.mapped('balance'))

                # Activos fijos (cuentas 12xx, 13xx)
                fixed_asset_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '1%'),
                    ('code', '!=ilike', '11%'),
                    ('internal_group', '=', 'asset'),
                ])

                fixed_asset_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', fixed_asset_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.fixed_assets = sum(fixed_asset_lines.mapped('balance'))

                record.total_assets = record.current_assets + record.fixed_assets

                # Pasivos circulantes (cuentas 21xx)
                current_liability_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '21%'),
                    ('internal_group', '=', 'liability'),
                ])

                current_liability_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', current_liability_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.current_liabilities = abs(sum(current_liability_lines.mapped('balance')))

                # Pasivos largo plazo (cuentas 22xx, 23xx)
                long_term_liability_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '2%'),
                    ('code', '!=ilike', '21%'),
                    ('internal_group', '=', 'liability'),
                ])

                long_term_liability_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', long_term_liability_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.long_term_liabilities = abs(sum(long_term_liability_lines.mapped('balance')))

                record.total_liabilities = record.current_liabilities + record.long_term_liabilities

                # Patrimonio (cuentas 31xx, 32xx)
                equity_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '3%'),
                    ('internal_group', '=', 'equity'),
                ])

                equity_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', equity_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.total_equity = sum(equity_lines.mapped('balance'))

            except Exception as e:
                _logger.warning(f"Error computing balance sheet: {e}")
                record.total_assets = 0
                record.current_assets = 0
                record.fixed_assets = 0
                record.total_liabilities = 0
                record.current_liabilities = 0
                record.long_term_liabilities = 0
                record.total_equity = 0

    @api.depends('end_date', 'company_id')
    def _compute_cash_flow(self):
        """Calcula flujo de caja"""
        for record in self:
            if not record.end_date or not record.start_date:
                record.operating_cash_flow = 0
                record.investing_cash_flow = 0
                record.financing_cash_flow = 0
                continue

            try:
                # Simplificado: basado en cambios en cuentas
                moves = self.env['account.move'].search([
                    ('company_id', '=', record.company_id.id),
                    ('date', '>=', record.start_date),
                    ('date', '<=', record.end_date),
                    ('state', '=', 'posted'),
                ])

                # Cash flow operativo: cambios en activos/pasivos circulantes
                operating_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', 'in', ['1101', '1105', '2101', '2105']),  # Caja, bancos, cxc, cxp
                ])

                operating_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', operating_accounts.ids),
                ])
                record.operating_cash_flow = sum(operating_lines.mapped('balance'))

                # Simplificado para esta versión
                record.investing_cash_flow = 0
                record.financing_cash_flow = 0

            except Exception as e:
                _logger.warning(f"Error computing cash flow: {e}")
                record.operating_cash_flow = 0
                record.investing_cash_flow = 0
                record.financing_cash_flow = 0

    @api.depends('total_revenue', 'cost_of_goods_sold', 'operating_profit', 'net_income',
                 'total_assets', 'total_equity', 'current_assets', 'current_liabilities',
                 'total_liabilities')
    def _compute_kpis(self):
        """Calcula indicadores financieros clave"""
        for record in self:
            # Márgenes
            record.gross_margin = (record.gross_profit / record.total_revenue * 100) if record.total_revenue else 0
            record.operating_margin = (record.operating_profit / record.total_revenue * 100) if record.total_revenue else 0
            record.net_margin = (record.net_income / record.total_revenue * 100) if record.total_revenue else 0

            # Rentabilidad
            record.roa = (record.net_income / record.total_assets * 100) if record.total_assets else 0
            record.roe = (record.net_income / record.total_equity * 100) if record.total_equity else 0

            # Liquidez
            record.current_ratio = record.current_assets / record.current_liabilities if record.current_liabilities else 0
            record.quick_ratio = (record.current_assets - 0) / record.current_liabilities if record.current_liabilities else 0  # Simplified

            # Endeudamiento
            record.debt_to_equity = record.total_liabilities / record.total_equity if record.total_equity else 0
            record.interest_coverage = record.operating_profit / 1 if record.operating_profit > 0 else 0  # Simplified

            # Eficiencia
            record.asset_turnover = record.total_revenue / record.total_assets if record.total_assets else 0

    @api.depends('revenue_growth', 'profit_growth', 'current_ratio', 'debt_to_equity', 'net_margin', 'roe')
    def _compute_overall_health(self):
        """Calcula calificación general de salud financiera"""
        for record in self:
            score = 50  # Base score

            # Rentabilidad (25 puntos)
            if record.net_margin > 20:
                score += 25
            elif record.net_margin > 15:
                score += 20
            elif record.net_margin > 10:
                score += 15
            elif record.net_margin > 5:
                score += 10
            elif record.net_margin > 0:
                score += 5

            # Liquidez (25 puntos)
            if 1.5 <= record.current_ratio <= 3:
                score += 25
            elif 1.2 <= record.current_ratio < 1.5:
                score += 20
            elif 1 <= record.current_ratio < 1.2:
                score += 15
            elif 0.8 <= record.current_ratio < 1:
                score += 10

            # Endeudamiento (25 puntos)
            if record.debt_to_equity < 0.5:
                score += 25
            elif record.debt_to_equity < 1:
                score += 20
            elif record.debt_to_equity < 1.5:
                score += 15
            elif record.debt_to_equity < 2:
                score += 10

            # Crecimiento (25 puntos)
            if record.revenue_growth > 10:
                score += 25
            elif record.revenue_growth > 5:
                score += 20
            elif record.revenue_growth > 0:
                score += 15
            elif record.revenue_growth >= -5:
                score += 10

            record.health_score = min(score, 100)

            if record.health_score >= 85:
                record.overall_health = 'excellent'
            elif record.health_score >= 70:
                record.overall_health = 'good'
            elif record.health_score >= 50:
                record.overall_health = 'fair'
            elif record.health_score >= 30:
                record.overall_health = 'poor'
            else:
                record.overall_health = 'critical'

    @api.depends('previous_analysis_id', 'total_revenue', 'net_income')
    def _compute_comparisons(self):
        """Calcula cambios respecto al período anterior"""
        for record in self:
            if record.previous_analysis_id:
                prev = record.previous_analysis_id
                record.revenue_growth = ((record.total_revenue - prev.total_revenue) / prev.total_revenue * 100) if prev.total_revenue else 0
                record.profit_growth = ((record.net_income - prev.net_income) / abs(prev.net_income) * 100) if prev.net_income else 0
            else:
                record.revenue_growth = 0
                record.profit_growth = 0

    def _compute_summary(self):
        """Genera resumen ejecutivo"""
        for record in self:
            summary = f"Financial Analysis for period {record.start_date} to {record.end_date}\n\n"
            summary += f"Overall Health: {record.overall_health.upper()} (Score: {record.health_score:.1f}/100)\n\n"
            summary += f"Key Metrics:\n"
            summary += f"- Revenue: ${record.total_revenue:,.2f}\n"
            summary += f"- Net Income: ${record.net_income:,.2f}\n"
            summary += f"- Net Margin: {record.net_margin:.2f}%\n"
            summary += f"- ROE: {record.roe:.2f}%\n"
            summary += f"- Current Ratio: {record.current_ratio:.2f}\n"
            summary += f"- Debt/Equity: {record.debt_to_equity:.2f}\n"

            record.summary_text = summary

    def action_analyze(self):
        """Ejecuta análisis completo"""
        self.ensure_one()

        if self.state != 'draft':
            raise UserError('Analysis must be in draft state to analyze.')

        try:
            # Crear indicadores financieros
            self._create_financial_indicators()

            # Crear diagnósticos
            self._create_diagnostics()

            # Crear recomendaciones
            self._create_recommendations()

            # Marcar como completado
            self.state = 'completed'

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Financial analysis completed successfully.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            raise UserError(f'Error during analysis: {str(e)}')

    def _create_financial_indicators(self):
        """Crea registros de indicadores financieros"""
        self.ensure_one()

        indicators_data = [
            ('Gross Margin', 'profitability', self.gross_margin),
            ('Operating Margin', 'profitability', self.operating_margin),
            ('Net Margin', 'profitability', self.net_margin),
            ('ROE', 'profitability', self.roe),
            ('ROA', 'profitability', self.roa),
            ('Current Ratio', 'liquidity', self.current_ratio),
            ('Quick Ratio', 'liquidity', self.quick_ratio),
            ('Debt to Equity', 'leverage', self.debt_to_equity),
            ('Interest Coverage', 'leverage', self.interest_coverage),
            ('Asset Turnover', 'efficiency', self.asset_turnover),
        ]

        for name, category, value in indicators_data:
            self.env['financial.indicator'].create({
                'name': name,
                'analysis_id': self.id,
                'category': category,
                'value': value,
                'unit': '%' if category == 'profitability' else 'ratio',
            })

    def _create_diagnostics(self):
        """Crea diagnósticos automáticos"""
        self.ensure_one()

        diagnostics = []

        # Análisis de rentabilidad
        if self.net_margin < 5:
            diagnostics.append({
                'name': 'Low Profitability',
                'category': 'profitability',
                'severity': 'high' if self.net_margin < 0 else 'medium',
                'description': f'Net margin is {self.net_margin:.2f}%, below healthy levels (target: >10%)',
                'analysis_id': self.id,
            })
        elif self.net_margin > 20:
            diagnostics.append({
                'name': 'Excellent Profitability',
                'category': 'profitability',
                'severity': 'info',
                'description': f'Net margin of {self.net_margin:.2f}% indicates strong profitability.',
                'analysis_id': self.id,
            })

        # Análisis de liquidez
        if self.current_ratio < 1:
            diagnostics.append({
                'name': 'Liquidity Crisis',
                'category': 'liquidity',
                'severity': 'critical',
                'description': f'Current ratio of {self.current_ratio:.2f} indicates inability to cover short-term obligations.',
                'analysis_id': self.id,
            })
        elif self.current_ratio < 1.5:
            diagnostics.append({
                'name': 'Low Liquidity',
                'category': 'liquidity',
                'severity': 'high',
                'description': f'Current ratio of {self.current_ratio:.2f} is below recommended levels (target: 1.5-3.0).',
                'analysis_id': self.id,
            })
        elif self.current_ratio > 3:
            diagnostics.append({
                'name': 'Excess Liquidity',
                'category': 'liquidity',
                'severity': 'medium',
                'description': f'Current ratio of {self.current_ratio:.2f} suggests underutilized resources.',
                'analysis_id': self.id,
            })

        # Análisis de endeudamiento
        if self.debt_to_equity > 2:
            diagnostics.append({
                'name': 'High Leverage',
                'category': 'leverage',
                'severity': 'high',
                'description': f'Debt-to-equity ratio of {self.debt_to_equity:.2f} indicates high financial risk.',
                'analysis_id': self.id,
            })
        elif self.debt_to_equity > 1:
            diagnostics.append({
                'name': 'Moderate Leverage',
                'category': 'leverage',
                'severity': 'medium',
                'description': f'Debt-to-equity ratio of {self.debt_to_equity:.2f} is acceptable but should be monitored.',
                'analysis_id': self.id,
            })

        # Crear diagnósticos
        for diag_data in diagnostics:
            self.env['financial.diagnostic'].create(diag_data)

    def _create_recommendations(self):
        """Crea recomendaciones automáticas"""
        self.ensure_one()

        recommendations = []

        # Recomendaciones basadas en márgenes
        if self.net_margin < 10:
            recommendations.append({
                'name': 'Improve Profitability',
                'priority': 'high',
                'category': 'profitability',
                'description': 'Current profit margins are below industry standards. Consider cost reduction initiatives or price optimization.',
                'expected_impact': 'Increase net margin by 2-5% through operational efficiency.',
                'analysis_id': self.id,
            })

        # Recomendaciones basadas en liquidez
        if self.current_ratio < 1.5:
            recommendations.append({
                'name': 'Improve Working Capital',
                'priority': 'high',
                'category': 'liquidity',
                'description': 'Strengthen liquidity position by accelerating collections or negotiating better payment terms with suppliers.',
                'expected_impact': 'Increase current ratio to 1.5-2.0 range.',
                'analysis_id': self.id,
            })

        # Recomendaciones basadas en endeudamiento
        if self.debt_to_equity > 1.5:
            recommendations.append({
                'name': 'Reduce Debt Level',
                'priority': 'high',
                'category': 'leverage',
                'description': 'Develop a debt reduction strategy through profit retention or asset sales to lower financial risk.',
                'expected_impact': 'Reduce debt-to-equity ratio below 1.0.',
                'analysis_id': self.id,
            })

        # Recomendaciones de eficiencia
        if self.asset_turnover < 1:
            recommendations.append({
                'name': 'Improve Asset Utilization',
                'priority': 'medium',
                'category': 'efficiency',
                'description': 'Increase sales or reduce non-productive assets to improve asset turnover ratio.',
                'expected_impact': 'Increase asset turnover by 20-30%.',
                'analysis_id': self.id,
            })

        # Crear recomendaciones
        for rec_data in recommendations:
            self.env['financial.recommendation'].create(rec_data)

    def action_mark_reviewed(self):
        """Marca análisis como revisado"""
        self.ensure_one()
        self.state = 'reviewed'
        self.reviewed_by = self.env.user
        self.reviewed_date = fields.Datetime.now()

    def action_reset_to_draft(self):
        """Resetea análisis a estado draft"""
        self.ensure_one()
        self.state = 'draft'
        self.diagnostic_ids.unlink()
        self.indicator_ids.unlink()
        self.recommendation_ids.unlink()

    def action_print_report(self):
        """Genera y descarga reporte PDF"""
        return self.env.ref('financial_analysis.action_financial_analysis_report').report_action(self)
