from odoo import api, fields, models


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
    )
    conversion_rate = fields.Float(
    )
    variable_density = fields.Boolean(
    )
    supplier_cost = fields.Monetary(
        currency_field='currency_id',
    )

    @api.onchange('supplier_cost', 'conversion_rate')
    def _price_from_supplier_cost(self):
        self.price = self.supplier_cost / (self.conversion_rate or 1)
