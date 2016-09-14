# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name": "Vietnam - Accounting",
    "version": "1.0",
    "author": "General Solutions",
    'website': 'http://gscom.vn',
    'category': 'Localization',
    "description": """
This is the module to manage the accounting chart for Vietnam in OpenERP.
=========================================================================

This module applies to companies based in Vietnamese Accounting Standard (VAS)
with Chart of account under Circular No. 200/2014/TT-BTC

**Credits:**
    - General Solutions.
    - Trobz
""",
    "depends": [
        "account",
        "base_vat",
        "base_iban"
    ],
    "data": [
        "account_chart.xml",
        "account_tax.xml",
        "account_chart_template.yml"
    ],
    "demo": [],
    "installable": True,
}
