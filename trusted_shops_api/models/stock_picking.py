# coding: utf-8
from openerp import api, fields, models

class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking']

    trustedshops_invitation = fields.Boolean(
        default=True,
    )

    @api.multi    
    def do_transfer(self):
        """ Trigger eTrusted event (Trusted Shops) on transfer of outgoing
        delivery to automatically send a Trusted Shops invitation to the customer.
        Trigger only applies if the destination usage is a customer, the
        trustedshops_invitation boolean is true and if there are related
        sale orders to the picking. """
        res = super(Picking, self).do_transfer()
        for picking in self:
            if (picking.location_dest_id.usage == 'customer' and
                    picking.trustedshops_invitation and
                    (picking.group_id and self.env['sale.order'].search([
                        ('procurement_group_id', '=', picking.group_id.id)]))):
                self.env['trusted.shops.api'].post_invite(picking)
        return res
