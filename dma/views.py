# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages

import json
import random
from datetime import datetime

from mptt.utils import get_cached_trees
from mptt.templatetags.mptt_tags import cache_tree_children

from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission

from django.urls import reverse_lazy
from .forms import DMABaseinfoForm,CreateDMAForm,TestForm,StationsCreateManagerForm,StationsForm
from . models import Organization,Stations,DMABaseinfo,Alarms
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

# from django.core.urlresolvers import reverse_lazy


PERMISSION_TREE = [
        {"name":"数据监控","pId":"0","id":"perms_datamonitor"},
        {"name":"数据分析","pId":"0","id":"perms_datanalys"},
        {"name":"报警中心","pId":"0","id":"perms_alarmcenter"},
        {"name":"基础管理","pId":"0","id":"perms_basemanager"},
        {"name":"设备管理","pId":"0","id":"perms_devicemanager"},
        {"name":"企业管理","pId":"0","id":"perms_firmmanager"},
        {"name":"基准分析","pId":"0","id":"perms_basenalys"},
        {"name":"报表统计","pId":"0","id":"perms_reporttable"},
        {"name":"系统管理","pId":"0","id":"perms_systemconfig"},

        # 数据监控 sub
        {"name":"地图监控","pId":"perms_datamonitor","id":"mapmonitor_perms_datamonitor"},
        {"name":"可写","pId":"mapmonitor_perms_datamonitor","id":"mapmonitor_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"实时曲线","pId":"perms_datamonitor","id":"realcurlv_perms_datamonitor"},
        {"name":"可写","pId":"realcurlv_perms_datamonitor","id":"realcurlv_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"实时数据","pId":"perms_datamonitor","id":"realdata_perms_datamonitor"},
        {"name":"可写","pId":"realdata_perms_datamonitor","id":"realdata_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"DMA在线监控","pId":"perms_datamonitor","id":"dmaonline_perms_datamonitor"},
        {"name":"可写","pId":"dmaonline_perms_datamonitor","id":"dmaonline_perms_datamonitor_edit","type":"premissionEdit"},

        # 数据分析 sub
        {"name":"日用水分析","pId":"perms_datanalys","id":"dailyuse_perms_datanalys"},
        {"name":"可写","pId":"dailyuse_perms_datanalys","id":"dailyuse_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"月用水分析","pId":"perms_datanalys","id":"monthlyuse_perms_datanalys"},
        {"name":"可写","pId":"monthlyuse_perms_datanalys","id":"monthlyuse_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"DMA产销差分析","pId":"perms_datanalys","id":"dmacxc_perms_datanalys"},
        {"name":"可写","pId":"dmacxc_perms_datanalys","id":"dmacxc_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"流量分析","pId":"perms_datanalys","id":"flownalys_perms_datanalys"},
        {"name":"可写","pId":"flownalys_perms_datanalys","id":"flownalys_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"对比分析","pId":"perms_datanalys","id":"comparenalys_perms_datanalys"},
        {"name":"可写","pId":"comparenalys_perms_datanalys","id":"comparenalys_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"配表分析","pId":"perms_datanalys","id":"peibiao_perms_datanalys"},
        {"name":"可写","pId":"peibiao_perms_datanalys","id":"peibiao_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"原始数据","pId":"perms_datanalys","id":"rawdata_perms_datanalys"},
        {"name":"可写","pId":"rawdata_perms_datanalys","id":"rawdata_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"夜间最小流量","pId":"perms_datanalys","id":"mnf_perms_datanalys"},
        {"name":"可写","pId":"mnf_perms_datanalys","id":"mnf_perms_datanalys_edit","type":"premissionEdit"},

        # 报警中心 sub
        {"name":"站点报警设置","pId":"perms_alarmcenter","id":"stationalarm_perms_alarmcenter"},
        {"name":"可写","pId":"stationalarm_perms_alarmcenter","id":"stationalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        {"name":"DMA报警设置","pId":"perms_alarmcenter","id":"dmaalarm_perms_alarmcenter"},
        {"name":"可写","pId":"dmaalarm_perms_alarmcenter","id":"dmaalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        {"name":"报警查询","pId":"perms_alarmcenter","id":"queryalarm_perms_alarmcenter"},
        {"name":"可写","pId":"queryalarm_perms_alarmcenter","id":"queryalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        

        # 基础管理 sub
        {"name":"dma管理","pId":"perms_basemanager","id":"dmamanager_perms_basemanager"},
        {"name":"可写","pId":"dmamanager_perms_basemanager","id":"dmamanager_perms_basemanager_edit","type":"premissionEdit"},
        {"name":"站点管理","pId":"perms_basemanager","id":"stationmanager_perms_basemanager"},
        {"name":"可写","pId":"stationmanager_perms_basemanager","id":"stationmanager_perms_basemanager_edit","type":"premissionEdit"},

        # 企业管理 sub
        {"name":"角色管理","pId":"perms_firmmanager","id":"rolemanager_perms_firmmanager"},
        {"name":"可写","pId":"rolemanager_perms_firmmanager","id":"rolemanager_perms_firmmanager_edit","type":"premissionEdit"},
        {"name":"组织和用户管理","pId":"perms_firmmanager","id":"organusermanager_perms_basemanager"},
        {"name":"可写","pId":"organusermanager_perms_basemanager","id":"organusermanager_perms_basemanager_edit","type":"premissionEdit"},

        # 设备管理 sub
        {"name":"表具管理","pId":"perms_devicemanager","id":"meters_perms_devicemanager"},
        {"name":"可写","pId":"meters_perms_devicemanager","id":"meters_perms_devicemanager_edit","type":"premissionEdit"},
        {"name":"SIM卡管理","pId":"perms_devicemanager","id":"simcard_perms_devicemanager"},
        {"name":"可写","pId":"simcard_perms_devicemanager","id":"simcard_perms_devicemanager_edit","type":"premissionEdit"},
        {"name":"参数指令","pId":"perms_devicemanager","id":"params_perms_devicemanager"},
        {"name":"可写","pId":"params_perms_devicemanager","id":"params_perms_devicemanager_edit","type":"premissionEdit"},
        
        # 基准分析 sub
        {"name":"DMA基准分析","pId":"perms_basenalys","id":"dma_perms_basenalys"},
        {"name":"可写","pId":"dma_perms_basenalys","id":"dma_perms_basenalys_edit","type":"premissionEdit"},
        {"name":"最小流量分析","pId":"perms_basenalys","id":"mf_perms_basenalys"},
        {"name":"可写","pId":"mf_perms_basenalys","id":"mf_perms_basenalys_edit","type":"premissionEdit"},
        {"name":"日基准流量分析","pId":"perms_basenalys","id":"day_perms_basenalys"},
        {"name":"可写","pId":"day_perms_basenalys","id":"day_perms_basenalys_edit","type":"premissionEdit"},
        
        # 统计报表 sub
        {"name":"日志查询","pId":"perms_reporttable","id":"querylog_perms_reporttable"},
        {"name":"可写","pId":"querylog_perms_reporttable","id":"querylog_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"报警报表","pId":"perms_reporttable","id":"alarm_perms_reporttable"},
        {"name":"可写","pId":"alarm_perms_reporttable","id":"alarm_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"DMA统计报表","pId":"perms_reporttable","id":"dmastatics_perms_reporttable"},
        {"name":"可写","pId":"dmastatics_perms_reporttable","id":"dmastatics_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"大用户报表","pId":"perms_reporttable","id":"biguser_perms_reporttable"},
        {"name":"可写","pId":"biguser_perms_reporttable","id":"biguser_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"流量报表","pId":"perms_reporttable","id":"flows_perms_reporttable"},
        {"name":"可写","pId":"flows_perms_reporttable","id":"flows_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"水量报表","pId":"perms_reporttable","id":"waters_perms_reporttable"},
        {"name":"可写","pId":"waters_perms_reporttable","id":"waters_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"表务报表","pId":"perms_reporttable","id":"biaowu_perms_reporttable"},
        {"name":"可写","pId":"biaowu_perms_reporttable","id":"biaowu_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"大数据报表","pId":"perms_reporttable","id":"bigdata_perms_reporttable"},
        {"name":"可写","pId":"bigdata_perms_reporttable","id":"bigdata_perms_reporttable_edit","type":"premissionEdit"},
        


        
        # 系统管理 sub
        {"name":"平台个性化管理","pId":"perms_systemconfig","id":"personality_perms_systemconfig"},
        {"name":"可写","pId":"personality_perms_systemconfig","id":"personality_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"系统设置","pId":"perms_systemconfig","id":"system_perms_systemconfig"},
        {"name":"可写","pId":"system_perms_systemconfig","id":"system_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"转发设置","pId":"perms_systemconfig","id":"retransit_perms_systemconfig"},
        {"name":"可写","pId":"retransit_perms_systemconfig","id":"retransit_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"图标配置","pId":"perms_systemconfig","id":"icons_perms_systemconfig"},
        {"name":"可写","pId":"icons_perms_systemconfig","id":"icons_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"日志查询","pId":"perms_systemconfig","id":"querylog_perms_systemconfig"},
        {"name":"可写","pId":"querylog_perms_systemconfig","id":"querylog_perms_systemconfig_edit","type":"premissionEdit"},
    ]


def error_404(request):
    return render(request,"404.html",{})

def error_500(request):
    return render(request,"500.html",{})

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


class StaticView(TemplateView):
    def get(self, request, page, *args, **kwargs):
        self.template_name = page
        print(page)
        response = super(StaticView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise Http404()

def recursive_node_to_dict(node,url_cat):
    result = {
        'id':node.pk,
        'name': node.name,
        'open':'true',
        'url':'/dma/{}/{}'.format(node.pk,url_cat),
        'target':'_self',
        'icon':"/static/virvo/images/站点管理/u842_1.png",
        'class':"J_menuItem",
    }
    
    children = [recursive_node_to_dict(c,url_cat) for c in node.get_children()]
    
    # get each node's station if exist
    if url_cat != '':
        try:
            sats = node.station.all()
            for s in sats:
                children.append({
                    'name':s.station_name,
                    'url':'/dma/{}/{}/{}'.format(node.pk,url_cat,s.id),
                    'target':'_self',
                    'icon':"/static/virvo/images/u3672.png",
                    # 'class':"J_menuItem",
                })
            # children.append({'name':})
        except:
            pass

    if children:
        result['children'] = children
    
    return result

def get_stationtree(request):
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,'station'))

    
    # print json.dumps(dicts, indent=4)

    
    
    return JsonResponse({'trees':dicts})


def get_dmatree(request):
    # page_name = request.GET.get('page_name') or ''
    '''只获取分区结构，不获取站点信息'''
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,''))

    virvo_tree = [{'name':'威尔沃','open':'true','children':dicts}]
    return JsonResponse({'trees':virvo_tree})
    
    # return JsonResponse({'trees':dicts})

def gettree(request):
    page_name = request.GET.get('page_name') or ''
    print(page_name)
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,page_name))

    
    # print json.dumps(dicts, indent=4)

    virvo_tree = [{'name':'威尔沃','open':'true','children':dicts}]
    return JsonResponse({'trees':virvo_tree})
    # return JsonResponse({'trees':dicts})

def choicePermissionTree(request):

    roleid = request.POST.get('roleId') or -1

    if roleid < 0:
        return HttpResponse(json.dumps(PERMISSION_TREE))

    
    instance = MyRoles.objects.get(id=roleid)
    permissiontree = instance.permissionTree
    ctree = PERMISSION_TREE[:]

    print(permissiontree)
    
    if len(permissiontree) > 0:
        ptree = json.loads(permissiontree)
        

        for pt in ptree:
            nodeid = pt['id']
            node_edit = '{}_edit'.format(nodeid)
            p_edit = pt['edit']

            node = [n for n in ctree if n['id']==nodeid][0]
            if p_edit:
                node['checked'] = 'true'
                node_sub = [n for n in ctree if n['id']==node_edit][0]
                node_sub['checked'] = 'true'
            else:
                node['checked'] = 'true'
            
                


    

    # return JsonResponse(dicts,safe=False)
    return HttpResponse(json.dumps(ctree))

from django.core import serializers

def rolelist(request):

    draw = int(request.GET.get('draw', None)[0])
    length = int(request.GET.get('length', None)[0])
    start = int(request.GET.get('start', None)[0])
    search_value = request.GET.get('search[value]', None)
    # order_column = request.GET.get('order[0][column]', None)[0]
    # order = request.GET.get('order[0][dir]', None)[0]

    print('get rolelist:',draw,length,start,search_value)
    rolel = MyRoles.objects.all()
    data = []
    for r in rolel:
        data.append({'id':r.pk,'name':r.name,'notes':r.notes})
    # json = serializers.serialize('json', rolel)
    output = [{"draw":draw,"recordsTotal":rolel.count(),"length":length,"start":start,"records":data}]

    result = dict()
    result['data'] = data
    result['draw'] = draw
    result['recordsTotal'] = rolel.count()
    # result['recordsFiltered'] = music['count']
    
    return HttpResponse(json.dumps(result))
    # return JsonResponse(output,safe=False)

def getchartd(request):
    data = [random.randint(2,13), 20, 6, 10, 20, 30]

    return JsonResponse({'data':data})  

class rt_curveView(TemplateView):
    """docstring for rt_curveView"""
    template_name = 'dma/rt_curve.html'

    def get_context_data(self, *args, **kwargs):
        context = super(rt_curveView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '实时曲线'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        stations_list = Stations.objects.filter(belongto=orgs)
        context['station_list'] = stations_list

        for station in stations_list:
            pass

        rt_dataset = []
        def curse_data(s):
            result = {
                'chart_id':'chart_{}'.format(s.station_name),
                'data':[1,2,3,4,5,6],
                'station_name':s.station_name,
                'caliber':s.caliber
            }
            return result

        jsd=[]
        for s in stations_list:
            rt_dataset.append(curse_data(s) )
            jsd.append({'data':[random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13), random.randint(2,13)],
                'name':'chart_{}'.format(s.station_name)})
        
        context['rt_dataset'] = rt_dataset
        dum=json.dumps(jsd)
        # print(type(dum),dum)

        data = [random.randint(2,13), 20, 6, 10, 20, 30]
        context['jsd'] = json.dumps(jsd)

        

        return context
        

class rt_dataView(TemplateView):
    """docstring for rt_curveView"""
    template_name = 'dma/rt_data.html'

    def get_context_data(self, *args, **kwargs):
        context = super(rt_dataView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '实时数据'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        stations_list = Stations.objects.filter(belongto=orgs)
        context['stations_list'] = stations_list

        

        return context

"""
夜间最小流量
"""

def chart_mnf():

    options = {}

    options['tooltip'] = {}

    # options['backgroundColor'] = 'rgba(128, 128, 128, 0.5)'
    options['animation'] = 'false'
    options['legend'] = {
        'data':['MNF','最大流量','平均流量','背景漏损','压力曲线',] 
    }
    options['xAxis'] = {
        'splitLine': {'show': 'true'},
        'data':[str(x) for x in range(100)]
    }
    options['yAxis'] = {
        'name': 'm3/h'
    }
    today_curve = [5 for x in range(100)]
    options['series'] = [
        {
            'name': 'MNF',
            'type': 'line',
            'smooth':'true',
            # 'showSymbol': 'false',
            'data': today_curve
        },
        {
            'name': '最大流量',
            'type': 'line',
            'smooth':'true',
            'data': [28 for x in range(100)]
        },
        {
            'name':'压力曲线',
            'type':'line',
            'smooth':'true',
            'data':[random.randint(20,50) for x in range(100)]
        },
        {
            'name': '平均流量',
            'type': 'line',
            'smooth':'true',
            'data': [15 for x in range(100)]
        },
        {
            'name':'背景漏损',
            'type':'line',
            'smooth':'true',
            'data':[random.randint(15,30) for x in range(100)]
        },
        
        
    ]

    return json.dumps(options)

class MNFView(TemplateView):
    """docstring for StationsView"""

    
    template_name = 'dma/mnf.html'
    
    def get_context_data(self, *args, **kwargs):
        
        context = super(MNFView, self).get_context_data(*args, **kwargs)

        context['page_title'] = '夜间最小流量'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station = Stations.objects.filter(belongto=orgs).first()
        context['station'] = station

        context['options'] = chart_mnf()
        
                
        return context                 



'''夜间最小流量 站点显示'''
class MNFDetailView(TemplateView):
    """docstring for MonthlyuseDetailView"""
    template_name = 'dma/mnf.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MNFDetailView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '夜间最小流量'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station_id = self.kwargs.get('station_id')
        station = Stations.objects.get(id=station_id)
        
        context['station'] = station

        context['options'] = chart_mnf()

        return context          


def create_dma(request):
    
    
    dma_form = CreateDMAForm(request.POST or None)

    if dma_form.is_valid():
        # parent = Organization.objects.first()
        orgs = Organization.objects.create(name=dma_form.cleaned_data.get('dma_name'),parent=None)

        obj = DMABaseinfo.objects.create(
            dma_no=dma_form.cleaned_data.get('dma_no'),
            dma=orgs,
            create_date = dma_form.cleaned_data.get('create_date')
        )
        # return HttpResponseRedirect("/dma/dma/1/")
    if dma_form.errors:
        print(dma_form.errors)
    response = {'status': 1, 'message': "Ok",'url':"/dma/{}".format(obj.pk)} # for ok
    return HttpResponse(json.dumps(response), content_type='application/json')
    # return render(request,'dma/dma_manager.html',{'dma_form':dma_form})
    # return redirect(reverse_lazy('dma:dma_manager',kwargs={'pk':obj.pk}))


class DMABaseView(TemplateView):
    template_name = 'dma/dma_manager.html'
    # form_class = DMABaseinfoForm
    model = DMABaseinfo
    # success_url = '/dma/dma/1'

    # def get_queryset(self):
        
    #     return DMABaseinfo.objects.all()
    #     # return get_object_or_404(DMABaseinfo)

    # def get_form_kwargs(self):
    #     print (self.kwargs)
    #     kwargs = super(DMABaseView, self).get_form_kwargs()
    #     # kwargs['user'] = self.request.user
    #     print (kwargs)
    #     return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(DMABaseView, self).get_context_data(*args, **kwargs)
        context['title'] = 'DMA 管理'
        context['page_title'] = 'DMA管理'
        try:
            pk = self.kwargs.get('pk')
            orgs = Organization.objects.get(pk=pk)
            context['station_list'] = Stations.objects.filter(belongto=orgs)
        except:
            pass

        create_dma_form = CreateDMAForm()
        context['dma_form'] = create_dma_form
        context['form'] = DMABaseinfoForm()

        return context

    


class DMAListView(UpdateView):
    template_name = 'dma/dma_manager.html'
    form_class = DMABaseinfoForm
    model = DMABaseinfo
    # success_url = '/dma/dma/1'

    def get_queryset(self):
        
        return DMABaseinfo.objects.all()
        # return get_object_or_404(DMABaseinfo)

    def get_form_kwargs(self):
        print (self.kwargs)
        kwargs = super(DMAListView, self).get_form_kwargs()
        # kwargs['user'] = self.request.user
        print (kwargs)
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(DMAListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'DMA 管理'
        context['page_title'] = 'DMA 管理'
        try:
            pk = self.kwargs.get('pk')
            orgs = Organization.objects.get(pk=pk)
            context['station_list'] = Stations.objects.filter(belongto=orgs)
        except:
            pass

        create_dma_form = CreateDMAForm()
        context['dma_form'] = create_dma_form

        return context

    def form_valid(self,form):
        orgs = form.cleaned_data.get('orgs')
        # print(orgs,type(orgs))
        # print (form.instance)
        # print(form.instance.dma)
        # print(form.instance.dma.parent)
        form.instance.dma.parent = orgs
        form.instance.dma.save()

        return super(DMAListView,self).form_valid(form)





"""
Stations creation, manager
"""
class StationsCreateMangerView(CreateView):
    model = Stations
    template_name = 'dma/stations_create_manager.html'
    form_class = StationsCreateManagerForm
    # success_url = reverse_lazy('stations_list_manager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(StationsCreateMangerView, self).dispatch(*args, **kwargs)


"""
Stationss , manager
"""
class StationsMangerView(ListView):
    model = Stations
    template_name = 'dma/stations_list_manager.html'

    
    def get_context_data(self,**kwargs):
        context = super(StationsMangerView,self).get_context_data(**kwargs)

        context['object_list'] = Stations.objects.all()
        context['page_title'] = '站点管理'

        return context


"""
Stationss list, manager
"""
class StationsListMangerView(ListView):
    model = Stations
    template_name = 'dma/stations_list_manager.html'

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        print('when call dispatch..?')
        return super(StationsListMangerView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # user = self.request.user
        # manager_group = Group.objects.get(name=settings.BANCOAUSILI_MANAGER_GROUP)
        # if manager_group in user.groups.all():
        #     manager = Manager.objects.get(user=user)
        #     return Stations.objects.filter(centre__in=manager.centres.all())
        # else:
        #     return Stations.objects.all()
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        # print(pk,orgs)
        return Stations.objects.filter(belongto=orgs)

    def get_context_data(self,**kwargs):
        context = super(StationsListMangerView,self).get_context_data(**kwargs)
        context['page_title'] = '站点管理'

        return context


"""
Stations edit, manager
"""
class StationsUpdateManagerView(UpdateView):
    model = Stations
    form_class = StationsForm
    template_name = 'dma/stations_edit_manager.html'

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.stations_id = kwargs['pk']
        return super(StationsUpdateManagerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        stations = Stations.objects.get(id=self.stations_id)
        return HttpResponse(render_to_string('dma/stations_edit_manager_success.html', {'stations': stations}))

    def get_context_data(self, **kwargs):
        context = super(StationsUpdateManagerView, self).get_context_data(**kwargs)
        context['page_title'] = '修改站点'
        return context


class StationsAlarmView(DetailView):
    """docstring for StationsAlarmView"""
    template_name = 'dma/alarminfo.html'


    def get_queryset(self):
        pk = self.kwargs.get('pk')

        return Alarms.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(StationsAlarmView, self).get_context_data(**kwargs)
        context['page_title'] = '报警信息'

        pk = self.kwargs.get('pk')
        print(pk)

        qs = Stations.objects.get(id=pk)

        context['qs'] = qs.alarms_set.all()
        return context

'''echarts option 配置'''
def chart_options():

    options = {}

    options['tooltip'] = {}

    # options['backgroundColor'] = 'rgba(128, 128, 128, 0.5)'
    options['animation'] = 'false'
    options['legend'] = {
        'data':['今日曲线','昨日曲线','2018-01-23','2018-02-23','压力曲线','当日柱状图',] 
    }
    options['xAxis'] = {
        'splitLine': {'show': 'true'},
        'data':[str(x) for x in range(1,30)]
    }
    options['yAxis'] = {
        'name': 'm3/h'
    }
    today_curve = [random.randint(40,60) for x in range(30)]
    options['series'] = [
        {
            'name': '今日曲线',
            'type': 'line',
            'smooth':'true',
            # 'showSymbol': 'false',
            'data': today_curve
        },
        {
            'name': '昨日曲线',
            'type': 'line',
            'smooth':'true',
            'data': [random.randint(40,60) for x in range(30)]
        },
        {
            'name':'压力曲线',
            'type':'line',
            'smooth':'true',
            'data':[random.randint(40,60) for x in range(30)]
        },
        {
            'name': '2018-01-23',
            'type': 'line',
            'smooth':'true',
            'data': [random.randint(40,60) for x in range(30)]
        },
        {
            'name':'2018-02-23',
            'type':'line',
            'smooth':'true',
            'data':[random.randint(40,60) for x in range(30)]
        },
        {
            'name': '当日柱状图',
            'type': 'bar',
            'data': today_curve
        },

        # {
        #     'name': '背景显示',
        #     'type': 'line',
        #     'data': [60,60,60,60,60,60,60],
        #     'areaStyle': {}
        # },
        
    ]

    return json.dumps(options)

'''日用水分析'''
class DailyuseView(TemplateView):
    """docstring for DailyuseView"""
    template_name = 'dma/daily_use.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DailyuseView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '日用水分析'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station = Stations.objects.filter(belongto=orgs).first()
        context['station'] = station

        context['options'] = chart_options()

        return context        

'''日用水分析 站点显示'''
class DailyuseDetailView(TemplateView):
    """docstring for DailyuseDetailView"""
    template_name = 'dma/daily_use.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DailyuseDetailView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '日用水分析'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station_id = self.kwargs.get('station_id')
        station = Stations.objects.get(id=station_id)
        
        context['station'] = station

        context['options'] = chart_options()

        return context            


'''月用水分析'''
class MonthlyuseView(TemplateView):
    """docstring for MonthlyuseView"""
    template_name = 'dma/monthly_use.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MonthlyuseView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '月用水分析'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station = Stations.objects.filter(belongto=orgs).first()
        context['station'] = station

        context['options'] = chart_options()

        return context        

'''月用水分析 站点显示'''
class MonthlyuseDetailView(TemplateView):
    """docstring for MonthlyuseDetailView"""
    template_name = 'dma/monthly_use.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MonthlyuseDetailView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '月用水分析'
        dma_id = self.kwargs.get('dma_id') or 1
        orgs = Organization.objects.get(pk=dma_id)
        station_id = self.kwargs.get('station_id')
        station = Stations.objects.get(id=station_id)
        
        context['station'] = station

        context['options'] = chart_options()

        return context                    


# 角色管理
class RolesMangerView(TemplateView):
    template_name = 'dma/role_manager.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RolesMangerView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '角色管理'
        context['role_list'] = MyRoles.objects.all()

        return context  

    

"""
Roles creation, manager
"""
class RolesCreateMangerView(CreateView):
    model = MyRoles
    template_name = 'dma/role_create.html'
    form_class = RoleCreateForm
    success_url = reverse_lazy('dma:roles_manager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(RolesCreateMangerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('role create here?:',self.request.POST)
        # print(form)
        # do something
        permissiontree = form.cleaned_data.get('permissionTree')
        ptree = json.loads(permissiontree)
        instance = form.save()
        # old_permissions = instance.permissions.all()
        # instance.permissions.clear()

        for pt in ptree:
            pname = pt['id']
            p_edit = pt['edit']
            perms = Permission.objects.get(codename=pname)
            
            if p_edit:
                node_edit = '{}_edit'.format(pname)
                perms_edit = Permission.objects.get(codename=node_edit)
                instance.permissions.add(perms)
                instance.permissions.add(perms_edit)


        return super(RolesCreateMangerView,self).form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     print('do you been here 123?')
    #     print (request.POST)
    #     print(kwargs)

    #     form = self.get_form()
    #     instance = form.save(commit=False)
    #     print(form.cleaned_data['permissionTree'])
        
    #     form.save()
            
        

    #     # return super(AssignRoleView,self).render_to_response(context)
    #     return redirect(reverse_lazy('dma:roles_manager'))



"""
Roles edit, manager
"""
class RolesUpdateManagerView(UpdateView):
    model = MyRoles
    form_class = MyRolesForm
    template_name = 'dma/role_edit_manager.html'
    success_url = reverse_lazy('dma:roles_manager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.role_id = kwargs['pk']
        return super(RolesUpdateManagerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('role update here?:',self.request.POST)
        # print(form)
        # do something
        permissiontree = form.cleaned_data.get('permissionTree')
        ptree = json.loads(permissiontree)
        instance = self.object
        old_permissions = instance.permissions.all()
        instance.permissions.clear()

        for pt in ptree:
            pname = pt['id']
            p_edit = pt['edit']
            perms = Permission.objects.get(codename=pname)
            
            if p_edit:
                node_edit = '{}_edit'.format(pname)
                perms_edit = Permission.objects.get(codename=node_edit)
                instance.permissions.add(perms)
                instance.permissions.add(perms_edit)
                

        return super(RolesUpdateManagerView,self).form_valid(form)
        

    # def post(self,request,*args,**kwargs):
    #     print('role update ?')
    #     print (request.POST)
    #     print(kwargs)

    #     form = self.get_form()
    #     if form.is_valid():
    #         print(form)
    #         print(form.cleaned_data['permissionTree'])
    #         # instance = form.save(commit=False)
    #         return self.form_valid(form)
            
    #     else:
    #         print(form.errors)
            
            
        

    #     # return super(AssignRoleView,self).render_to_response(context)
    #     return redirect(reverse_lazy('dma:roles_manager'))

    def get_context_data(self, **kwargs):
        context = super(RolesUpdateManagerView, self).get_context_data(**kwargs)
        context['page_title'] = '修改角色'
        return context


"""
组织和用户管理
"""
class OrganUserMangerView(TemplateView):
    template_name = 'dma/organ_user_manager.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrganUserMangerView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '组织和用户管理'

        context['user_list'] = User.objects.all()
        

        return context  


"""
User creation, manager
"""
class UserCreateMangerView(CreateView):
    model = User
    template_name = 'dma/user_create.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dma:organ_users');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(UserCreateMangerView, self).dispatch(*args, **kwargs)


"""
User edit, manager
"""
class UserUpdateManagerView(UpdateView):
    model = User
    form_class = UserDetailChangeForm
    template_name = 'dma/user_edit_manager.html'
    success_url = reverse_lazy('dma:organ_users')

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.user_id = kwargs['pk']
        return super(UserUpdateManagerView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        return super(UserUpdateManagerView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string('dma/role_manager.html', {'role_list':role_list}))

    def get_context_data(self, **kwargs):
        context = super(UserUpdateManagerView, self).get_context_data(**kwargs)
        context['page_title'] = '修改用户'
        return context


class AssignRoleView(TemplateView):
    """docstring for AssignRoleView"""
    template_name = 'dma/assign_role.html'
        
    def get_context_data(self, **kwargs):
        context = super(AssignRoleView, self).get_context_data(**kwargs)
        context['page_title'] = '分配角色'
        context['role_list'] = MyRoles.objects.all()
        pk = kwargs['pk']
        context['object_id'] = pk
        context['user'] = User.objects.get(pk=pk)
        return context

    def post(self,request,*args,**kwargs):
        print (request.POST)
        print(kwargs)
        context = self.get_context_data(**kwargs)

        role = request.POST.get("checks[]")
        user = context['user']
        # user.Role = role
        group = MyRoles.objects.filter(name__iexact=role).first()
        print(group)
        user.groups.add(group)
        user.save()

        # return super(AssignRoleView,self).render_to_response(context)
        return redirect(reverse_lazy('dma:organ_users'))



class AuthStationView(TemplateView):
    """docstring for AuthStationView"""
    template_name = 'dma/auth_station.html'
        
    def get_context_data(self, **kwargs):
        context = super(AuthStationView, self).get_context_data(**kwargs)
        context['page_title'] = '分配角色'
        return context        


class PersonalityView(TemplateView):
    """docstring for AuthStationView"""
    template_name = 'dma/personality.html'
        
    def get_context_data(self, **kwargs):
        context = super(PersonalityView, self).get_context_data(**kwargs)
        context['page_title'] = '个性化设置'
        return context       