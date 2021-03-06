from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from menu.models import Category, MenuItem, Advertisement, Order, Allergen, AdminMenu, Notification, Drink, DrinkFlavor, DrinkOrder, CookStatus, Survey
from django_project import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
import datetime
from django.utils.timezone import utc


def home(request):
	# If an order for this table has been served, show the PAY button on the home screen.
	payable_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	# Showing the ad
	advertisement = Advertisement.objects.all()
	for x in advertisement:
		b = x
	try:
		context = {'ready_to_pay': payable_order.exists(), 'Advertisement' : b.ad }
	except:
		context = {'ready_to_pay': payable_order.exists() }
	
	template = "home.html"
	return render(request, template, context)

def login(request):
	context = {}
	template = "staff/login.html"
	return render(request, template, context)

def auth_view(request): # Enables the staff to login based on their permissions
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	managers = Group.objects.get(name="managers").user_set.all()
	kitchenStaff = Group.objects.get(name="kitchenStaff").user_set.all()
	waitStaff = Group.objects.get(name="waitStaff").user_set.all()
	if user in managers:
		auth.login(request,user)
		return HttpResponseRedirect("/managers")
	elif user in kitchenStaff:
		auth.login(request,user)
		return HttpResponseRedirect("/kitchenStaff")
	elif user in waitStaff:
		auth.login(request,user)
		return HttpResponseRedirect("/waitStaff")
	else:
		return HttpResponseRedirect("/invalid")
	

# There is three types of staff users listed below: manager(s), kitchenstaff and waitstaff
def managers(request): 
	if request.user.is_authenticated():
		options = AdminMenu.objects.all()
		template = "staff/managers.html"
		context = {'options': options,'full_name':request.user.username}
		return render(request, template, context)

	else:
		template = "staff/accessDenied.html"
		return render(request, template)


