from django.conf.urls import patterns, include, url

from receiver import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<receiver_id>[a-zA-Z0-9]+)/$',
        views.detail, name='receiver'),
)
