# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'dma'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='dma/home.html'),name='virvo_home'),

    url(r'editform/$', TemplateView.as_view(template_name='dma/edit_form.html'),name='editform'),
    url(r'getstationtree/$',views.get_stationtree,name='getstationtree'),
    url(r'getdmatree/$',views.get_dmatree,name='getdmatree'),

    url(r'gettree/$',views.gettree,name='gettree'),
    url(r'getchartd/$',views.getchartd,name='getchartd'),

    url(r'createdma/$',views.create_dma,name='create_dma'),
    url(r'^base/$', views.DMABaseView.as_view(),name='dma_manager_base'),
    url(r'^(?P<pk>\d+)/$', views.DMAListView.as_view(),name='dma_manager'),

    url(r'^(?P<dma_id>\d+)/daily/$', views.DailyuseView.as_view(), name="daily_use"),
    url(r'^(?P<dma_id>\d+)/daily/(?P<station_id>\d+)$', views.DailyuseDetailView.as_view(), name="daily_use_detail"),
    
    url(r'mnf/$', views.MNFView.as_view(),name='mnf'),
    url(r'^(?P<dma_id>\d+)/mapmonitor/?$', TemplateView.as_view(template_name='dma/map_monitor.html'),name='map_monitor'),

    url(r'^(?P<dma_id>\d+)/rt_curve/$', views.rt_curveView.as_view(), name="rt_curve"),
    url(r'^(?P<dma_id>\d+)/rt_data/$', views.rt_dataView.as_view(), name="rt_data"),
    url(r'^station/alarms/(?P<pk>[0-9]+)/?$', views.StationsAlarmView.as_view(), name='stations_alarms_message'),

    # 
    url(r'^station/create/?$', views.StationsCreateMangerView.as_view(), name='stations_create_manager'),
    url(r'^(?P<dma_id>\d+)/station/?$', views.StationsListMangerView.as_view(), name='stations_list_manager'),
    url(r'^station/update/(?P<pk>[0-9]+)/?$', views.StationsUpdateManagerView.as_view(), name='stations_edit_manager'),
    
]