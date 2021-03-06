# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'dma'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='dma/home.html'),name='virvo_home'),

    url(r'^(?P<page>.+\.html)$', views.StaticView.as_view()),

    url(r'editform/$', TemplateView.as_view(template_name='dma/edit_form.html'),name='editform'),
    url(r'getstationtree/$',views.get_stationtree,name='getstationtree'),
    url(r'getdmatree/$',views.get_dmatree,name='getdmatree'),

    url(r'gettree/$',views.gettree,name='gettree'),

    

    url(r'getchartd/$',views.getchartd,name='getchartd'),

    
    # 数据分析 日用水分析
    url(r'^daily/$', views.DailyuseView.as_view(), name="daily_use_base"),
    url(r'^(?P<dma_id>\d+)/daily/$', views.DailyuseView.as_view(), name="daily_use"),
    url(r'^(?P<dma_id>\d+)/daily/(?P<station_id>\d+)$', views.DailyuseDetailView.as_view(), name="daily_use_detail"),

    # 月用水分析
    url(r'^monthly/$', views.MonthlyuseView.as_view(), name="monthly_use_base"),
    url(r'^(?P<dma_id>\d+)/monthly/$', views.MonthlyuseView.as_view(), name="monthly_use"),
    url(r'^(?P<dma_id>\d+)/monthly/(?P<station_id>\d+)$', views.MonthlyuseDetailView.as_view(), name="monthly_use_detail"),
    
    url(r'^mnf/$', views.MNFView.as_view(),name='mnf_base'),  #夜间最小流量
    url(r'^(?P<dma_id>\d+)/mnf/$', views.MNFView.as_view(),name='mnf'),  #夜间最小流量
    url(r'^(?P<dma_id>\d+)/mnf/(?P<station_id>\d+)$', views.MNFDetailView.as_view(), name="mnf_detail"),

    # 数据监控 -实时曲线
    url(r'^h5_mapmonitor/?$', TemplateView.as_view(template_name='dma/h5_mapmonitor.html'),name='map_monitor_hplus'),
    url(r'^mapmonitor/?$', TemplateView.as_view(template_name='dma/map_monitor.html'),name='map_monitor_base'),
    url(r'^(?P<dma_id>\d+)/mapmonitor/?$', TemplateView.as_view(template_name='dma/map_monitor.html'),name='map_monitor'),
    url(r'^h5_rt_curve/$', TemplateView.as_view(template_name='dma/h5_rt_curve.html'), name="rt_curve_hplus"),
    url(r'^rt_curve/$', views.rt_curveView.as_view(), name="rt_curve_base"),
    url(r'^(?P<dma_id>\d+)/rt_curve/$', views.rt_curveView.as_view(), name="rt_curve"),
    url(r'^h5_rt_data/$', TemplateView.as_view(template_name='dma/h5_rt_data.html'), name="rt_data_hplus"),
    url(r'^rt_data/$', views.rt_dataView.as_view(), name="rt_data_base"),
    url(r'^(?P<dma_id>\d+)/rt_data/$', views.rt_dataView.as_view(), name="rt_data"),
    url(r'^station/alarms/(?P<pk>[0-9]+)/?$', views.StationsAlarmView.as_view(), name='stations_alarms_message'),



    # 基础管理 --站点管理
    url(r'^station/create/?$', views.StationsCreateMangerView.as_view(), name='stations_create_manager'),
    url(r'^station/?$', views.StationsMangerView.as_view(), name='stations_manager'),
    url(r'^(?P<dma_id>\d+)/station/?$', views.StationsListMangerView.as_view(), name='stations_list_manager'),
    url(r'^station/update/(?P<pk>[0-9]+)/?$', views.StationsUpdateManagerView.as_view(), name='stations_edit_manager'),

    # 基础管理 --dma管理
    url(r'createdma/$',views.create_dma,name='create_dma'),
    url(r'^base/$', views.DMABaseView.as_view(),name='dma_manager_base'),
    url(r'^(?P<pk>\d+)/$', views.DMAListView.as_view(),name='dma_manager'),

    # 企业管理 --角色管理
    url(r'^role/choicePermissionTree/',views.choicePermissionTree,name='choicePermissionTree'),
    url(r'^role/rolelist/',views.rolelist,name='rolelist'),
    url(r'^roles/?$', views.RolesMangerView.as_view(), name='roles_manager'),
    url(r'^roles/create/?$', views.RolesCreateMangerView.as_view(), name='role_create_manager'),
    url(r'^roles/update/(?P<pk>[0-9]+)/?$', views.RolesUpdateManagerView.as_view(), name='role_edit_manager'),

    url(r'^user/oranizationtree/',views.oranizationtree,name='oranizationtree'),
    url(r'^user/group/add/',views.groupadd,name='groupadd'),
    url(r'^user/userlist/',views.userlist,name='userlist'),
    url(r'^organ_users/?$', views.OrganUserMangerView.as_view(), name='organ_users'),#组织和用户管理
    url(r'^user/create/?$', views.UserCreateMangerView.as_view(), name='user_create_manager'),
    url(r'^user/update/(?P<pk>[0-9]+)/?$', views.UserUpdateManagerView.as_view(), name='user_edit_manager'),
    url(r'^user/assign_role/(?P<pk>[0-9]+)/?$', views.AssignRoleView.as_view(), name='assign_role'),#分配角色
    url(r'^user/auth_station/(?P<pk>[0-9]+)/?$', views.AuthStationView.as_view(), name='auth_station'),#授权站点


    # 系统管理 
    url(r'^sysconfig/personality/?$', views.PersonalityView.as_view(), name='personality'), #平台个性化配置
    
]