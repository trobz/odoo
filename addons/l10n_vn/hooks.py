# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    def clean_unused_accounts():
        '''
        clean up some unused accounts that were created auto by account modules
        like:
            the current year earning account (outside of the CoA) - code 999999
        '''

        vn_chart = env.ref('l10n_vn.vn_template')
        domain = [['chart_template_id', '=', vn_chart.id]]
        company = env['res.company'].search(domain, limit=1)
        # we remove redundant account with code "999999" that created by Account module
        # This account is not need in Vietnamese Accounting System.
        # Only remove account of company which installed "l10n_vn" module
        if company:
            domain = [['code', '=', '999999'], ['company_id', '=', company.id]]
            accounts = env['account.account'].search(domain)
            # unlink() can handle if "accounts" is null objects.
            accounts.unlink()

    #===  Main hook function ===#
    env = api.Environment(cr, SUPERUSER_ID, {})

    # start hook
    clean_unused_accounts()


