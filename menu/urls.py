from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$', views.menu, name='menu'),
	# /menu/category/7
	url(r'^category/(?P<category_id>\d+)/$', views.categories, name='category'),
	# /menu/category/items/7
	url(r'^category/items/(?P<menu_item_id>\d+)/$', views.menu_items, name='menu_item')
)
