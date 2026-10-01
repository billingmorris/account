{
    'name': 'Account Global Tax',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'author': 'El Monitor',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'depends': ['base', 'account', 'sale', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/global_tax_wizard_views.xml',
    ],
    'description': '''
Account Global Tax Module - Odoo v14

Funcionalidades:
* Asignar impuestos globales a todas las líneas de documentos
* Soporta facturas de venta y compra
* Soporta órdenes de venta y compra
* Soporta cotizaciones y presupuestos
* Interfaz wizard para configuración simple
* Filtrado automático de impuestos por tipo (venta/compra)
* Detección automática de duplicados
* Aplicar y remover impuestos con un clic
    ''',
}
