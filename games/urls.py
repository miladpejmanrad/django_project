from django.conf.urls import patterns, url
from games import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$',  views.games, name='games'),
	url(r'^flappybird/$', views.flappybird, name='flappybird'),
	url(r'^chancegame/$', views.chancegame, name='chancegame'),
    
)
