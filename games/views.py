from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from menu.models import Category, MenuItem, Order
from menu.modelforms import OrderForm
from menu import settings

# This returns and sets up the contexts for the main menu.html template
def games(request):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	context = {
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
	}
	return render(request, 'games.html', context)

# This returns and sets up the contexts for the individual categories and their menu items for the menu.html template
def flappybird(request):

	return render(request, 'flappybird.html')
