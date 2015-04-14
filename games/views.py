from django.shortcuts import render
from menu.models import MenuItem, Order
from django_project import settings

# This returns and sets up the contexts for the main menu.html template
def games(request):
	return render(request, 'games.html')

# This returns and sets up the contexts for the individual categories and their menu items for the menu.html template
def flappybird(request):
	return render(request, 'flappybird.html')

def chancegame(request):
	context = {}
	
	# First, check to see if an order already exists. If not, create one.
	if not Order.objects.filter(table_number=settings.TABLE_NUMBER).exclude(status='paid').exists():
		current_order = Order(
			table_number = settings.TABLE_NUMBER,
			status = 'ordering',
			total_price = '0.00'
		)
		eligibility = True
		current_order.save()
	else:
		current_order = Order.objects.filter(table_number=settings.TABLE_NUMBER).exclude(status='paid').latest("id")
		eligibility = current_order.freebie_eligible
		
	# Next, once they play the game, grab the POST data to see if they won on the first try. Update data accordingly.
	if request.method == 'POST':
		if request.POST['winner'] == 'yes':
			current_order.menu_items.add(name="Free Dessert")
		current_order.freebie_eligible = False
		eligibility = False
		current_order.save()
		
	context = {
		'eligible': eligibility
	}
		
	return render(request, 'chancegame.html', context)
