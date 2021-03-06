from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from menu.models import Category, Advertisement, MenuItem, Order, SplitOrder, SplitOrderContainer, Allergen, AdminMenu, Notification, Drink, DrinkFlavor, DrinkOrder, Survey
from menu.modelforms import AddItemToOrderForm, PlaceOrderForm, TipOrderForm
from decimal import Decimal
from binascii import a2b_base64
from django_project import settings
from django.core.mail import send_mail
import datetime

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
	drinks_list = Drink.objects.filter(category=category_id)
	allergies_list = Allergen.objects.all()
	
	# Check if it's Monday. We'll use this to print a notification on the menu about the Monday deal.
	today = datetime.date.today()
	if today.today().weekday() is 0:
		is_monday = True
	else:
		is_monday = False
	
	context = {
		'menuitems_list': menuitems_list,
		'drinks_list': drinks_list,
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
		'allergies_list': allergies_list,
		'current_category': category_id,
		'is_monday': is_monday
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
	
# This returns and sets up the contexts for low calorie filtered menu items within a category
def low_calorie(request, category_id):
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	categories_list = Category.objects.order_by('name')
	allergies_list = Allergen.objects.all()
	menuitems_list = MenuItem.objects.filter(category=category_id, visible=True).exclude(low_calorie=False) # Exclude items that aren't low calorie
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list,
		'order_exists': existing_order.exists(),
		'allergies_list': allergies_list,
		'current_category': category_id,
		'low_calorie': True
	}
	return render(request, 'menu/menu.html', context)

def is_happy_hour() :
	currentHour = datetime.datetime.now().hour
	if currentHour >= 16 and currentHour <= 19:
		return True
	else:
		return False

# This builds the menu item order form and returns the information for an individual menu item using the menu-item.html template
def menu_items(request, menu_item_id):
	
	# First, see if they already have an order in the system that's been placed, but not paid for.
	if not (Order.objects.filter(table_number=settings.TABLE_NUMBER).exists()) or not (Order.objects.filter(table_number=settings.TABLE_NUMBER).exclude(status='ordering').exclude(status='paid')):
		order_in_progress = True
	else:
		order_in_progress = False
		
	# Check if it's Monday. We'll use this to help calculate the price of the order based on the Monday deal.
	today = datetime.date.today()
	if today.today().weekday() is 0:
		is_monday = True
	else:
		is_monday = False
	
	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	menu_item = MenuItem.objects.get(id=menu_item_id)
	
	# This generates the form that appears on an individual menu item page.
	if existing_order.exists():
		order_form = AddItemToOrderForm(instance=existing_order.get()) # Grab the form data first so we can modify it
		ordered_items = list(existing_order.get().menu_items.all()) # Get the menu items already on the order
		ordered_drinks = list(existing_order.get().drinks.all()) # Get the drinks already on the order
		if not menu_item in ordered_items:
			ordered_items.append(menu_item) # Add the new menu item if it's not already there
		
		# Calculate the new total price
		total_price = 0
		kids_meals = existing_order.get().menu_items.filter(category__id=8).count()
		entrees = existing_order.get().menu_items.filter(category__id=5).count()
		if menu_item.category.id is 8:
			kids_meals += 1
		if menu_item.category.id is 5:
			entrees += 1
		if kids_meals >= entrees:
			free_kidsmeals = entrees
		elif entrees > kids_meals:
			free_kidsmeals = kids_meals
		else:
			free_kidsmeals = 0
		
		for item in ordered_items:
			if is_monday and free_kidsmeals > 0:
				# Take off the price of a kid's meal for each entree if applicable.
				if not MenuItem.objects.get(id=item.id).category.id is 8:
					item_price = MenuItem.objects.get(id=item.id)
					total_price = total_price + item_price.price
				else:
					free_kidsmeals = free_kidsmeals - 1
					total_price = total_price + 0
			else:
				item_price = MenuItem.objects.get(id=item.id)
				total_price = total_price + item_price.price
		
		if is_happy_hour():
			discount = Decimal('0.5')
		else:
			discount = Decimal('1.0')

		for drink in ordered_drinks:
			drink_price = Drink.objects.get(id=drink.drink.id)
			total_price = "{0:.2f}".format(total_price + (drink_price.price * discount))
		
		# Set the form to use the new data
		order_form = AddItemToOrderForm(
			initial={
				'menu_items': ordered_items,
				'total_price': total_price
			},
			instance=existing_order.get()
		)
	
	else:
		order_form = AddItemToOrderForm(
			initial={
				'menu_items': [menu_item_id],
				'table_number': settings.TABLE_NUMBER,
				'total_price': menu_item.price
			}
		)
	
	# This sets up the contexts to use in the menu-item.html template.
	context = {
		'menu_item': menu_item,
		'form': order_form,
		'order_exists': existing_order.exists(),
		'can_order': order_in_progress
	}
			
	return render(request, 'menu/menu-item.html', context)

