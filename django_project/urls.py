from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # Django admin related patterns
    url(r'^admin/', include(admin.site.urls)),
    
    # Menu related patterns
    url(r'^menu/', include('menu.urls')),
    
    # Game related patterns
    url(r'^games/', include('games.urls')),
    
    # Payment related patterns
    url(r'^pay/$', 'menu.views.order_summary', name='order_summary'),
    url(r'^pay/card/$', 'menu.views.paying', name='paying'),
    url(r'^pay/cash/$', 'menu.views.paying', name='paying'),
	url(r'^pay/split/$', 'menu.views.split_summary', name='split_summary'),
    url(r'^pay/card/sign/$', 'menu.views.signing', name='signing'),
    url(r'^pay/card/tip/$', 'menu.views.tipping', name='tipping'),
    url(r'^pay/receipt/(?P<receipt_type>\w+)/$', 'menu.views.receipt', name='receipt'),
    
    # Notification related patterns
    url(r'^notify/$', 'menu.views.send_notification', name='send_notification'),
    
    # Staff related patterns
    url(r'^login/$', 'django_project.views.login', name='login'),
    url(r'^auth_view/$', 'django_project.views.auth_view', name='auth_view'),
    url(r'^logout/$', 'django_project.views.logout', name='logout'),
    url(r'^managers/$', 'django_project.views.managers', name='managers'),
    url(r'^kitchenStaff/$', 'django_project.views.kitchenStaff', name='kitchenStaff'),
    url(r'^waitStaff/$', 'django_project.views.waitStaff', name='waitStaff'),
    url(r'^invalid/$', 'django_project.views.invalid', name='invalid'),
    # url(r'^viewNotifications/$', 'django_project.views.viewNotifications', name='viewNotifications'),
    # url(r'^modifyOrders/$', 'django_project.views.modifyOrders', name='modifyOrders'),
    # url(r'^viewSurveys/$', 'django_project.views.viewSurveys', name='viewSurveys'),
    # url(r'^viewOrderReports/$', 'django_project.views.viewOrderReports', name='viewOrderReports'),
    url(r'^cookOrdersList/$', 'django_project.views.cookOrdersList', name='cookOrdersList'),
    url(r'^modifyMenu/$', 'django_project.views.modifyMenu', name='modifyMenu'),
    url(r'^orderIsReady/$', 'django_project.views.orderIsReady', name='orderIsReady'),
    url(r'^cookTheOrder/(?P<order_id>\d+)/$', 'django_project.views.cookTheOrder', name='cookTheOrder'),
    url(r'^showItem/(?P<item_id>\d+)/$', 'django_project.views.showItem', name='showItem'),
    url(r'^hideItem/(?P<item_id>\d+)/$', 'django_project.views.hideItem', name='hideItem'),


    url(r'^waitStaffModifyOrderList/$', 'django_project.views.waitStaffModifyOrderList', name='waitStaffModifyOrderList'),
    url(r'^waitStaffModifyOrderEdit/$', 'django_project.views.waitStaffModifyOrderEdit', name='waitStaffModifyOrderEdit'),
    url(r'^WaitStaffViewNotifications/$', 'django_project.views.WaitStaffViewNotifications', name='WaitStaffViewNotifications'),
    url(r'^WaitStaffDeleteNotification/$', 'django_project.views.WaitStaffDeleteNotification', name='WaitStaffDeleteNotification'),
    url(r'^managersViewNotifications/$', 'django_project.views.managersViewNotifications', name='managersViewNotifications'),
    url(r'^managersDeleteNotification/$', 'django_project.views.managersDeleteNotification', name='managersDeleteNotification'),
    url(r'^managersModifyOrderList/$', 'django_project.views.managersModifyOrderList', name='managersModifyOrderList'),
    url(r'^managersModifyOrderEdit/$', 'django_project.views.managersModifyOrderEdit', name='managersModifyOrderEdit'),
    url(r'^viewSurvey/$', 'django_project.views.viewSurvey', name='viewSurvey'),
    url(r'^viewReports/$', 'django_project.views.viewReports', name='viewReports'),
    url(r'^managersAd/$', 'django_project.views.managersAd', name='managersAd'),

    # Kitchen staff 
    # Waiter staff 
    # url(r'^staff/', include('staff.urls')),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
