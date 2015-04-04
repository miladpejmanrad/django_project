from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from menu.models import Category, MenuItem, Order
from menu.modelforms import OrderForm
from menu import settings

# This returns and sets up the contexts for the main menu.html template
def menu(request):
	categories_list = Category.objects.order_by('name')
	context = {'categories_list': categories_list}
	return render(request, 'menu.html', context)

# This returns and sets up the contexts for the individual categories and their menu items for the menu.html template
def categories(request, category_id):
	# return HttpResponse("You're looking at category %s." % category_id)
	categories_list = Category.objects.order_by('name')
	menuitems_list = MenuItem.objects.filter(category=category_id)
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list
	}
	return render(request, 'menu.html', context)

# This builds the menu item order form and returns the information for an individual menu item using the menu-item.html template
def menu_items(request, menu_item_id):
	
	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	menu_item = MenuItem.objects.get(id=menu_item_id)
	
	# This generates the form that appears on an individual menu item page.
	if existing_order.exists():
		order_form = OrderForm(instance=existing_order.get())
	
	else:
		order_form = OrderForm(
			initial={
				'menu_items': [menu_item_id],
				'table_number': settings.TABLE_NUMBER, # This is a dummy value that needs to be replaced.
				'total_price': menu_item.price
			}
		)
	
	# This sets up the contexts to use in the menu-item.html template.
	context = {
		'menu_item': menu_item,
		'form': order_form
	}
			
	return render(request, 'menu-item.html', context)

# This view processes the form sent by the menu-item.html template
def add_to_order(request, menu_item_id):

	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	menu_item = MenuItem.objects.get(id=menu_item_id)

	if request.method == "POST":
		if existing_order.exists():
			order_form = OrderForm(request.POST, instance=existing_order.get())
		else:
			order_form = OrderForm(request.POST)
		if order_form.is_valid():
			order_form.save()
			return HttpResponseRedirect("/menu/")
			
	return HttpResponse("You're trying to order %s, but it didn't go through." % menu_item)
    