def kitchenStaff(request):
	if request.user.is_authenticated():
		options = AdminMenu.objects.all()
		template = "staff/kitchenStaff.html"
		context = {'options': options,'full_name':request.user.username}
		return render(request, template, context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def waitStaff(request):
	if request.user.is_authenticated():
		options = AdminMenu.objects.all()
		template = "staff/waitStaff.html"
		context = {'options': options,'full_name':request.user.username}
		return render(request, template, context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)


def logout(request):
	auth.logout(request)
	template = "staff/login.html"
	return render(request, template)


def invalid(request): # If the users put incorrect username and/or password this view will operate
	context = {}
	template = "staff/invalid.html"
	return render(request, template, context)

def cookOrdersList(request): # This view belongs to the kitchenstaff to view the orders that are either ready too cook or being cooked
	all_orders = Order.objects.all().order_by("id")
	al = []
	for orders in all_orders:
		if orders.status=="cooking" or orders.status=="in-progress":
			al.append(orders)
	all_orders = al # Trying to show only the orders which are either being cooked or in progress
	if request.user.is_authenticated():
		"""
		get all orders 
		and find the time span 
		if order have been prepared , the chef's name will store in the order-data
		"""
		# all_orders = Order.objects.all().order_by("-id")
		css = CookStatus.objects.filter(cook_name=request.user)
		cs = None
		current_order = None
		if len(css) != 0:
			cs = css[0]
			if cs.current_order != None :
				current_order = cs.current_order.menu_items.all()

		new_orders = []
		for order in all_orders:
			#print order.table_number
			a = {}
			a['id'] = order.id
			a['status'] = order.status

			a['timespan'] = (datetime.datetime.utcnow().replace(tzinfo=utc) - order.timestamp_created).seconds//60
			cookofthis = CookStatus.objects.filter(current_order=order)
			if len(cookofthis) != 0:
				a['cookname'] = cookofthis[0].cook_name.username
			elif order.chef != None:
				a['cookname'] = order.chef

			new_orders.append(a)
			#print current_order
			for x in all_orders:
				if x.chef==request.user.username:
					current_order=x
					

		try:
			context = {'all_orders':new_orders,'modifications':current_order.modifications, 'current_order':current_order.menu_items.all(), 'full_name':request.user.username}
		except:
			context = {'all_orders':new_orders, 'full_name':request.user.username}
		return render(request,'staff/cookOrders.html', context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def cookTheOrder(request, order_id): # This will change the order status to cooking and showing the name of the chef cooking it
	"""
	chang the order's status to be "cooking" which is selected by the id of order 
	"""
	# order_id = request.GET.get('order_id', 0)
	cs , status = CookStatus.objects.get_or_create(cook_name=request.user)

	if cs.current_order is None:
		cs.current_order = Order.objects.get(id=order_id)
		cs.current_order.status = 'cooking'
		cs.current_order.chef = request.user.username
		cs.current_order.save()
		cs.save()

	return HttpResponseRedirect("/cookOrdersList")


def orderIsReady(request): # When the order is ready, the chef uses this def to change the status of the order to ready-to-serve
	"""
	change the order's status to be "ready-to-serve" which is selected by the id of order 
	"""
	cs , status = CookStatus.objects.get_or_create(cook_name=request.user)
	if cs.current_order is not None:
		cs.current_order.status = 'ready-to-serve'
		cs.current_order.save()

		n = Notification(type='ready', table_number=cs.current_order.table_number, order=cs.current_order)
		n.save()

		cs.current_order = None
		cs.save()

	return HttpResponseRedirect("/cookOrdersList/")



def waitStaffModifyOrderList(request): # The waitstaff will view the menu items of the orders that are ready to serve
	"""
	 list all orders 
	"""
	all_orders = Order.objects.filter(status='ready-to-serve').order_by('-id')
	#print all_orders
	return render(request,'staff/staffOrderList.html', 
		{'all_orders':all_orders, 'user':request.user })


def waitStaffModifyOrderEdit(request): # The waitstaff will be able to modify the menu items of the orders that are ready to serve
	"""
	 show details and comp
	 comp = 0 : get details of certain order by id 
	 comp = 1 : make the order to be served 
	"""
	try:
		comp = request.GET.get('comp', 0)
		order_id = request.GET.get('order_id', 0)
		order = Order.objects.get(id=order_id)
		if comp == 0:
			return render(request,'staff/staffOrderDtail.html', 
				{'order':order, 'user':request.user, 'items':order.menu_items.all()})
		else:
			item_id = request.GET.get('item_id', 0)
			order.total_price = order.total_price - MenuItem.objects.get(id=item_id).price
			order.menu_items.remove(MenuItem.objects.get(id=item_id))
			order.save()
		return HttpResponseRedirect("/waitStaffModifyOrderList/")

	except:
		return HttpResponseRedirect("/waitStaffModifyOrderList/")


def WaitStaffViewNotifications(request): # The waitstaff wcan view the notofications through this def
	"""
		type_choices = (
		('help', 'Help'),
		('refill', 'Refill'),
		('ready', 'Ready to serve'),
		('cash', 'Pay with cash')
	)


	"""
	notifications = Notification.objects.all().order_by('-id')
	all_n = []
	for notification in notifications :
		n = {}
		n['id'] = notification.id
		if notification.type == 'help':
			n['info'] = 'Table ' + str(notification.table_number) + ' Need assistance'
		elif notification.type == 'refill':
			n['info'] = 'Table ' + str(notification.table_number) + ' refill ' + notification.drink
		elif notification.type == 'ready':
			n['info'] = 'Table ' + str(notification.table_number) + ' order #' + str(notification.order) + ' Ready'
		elif notification.type == 'cash':
			n['info'] = 'Table ' + str(notification.table_number) + ' Pay with cash'
		all_n.append(n)

	return render(request,'staff/WaitStaffViewNotifications.html', 
		{'notifications':all_n, 'user':request.user })


def WaitStaffDeleteNotification(request): # This works for deleting the notofications that are shown to the waitstaff 
	"""
	"""
	try:
		nid = request.GET.get('nid', 0)
		n = Notification.objects.get(id=nid)
		o = n.order 
		o.status = 'served'
		o.save()
		n.delete()
		return HttpResponseRedirect("/WaitStaffViewNotifications/")
	except :
		return HttpResponseRedirect("/WaitStaffViewNotifications/")


def modifyMenu(request): # For viewing the ModifyMenu page
	MenuItems = MenuItem.objects.all()

	if request.user.is_authenticated():
		"""
		
		"""
		
		context = {'MenuItems':MenuItems}
		return render(request,'staff/ModifyMenu.html', context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def showItem(request, item_id): # To show an item if it is in stock
	menu_item = MenuItem.objects.get(id=item_id)
	if request.user.is_authenticated():
		menu_item.visible = True
		menu_item.save()
		return HttpResponseRedirect("/modifyMenu")
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def hideItem(request, item_id): # To hide an item if it is not in stock
	menu_item = MenuItem.objects.get(id=item_id)
	if request.user.is_authenticated():
		menu_item.visible = False
		menu_item.save()
		return HttpResponseRedirect("/modifyMenu")
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def managersViewNotifications(request): # The manager(s) wcan view the notofications through this def
	"""
		type_choices = (
		('help', 'Help'),
		('refill', 'Refill'),
		('ready', 'Ready to serve'),
		('cash', 'Pay with cash')
	)


	"""
	notifications = Notification.objects.all().order_by('-id')
	all_n = []
	for notification in notifications :
		n = {}
		n['id'] = notification.id
		if notification.type == 'help':
			n['info'] = 'Table ' + str(notification.table_number) + ' Need assistance'
		elif notification.type == 'refill':
			n['info'] = 'Table ' + str(notification.table_number) + ' refill ' + notification.drink
		elif notification.type == 'ready':
			n['info'] = 'Table ' + str(notification.table_number) + ' order #' + str(notification.order) + ' Ready'
		elif notification.type == 'cash':
			n['info'] = 'Table ' + str(notification.table_number) + ' Pay with cash'
		all_n.append(n)

	return render(request,'staff/managersViewNotifications.html', 
		{'notifications':all_n, 'user':request.user })


def managersDeleteNotification(request): # The manager also will be able to delete the notifications like refill and ...
	"""
	"""
	try:
		nid = request.GET.get('nid', 0)
		n = Notification.objects.get(id=nid)
		o = n.order 
		o.status = 'served'
		o.save()
		n.delete()
		return HttpResponseRedirect("/managersViewNotifications/")
	except :
		return HttpResponseRedirect("/managersViewNotifications/")

def managersModifyOrderList(request): # The waitstaff will view the menu items of the orders that are ready to serve
	"""
	 list all orders 
	"""
	all_orders = Order.objects.filter(status='ready-to-serve').order_by('-id')
	# print all_orders
	return render(request,'staff/managersOrderList.html', 
		{'all_orders':all_orders, 'user':request.user })


def managersModifyOrderEdit(request): # The waitstaff will be able to modify the menu items of the orders that are ready to serve
	"""
	 show details and comp 
	 comp = 0 : get details of certain order by id 
	 comp = 1 : make the order to be served 
	"""
	try:
		comp = request.GET.get('comp', 0)
		order_id = request.GET.get('order_id', 0)
		order = Order.objects.get(id=order_id)
		if comp == 0:
			return render(request,'staff/managersOrderDtail.html', 
				{'order':order, 'user':request.user, 'items':order.menu_items.all()})
		else:
 			item_id = request.GET.get('item_id', 0)
 			order.menu_items.remove(item_id)
 			order.menu_items.save()
 			order.save()
 			return HttpResponseRedirect("/managersModifyOrderList/")
	
	except:
		return HttpResponseRedirect("/managersModifyOrderList/")

def viewSurvey(request): # The manager(s) will have the option the view the surveys
	surveyResults = Survey.objects.all()

	context = {'surveyResults':surveyResults}
	template = 'staff/viewSurvey.html'
	return render(request, template, context)

def viewReports(request): # The manager(s) will have the option the view the reports. 
	paid_orders = Order.objects.filter(status='paid')
	items = {} #The menu items sold with their rate
	for order in paid_orders:
		if order.timestamp_created.month == (datetime.datetime.utcnow()).month:
			for item in order.menu_items.all():
				if items.has_key(item)==False:
			  		items[item] = 1
				else:
			  		items[item] += 1
	highest = []
	highest = sorted(items.values(), reverse=True)
	top_dishes_month = []
	for item in items:
		if items[item] == highest[0]:
			top_dishes_month.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[1]:
			top_dishes_month.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[2]:
			top_dishes_month.append(item)
			items.pop(item, None)
			break

	items = {} #The menu items sold with their rate
	for order in paid_orders:
		if order.timestamp_created.day - (datetime.datetime.utcnow()).day < 7:
			for item in order.menu_items.all():
				if items.has_key(item)==False:
			  		items[item] = 1
				else:
			  		items[item] += 1
	highest = []
	highest = sorted(items.values(), reverse=True)
	top_dishes_week = []
	for item in items:
		if items[item] == highest[0]:
			top_dishes_week.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[1]:
			top_dishes_week.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[2]:
			top_dishes_week.append(item)
			items.pop(item, None)
			break

	items = {} #The menu items sold with their rate
	for order in paid_orders:
		item = order.timestamp_created.hour
		if order.timestamp_created.day - (datetime.datetime.utcnow()).day < 7:
			if items.has_key(item)==False:
			  	items[item] = 1
			else:
			  	items[item] += 1
	highest = []
	highest = sorted(items.values(), reverse=True)
	busiest_times_week = []
	for item in items:
		if items[item] == highest[0]:
			busiest_times_week.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[1]:
			busiest_times_week.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[2]:
			busiest_times_week.append(item)
			items.pop(item, None)
			break

	items = {} #The menu items sold with their rate
	for order in paid_orders:
		item = order.timestamp_created.hour
		if order.timestamp_created.month == (datetime.datetime.utcnow()).month:
			if items.has_key(item)==False:
			  	items[item] = 1
			else:
			  	items[item] += 1
	highest = []
	highest = sorted(items.values(), reverse=True)
	busiest_times_month = []
	for item in items:
		if items[item] == highest[0]:
			busiest_times_month.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[1]:
			busiest_times_month.append(item)
			items.pop(item, None)
			break
	for item in items:
		if items[item] == highest[2]:
			busiest_times_month.append(item)
			items.pop(item, None)
			break

	context = {'top_dishes_month':top_dishes_month, 'top_dishes_week':top_dishes_week, 
	'busiest_times_week':busiest_times_week, 'busiest_times_month':busiest_times_month}
	template = 'staff/viewReports.html'
	return render(request, template, context)

def managersAd(request): # The manager will be able to add advertisement to the home page
	context = {}
	if request.method == 'POST':
		new_ad = Advertisement(
			ad = request.POST['ad']
		)
		new_ad.save()
		return HttpResponseRedirect("/managersAd")
		
	return render(request, 'staff/managersAd.html', context)