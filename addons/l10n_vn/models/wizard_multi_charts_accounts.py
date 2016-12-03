# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models

class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.multi
    def _create_bank_journals_from_o2m(self, company, acc_template_ref):
        '''
        This function creates bank journals and its accounts for each line encoded in the field bank_account_ids of the
        wizard (which is currently only used to create a default bank and cash journal when the CoA is installed).

        For l10n_vn, we will use:
            - account 1111 as default credit/debit for Cash journal
            - account 1121 as default credit/debit for Bank journal

        For other l10n_xx, use normal native behavior of Odoo

        :param company: the company for which the wizard is running.
        :param acc_template_ref: the dictionary containing the mapping between the ids of account templates and the ids
            of the accounts that have been generated from them.
        '''
        self.ensure_one()
        # Create the journals that will trigger the account.account creation
        vn_chart = self.env.ref('l10n_vn.vn_template')
        company = self.company_id

        # if current chart is vn_template, use 1111 and 1121 as default account
        # for Cash or Bank
        if vn_chart and vn_chart.id == self.chart_template_id.id:
            for acc in self.bank_account_ids:
                vals = {
                    'name': acc.acc_name,
                    'type': acc.account_type,
                    'company_id': company.id,
                    'currency_id': acc.currency_id.id,
                    'sequence': 10
                }

                # if account type is bank, use prefix of bank_account_code
                if acc.account_type == 'bank':
                    account_code_prefix = company.bank_account_code_prefix or ''
                else:
                    # if account type is cash, use prefix of cash_account_code
                    account_code_prefix = company.cash_account_code_prefix or company.bank_account_code_prefix or ''

                default_account = False

                # Get the first one of account as default
                # account for Bank or Cash Journal
                for num in xrange(1, 100):
                    code_prefix = str(account_code_prefix.ljust(self.code_digits - 1, '0'))
                    new_code = code_prefix + str(num)
                    domain = [('code', '=', new_code), ('company_id', '=', company.id)]
                    default_account = self.env['account.account'].search(domain, limit=1)

                    # Get the first one matched, normally, it should be first
                    # account of Cash prefix 111 (aka account 1111)
                    # or Bank prefix 112 (aka account 1121)
                    if default_account:
                        break

                # add default debit/create account for journal
                vals['default_debit_account_id'] = default_account and default_account.id
                vals['default_credit_account_id'] = default_account and default_account.id

                # create default journal for Cash/Bank
                self.env['account.journal'].create(vals)
        else:
            # for not l10n_vn, used the native Odoo function
            return super(WizardMultiChartsAccounts, self)._create_bank_journals_from_o2m(company, acc_template_ref)
