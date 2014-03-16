from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'leakdirectory.views.home', name='home'),
    url(r'^receiver/', include('receiver.urls')),
    url(r'^node/', include('node.urls')),
    url(r'^ping$', 'leakdirectory.views.ping', name='ping'),

    url(r'^admin/', include(admin.site.urls)),
)