# This returns and sets up the contexts for drinks
def drinks(request, drink_id):

	# First, see if they already have an order in the system that's been placed, but not paid for.
	if not (Order.objects.filter(table_number=settings.TABLE_NUMBER).exists()) or not (Order.objects.filter(table_number=settings.TABLE_NUMBER).exclude(status='ordering').exclude(status='paid')):
		order_in_progress = True
	else:
		order_in_progress = False
		
	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	drink = Drink.objects.get(id=drink_id)

	flavors_list = DrinkFlavor.objects.all()
	context = {
		'flavors_list': flavors_list,
		'order_exists': existing_order.exists(),
		'selected_drink': Drink.objects.get(id=drink_id),
		'can_order': order_in_progress
	}
	
	if request.method == 'POST':
		# Create the new drink order
		new_drink = DrinkOrder(
			drink = drink
		)
		new_drink.save()
		this_drink_id = new_drink.id
		if request.POST['flavor'] != 'None':
			this_drink = DrinkOrder.objects.filter(id=this_drink_id) # Get the query set so we can perform an update to add the flavor
			this_drink.update(flavor = DrinkFlavor.objects.get(flavor=request.POST['flavor']))
			this_drink = this_drink.get() # Get the actual instance of this drink order so we can save it
			this_drink.save()
		
		discount = Decimal('1.0')
		if existing_order.exists():
			# Calculate the new total price
			if is_happy_hour():
				discount = Decimal('0.5')
				total_price = "{0:.2f}".format(existing_order.get().total_price + round(new_drink.drink.price * discount, 2))
			else:
				total_price = existing_order.get().total_price + new_drink.drink.price
			existing_order.update(total_price=total_price)
			existing_order.get().drinks.add(new_drink)
			existing_order.get().save()
		
		else:
			if is_happy_hour():
				discount = Decimal('0.5')
			new_order = Order(
				table_number = settings.TABLE_NUMBER,
				status = 'ordering',
				total_price = "{0:.2f}".format(new_drink.drink.price * discount),
			)
			new_order.save()
			new_order.drinks.add(new_drink)
			new_order.save()
			
		return HttpResponseRedirect("/menu/")
	
	return render(request, 'menu/drink.html', context)

# This view processes the form sent by the menu-item.html template
def add_to_order(request, menu_item_id):

	# Check to see if an order is already set for this table. If so, modify it. If not, create a new one.
	existing_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	menu_item = MenuItem.objects.get(id=menu_item_id)

	if request.method == "POST":
		if existing_order.exists():
			order_form = AddItemToOrderForm(request.POST, instance=existing_order.get())
		else:
			order_form = AddItemToOrderForm(request.POST)
		if order_form.is_valid():
			order_form.save()
			return HttpResponseRedirect("/menu/")
			
	return HttpResponse("You're trying to order %s, but it didn't go through." % menu_item)
	
