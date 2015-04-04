from menu.models import Category, MenuItem, Order
from django.forms import ModelForm

# This constructs a form that we can use for creating an order.
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ['modifications']