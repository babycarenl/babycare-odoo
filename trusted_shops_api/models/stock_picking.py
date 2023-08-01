# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    trustedshops_invitation = fields.Boolean(
        default=True,
    )

    def _action_done(self):
        """Trigger eTrusted event (Trusted Shops) on transfer of outgoing
        delivery to automatically send a Trusted Shops invitation to the customer.
        Trigger only applies if the destination usage is a customer, the
        trustedshops_invitation boolean is true and if there are related
        sale orders to the picking."""
        result = super(StockPicking, self)._action_done()
        for picking in self:
            if (
                picking.location_dest_id.usage == "customer"
                and picking.trustedshops_invitation
                and (
                    picking.group_id
                    and self.env["sale.order"].search(
                        [("procurement_group_id", "=", picking.group_id.id)]
                    )
                )
            ):
                self.env["trusted.shops.api"].post_invite(picking)
        return result