# This view shows the user their order BEFORE sending it to the kitchen and lets them submit to the kitchen.
# Submitting the order changes the status to "in-progress", which should be handled by the kitchen views.
def place_order(request):

	# Check to see if an order is ready to be placed for this table.
	order_to_send = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='ordering')
	
	# Check to see if it's Monday.
	today = datetime.date.today()
	if today.today().weekday() is 0:
		is_monday = True
	else:
		is_monday = False
	
	# If the order gets submitted, save it and redirect.
	if request.method == "POST":
		order_form = PlaceOrderForm(request.POST, instance=order_to_send.get())
		if order_form.is_valid():
			order_form.save()
			return HttpResponseRedirect("/menu/review-order/")
	
	# Build the context and form for the template if an order is ready to be placed.
	if order_to_send.exists():
		ordered_items = list(order_to_send.get().menu_items.all()) # Get the menu items already on the order
		ordered_drinks = list(order_to_send.get().drinks.all()) # Get the ordered drinks
		order_form = PlaceOrderForm(
			initial={
				'status': 'in-progress'
			}, instance=order_to_send.get())
			
		if is_happy_hour():
			discount = Decimal('0.5')
			for drink in ordered_drinks:
				drink.drink.original_price = drink.drink.price
				drink.drink.price = round(drink.drink.price * discount, 2)
			
		kids_meals = order_to_send.get().menu_items.filter(category__id=8).count()
		entrees = order_to_send.get().menu_items.filter(category__id=5).count()
		if kids_meals >= entrees:
			free_kidsmeals = entrees
		elif entrees > kids_meals:
			free_kidsmeals = kids_meals
		else:
			free_kidsmeals = 0
		
		kids_meals_check = free_kidsmeals
		for item in ordered_items:
			if kids_meals_check > 0 and item.category.id is 8 and is_monday:
				item.is_free = True
				kids_meals_check = kids_meals_check - 1
			else:
				item.is_free = False
		
		context = {
			'order': order_to_send.get(),
			'ordered_items': ordered_items,
			'ordered_drinks': ordered_drinks,
			'form': order_form,
			'free_kidsmeals': free_kidsmeals,
			'is_monday': is_monday,
			'is_happy_hour': is_happy_hour()
		}
		return render(request, 'menu/review-order.html', context)
	
	return render(request, 'menu/review-order.html')
	
