from menu.models import Category, MenuItem, Order
from django.forms import ModelForm
from django import forms

# This constructs a form that we can use for adding items to an order.
# Hides most fields.
class AddItemToOrderForm(ModelForm):
	class Meta:
		model = Order
		widgets = {
			'total_price': forms.HiddenInput(),
			'menu_items': forms.MultipleHiddenInput(),
			'status': forms.HiddenInput(),
			'table_number': forms.HiddenInput(),
			'tip': forms.HiddenInput(),
			'modifications': forms.HiddenInput(),
			'drinks': forms.MultipleHiddenInput(),
			'tikchen': forms.HiddenInput()
		}

# This constructs a form for placing an order.
# Shows the Modifications field.
class PlaceOrderForm(ModelForm):
	class Meta:
		model = Order
		widgets = {
			'total_price': forms.HiddenInput(),
			'menu_items': forms.MultipleHiddenInput(),
			'status': forms.HiddenInput(),
			'table_number': forms.HiddenInput(),
			'tip': forms.HiddenInput(),
			'drinks': forms.MultipleHiddenInput(),
			'tikchen': forms.HiddenInput()
		}

# This constructs a form for adding a tip.
# Shows the Tip field.
class TipOrderForm(ModelForm):
	class Meta:
		model = Order
		widgets = {
			'total_price': forms.HiddenInput(),
			'menu_items': forms.MultipleHiddenInput(),
			'status': forms.HiddenInput(),
			'table_number': forms.HiddenInput(),
			'modifications': forms.HiddenInput(),
			'drinks': forms.MultipleHiddenInput(),
			'tikchen': forms.HiddenInput()
		}