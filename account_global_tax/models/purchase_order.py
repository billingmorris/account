from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    global_tax_ids = fields.Many2many(
        'account.tax',
        'purchase_order_global_tax_rel',
        'order_id',
        'tax_id',
        string='Impuestos Globales',
        domain="[('type_tax_use', '=', 'purchase')]"
    )

    def action_open_global_tax_wizard(self):
        """Abrir wizard de configuración de impuestos globales"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'global.tax.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'active_model': 'purchase.order',
                'active_id': self.id,
            }
        }
