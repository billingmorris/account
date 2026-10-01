from odoo import models, fields, api
from odoo.exceptions import UserError


class GlobalTaxWizard(models.TransientModel):
    _name = 'global.tax.wizard'
    _description = 'Global Tax Configuration Wizard'

    document_model = fields.Char(string='Document Model', readonly=True)
    document_id = fields.Integer(string='Document ID', readonly=True)
    move_type = fields.Char(string='Move Type', readonly=True)  # Para filtrar impuestos
    global_tax_ids = fields.Many2many(
        'account.tax',
        'wizard_tax_rel',
        'wizard_id',
        'tax_id',
        string='Seleccionar Impuestos'
    )
    total_lines = fields.Integer(string='Total líneas', readonly=True)
    tax_count = fields.Integer(string='Impuestos seleccionados', compute='_compute_tax_count')

    @api.depends('global_tax_ids')
    def _compute_tax_count(self):
        for wizard in self:
            wizard.tax_count = len(wizard.global_tax_ids)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Filtrar dinámicamente los impuestos según el tipo de documento"""
        result = super().fields_get(allfields, attributes)

        if 'global_tax_ids' in result:
            active_model = self.env.context.get('active_model')
            move_type = self.env.context.get('default_move_type')

            # Filtrar según el tipo de documento
            if active_model == 'account.move':
                if move_type in ('out_invoice', 'out_refund'):
                    # Facturas de venta: solo impuestos de venta
                    result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'sale')]"
                elif move_type in ('in_invoice', 'in_refund'):
                    # Facturas de compra: solo impuestos de compra
                    result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'purchase')]"
            elif active_model == 'sale.order':
                # Órdenes de venta: solo impuestos de venta
                result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'sale')]"
            elif active_model == 'purchase.order':
                # Órdenes de compra: solo impuestos de compra
                result['global_tax_ids']['domain'] = "[('type_tax_use', '=', 'purchase')]"

        return result

    @api.model
    def default_get(self, fields_list):
        """Pre-llenar wizard con datos del documento"""
        defaults = super().default_get(fields_list)

        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        if active_model and active_id:
            document = self.env[active_model].browse(active_id)

            defaults['document_model'] = active_model
            defaults['document_id'] = active_id

            # Contar líneas y obtener tipo de documento
            if active_model == 'account.move':
                defaults['total_lines'] = len(document.invoice_line_ids)
                defaults['move_type'] = document.move_type
            elif active_model == 'sale.order':
                defaults['total_lines'] = len(document.order_line)
                defaults['move_type'] = 'sale'
            elif active_model == 'purchase.order':
                defaults['total_lines'] = len(document.order_line)
                defaults['move_type'] = 'purchase'

            # Pre-llenar impuestos seleccionados
            if hasattr(document, 'global_tax_ids'):
                defaults['global_tax_ids'] = [(6, 0, document.global_tax_ids.ids)]

        return defaults

    def action_apply_taxes(self):
        """Aplicar impuestos seleccionados a todas las líneas"""
        if not self.global_tax_ids:
            raise UserError('Selecciona al menos un impuesto primero')

        document = self.env[self.document_model].browse(self.document_id)

        # Obtener líneas según tipo de documento
        if self.document_model == 'account.move':
            lines = document.invoice_line_ids
            tax_field_name = 'tax_ids'
        elif self.document_model == 'sale.order':
            lines = document.order_line
            tax_field_name = 'tax_id'
        elif self.document_model == 'purchase.order':
            lines = document.order_line
            tax_field_name = 'taxes_id'
        else:
            raise UserError(f'Modelo no soportado: {self.document_model}')

        # Aplicar impuestos a cada línea
        for line in lines:
            current_taxes = line[tax_field_name]

            # Agregar nuevos impuestos evitando duplicados
            for tax in self.global_tax_ids:
                if tax not in current_taxes:
                    line[tax_field_name] = [(4, tax.id)]

        # Actualizar documento con impuestos globales
        document.global_tax_ids = [(6, 0, self.global_tax_ids.ids)]

        # Registrar en chatter
        document.message_post(
            body=f'Se aplicaron {len(self.global_tax_ids)} impuestos globales a {len(lines)} líneas'
        )

        return {'type': 'ir.actions.act_window_close'}

    def action_remove_taxes(self):
        """Remover impuestos seleccionados de todas las líneas"""
        if not self.global_tax_ids:
            raise UserError('Selecciona al menos un impuesto primero')

        document = self.env[self.document_model].browse(self.document_id)

        # Obtener líneas según tipo de documento
        if self.document_model == 'account.move':
            lines = document.invoice_line_ids
            tax_field_name = 'tax_ids'
        elif self.document_model == 'sale.order':
            lines = document.order_line
            tax_field_name = 'tax_id'
        elif self.document_model == 'purchase.order':
            lines = document.order_line
            tax_field_name = 'taxes_id'
        else:
            raise UserError(f'Modelo no soportado: {self.document_model}')

        # Remover impuestos de cada línea
        for line in lines:
            for tax in self.global_tax_ids:
                if tax in line[tax_field_name]:
                    line[tax_field_name] = [(3, tax.id)]

        # Limpiar impuestos globales
        document.global_tax_ids = [(5,)]

        # Registrar en chatter
        document.message_post(
            body=f'Se removieron {len(self.global_tax_ids)} impuestos globales de {len(lines)} líneas'
        )

        return {'type': 'ir.actions.act_window_close'}
