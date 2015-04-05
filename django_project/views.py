from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from menu.models import Order 
from menu import settings

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

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect("/loggedin")
	else:
		return HttpResponseRedirect("/invalid")
	

def loggedin(request):
	template = "staff/loggedin.html"
	return render(request, template,
				 {'full_name':request.user.username})


def logout(request):
	auth.logout(request)
	template = "staff/logout.html"
	return render(request, template)


def invalid(request):
	context = {}
	template = "staff/invalid.html"
	return render(request, template, context)