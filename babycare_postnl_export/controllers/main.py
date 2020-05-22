# coding: utf-8
from openerp import http
from openerp.http import request

from datetime import datetime
from pytz import timezone

import base64


class StockPickingController(http.Controller):
    @http.route('/csv/download/stock_picking/<string:csv>', auth='user')
    def sale_order_lines_csv_download(self, csv, **kw):
        amsterdam_timezone = timezone('Europe/Amsterdam')
        time_now = datetime.now(amsterdam_timezone)
        filename = 'export_postnl_%s.csv' % time_now.strftime(
            '%d_%m_%Y_%H_%M_%S')
        csv_output = base64.decodestring(csv)
        return request.make_response(csv_output, [('Content-Type', 'application/octet-stream'),
                                                  ('Content-Disposition', 'attachment; filename="%s"' % filename)])
