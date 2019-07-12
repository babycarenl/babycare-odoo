# coding: utf-8
import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.multi
    def update_availability(self):
        all_variants = self.env['product.product']
        for bom in self:
            variants = (bom.product_id or
                        bom.product_tmpl_id.product_variant_ids)
            all_variants += variants
            for variant in variants:
                avail = []
                var_eol = []
                for line in bom.bom_line_ids:
                    if (line.attribute_value_ids <=
                            variant.attribute_value_ids):
                        avail.append(
                            int(line.product_id.x_availability /
                                line.product_qty))
                        var_eol.append(
                            line.product_id.variant_eol)
                x_availability = avail and min(avail) or 0
                variant_eol = True if True in var_eol else False
                if variant.x_availability != x_availability:
                    _logger.debug(
                        "Updating availability of composed product %s "
                        "from %s to %s",
                        variant.default_code or variant.name,
                        variant.x_availability, x_availability)
                    variant.write({'x_availability': x_availability})
                if variant.variant_eol != var_eol:
                    variant.write({'variant_eol': variant_eol})
        return all_variants

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        res.update_availability()
        return res

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        self.update_availability()
        return res
