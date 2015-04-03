from django.conf.urls import patterns, url
from menu import views

urlpatterns = patterns('',
	# /menu/
	url(r'^$', views.menu, name='menu'),
	# /menu/category/7
	url(r'^category/(?P<category_id>\d+)/$', views.categories, name='category')
)
