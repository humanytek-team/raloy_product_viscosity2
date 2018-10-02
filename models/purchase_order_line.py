from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_uom = fields.Many2one(
        comodel_name="product.uom",
        compute='_compute_viscosity_vals',
        store=True,
    )
    pack = fields.Integer(
        compute='_compute_viscosity_vals',
        store=True,
    )
    pack_uom = fields.Char(
        compute='_compute_viscosity_vals',
        store=True,
    )
    conversion_rate = fields.Float(
        digits=dp.get_precision('Product Price'),
    )
    variable_density = fields.Boolean(
        compute='_compute_viscosity_vals',
        store=True,
    )
    supplier_cost = fields.Monetary(
        digits=dp.get_precision('Product Price'),
    )
    supplier_qty = fields.Float(
        digits=dp.get_precision('Product Price'),
    )

    @api.onchange('price_unit')
    def _supplier_cost_from_price_unit(self):
        self.supplier_cost = self.price_unit * self.conversion_rate

    @api.onchange('supplier_cost', 'conversion_rate')
    def _price_unit_from_supplier_cost(self):
        self.price_unit = self.supplier_cost / (self.conversion_rate or 1)

    @api.onchange('supplier_qty')
    def _onchange_supplier_qty(self):
        self.product_qty = self.supplier_qty * self.conversion_rate

    @api.onchange('product_qty', 'product_uom')
    def _onchange_product_id_viscosity(self):
        if not self.product_id:
            return
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)
        self.conversion_rate = (seller and seller.conversion_rate) or 1
        self.supplier_cost = (seller and seller.supplier_cost) or self.price_unit
        self.supplier_qty = self.product_qty / (self.conversion_rate or 1)

    @api.depends('product_qty')
    @api.one
    def _compute_viscosity_vals(self):
        if not self.product_id:
            return
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)
        self.update({
            'purchase_uom': (seller and seller.purchase_uom.id) or self.product_uom,
            'pack': (seller and seller.pack) or 1,
            'pack_uom': (seller and seller.pack_uom) or self.product_uom.name,
            'variable_density': (seller and seller.variable_density) or False,
        })

    @api.one
    @api.constrains('pack', 'supplier_qty')
    def _check_pack_supplier_qty_relation(self):
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom)
        if seller and self.supplier_qty % self.pack != 0:
            raise ValidationError(_('The Supplier Qty of {} must be pack multiple.'.format(self.product_id.name)))
