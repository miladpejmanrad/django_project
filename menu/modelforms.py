from menu.models import Category, MenuItem, Order
from django.forms import ModelForm
from django import forms

# This constructs a form that we can use for creating an order.
class OrderForm(ModelForm):
	class Meta:
		model = Order
		widgets = {
			'total_price': forms.HiddenInput(),
			'menu_items': forms.MultipleHiddenInput(),
			'status': forms.HiddenInput(),
			'table_number': forms.HiddenInput()
		}