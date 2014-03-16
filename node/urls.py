from django.conf.urls import patterns, url

from node import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<node_id>[a-zA-Z0-9]+)/$',
        views.detail, name='receiver'),
)
