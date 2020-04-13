# coding: utf-8
import base64
from openerp import http
from openerp.http import request


class StockPickingController(http.Controller):
    @http.route('/csv/download/stock_picking/<string:csv>', auth='user')
    def sale_order_lines_csv_download(self, csv, **kw):
        filename = 'export_postnl.csv'
        csv_output = base64.decodestring(csv)
        return request.make_response(csv_output, [('Content-Type', 'application/octet-stream'),
                                           ('Content-Disposition', 'attachment; filename="%s"' % filename)])
