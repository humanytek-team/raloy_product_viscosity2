from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    purchase_uom = fields.Many2one(
        comodel_name="product.uom",
        required=True,
    )
    pack = fields.Integer(
        default=1,
    )
    pack_uom = fields.Char(
        required=True,
    )
    conversion_rate = fields.Float(
        default=1,
        digits=dp.get_precision('Product Price'),
    )
    variable_density = fields.Boolean(
    )
    supplier_cost = fields.Monetary(
        currency_field='currency_id',
        digits=dp.get_precision('Product Price'),
    )
    supplier_min_qty = fields.Float(
        compute="_get_supplier_min_qty",
        inverse="_set_min_qty",
    )

    @api.onchange('min_qty')
    def _get_supplier_min_qty(self):
        self.supplier_min_qty = self.min_qty / (self.conversion_rate or 1)

    @api.onchange('supplier_min_qty', 'conversion_rate')
    def _set_min_qty(self):
        self.min_qty = self.supplier_min_qty * self.conversion_rate

    @api.onchange('price')
    def _supplier_cost_from_price(self):
        self.supplier_cost = self.price * self.conversion_rate

    @api.onchange('supplier_cost', 'conversion_rate')
    def _price_from_supplier_cost(self):
        self.price = self.supplier_cost / (self.conversion_rate or 1)
