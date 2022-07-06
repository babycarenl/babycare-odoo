from openerp import api
from openerp.osv import osv, fields


#This has to be done on sale.order instead of stock.picking or stock.move
#This is because each move is checked individually during confirmation for a picking
#If you change state to assigned, it will disregard the picking and create another
#IMO this is not the best implementation by Odoo for the problem caused here
#And because it does a sql search for a picking after each move. If you have 100
#moves, it will search database 100 times for a picking.

#Also its standard functionality in ERP system to check and assign stock. In many
#other software there is no concept of having to run a scheduler to assign stock
#Odoo should stop and take a look and not design a manufacturing software called ERP

class SaleOrder(osv.osv):
    _inherit = 'sale.order'


    def action_ship_create(self, cr, uid, ids, context=None):
	picking_obj = self.pool.get('stock.picking')
        res = super(SaleOrder, self).action_ship_create(cr, uid, ids, context=context)
	for order in self.browse(cr, uid, ids):
	    for picking in order.picking_ids:
		if picking.state == 'confirmed':
		    picking_obj.action_assign(cr, uid, picking.id)

	return res
