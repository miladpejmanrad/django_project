from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf


def home(request):
	context = {}
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