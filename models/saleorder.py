import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def setbackto_saleorder(self):
        param_value = self.env['ir.config_parameter'].sudo().get_param('infs_saleorder_reset_ids')
        
        if not param_value:
            _logger.info("No config parameter 'infs_saleorder_reset_ids' found or it's empty.")
            return

        try:
            ids = [int(x.strip()) for x in param_value.split(',') if x.strip().isdigit()]
        except Exception as e:
            _logger.error(f"Invalid config parameter format: {param_value}. Error: {e}")
            return

        if not ids:
            _logger.info("No valid IDs found in config parameter.")
            return

        orders = self.browse(ids).exists()
        _logger.info(f"Updating {len(orders)} sale orders to 'sale' state. IDs: {ids}")
        orders.write({'state': 'sale'})
