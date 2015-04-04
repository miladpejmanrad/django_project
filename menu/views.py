from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from menu.models import Category, MenuItem
from menu.modelforms import OrderForm

# Create your views here.
def menu(request):
	categories_list = Category.objects.order_by('name')
	context = {'categories_list': categories_list}
	return render(request, 'menu.html', context)

def categories(request, category_id):
	# return HttpResponse("You're looking at category %s." % category_id)
	categories_list = Category.objects.order_by('name')
	menuitems_list = MenuItem.objects.filter(category=category_id)
	context = {
		'menuitems_list': menuitems_list,
		'categories_list': categories_list
	}
	return render(request, 'menu.html', context)

def menu_items(request, menu_item_id):
	# return HttpResponse("You're looking at menu item %s." % menu_item_id)
	order_form = OrderForm()
	menu_item = MenuItem.objects.get(id=menu_item_id)
	context = {
		'menu_item': menu_item,
		'form': order_form
	}

	if request.method == "POST":
		order_form = OrderForm(request.POST)
		if form.is_valid():
			order = order_form.save(commit=False)
			order.save()
			return HttpResponseRedirect("/menu/")
			
	return render(request, 'menu-item.html', context)

def add_to_order(request, menu_item_id):
	menu_item_name = MenuItem.objects.get(id=menu_item_id)
	return HttpResponse("You're trying to order %s." % menu_item_name)
	
    