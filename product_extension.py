from odoo import models, fields, api

class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    # Existing Threshold
    low_stock_threshold = fields.Float(string="Low Stock Threshold", default=10.0)
    
    # Existing Boolean
    is_low_stock = fields.Boolean(
        string="Is Low Stock",
        compute="_compute_inventory_status",
        store=True
    )

    # NEW: Categorical Status for UI badges
    inventory_status = fields.Selection([
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock')
    ], string="Health Status", compute="_compute_inventory_status", store=True)

    # NEW: Financial Valuation
    total_stock_value = fields.Float(
        string="Total Stock Value",
        compute="_compute_stock_value",
        store=True
    )

    @api.depends('qty_available', 'standard_price')
    def _compute_stock_value(self):
        """Calculates the financial value of the current inventory."""
        for record in self:
            record.total_stock_value = record.qty_available * record.standard_price

    @api.depends('qty_available', 'low_stock_threshold')
    def _compute_inventory_status(self):
        """Determines both the boolean flag and the categorical health status."""
        for record in self:
            if record.type == 'product': 
                # Set boolean
                record.is_low_stock = record.qty_available <= record.low_stock_threshold
                
                # Set categorical status
                if record.qty_available <= 0:
                    record.inventory_status = 'out_of_stock'
                elif record.qty_available <= record.low_stock_threshold:
                    record.inventory_status = 'low_stock'
                else:
                    record.inventory_status = 'in_stock'
            else:
                record.is_low_stock = False
                record.inventory_status = 'in_stock'