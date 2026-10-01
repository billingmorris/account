from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    global_tax_ids = fields.Many2many(
        'account.tax',
        'account_move_global_tax_rel',
        'move_id',
        'tax_id',
        string='Impuestos Globales'
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Override para filtrar dinámicamente impuestos según move_type"""
        result = super().fields_get(allfields, attributes)
        if 'global_tax_ids' in result:
            move_type = self.env.context.get('default_move_type')
            if move_type in ('out_invoice', 'out_refund'):
                # Impuestos de venta
                result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'sale')]"
            elif move_type in ('in_invoice', 'in_refund'):
                # Impuestos de compra
                result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'purchase')]"
        return result

    def action_open_global_tax_wizard(self):
        """Abrir wizard de configuración de impuestos globales"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'global.tax.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'account.move',
                'active_id': self.id,
                'default_move_type': self.move_type,
            }
        }
