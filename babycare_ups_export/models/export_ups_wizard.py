# coding: utf-8
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError

import base64
import logging

_logger = logging.getLogger(__name__)


class ExportUPSWizard(models.TransientModel):
    _name = 'export.ups.wizard'
    csv_data = fields.Binary()

    @api.multi
    def create_ups_export(self):
        """
        Method is triggered from create button on wizard.
        It retrieves active_ids from context and creates a csv formatted string.
        Base64 encoded string is passed a parameter to sftp_export.
        """

        data = self._create_csv_data(
            {'picking_ids': self.env.context['active_ids']})
        data = data.encode("utf-8")
        try:
            self.csv_data = base64.encodestring(data)
        except UnicodeEncodeError:
            raise UserError(
                _(
                    'A UnicodeEncodeError occured.\n'
                    'Most likely, there is a record with non UTF-8 characters.'
                )
            )

        sftp_model = self.env['sftp.export']
        ups_connection = sftp_model.search([('export_type', '=', 'ups')])
        if ups_connection:
            sftp_model.search([]).sftp_export(self.csv_data, 'ups')
        else:
            raise UserError(
                _("UPS connection does not exist in the SFTP configuration.\n \
                Please create a configuration in Settings > Technical > SFTP > Configure SFTP"))

    @api.model
    def _create_csv_data(self, vals):
        """
        Creates csv string based on given picking_ids.
        :param vals: picking_ids obtained via selected ids on stock.picking.
        :return: csv data as string formatted in UPS format.
        """

        picking_ids = vals.get('picking_ids')

        columns = [
            u'CompanyOrName',
            u'Attention',
            u'Street1',
            u'Street2',
            u'Street3',
            u'PostalCode',
            u'City',
            u'State',
            u'Country',
            u'Tel',
            u'DescriptionOfGoods',
            u'Reference1',
            u'Reference2',
            u'BillingOption',
            u'UPSservice',
            u'TypeVerpakking',
            u'Totaalgewicht',
            u'AantalPakketten',
            u'BillTransportation',
            u'BillDuties'
        ]

        csv_columns = u'","'.join(columns)
        csv = u"\"{}\"\n".format(csv_columns)

        for p in picking_ids:
            delivery = self.env['stock.picking'].browse(p)

            for d in delivery:
                data = []

                # CompanyOrName
                """ check if delivery has company in shipping address,
                if so: append company to surname, else: surname
                # if d.sale_id.partner_shipping_id.parent_id:
                """
                data.append(
                    d.sale_id.partner_shipping_id.name if d.sale_id.partner_shipping_id.name else '')

                # Attention (-) (alleen verplicht bij non-domestic zendingen)
                data.append('')

                # Street1
                street_name = (d.sale_id.partner_shipping_id.street_name if
                               d.sale_id.partner_shipping_id.street_name else '')
                street_number = (d.sale_id.partner_shipping_id.street_number if
                                 d.sale_id.partner_shipping_id.street_number else '')
                street_number_addition = (d.sale_id.partner_shipping_id.street_number_addition if
                                          d.sale_id.partner_shipping_id.street_number_addition else '')
                data.append(street_name + street_number +
                            street_number_addition)

                # Street2 (optioneel)
                data.append('')

                # Street3 (optioneel)
                data.append('')

                # PostalCode
                data.append(
                    d.sale_id.partner_shipping_id.zip if d.sale_id.partner_shipping_id.zip else '')

                # City
                data.append(
                    d.sale_id.partner_shipping_id.city if d.sale_id.partner_shipping_id.city else '')

                # State (verplicht bij zendingen naar US)
                data.append('')

                # Country
                data.append(
                    d.partner_id.country_id.code if d.partner_id.country_id.code else '')

                # Tel (alleen verplicht bij non-domestic zendingen)
                data.append(
                    d.sale_id.partner_shipping_id.phone if d.sale_id.partner_shipping_id.phone else '')

                # DescriptionOfGoods (alleen verplicht bij non-domestic zendingen)
                data.append('')

                # Reference1 (optioneel)
                data.append(d.origin if d.origin else '')

                # Reference2 (optioneel)
                data.append('')

                # BillingOption (altijd PP)
                data.append('PP')

                # UPSservice
                """
                Service Code (UPS Service Type)
                EP  Express Plus 
                ES  Express 
                SV  Express Saver 
                EX  Expedited 
                ST  Standard 
                ND  Express (NA1)
                
                All EU(+NL) shipments is Standard.
                Non-EU shipments is Express Saver.
                """
                europe = self.env.ref('base.europe').country_ids
                if d.sale_id.partner_shipping_id.country_id in europe:
                    data.append('ST')
                else:
                    data.append('SV')

                # TypeVerpakking (zie bijlage Codes import-export)
                """
                Code (Soort verpakking)
                CP Custom Package (eigen verpakking/doos)
                EE UPS Express Enveloppe
                PK UPS Express PAK
                TB UPS Express Tube
                """
                data.append('CP')

                # Totaalgewicht
                weight = d.weight if d.weight else 0.5
                data.append(str(weight))

                # AantalPakketten
                number_of_packages = d.number_of_packages if d.number_of_packages > 1 else 1
                data.append(str(number_of_packages))

                # BillTransportation (alleen non-EU)
                data.append('')

                _logger.debug(data)

                csv_row = u'","'.join(data)
                csv += u"\"{}\"\n".format(csv_row)
        return csv
