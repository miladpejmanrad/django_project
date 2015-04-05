from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from menu.models import Category, MenuItem, Order, Allergen
from menu.modelforms import OrderForm
from menu import settings

# This returns and sets up the contexts for the main menu.html template
def menu(request):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	context = {
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
	}
	return render(request, 'menu/menu.html', context)

# This returns and sets up the contexts for the individual categories and their menu items for the menu.html template
def categories(request, category_id):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	menuitems_list = MenuItem.objects.filter(category=category_id, visible=True)
	allergies_list = Allergen.objects.all()
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
		'allergies_list': allergies_list,
		'current_category': category_id
	}
	return render(request, 'menu/menu.html', context)

# This returns and sets up the contexts for allergy filtered menu items within a category
def filtered_categories(request, category_id, allergy_id):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	allergies_list = Allergen.objects.all()
	menuitems_list = MenuItem.objects.filter(category=category_id, visible=True).exclude(allergens=allergy_id)
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
		'allergies_list': allergies_list,
		'current_category': category_id,
		'current_allergen': Allergen.objects.get(id=allergy_id)
	}
	return render(request, 'menu/menu.html', context)	
	
# This returns and sets up the contexts for vegetarian filtered menu items within a category
def vegetarian(request, category_id):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	allergies_list = Allergen.objects.all()
	menuitems_list = MenuItem.objects.filter(category=category_id, visible=True).exclude(vegetarian=False) # Exclude items that aren't vegetarian
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
		'allergies_list': allergies_list,
		'current_category': category_id,
		'vegetarian': True
	}
	return render(request, 'menu/menu.html', context)	

# This builds the menu item order form and returns the information for an individual menu item using the menu-item.html template
def menu_items(request, menu_item_id):
	
	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	menu_item = MenuItem.objects.get(id=menu_item_id)
	
	# This generates the form that appears on an individual menu item page.
	if existing_order.exists():
		order_form = OrderForm(instance=existing_order.get()) # Grab the form data first so we can modify it
		ordered_items = list(existing_order.get().menu_items.all()) # Get the menu items already on the order
		if not menu_item in ordered_items:
			ordered_items.append(menu_item) # Add the new menu item if it's not already there
		
		# Calculate the new total price
		total_price = 0
		for item in ordered_items:
			item_price = MenuItem.objects.get(id=item.id)
			total_price = total_price + item_price.price
		
		# Set the form to use the new data
		order_form = OrderForm(
			initial={
				'menu_items': ordered_items,
				'total_price': total_price
			},
			instance=existing_order.get()
		)
	
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
		'form': order_form,
		'order_exists': existing_order.exists()
	}
			
	return render(request, 'menu/menu-item.html', context)

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
	
# This view shows the user their order BEFORE sending it to the kitchen and lets them submit to the kitchen.
# Submitting the order changes the status to "in-progress", which should be handled by the kitchen views.
def review_order(request):

	# Check to see if an order is ready to be placed for this table.
	order_to_send = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	
	# If the order gets submitted, save it and redirect.
	if request.method == "POST":
		order_form = OrderForm(request.POST, instance=order_to_send.get())
		if order_form.is_valid():
			order_form.save()
			return HttpResponseRedirect("/menu/review-order/")
	
	# Build the context and form for the template if an order is ready to be placed.
	if order_to_send.exists():
		ordered_items = list(order_to_send.get().menu_items.all()) # Get the menu items already on the order
		order_form = OrderForm(
			initial={
				'status': 'in-progress'
			}, instance=order_to_send.get())
		
		context = {
			'order': order_to_send.get(),
			'ordered_items': ordered_items,
			'form': order_form
		}
		return render(request, 'menu/review-order.html', context)
	
	return render(request, 'menu/review-order.html')
	
# This view shows the user their order AFTER sending it to the kitchen so they can pay for it.
def order_summary(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		ordered_items = list(order_to_pay.get().menu_items.all()) # Get the menu items already on the order
		context = {
			'order': order_to_pay.get(),
			'ordered_items': ordered_items,
		}
	
	return render(request, 'payment/order-summary.html', context)
	
	
# This view shows the user various payment-related messages as they're paying for their order
def paying(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		context = {
			'order': order_to_pay.get(),
		}
	
	return render(request, 'payment/paying.html', context)
	
# This view shows the user various payment-related messages as they're paying for their order
def signing(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		context = {
			'order': order_to_pay.get(),
		}
	
	return render(request, 'payment/signing.html', context)

	
