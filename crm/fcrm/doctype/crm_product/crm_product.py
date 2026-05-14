# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class CRMProduct(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.TextEditor | None
		disabled: DF.Check
		image: DF.AttachImage | None
		naming_series: DF.Literal["CRM-PROD-.YYYY.-"]
		product_code: DF.Data
		product_name: DF.Data | None
		standard_rate: DF.Currency
	# end: auto-generated types

	def validate(self):
		self.set_product_name()

	def set_product_name(self):
		if not self.product_name:
			self.product_name = self.product_code
		else:
			self.product_name = self.product_name.strip()

	@staticmethod
	def default_list_data():
		columns = [
			{"label": "Product Code", "type": "Data", "key": "product_code", "width": "14rem"},
			{"label": "Product Name", "type": "Data", "key": "product_name", "width": "14rem"},
			{"label": "Standard Rate", "type": "Currency", "key": "standard_rate", "width": "10rem"},
			{"label": "Disabled", "type": "Check", "key": "disabled", "width": "8rem"},
			{"label": "Modified", "type": "Datetime", "key": "modified", "width": "10rem"},
		]
		rows = ["name", "product_code", "product_name", "standard_rate", "disabled", "modified"]
		return {"columns": columns, "rows": rows}
