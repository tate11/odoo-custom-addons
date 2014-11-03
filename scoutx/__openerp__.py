{
    'name': 'ScoutX Management',
    'version': '1.0',
    'category': 'Purchase Management',
    'sequence': 19,
    'summary': 'Base module to manage Scout Group',
    'description': """
ScoutX : Base Module
==================================================

* Customize partner to create a correct listing of different type of people in the Group
* Insert the concept of Staff, kids, parents, ...
* History of the staff composition
* ...

    """,
    'author': 'jejemaes',
    'website': 'http://www.jejemaes.net/scoutx',
    'depends': ['base'],
    'data': [
        'wizard/wizard_make_subscription.xml',
        'views/res_partner_view.xml',
        'views/scoutx_view.xml',
        'data/scoutx_data.xml',
    ],
    'demo': [
        'data/scoutx_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

