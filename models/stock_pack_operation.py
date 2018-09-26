from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp


class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    conversion_rate = fields.Float(
        digits=dp.get_precision('Product Price'),
    )
    variable_density = fields.Boolean(
    )
    supplier_qty = fields.Float(
        digits=dp.get_precision('Product Price'),
    )
    supplier_qty_done = fields.Float(
        digits=dp.get_precision('Product Price'),
    )
    picking_type_code = fields.Selection(
        related='picking_id.picking_type_code',
    )

    @api.onchange('conversion_rate', 'supplier_qty_done')
    def _onchange_conversion_rate(self):
        self.qty_done = self.supplier_qty_done * self.conversion_rate

    @api.onchange('qty_done')
    def _onchange_qty_done(self):
        self.supplier_qty_done = self.qty_done / (self.conversion_rate or 1)

    @api.model
    def create(self, vals):
        vals = vals or {}
        picking = self.env['stock.picking'].browse(vals['picking_id'])
        if picking.picking_type_code == 'incoming':
            picking = self.env['stock.picking'].browse(vals['picking_id'])
            uom = self.env['product.uom'].browse(vals['product_uom_id'])
            product = self.env['product.product'].browse(vals['product_id'])
            seller = product._select_seller(
                partner_id=picking.partner_id,
                quantity=vals['product_qty'],
                date=fields.Date.context_today,
                uom_id=uom)
            vals['conversion_rate'] = seller.conversion_rate
            vals['supplier_qty'] = vals['product_qty'] / (seller.conversion_rate or 1)
            vals['variable_density'] = seller.variable_density
        return super(StockPackOperation, self).create(vals)
