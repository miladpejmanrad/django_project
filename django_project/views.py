from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from menu.models import Order, AdminMenu
from django_project import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

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