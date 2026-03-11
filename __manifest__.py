# -*- coding: utf-8 -*-
{
    'name': "INFS_Config",
    'version': '1.0.0',
    'category': 'infs',
    'author': "INFS",
    'summary': 'INFS Module for Configuration',
    'description': """
        INFS module for Configuration.
    """,
    'depends': ['sale', 'purchase', 'base', 'web', 'portal', 'mail','mass_mailing','crm','sale_margin','sale_management','account','website', 'website_sale', 'l10n_th', 'l10n_th_reports', 'hr_timesheet', 'project_todo','infs_crm', 'timer'],
    'data': [
        'security/group.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        'data/saleorder.xml',
        # 'data/cron.xml',
        'views/menu.xml',
        'views/res_users_views.xml',
    ],
    'assets': {
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
    'sequence': -100,
}
