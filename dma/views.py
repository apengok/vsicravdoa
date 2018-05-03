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

from .tables import StationsTable
from django_tables2 import RequestConfig

from django.urls import reverse_lazy
from .forms import DMABaseinfoForm,CreateDMAForm,TestForm,StationsCreateManagerForm,StationsForm
from . models import Organization,Stations,DMABaseinfo,Alarms
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

# from django.core.urlresolvers import reverse_lazy

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

def gettreenode(request):
    node = request.POST['node']
    
    orgs = Organization.objects.filter(name=node).first()
    
    table = StationsTable(Stations.objects.filter(belongto=orgs))
    
    # table = StationsTable(orgs.station_set.all())
    
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    
    vals = {'table':table}
    return render(request,'dma/table_station.html',vals)
    # return JsonResponse(vals)    

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

        {
            'name': '背景显示',
            'type': 'line',
            'data': [60,60,60,60,60,60,60],
            'areaStyle': {}
        },
        
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
        form.save()
        return super(RolesUpdateManagerView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string('dma/role_manager.html', {'role_list':role_list}))

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