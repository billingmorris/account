{
    'name': 'Financial Analysis & Diagnostics',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'author': 'El Monitor',
    'website': 'https://elmonitor.net',
    'depends': ['base', 'account', 'sale', 'purchase', 'mail'],
    'data': [
        'security/ir_model_access.xml',
        'views/menu_views.xml',
        'views/financial_analysis_views_simple.xml',
        'views/financial_indicator_views.xml',
        'views/financial_analysis_report_simple.xml',
        'views/batch_analysis_wizard_views.xml',
        'data/indicator_legends_data.xml',
    ],
    'post_init_hook': '_post_install_hook',
    'installable': True,
    'application': True,
    'auto_install': False,
    'summary': 'Análisis Financiero Avanzado con Diagnósticos Automáticos y Dashboards',
    'description': '''
        Módulo de análisis financiero para Odoo 16 Community.

        Características:
        - Cálculo automático de indicadores financieros (rentabilidad, liquidez, endeudamiento)
        - Diagnósticos automáticos con insights y recomendaciones
        - Comparativas interanuales (YoY) y período a período
        - Análisis presupuesto vs realidad
        - Dashboard interactivo con KPIs
        - Reportes de tendencias y proyecciones
        - Sugerencias automáticas para mejorar márgenes
        - Análisis de eficiencia operacional

        Indicadores Incluidos:
        - ROE, ROA, Margen Neto, Margen Bruto
        - Razón Corriente, Prueba Ácida, Ciclo de Caja
        - Deuda/Patrimonio, Cobertura de Intereses
        - Rotación de Activos, Ciclo de Inventario
        - Rotación de Cuentas por Cobrar/Pagar
    ''',
}
