from odoo import models

class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("key") == "web.base.url":
                default_url = self.sudo().get_param("default.web.base.url")
                if default_url:
                    vals["value"] = default_url
        return super().create(vals_list)

    def write(self, vals):
        if self.filtered(lambda rec: rec.key == "web.base.url") and "value" in vals:
            default_url = self.sudo().get_param("default.web.base.url")
            if default_url:
                vals["value"] = default_url
        return super().write(vals)
