# -*- coding: utf-8 -*-
{
    'name': "mod2",
    'summary': "This module sum2",
    'description': """
        This module des2
    """,
    'author': "TG",
    'category': 'Productivity',
    'version': '16.0.1.2.0',
    'depends': ['base'],
    'data': [
        'data/openai_model_data.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/openai_model_views.xml'
    ],
    "external_dependencies": {
        "python" : ['matplotlib', 'numpy', 'openai', 'pandas', 'plotly', 'scipy', 'scikit-learn']
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'price': 10000.00,
    'currency': 'EUR',

}
