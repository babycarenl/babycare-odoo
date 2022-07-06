# coding: utf-8
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError

import base64


class ExportPostNLWizard(models.TransientModel):
    _name = 'export.postnl.wizard'
    csv_data = fields.Binary()
    filename = fields.Char()

    @api.multi
    def create_postnl_export(self):
        """
        Method is triggered from create button on wizard.
        It retrieves active_ids from context and creates a csv formatted string.
        Base64 encoded string is passed a parameter to return act_url
        :return: act_url to /csv/download/stock_picking/%s with csv data in base64.
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

        return {
            'type': 'ir.actions.act_url',
            'url': '/csv/download/stock_picking/%s' % self.csv_data,
            'target': 'self'
        }

    @api.model
    def _create_csv_data(self, vals):
        """
        Creates csv string based on given picking_ids.
        :param vals: picking_ids obtained via selected ids on stock.picking.
        :return: csv data as string formatted in PostNL format.
        """

        picking_ids = vals.get('picking_ids')

        columns = [
            u'YourReference',
            u'CompanyName',
            u'Surname',
            u'FirstName',
            u'CountryCode',
            u'Street',
            u'HouseNo',
            u'HouseNoSuffix',
            u'Postcode',
            u'City',
            u'Email',
            u'MobileNumber',
            u'ProductCode',
            u'DeliveryToPostnl',
            u'Barcode',
            u'CODAmount',
            u'CODReference',
            u'InsuredValue'
        ]

        csv_columns = u'","'.join(columns)
        csv = u"\"{}\"\n".format(csv_columns)

        for p in picking_ids:
            delivery = self.env['stock.picking'].browse(p)

            for d in delivery:
                number_of_packages = d.number_of_packages if d.number_of_packages > 1 else 1
                for _ in range(number_of_packages):
                    data = []

                    # YourReference
                    data.append(d.origin if d.origin else '')
                    # CompanyName
                    data.append('')
                    # Surname
                    data.append(
                        d.sale_id.partner_shipping_id.name if d.sale_id.partner_shipping_id.name else '')
                    # FirstName
                    data.append('')
                    # CountryCode
                    data.append(
                        d.partner_id.country_id.code if d.partner_id.country_id.code else '')
                    # Street
                    data.append(d.sale_id.partner_shipping_id.street_name if
                                d.sale_id.partner_shipping_id.street_name else '')
                    # HouseNo
                    data.append(d.sale_id.partner_shipping_id.street_number if
                                d.sale_id.partner_shipping_id.street_number else '')
                    # HouseNoSuffix
                    data.append(d.sale_id.partner_shipping_id.street_number_addition if
                                d.sale_id.partner_shipping_id.street_number_addition else '')
                    # Postcode
                    data.append(
                        d.sale_id.partner_shipping_id.zip if d.sale_id.partner_shipping_id.zip else '')
                    # City
                    data.append(
                        d.sale_id.partner_shipping_id.city if d.sale_id.partner_shipping_id.city else '')
                    # Email
                    data.append(
                        d.sale_id.partner_shipping_id.email if d.sale_id.partner_shipping_id.email else '')
                    # MobileNumber
                    data.append(
                        d.sale_id.partner_shipping_id.phone if d.sale_id.partner_shipping_id.phone else '')

                    # ProductCode
                    nl = self.env.ref('base.nl')
                    be = self.env.ref('base.be')
                    europe = self.env.ref('base.europe').country_ids
                    if d.sale_id.partner_shipping_id.country_id == nl:
                        # shipping address in within the Netherlands. ProductCode is NL:
                        # NL > 3085 (zending NL zonder bezorgopties)
                        data.append('3085')
                    elif d.sale_id.partner_shipping_id.country_id == be:
                        # shipping address in Belgium. ProductCode is BE: 4946.
                        data.append('4946')
                    elif d.sale_id.partner_shipping_id.country_id in europe:
                        # shipping address in europe. ProductCode is EU:
                        # 4940 EU to business – single label
                        # 4944 EU to consumer – single label
                        data.append('4944')

                    # DeliveryToPostnl (empty value)
                    data.append('')
                    # Barcode (empty value because generated by PostNL)
                    data.append('')
                    # CODAmount (empty value)
                    data.append('')
                    # CODReference (empty value)
                    data.append('')
                    # InsuredValue (empty value)
                    data.append('')

                    csv_row = u'","'.join(data)
                    csv += u"\"{}\"\n".format(csv_row)
        return csv