# This view shows the user their order AFTER sending it to the kitchen so they can pay for it.
def order_summary(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# Check to see if it's Monday.
	today = datetime.date.today()
	if today.today().weekday() is 0:
		is_monday = True
	else:
		is_monday = False
	
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		ordered_items = list(order_to_pay.get().menu_items.all()) # Get the menu items already on the order
		ordered_drinks = list(order_to_pay.get().drinks.all()) # Get the ordered drinks
		
		if is_happy_hour():
			discount = Decimal('0.5')
			for drink in ordered_drinks:
				drink.drink.original_price = drink.drink.price
				drink.drink.price = round(drink.drink.price * discount, 2)
			
		kids_meals = order_to_pay.get().menu_items.filter(category__id=8).count()
		entrees = order_to_pay.get().menu_items.filter(category__id=5).count()
		if kids_meals >= entrees:
			free_kidsmeals = entrees
		elif entrees > kids_meals:
			free_kidsmeals = kids_meals
		else:
			free_kidsmeals = 0
		
		kids_meals_check = free_kidsmeals
		for item in ordered_items:
			if kids_meals_check > 0 and item.category.id is 8 and is_monday:
				item.is_free = True
				kids_meals_check = kids_meals_check - 1
			else:
				item.is_free = False
			
		
		context = {
			'order': order_to_pay.get(),
			'ordered_items': ordered_items,
			'ordered_drinks': ordered_drinks,
			'free_kidsmeals': free_kidsmeals,
			'is_monday': is_monday,
			'is_happy_hour': is_happy_hour()
		}
	
	return render(request, 'payment/order-summary.html', context)
	
# This view shows the user their order to split.
def split_summary(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	paid = False

	if request.method == 'POST':
		container = SplitOrderContainer.objects.get(parent_order=Order.objects.get(id=request.POST['order_id']))
		items_to_pay = request.POST.getlist('pay_these_items[]')
		drinks_to_pay = request.POST.getlist('pay_these_drinks[]')
		new_split = SplitOrder(
			container = container,
			parent_order = Order.objects.get(id=request.POST['order_id']),
			total_price = '0.00'
		)
		new_split.save()
		total_price = 0
		for item_id in items_to_pay:
			added_item = MenuItem.objects.get(id=item_id)
			new_split.menu_items.add(added_item)
			total_price = total_price + added_item.price
			container.menu_items.remove(added_item)
		discount = Decimal('1.0')
		if is_happy_hour() == True:
			discount = Decimal('0.5')
		for drink_id in drinks_to_pay:
			added_drink = DrinkOrder.objects.get(id=drink_id)
			new_split.drinks.add(added_drink)
			total_price = total_price + (added_drink.drink.price * discount)
			container.drinks.remove(added_drink)
		new_split.total_price = total_price
		new_split.save()
		
	# See if a split container has been created. If not, create one and populate it.
	existing_container = SplitOrderContainer.objects.filter(parent_order=order_to_pay.get())
	if not existing_container.exists():
		split_container = SplitOrderContainer(
			parent_order = order_to_pay.get(),
		)
		split_container.save()
		for item in list(order_to_pay.get().menu_items.all()):
			split_container.menu_items.add(item)
		for drink in list(order_to_pay.get().drinks.all()):
			split_container.drinks.add(drink)
		split_container.save()
	else:
		split_container = existing_container.get()
		
	# If the container's empty, get rid of it.
	if split_container.menu_items.count() == 0 and split_container.drinks.count() == 0:
		splits = SplitOrder.objects.filter(container=split_container)
		for split in splits:
			split.container = None
			split.save()
		split_container.delete()
		paid = True
		order_to_pay.get().status = 'paid'
		order_to_pay.get().save()
	
	# Build the context for the template
	if order_to_pay.exists() and paid is not True:
		ordered_items = split_container.menu_items.all() # Get the menu items already on the order
		ordered_drinks = split_container.drinks.all() # Get the ordered drinks
		context = {
			'order': split_container,
			'ordered_items': ordered_items,
			'ordered_drinks': ordered_drinks,
			'parent_id': order_to_pay.get().id
		}
	
	return render(request, 'payment/split-summary.html', context)
	
	
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
	
# This view lets the user sign their name after a successful credit card swipe
def signing(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# When a signature is submitted, save the signature as an image to /media/signatures/ and move on.
	if request.method == "POST":
		# Convert the base64 data from DrawingBoard's getImg method into binary. (We need to skip the "data:image/png;base64," part first though.)
		binary_data = a2b_base64(request.POST['signature_data'][22:])
		
		# Open up a file for storing the image's binary data.
		signature_image=open(
			settings.SIGNATURES_DIR + # Where it goes
			'OrderID_' + str(order_to_pay.get().id) + '.png', # The name of the image file
			'wb+')
			
		# Store the image data and then move on to tips.
		signature_image.write(binary_data)
		signature_image.close()
		return HttpResponseRedirect("/pay/card/tip/")
			
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		context = {
			'order': order_to_pay.get(),
		}
	
	return render(request, 'payment/signing.html', context)
	
	
# This view shows the tip options.
def tipping(request):

	# Check to see if an order is ready to be paid for at this table.
	order_to_pay = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {}
	
	# If the order gets submitted, save it and redirect.
	if request.method == "POST":
		order_form = TipOrderForm(request.POST, instance=order_to_pay.get())
		if order_form.is_valid():
			order_form.save()
			return HttpResponseRedirect("/pay/card/tip/")
	
	# Build the context for the template if an order is ready to be paid.
	if order_to_pay.exists():
		tip_form = TipOrderForm(
			initial={
				'status': 'paid'
			}, instance=order_to_pay.get())
		tip_05 = "{0:.2f}".format(order_to_pay.get().total_price * Decimal(.05))
		tip_10 = "{0:.2f}".format(order_to_pay.get().total_price * Decimal(.10))
		tip_15 = "{0:.2f}".format(order_to_pay.get().total_price * Decimal(.15))
		tip_20 = "{0:.2f}".format(order_to_pay.get().total_price * Decimal(.20))
		context = {
			'order': order_to_pay.get(),
			'tip_05': tip_05,
			'tip_10': tip_10,
			'tip_15': tip_15,
			'tip_20': tip_20,
			'form': tip_form
		}
	
	return render(request, 'payment/tipping.html', context)
	
# This view handles the receipts.
def receipt(request, receipt_type):

	# Get the latest paid order for this table.
	last_paid_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='paid')
	context = {}
	
	discount = Decimal('1.0')
	# If the user wants to email their receipt, send a copy of it to the entered email.
	if request.method == "POST":
		if is_happy_hour() == True:
			discount = Decimal('0.5')
		email = request.POST['email_address']
		receipt_contents = 'Here is a copy of your receipt.\r\n'
		for items in last_paid_order.latest('id').menu_items.all():
			receipt_contents += items.name + ': ' + str(items.price) + '\r\n'
		for drinks in last_paid_order.latest('id').drinks.all():
			receipt_contents += drinks.drink.name + ': ' + str(drinks.drink.price * discount) + '\r\n'
		receipt_contents += '\r\nTip: ' + str(last_paid_order.latest('id').tip) + ' \r\n'
		receipt_contents += 'Total: ' + str(last_paid_order.latest('id').total_price)
		send_mail('Your restaurant receipt', receipt_contents, 'from@example.com', [email], fail_silently=False)
		context = {
			'received_receipt': True,
		}
	
	# Build the context for the template
	elif last_paid_order.exists():
		if is_happy_hour():
			discount = Decimal('0.5')
		ordered_items = list(last_paid_order.latest('id').menu_items.all()) # Get the menu items on the order
		ordered_drinks = list(last_paid_order.latest('id').drinks.all()) # Get the drinks on the order
		
		if is_happy_hour():
			discount = Decimal('0.5')
			for drink in ordered_drinks:
				drink.drink.original_price = drink.drink.price
				drink.drink.price = round(drink.drink.price * discount, 2)
		
		context = {
			'order': last_paid_order.latest('id'),
			'ordered_items': ordered_items,
			'ordered_drinks': ordered_drinks,
			'receipt_type': receipt_type,
			'is_happy_hour': is_happy_hour()
		}
	
	return render(request, 'payment/receipt.html', context)

# This view handles the options available when selecting the refill button.
def refill(request):
	try:
		current_order = Order.objects.filter(table_number=settings.TABLE_NUMBER).exclude(status='paid').exclude(status='ordering')
		ordered_drinks = list(current_order.latest('id').drinks.all()) # Get the drinks on the order
		context = {
			'drinks_list': ordered_drinks,
		}
		return render(request, 'menu/refill.html', context)
	except:
		return render(request, 'menu/refill.html', {})
	
# This view handles the notifications sent by the customer.
def send_notification(request):
	context = {}
	if request.method == "POST":
		notification_type = request.POST['type']
		drink_name = ''
		if notification_type == 'refill':
			drink_name = request.POST['drink']
		new_notification = Notification(
			table_number = settings.TABLE_NUMBER,
			type = notification_type,
			drink = drink_name
		)
		new_notification.save()
		context = {
			'notification_type': notification_type,
		}
		
	return render(request, 'notification.html', context)

def askIfSurvey(request): # To show the page asking the customers if they are willing to do a quick survey
	context = {}
	return render(request, 'payment/askIfSurvey.html', context)

def survey(request): # Stores the survey instance 
	context = {}
	if request.method == 'POST':
		new_survey = Survey(
			server = request.POST['server'],
			food = request.POST['food'],
			ordering = request.POST['ordering'],
			Comments = request.POST['Comments']
		)
		new_survey.save()
		return HttpResponseRedirect("/")
		
	return render(request, 'payment/survey.html', context)

