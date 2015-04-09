from django.shortcuts import render

# This returns and sets up the contexts for the main menu.html template
def games(request):
	return render(request, 'games.html')

# This returns and sets up the contexts for the individual categories and their menu items for the menu.html template
def flappybird(request):
	return render(request, 'flappybird.html')

def chancegame(request):
	return render(request, 'chancegame.html')
