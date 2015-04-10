from django.shortcuts import render, render_to_response
from staff.models import CookStatus
from menu.models import  Order
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.utils.timezone import utc
# Create your views here.



def cook_order_list(request):
	"""
	get all orders 
	and find the time span 
	if order have been prepared , the ticchen's name will store in the order-data
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
		elif order.tikchen != None:
			a['cookname'] = order.tikchen

		new_orders.append(a)


	return render_to_response('staff/cook_order_list.html', 
		{'all_orders':new_orders, 'user':request.user, 'current_order':current_order})


def cook_order(request):
	"""
	chang the order's status to be "cooking" which is selected by the id of order 
	"""
	order_id = request.GET.get('order_id', 0)
	cs , status = CookStatus.objects.get_or_create(cook_name=request.user)

	if cs.current_order is None:
		cs.current_order = Order.objects.get(id=order_id)
		cs.current_order.status = 'cooking'
		cs.current_order.tikchen = request.user.username
		cs.current_order.save()
		cs.save()

	return HttpResponseRedirect("/staff/cook_order_list/")


def order_ready(request):
	"""
	chang the order's status to be "ready-to-serve" which is selected by the id of order 
	"""
	cs , status = CookStatus.objects.get_or_create(cook_name=request.user)
	if cs.current_order is not None:
		cs.current_order.status = 'ready-to-serve'
		cs.current_order.save()
		cs.current_order = None
		cs.save()

	return HttpResponseRedirect("/staff/cook_order_list/")
