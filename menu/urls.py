from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$', views.index, name='index'),
	url(r'^mainMenu/$', views.mainMenu, name='mainMenu'),
	# /menu/category/7
	url(r'^category/(?P<category_id>\d+)/$', views.categories, name='category')
)
