from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$', views.menu, name='menu'),
	# /menu/category/7
	url(r'^category/(?P<category_id>\d+)/$', views.categories, name='category'),
	# /menu/items/3
	url(r'^items/(?P<menu_item_id>\d+)/$', views.menu_items, name='menu_item'),
	# /menu/items/3/order
	url(r'^items/(?P<menu_item_id>\d+)/order/$', views.add_to_order, name='add_to_order'),
	# /menu/category/3/exclude/peanuts
	url(r'^category/(?P<category_id>\d+)/exclude/(?P<allergy_name>\S+)/$', views.filtered_categories, name='filtered_category'),
)
