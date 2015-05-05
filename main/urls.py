from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('main.views',
    url(r'^claim_new_graphs/$', 'claim_new_graphs', name='claim_new_graphs'),
    url(r'^get_graph/(?P<graph_id>(\d+))/$', 'get_graph', name='get_graph'),
    url(r'^add_result/(?P<graph_id>(\d+))/$', 'add_result', name='add_result'),
    url(r'^unclaim/(?P<graph_id>(\d+))/$', 'unclaim', name='unclaim'),
    url(r'^$', 'index', name='index'),
)
