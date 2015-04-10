from django.conf.urls import patterns, url
from staff import views

urlpatterns = patterns('',
	# /menu/

	url(r'^cook_order_list/$', views.cook_order_list, name='cook_order_list'),
	url(r'^cook_order/$', views.cook_order, name='cook_order'),
	url(r'^order_ready/$', views.order_ready, name='order_ready'),
    
)
