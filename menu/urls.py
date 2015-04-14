from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$', views.menu, name='menu'),
	# /menu/category/7/
	url(r'^category/(?P<category_id>\d+)/$', views.categories, name='category'),
	# /menu/items/3/
	url(r'^items/(?P<menu_item_id>\d+)/$', views.menu_items, name='menu_item'),
	# /menu/drinks/3/
	url(r'^drinks/(?P<drink_id>\d+)/$', views.drinks, name='drink'),
	# /menu/items/3/order/
	url(r'^items/(?P<menu_item_id>\d+)/order/$', views.add_to_order, name='add_to_order'),
	# /menu/category/3/exclude/1/
	url(r'^category/(?P<category_id>\d+)/exclude/(?P<allergy_id>\d+)/$', views.filtered_categories, name='filtered_category'),
	# /menu/category/3/vegetarian/
	url(r'^category/(?P<category_id>\d+)/vegetarian/$', views.vegetarian, name='vegetarian'),
	# /menu/category/3/low-calorie/
	url(r'^category/(?P<category_id>\d+)/low-calorie/$', views.low_calorie, name='low_calorie'),
	# /menu/review-order/
	url(r'^review-order/$', views.place_order, name='place_order'),
	# /menu/refill/
	url(r'^refill/$', views.refill, name='refill'),
	# /menu/AskIfsurvey/
	url(r'^askIfSurvey/$', views.askIfSurvey, name='askIfSurvey'),
	# /menu/survey/
	url(r'^survey/$', views.survey, name='survey'),
)
