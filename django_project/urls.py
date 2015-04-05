from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^menu/', include('menu.urls')),
    url(r'^games/', include('games.urls')),
	url(r'^pay/$', 'menu.views.order_summary', name='order_summary'),
    url(r'^login/$', 'django_project.views.login', name='login'),
    url(r'^auth_view/$', 'django_project.views.auth_view', name='auth_view'),
    url(r'^logout/$', 'django_project.views.logout', name='logout'),
    url(r'^loggedin/$', 'django_project.views.loggedin', name='loggedin'),
    url(r'^invalid/$', 'django_project.views.invalid', name='invalid'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
