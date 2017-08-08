# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_color_id = fields.Many2one(
        'product.color',
        string='Color',
        help='Select a color for this product',
        related='product_variant_ids.product_color_id',
        readonly=True
    )
    product_options_ids = fields.Many2many(
        'product.options',
        string='Options',
        help='Select options for this product',
        ondelete='restrict'
    )
    product_buggies_agecategory_id = fields.Many2one(
        'product.buggies.agecategory',
        string="Age Category",
        ondelete='restrict'
    )
    product_buggies_maxcarryweight_id = fields.Many2one(
        'product.buggies.maxcarryweight',
        string="Maximum Carry Weight",
        ondelete='restrict'
    )
    product_buggies_numberofwheels_id = fields.Many2one(
        'product.buggies.numberofwheels',
        string="Number of Wheels",
        ondelete='restrict'
    )
    product_carriers_directionofuse_id = fields.Many2one(
        'product.carriers.directionofuse',
        string="Direction of Use",
        ondelete='restrict'
    )
    product_carriers_maxcarryweight_id = fields.Many2one(
        'product.carriers.maxcarryweight',
        string="Maximum Carry Weight",
        ondelete='restrict'
    )
    product_carriers_type_id = fields.Many2one(
        'product.carriers.type',
        string="Type",
        ondelete='restrict'
    )
    product_carseats_agecategory_id = fields.Many2one(
        'product.carseats.agecategory',
        string="Age Category",
        ondelete='restrict'
    )
    product_carseats_childlength_id = fields.Many2one(
        'product.carseats.childlength',
        string="Child Length",
        ondelete='restrict'
    )
    product_carseats_childweight_id = fields.Many2one(
        'product.carseats.childweight',
        string="Child Weight",
        ondelete='restrict'
    )
    product_carseats_directionofuse_id = fields.Many2one(
        'product.carseats.directionofuse',
        string="Direction of Use",
        ondelete='restrict'
    )
    product_carseats_installmethod_id = fields.Many2one(
        'product.carseats.installmethod',
        string="Install Method",
        ondelete='restrict'
    )
    product_clothes_season_id = fields.Many2one(
        'product.clothes.season',
        string="Season",
        ondelete='restrict'
    )
    product_clothes_size_id = fields.Many2one(
        'product.clothes.size',
        string="Size",
        ondelete='restrict'
    )
    product_highchairs_agecategory_id = fields.Many2one(
        'product.highchairs.agecategory',
        string="Age Category",
        ondelete='restrict'
    )
    product_highchairs_material_id = fields.Many2one(
        'product.highchairs.material',
        string="Material",
        ondelete='restrict'
    )
    product_monitors_maxrange_id = fields.Many2one(
        'product.monitors.maxrange',
        string="Maximum Range",
        ondelete='restrict'
    )
    product_rockers_maxcarryweight_id = fields.Many2one(
        'product.rockers.maxcarryweight',
        string="Maximum Carry Weight",
        ondelete='restrict'
    )
    product_strollers_numberofwheels_id = fields.Many2one(
        'product.strollers.numberofwheels',
        string="Number of Wheels",
        ondelete='restrict'
    )
    product_textiles_size_id = fields.Many2one(
        'product.textiles.size',
        string="Size",
        ondelete='restrict'
    )
    product_toys_agecategory_id = fields.Many2one(
        'product.toys.agecategory',
        string="Age Category",
        ondelete='restrict'
    )
    product_toys_type_id = fields.Many2one(
        'product.toys.type',
        string="Type",
        ondelete='restrict'
    )
    product_buggies_adjustablebackrest = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Adjustable Backrest?"
    )
    product_clothes_gender = fields.Selection(
        [('boy', 'Boy'), ('girl', 'Girl'), ('unisex', 'Unisex')],
        string="Gender"
    )
    product_highchairs_includingdinnertray = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Dinner Tray"
    )
    product_highchairs_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible"
    )
    product_monitors_includingcamera = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Camera"
    )
    product_monitors_includingrecallfunction = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="2-way voice operation"
    )
    product_rockers_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible"
    )
    product_travelcots_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible"
    )
    product_travelcots_includingwheels = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Wheels"
    )
    product_travelcots_includingcreephatch = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Creep Hatch"
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_color_id = fields.Many2one(
        'product.color',
        string='Color',
        help='Select a color for this product'
    )

    @api.multi
    def open_attribute_manager(self):
        res = {
            'type': 'ir.actions.act_window',
            'name': 'Attribute Manager',
            'res_model': 'product.attributemanager',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'self',
            'flags': {'action_buttons': False},
        }
        return res
