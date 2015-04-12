from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from menu.models import Category, MenuItem, Order, Allergen, AdminMenu, Notification, Drink, DrinkFlavor, DrinkOrder, CookStatus
from django_project import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
import datetime
from django.utils.timezone import utc


def home(request):
	# If an order for this table has been served, show the PAY button on the home screen.
	payable_order = Order.objects.filter(table_number=settings.TABLE_NUMBER, status='served')
	context = {
		'ready_to_pay': payable_order.exists(),
	}
	
	template = "home.html"
	return render(request, template, context)

def login(request):
	context = {}
	template = "staff/login.html"
	return render(request, template, context)

def auth_view(request):
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


def invalid(request):
	context = {}
	template = "staff/invalid.html"
	return render(request, template, context)

def cookOrdersList(request):
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
			context = {'all_orders':new_orders, 'current_order':current_order.menu_items.all(), 'full_name':request.user.username}
		except:
			context = {'all_orders':new_orders, 'full_name':request.user.username}
		return render(request,'staff/cookOrders.html', context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def cookTheOrder(request, order_id):
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


def orderIsReady(request):
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



def waitStaffModifyOrderList(request):
	"""
	 list all orders 
	"""
	all_orders = Order.objects.filter(status='ready-to-serve').order_by('-id')
	print all_orders
	return render(request,'staff/staffOrderList.html', 
		{'all_orders':all_orders, 'user':request.user })


def waitStaffModifyOrderEdit(request):
	"""
	 show datails and change the status from ready-to-serve to served 
	 served = 0 : get details of certain order by id 
	 served = 1 : make the order to be rerved 
	"""
	try :
		served = request.GET.get('served', 0)
		order_id = request.GET.get('order_id', 0)
		order = Order.objects.get(id=order_id)
		if served == 0 :
			return render(request,'staff/staffOrderDtail.html', 
				{'order':order, 'user':request.user, 'items':order.menu_items.all()})
		else :
			order.status = 'served'
			order.save()
			return HttpResponseRedirect("/waitStaffModifyOrderList/")

	except:
		return HttpResponseRedirect("/waitStaffModifyOrderList/")


def ViewNotifications(request):
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

	return render(request,'staff/Notificaiton.html', 
		{'notifications':all_n, 'user':request.user })


def DeleteNotification(request):
	"""
	"""
	try:
		nid = request.GET.get('nid', 0)
		n = Notification.objects.get(id=nid)
		n.delete()
		return HttpResponseRedirect("/ViewNotifications/")
	except :
		return HttpResponseRedirect("/ViewNotifications/")


def modifyMenu(request):
	MenuItems = MenuItem.objects.all()

	if request.user.is_authenticated():
		"""
		
		"""
		
		context = {'MenuItems':MenuItems}
		return render(request,'staff/ModifyMenu.html', context)
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def showItem(request, item_id):
	menu_item = MenuItem.objects.get(id=item_id)
	if request.user.is_authenticated():
		menu_item.visible = True
		menu_item.save()
		return HttpResponseRedirect("/modifyMenu")
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def hideItem(request, item_id):
	menu_item = MenuItem.objects.get(id=item_id)
	if request.user.is_authenticated():
		menu_item.visible = False
		menu_item.save()
		return HttpResponseRedirect("/modifyMenu")
	else:
		template = "staff/accessDenied.html"
		return render(request, template)
