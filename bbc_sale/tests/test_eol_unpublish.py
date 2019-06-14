# coding: utf-8
from openerp.tests.common import TransactionCase


class TestUnpublishEOL(TransactionCase):
    def setUp(self):
        super(TestUnpublishEOL, self).setUp()

        self.ModelDataObj = self.env['ir.model.data']
        self.stock_location = self.ModelDataObj.xmlid_to_res_id('stock.stock_location_stock')
        self.Wiz = self.env['stock.change.product.qty']

        # create EOL product
        self.template = self.env['product.template'].create({
            'name': 'bbc_sale_test',
            'type': 'product',
            'state': 'end'
        })

    def test_01_unpublish_eol_product_once_out_of_stock(self):
        """ Unpublish simple EOL product once stock is zero """

        # assert template and variant are EOL
        variants = self.template.product_variant_ids
        self.assertEqual(len(variants), 1)
        self.assertEqual(self.template.state, 'end')
        self.assertTrue(variants[0].variant_eol)
        self.assertEqual(variants[0].state, 'end')

        # create stock (qty=1) for variant of EOL product
        self.env['stock.quant'].create({
            'product_id': self.template.product_variant_ids[0].id,
            'location_id': self.stock_location,
            'qty': 1.0,
        })

        # assert stock level is 1.0
        self.assertEqual(variants[0].qty_available, 1.0)

        # set website_published to true and assert template and variant are published
        self.template.write({
            'website_published': True
        })
        self.assertTrue(self.template.website_published)
        self.assertTrue(variants[0].variant_published)
        self.assertTrue(variants[0].website_published)

        # write zero stock on product variant and assert stock level of 0
        wiz = self.Wiz.create({'product_id': variants[0].id,
                               'new_quantity': 0,
                               'location_id': self.stock_location,
                               })
        wiz.change_product_qty()
        self.assertEqual(variants[0].qty_available, 0.0)

        # assert template and variant are not published anymore
        self.assertFalse(self.template.website_published)
        self.assertFalse(variants[0].variant_published)
        self.assertFalse(variants[0].website_published)

    def test_02_unpublish_eol_product_variant_once_out_of_stock(self):
        """ Unpublish EOL product variant of config product once stock is zero. If all
        product variants are unpublished, check that template is unpublished as well."""

        # create extra product variant for template
        self.env['product.product'].create({
            'product_tmpl_id': self.template.id})

        # create stock (qty=1) for variant 1 of EOL product
        self.env['stock.quant'].create({
            'product_id': self.template.product_variant_ids[0].id,
            'location_id': self.stock_location,
            'qty': 1.0,
        })

        # create stock (qty=2) for variant 2 of EOL product
        self.env['stock.quant'].create({
            'product_id': self.template.product_variant_ids[1].id,
            'location_id': self.stock_location,
            'qty': 2.0,
        })

        # assert template and all variants are EOL
        variants = self.template.product_variant_ids
        self.assertEqual(len(variants), 2)
        self.assertEqual(self.template.state, 'end')
        self.assertTrue(variants[0].variant_eol)
        self.assertTrue(variants[1].variant_eol)

        # assert stock levels for both variants
        self.assertEqual(variants[1].qty_available, 2.0)
        self.assertEqual(variants[0].qty_available, 1.0)

        # set website_published to true and assert template and both variants are published
        self.template.write({
            'website_published': True
        })
        self.assertTrue(self.template.website_published)
        self.assertTrue(variants[0].variant_published)
        self.assertTrue(variants[1].variant_published)

        # write zero stock on product variant 1 and assert stock level of 0 for variant 1
        wiz = self.Wiz.create({'product_id': variants[0].id,
                               'new_quantity': 0,
                               'location_id': self.stock_location,
                               })
        wiz.change_product_qty()
        self.assertEqual(variants[0].qty_available, 0.0)

        # assert variant 1 is not published and assert template and variant 2 are still published
        self.assertFalse(variants[0].variant_published)
        self.assertTrue(self.template.website_published)
        self.assertTrue(variants[1].variant_published)

        # write zero stock on product variant 2 and assert stock level of 0 for variant 2
        wiz = self.Wiz.create({'product_id': variants[1].id,
                               'new_quantity': 0,
                               'location_id': self.stock_location,
                               })
        wiz.change_product_qty()
        self.assertEqual(variants[1].qty_available, 0.0)

        # assert variant 1 is not published and assert that template is also unpublished
        self.assertFalse(variants[1].variant_published)
        self.assertFalse(self.template.website_published)
