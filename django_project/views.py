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
	all_orders = Order.objects.all().order_by("-id")
	if request.user.is_authenticated():
		"""
		get all orders 
		and find the time span 
		if order have been prepared , the chef's name will store in the order-data
		"""
		all_orders = Order.objects.all().order_by("-id")
		css = CookStatus.objects.filter(cook_name=request.user)
		cs = None
		current_order = None
		if len(css) != 0:
			cs = css[0]
			if cs.current_order != None :
				current_order = cs.current_order.menu_items.all()

		new_orders = []
		for order in all_orders:
			a = {}
			a['id'] = order.id
			a['status'] = order.status

			a['timespan'] = (datetime.datetime.utcnow().replace(tzinfo=utc) - order.timestamp_created).seconds
			cookofthis = CookStatus.objects.filter(current_order=order)
			if len(cookofthis) != 0:
				a['cookname'] = cookofthis[0].cook_name.username
			elif order.chef != None:
				a['cookname'] = order.chef

			new_orders.append(a)


		return render(request,'staff/cookOrders.html', 
			{'all_orders':new_orders, 'user':request.user, 'current_order':current_order, 'full_name':request.user.username})
	else:
		template = "staff/accessDenied.html"
		return render(request, template)

def cookTheOrder(request):
	"""
	chang the order's status to be "cooking" which is selected by the id of order 
	"""
	order_id = request.GET.get('order_id', 0)
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
	chang the order's status to be "ready-to-serve" which is selected by the id of order 
	"""
	cs , status = CookStatus.objects.get_or_create(cook_name=request.user)
	if cs.current_order is not None:
		cs.current_order.status = 'ready-to-serve'
		cs.current_order.save()
		cs.current_order = None
		cs.save()

	return HttpResponseRedirect("/cookOrdersList/")