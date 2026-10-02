from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class FinancialAnalysisPUC(models.Model):
    """Extensión para soportar PUC Colombiano"""
    _inherit = 'financial.analysis'

    @api.depends('start_date', 'end_date', 'company_id')
    def _compute_financial_data(self):
        """Override para soportar PUC Colombiano"""
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

                if not moves:
                    _logger.warning(f"No hay asientos publicados para el período {record.start_date} - {record.end_date}")
                    record.total_revenue = 0
                    record.cost_of_goods_sold = 0
                    record.gross_profit = 0
                    record.operating_expenses = 0
                    record.operating_profit = 0
                    record.net_income = 0
                    continue

                # PUC COLOMBIANO - Mapeo de cuentas
                # Ingresos (4000-4999)
                revenue_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '4%'),
                ])

                if not revenue_accounts:
                    _logger.warning("No se encontraron cuentas de ingresos (4xxx)")

                revenue_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', revenue_accounts.ids),
                ])
                record.total_revenue = abs(sum(revenue_lines.mapped('balance')))

                # COGS/Costo de Ventas (6000-6999)
                cogs_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '6%'),
                ])

                cogs_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', cogs_accounts.ids),
                ])
                record.cost_of_goods_sold = sum(cogs_lines.mapped('balance'))

                record.gross_profit = record.total_revenue - record.cost_of_goods_sold

                # Gastos Operacionales (5000-5999, excluyendo 6xxx)
                opex_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '=ilike', '5%'),
                ])

                opex_lines = self.env['account.move.line'].search([
                    ('move_id', 'in', moves.ids),
                    ('account_id', 'in', opex_accounts.ids),
                ])
                record.operating_expenses = sum(opex_lines.mapped('balance'))

                record.operating_profit = record.gross_profit - record.operating_expenses

                # Ingresos/Gastos Financieros (3000-3999)
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

                _logger.info(f"Financial Analysis para {record.company_id.name}:")
                _logger.info(f"  Ingresos: {record.total_revenue}")
                _logger.info(f"  COGS: {record.cost_of_goods_sold}")
                _logger.info(f"  Gastos Op: {record.operating_expenses}")
                _logger.info(f"  Ganancia Neta: {record.net_income}")

            except Exception as e:
                _logger.error(f"Error computing financial data: {e}", exc_info=True)
                record.total_revenue = 0
                record.cost_of_goods_sold = 0
                record.gross_profit = 0
                record.operating_expenses = 0
                record.operating_profit = 0
                record.net_income = 0

    @api.depends('end_date', 'company_id')
    def _compute_balance_sheet(self):
        """Override para soportar PUC Colombiano"""
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
                # PUC COLOMBIANO - Balance Sheet
                # Activos Circulantes (1100-1199)
                current_asset_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '>=', '1100'),
                    ('code', '<=', '1199'),
                ])

                current_asset_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', current_asset_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.current_assets = sum(current_asset_lines.mapped('balance'))

                # Activos Fijos (1200-1599)
                fixed_asset_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '>=', '1200'),
                    ('code', '<=', '1599'),
                ])

                fixed_asset_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', fixed_asset_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.fixed_assets = sum(fixed_asset_lines.mapped('balance'))

                record.total_assets = record.current_assets + record.fixed_assets

                # Pasivos Circulantes (2100-2199)
                current_liability_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '>=', '2100'),
                    ('code', '<=', '2199'),
                ])

                current_liability_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', current_liability_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.current_liabilities = abs(sum(current_liability_lines.mapped('balance')))

                # Pasivos Largo Plazo (2200-2299)
                long_term_liability_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '>=', '2200'),
                    ('code', '<=', '2299'),
                ])

                long_term_liability_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', long_term_liability_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.long_term_liabilities = abs(sum(long_term_liability_lines.mapped('balance')))

                record.total_liabilities = record.current_liabilities + record.long_term_liabilities

                # Patrimonio (3100-3199)
                equity_accounts = self.env['account.account'].search([
                    ('company_id', '=', record.company_id.id),
                    ('code', '>=', '3100'),
                    ('code', '<=', '3199'),
                ])

                equity_lines = self.env['account.move.line'].search([
                    ('account_id', 'in', equity_accounts.ids),
                    ('date', '<=', record.end_date),
                    ('move_id.state', '=', 'posted'),
                ])
                record.total_equity = sum(equity_lines.mapped('balance'))

                _logger.info(f"Balance Sheet para {record.company_id.name}:")
                _logger.info(f"  Activos Circulantes: {record.current_assets}")
                _logger.info(f"  Activos Fijos: {record.fixed_assets}")
                _logger.info(f"  Pasivos: {record.total_liabilities}")
                _logger.info(f"  Patrimonio: {record.total_equity}")

            except Exception as e:
                _logger.error(f"Error computing balance sheet: {e}", exc_info=True)
                record.total_assets = 0
                record.current_assets = 0
                record.fixed_assets = 0
                record.total_liabilities = 0
                record.current_liabilities = 0
                record.long_term_liabilities = 0
                record.total_equity = 0
