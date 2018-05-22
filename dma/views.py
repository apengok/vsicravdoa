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

    ctree = [{"name":"信息配置","pId":"0","id":"b46de828-6a8e-11e6-8b77-86f30ca893d3"},{"name":"企业管理","pId":"0","id":"e8d23fb4-64a9-44c5-9ed6-4836d7c2f9uj"},{"name":"监控对象","pId":"0","id":"96327be0-6aab-11e6-8b77-86f30ca893d3"},{"name":"设备管理","pId":"0","id":"96327f6e-6aab-11e6-8b77-86f30ca893d3"},{"name":"监控管理","pId":"0","id":"84113afa-df07-4247-8666-f164a7acbefa"},{"name":"报警中心","pId":"0","id":"9122dbfa-6a8c-11e6-8b77-86f30ca893d3"},{"name":"应用管理","pId":"0","id":"9f5ea704-6a90-11e6-8b77-86f30ca893d3"},{"name":"能源管理","pId":"0","id":"fc87ab62-7d62-11e6-ae22-56b6b6499611"},{"name":"信息列表","pId":"b46de828-6a8e-11e6-8b77-86f30ca893d3","id":"b46dec1a-6a8e-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"b46dec1a-6a8e-11e6-8b77-86f30ca893d3","id":"b46dec1a-6a8e-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"系统管理","pId":"0","id":"f9c65d06-f40e-11e6-bc64-92361f002671"},{"name":"报表管理","pId":"0","id":"f9c65d06-f40e-11e6-bc64-92361f006689"},{"name":"山西报表","pId":"0","id":"eac86c12-25a0-11e8-b467-0ed5f89f718b"},{"chkDisabled":"true","name":"组织与用户管理","pId":"e8d23fb4-64a9-44c5-9ed6-4836d7c2f9uj","id":"186a9eac-855c-4c52-995c-8af38bd2453b"},{"chkDisabled":"true","name":"可写","pId":"186a9eac-855c-4c52-995c-8af38bd2453b","id":"186a9eac-855c-4c52-995c-8af38bd2453bedit","type":"premissionEdit"},{"name":"分组管理","pId":"e8d23fb4-64a9-44c5-9ed6-4836d7c2f9uj","id":"ad23fb4-64a9-623c-9ed6-4836d7c2f9uj"},{"name":"可写","pId":"ad23fb4-64a9-623c-9ed6-4836d7c2f9uj","id":"ad23fb4-64a9-623c-9ed6-4836d7c2f9ujedit","type":"premissionEdit"},{"chkDisabled":"true","name":"角色管理","pId":"e8d23fb4-64a9-44c5-9ed6-4836d7c2f9uj","id":"a9f91a9a-f29a-4380-8751-16e1af38c31f"},{"chkDisabled":"true","name":"可写","pId":"a9f91a9a-f29a-4380-8751-16e1af38c31f","id":"a9f91a9a-f29a-4380-8751-16e1af38c31fedit","type":"premissionEdit"},{"name":"从业人员管理","pId":"e8d23fb4-64a9-44c5-9ed6-4836d7c2f9uj","id":"af69c3e3-037c-4e5e-ba23-ba04bc06ab2f"},{"name":"可写","pId":"af69c3e3-037c-4e5e-ba23-ba04bc06ab2f","id":"af69c3e3-037c-4e5e-ba23-ba04bc06ab2fedit","type":"premissionEdit"},{"name":"车辆信息","pId":"96327be0-6aab-11e6-8b77-86f30ca893d3","id":"963283ce-6aab-11e6-8b77-86f30ca893d3"},{"name":"人员信息","pId":"96327be0-6aab-11e6-8b77-86f30ca893d3","id":"963285e0-6aab-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"963285e0-6aab-11e6-8b77-86f30ca893d3","id":"963285e0-6aab-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"物品信息","pId":"96327be0-6aab-11e6-8b77-86f30ca893d3","id":"963289c8-6aab-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"963289c8-6aab-11e6-8b77-86f30ca893d3","id":"963289c8-6aab-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"终端管理","pId":"96327f6e-6aab-11e6-8b77-86f30ca893d3","id":"238286ce-6aad-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"238286ce-6aad-11e6-8b77-86f30ca893d3","id":"238286ce-6aad-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"SIM卡管理","pId":"96327f6e-6aab-11e6-8b77-86f30ca893d3","id":"23828bb0-6aad-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"23828bb0-6aad-11e6-8b77-86f30ca893d3","id":"23828bb0-6aad-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"报警参数设置","pId":"9122dbfa-6a8c-11e6-8b77-86f30ca893d3","id":"026607f0-6a8e-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"026607f0-6a8e-11e6-8b77-86f30ca893d3","id":"026607f0-6a8e-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"报警查询","pId":"9122dbfa-6a8c-11e6-8b77-86f30ca893d3","id":"0266048a-6a8e-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"0266048a-6a8e-11e6-8b77-86f30ca893d3","id":"0266048a-6a8e-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"传感器配置","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"b296585a-339c-11e7-a919-92ebcb67fe33"},{"name":"油量管理","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"a03ff712-9755-11e6-ae22-56b6b6499611"},{"name":"油耗管理","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"fc87a5b8-7d62-11e6-ae22-56b6b6499611"},{"name":"里程监测","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"80f558ba-391d-11e7-a919-92ebcb67fe33"},{"name":"工时管理","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"81649806-838d-11e6-ae22-56b6b6499611"},{"name":"开关信号监测","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"7d561544-5661-11e7-907b-a6006ad3dba0"},{"name":"温度监测","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"32e16952-622b-11e7-907b-a6006ad3dba0"},{"name":"湿度监测","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"32e16bc8-622b-11e7-907b-a6006ad3dba0"},{"name":"正反转管理","pId":"9f5ea704-6a90-11e6-8b77-86f30ca893d3","id":"32e16f92-622b-11e7-907b-a6006ad3dba0"},{"name":"移动源基础管理","pId":"fc87ab62-7d62-11e6-ae22-56b6b6499611","id":"fc87ab62-7d62-11e6-lb10-56b6b6499611"},{"name":"可写","pId":"fc87ab62-7d62-11e6-lb10-56b6b6499611","id":"fc87ab62-7d62-11e6-lb10-56b6b6499611edit","type":"premissionEdit"},{"name":"移动源基准管理","pId":"fc87ab62-7d62-11e6-ae22-56b6b6499611","id":"fc87ab62-7d62-11e6-lb13-56b6b6499611"},{"name":"移动源能耗报表","pId":"fc87ab62-7d62-11e6-ae22-56b6b6499611","id":"fc87ade2-7d62-11e6-lb02-56b6b6499611"},{"name":"808平台转发配置","pId":"f9c65d06-f40e-11e6-bc64-92361f002671","id":"f9c660e4-f40e-11e6-bc64-92361f002671"},{"name":"转发平台连接","pId":"f9c6629c-f40e-11e6-bc64-92368f002671","id":"f9c6629c-f40e-11e6-bc64-92361f002671"},{"name":"可写","pId":"f9c6629c-f40e-11e6-bc64-92361f002671","id":"f9c6629c-f40e-11e6-bc64-92361f002671edit","type":"premissionEdit"},{"name":"809平台转发配置","pId":"f9c65d06-f40e-11e6-bc64-92361f002671","id":"f9c6629c-f40e-11e6-bc64-92368f002671"},{"name":"对讲平台配置","pId":"f9c65d06-f40e-11e6-bc64-92361f002671","id":"6f720d14-095b-11e7-93ae-92361f002671"},{"name":"平台个性化配置","pId":"f9c65d06-f40e-11e6-bc64-92361f002671","id":"b2b25f96-3a09-11e7-a919-92ebcb67fe33"},{"name":"日志查询","pId":"f9c65d06-f40e-11e6-bc64-92361f002671","id":"f89767c1-6396-4819-8434-07f0229c8a83"},{"name":"可写","pId":"f89767c1-6396-4819-8434-07f0229c8a83","id":"f89767c1-6396-4819-8434-07f0229c8a83edit","type":"premissionEdit"},{"name":"大数据报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"f9c65d06-f40e-11e6-bc64-92361f668901"},{"name":"可写","pId":"f9c65d06-f40e-11e6-bc64-92361f668901","id":"f9c65d06-f40e-11e6-bc64-92361f668901edit","type":"premissionEdit"},{"name":"行驶里程报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9aa9af12-1510-11e7-93ae-92361f002671"},{"name":"可写","pId":"9aa9af12-1510-11e7-93ae-92361f002671","id":"9aa9af12-1510-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"停驶报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9e503d5e-2963-11e7-93ae-92361f002671"},{"name":"可写","pId":"9e503d5e-2963-11e7-93ae-92361f002671","id":"9e503d5e-2963-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"上线率报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9aa9b110-1510-11e7-93ae-92361f002671"},{"name":"可写","pId":"9aa9b110-1510-11e7-93ae-92361f002671","id":"9aa9b110-1510-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"报警信息报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9aa9aba2-1510-11e7-93ae-92361f002671"},{"name":"可写","pId":"9aa9aba2-1510-11e7-93ae-92361f002671","id":"9aa9aba2-1510-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"超速报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9e503aca-2963-11e7-93ae-92361f002671"},{"name":"可写","pId":"9e503aca-2963-11e7-93ae-92361f002671","id":"9e503aca-2963-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"超速报警报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"9e503e62-2963-11e7-93ae-92361f002671"},{"name":"可写","pId":"9e503e62-2963-11e7-93ae-92361f002671","id":"9e503e62-2963-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"工时报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"81649b30-838d-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"81649b30-838d-11e6-ae22-56b6b6499611","id":"81649b30-838d-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"油量报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"304b30c4-a00c-11e6-80f5-76304dec7eb7"},{"name":"可写","pId":"304b30c4-a00c-11e6-80f5-76304dec7eb7","id":"304b30c4-a00c-11e6-80f5-76304dec7eb7edit","type":"premissionEdit"},{"name":"油耗报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"fc87aa90-7d62-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"fc87aa90-7d62-11e6-ae22-56b6b6499611","id":"fc87aa90-7d62-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"里程报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"f8bbe8a8-281f-49e1-ad34-7a111f9115e0"},{"name":"可写","pId":"f8bbe8a8-281f-49e1-ad34-7a111f9115e0","id":"f8bbe8a8-281f-49e1-ad34-7a111f9115e0edit","type":"premissionEdit"},{"name":"温度报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"a1775bd8-13db-45e8-8514-d48664bec8f6"},{"name":"可写","pId":"a1775bd8-13db-45e8-8514-d48664bec8f6","id":"a1775bd8-13db-45e8-8514-d48664bec8f6edit","type":"premissionEdit"},{"name":"湿度报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"a8141c4a-6549-45d5-9a82-5fc9ffa5996a"},{"name":"可写","pId":"a8141c4a-6549-45d5-9a82-5fc9ffa5996a","id":"a8141c4a-6549-45d5-9a82-5fc9ffa5996aedit","type":"premissionEdit"},{"name":"正反转报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"56bf8dee-34c0-4064-acad-a8688ffd2430"},{"name":"可写","pId":"56bf8dee-34c0-4064-acad-a8688ffd2430","id":"56bf8dee-34c0-4064-acad-a8688ffd2430edit","type":"premissionEdit"},{"name":"多媒体管理","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"0d8162bb-4722-48bc-b321-456dbbd5540b"},{"name":"可写","pId":"0d8162bb-4722-48bc-b321-456dbbd5540b","id":"0d8162bb-4722-48bc-b321-456dbbd5540bedit","type":"premissionEdit"},{"name":"音视频日志查询","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"43b4dc62-3315-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"43b4dc62-3315-11e8-b467-0ed5f89f718b","id":"43b4dc62-3315-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"音视频流量报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"edf5a182-eb7d-11e7-8c3f-9a214cf093ae"},{"name":"可写","pId":"edf5a182-eb7d-11e7-8c3f-9a214cf093ae","id":"edf5a182-eb7d-11e7-8c3f-9a214cf093aeedit","type":"premissionEdit"},{"name":"离线查询报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"7d515b16-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d515b16-25a1-11e8-b467-0ed5f89f718b","id":"7d515b16-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"客流量报表","pId":"f9c65d06-f40e-11e6-bc64-92361f006689","id":"554e7242-2da9-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"554e7242-2da9-11e8-b467-0ed5f89f718b","id":"554e7242-2da9-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"车辆管理","pId":"963283ce-6aab-11e6-8b77-86f30ca893d3","id":"a1cf4672-6f4c-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"a1cf4672-6f4c-11e6-8b77-86f30ca893d3","id":"a1cf4672-6f4c-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"车型管理","pId":"963283ce-6aab-11e6-8b77-86f30ca893d3","id":"a1cf4258-6f4c-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"a1cf4258-6f4c-11e6-8b77-86f30ca893d3","id":"a1cf4258-6f4c-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"燃料管理","pId":"963283ce-6aab-11e6-8b77-86f30ca893d3","id":"fc87ab62-7d62-11e6-lb12-56b6b6499611"},{"name":"可写","pId":"fc87ab62-7d62-11e6-lb12-56b6b6499611","id":"fc87ab62-7d62-11e6-lb12-56b6b6499611edit","type":"premissionEdit"},{"name":"实时监控","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"2d253408-18d9-4bc3-971b-a3a737f9f5fb"},{"name":"可写","pId":"2d253408-18d9-4bc3-971b-a3a737f9f5fb","id":"2d253408-18d9-4bc3-971b-a3a737f9f5fbedit","type":"premissionEdit"},{"name":"油位传感器管理","pId":"a03ff712-9755-11e6-ae22-56b6b6499611","id":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d3","id":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"油箱管理","pId":"a03ff712-9755-11e6-ae22-56b6b6499611","id":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d4"},{"name":"可写","pId":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d4","id":"3c8b8c7e-6aad-11e6-8b77-86f30ca893d4edit","type":"premissionEdit"},{"name":"油量车辆设置","pId":"a03ff712-9755-11e6-ae22-56b6b6499611","id":"a66ee712-9755-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"a66ee712-9755-11e6-ae22-56b6b6499611","id":"a66ee712-9755-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"油量标定","pId":"a03ff712-9755-11e6-ae22-56b6b6499611","id":"a66ee712-9755-11e6-ae22-56b6b6499654"},{"name":"可写","pId":"a66ee712-9755-11e6-ae22-56b6b6499654","id":"a66ee712-9755-11e6-ae22-56b6b6499654edit","type":"premissionEdit"},{"name":"流量传感器管理","pId":"fc87a5b8-7d62-11e6-ae22-56b6b6499611","id":"fc87a98c-7d62-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"fc87a98c-7d62-11e6-ae22-56b6b6499611","id":"fc87a98c-7d62-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"油耗车辆设置","pId":"fc87a5b8-7d62-11e6-ae22-56b6b6499611","id":"94712ca2-7d7a-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"94712ca2-7d7a-11e6-ae22-56b6b6499611","id":"94712ca2-7d7a-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"外设管理","pId":"b296585a-339c-11e7-a919-92ebcb67fe33","id":"11941ebe-339d-11e7-a919-92ebcb67fe33"},{"name":"可写","pId":"11941ebe-339d-11e7-a919-92ebcb67fe33","id":"11941ebe-339d-11e7-a919-92ebcb67fe33edit","type":"premissionEdit"},{"name":"外设轮询","pId":"b296585a-339c-11e7-a919-92ebcb67fe33","id":"cdc11c04-339d-11e7-a919-92ebcb67fe33"},{"name":"可写","pId":"cdc11c04-339d-11e7-a919-92ebcb67fe33","id":"cdc11c04-339d-11e7-a919-92ebcb67fe33edit","type":"premissionEdit"},{"name":"轮速传感器管理","pId":"80f558ba-391d-11e7-a919-92ebcb67fe33","id":"f619da4e-391d-11e7-a919-92ebcb67fe33"},{"name":"可写","pId":"f619da4e-391d-11e7-a919-92ebcb67fe33","id":"f619da4e-391d-11e7-a919-92ebcb67fe33edit","type":"premissionEdit"},{"name":"轮胎规格管理","pId":"80f558ba-391d-11e7-a919-92ebcb67fe33","id":"23b38a2a-3a0b-11e7-a919-92ebcb67fe33"},{"name":"可写","pId":"23b38a2a-3a0b-11e7-a919-92ebcb67fe33","id":"23b38a2a-3a0b-11e7-a919-92ebcb67fe33edit","type":"premissionEdit"},{"name":"里程监测设置","pId":"80f558ba-391d-11e7-a919-92ebcb67fe33","id":"f619de0e-391d-11e7-a919-92ebcb67fe33"},{"name":"可写","pId":"f619de0e-391d-11e7-a919-92ebcb67fe33","id":"f619de0e-391d-11e7-a919-92ebcb67fe33edit","type":"premissionEdit"},{"name":"里程标定","pId":"80f558ba-391d-11e7-a919-92ebcb67fe33","id":"f03d2138-b043-4ac0-b7fc-46725c1b9ae5"},{"name":"可写","pId":"f03d2138-b043-4ac0-b7fc-46725c1b9ae5","id":"f03d2138-b043-4ac0-b7fc-46725c1b9ae5edit","type":"premissionEdit"},{"name":"振动传感器管理","pId":"81649806-838d-11e6-ae22-56b6b6499611","id":"81649a36-838d-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"81649a36-838d-11e6-ae22-56b6b6499611","id":"81649a36-838d-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"工时车辆设置","pId":"81649806-838d-11e6-ae22-56b6b6499611","id":"7a4fc0c6-838e-11e6-ae22-56b6b6499611"},{"name":"可写","pId":"7a4fc0c6-838e-11e6-ae22-56b6b6499611","id":"7a4fc0c6-838e-11e6-ae22-56b6b6499611edit","type":"premissionEdit"},{"name":"检测功能类型","pId":"7d561544-5661-11e7-907b-a6006ad3dba0","id":"7d5617ba-5661-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"7d5617ba-5661-11e7-907b-a6006ad3dba0","id":"7d5617ba-5661-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"开关信号管理","pId":"7d561544-5661-11e7-907b-a6006ad3dba0","id":"7d5618be-5661-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"7d5618be-5661-11e7-907b-a6006ad3dba0","id":"7d5618be-5661-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"温度传感器管理","pId":"32e16952-622b-11e7-907b-a6006ad3dba0","id":"3d128b3a-622c-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"3d128b3a-622c-11e7-907b-a6006ad3dba0","id":"3d128b3a-622c-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"温度监测设置","pId":"32e16952-622b-11e7-907b-a6006ad3dba0","id":"3d128dc4-622c-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"3d128dc4-622c-11e7-907b-a6006ad3dba0","id":"3d128dc4-622c-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"湿度传感器管理","pId":"32e16bc8-622b-11e7-907b-a6006ad3dba0","id":"d842fa18-622c-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"d842fa18-622c-11e7-907b-a6006ad3dba0","id":"d842fa18-622c-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"湿度监测设置","pId":"32e16bc8-622b-11e7-907b-a6006ad3dba0","id":"d842fcac-622c-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"d842fcac-622c-11e7-907b-a6006ad3dba0","id":"d842fcac-622c-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"正反转传感器管理","pId":"32e16f92-622b-11e7-907b-a6006ad3dba0","id":"9722ba04-622d-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"9722ba04-622d-11e7-907b-a6006ad3dba0","id":"9722ba04-622d-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"正反转车辆设置","pId":"32e16f92-622b-11e7-907b-a6006ad3dba0","id":"9722bc7a-622d-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"9722bc7a-622d-11e7-907b-a6006ad3dba0","id":"9722bc7a-622d-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"行驶能耗基准管理","pId":"fc87ab62-7d62-11e6-lb13-56b6b6499611","id":"fc87ab62-7d62-11e6-lb22-56b6b6499611"},{"name":"可写","pId":"fc87ab62-7d62-11e6-lb22-56b6b6499611","id":"fc87ab62-7d62-11e6-lb22-56b6b6499611edit","type":"premissionEdit"},{"name":"怠速能耗基准管理","pId":"fc87ab62-7d62-11e6-lb13-56b6b6499611","id":"fc87ab62-7d62-11e6-lb23-56b6b6499611"},{"name":"可写","pId":"fc87ab62-7d62-11e6-lb23-56b6b6499611","id":"fc87ab62-7d62-11e6-lb23-56b6b6499611edit","type":"premissionEdit"},{"name":"能耗对比报表","pId":"fc87ade2-7d62-11e6-lb02-56b6b6499611","id":"fc87ab62-7d62-11e6-lb24-56b6b6499611"},{"name":"可写","pId":"fc87ab62-7d62-11e6-lb24-56b6b6499611","id":"fc87ab62-7d62-11e6-lb24-56b6b6499611edit","type":"premissionEdit"},{"name":"轨迹回放","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"7df146e0-6a8f-11e6-8b77-86f30ca893d3"},{"name":"可写","pId":"7df146e0-6a8f-11e6-8b77-86f30ca893d3","id":"7df146e0-6a8f-11e6-8b77-86f30ca893d3edit","type":"premissionEdit"},{"name":"实时指令","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"5609426a-1f4b-11e7-93ae-92361f002671"},{"name":"可写","pId":"5609426a-1f4b-11e7-93ae-92361f002671","id":"5609426a-1f4b-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"实时视频","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"828985c2-eb7c-11e7-8c3f-9a214cf093ae"},{"name":"可写","pId":"828985c2-eb7c-11e7-8c3f-9a214cf093ae","id":"828985c2-eb7c-11e7-8c3f-9a214cf093aeedit","type":"premissionEdit"},{"name":"视频回放","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"8289884c-eb7c-11e7-8c3f-9a214cf093ae"},{"name":"可写","pId":"8289884c-eb7c-11e7-8c3f-9a214cf093ae","id":"8289884c-eb7c-11e7-8c3f-9a214cf093aeedit","type":"premissionEdit"},{"name":"视频参数设置","pId":"84113afa-df07-4247-8666-f164a7acbefa","id":"828989fa-eb7c-11e7-8c3f-9a214cf093ae"},{"name":"可写","pId":"828989fa-eb7c-11e7-8c3f-9a214cf093ae","id":"828989fa-eb7c-11e7-8c3f-9a214cf093aeedit","type":"premissionEdit"},{"name":"转发平台IP管理","pId":"f9c660e4-f40e-11e6-bc64-92361f002671","id":"f9c66436-f40e-11e6-bc64-92361f002671"},{"name":"可写","pId":"f9c66436-f40e-11e6-bc64-92361f002671","id":"f9c66436-f40e-11e6-bc64-92361f002671edit","type":"premissionEdit"},{"name":"接入平台IP管理","pId":"f9c660e4-f40e-11e6-bc64-92361f002671","id":"11f6b351-853b-40c1-a1b5-8bdc483d890a"},{"name":"可写","pId":"11f6b351-853b-40c1-a1b5-8bdc483d890a","id":"11f6b351-853b-40c1-a1b5-8bdc483d890aedit","type":"premissionEdit"},{"name":"监控对象转发管理","pId":"f9c660e4-f40e-11e6-bc64-92361f002671","id":"f9c6671a-f40e-11e6-bc64-92361f002671"},{"name":"可写","pId":"f9c6671a-f40e-11e6-bc64-92361f002671","id":"f9c6671a-f40e-11e6-bc64-92361f002671edit","type":"premissionEdit"},{"name":"监控对象转发管理","pId":"f9c6629c-f40e-11e6-bc64-92368f002671","id":"f9c6629c-f40e-11e6-bc64-92361f003671"},{"name":"可写","pId":"f9c6629c-f40e-11e6-bc64-92361f003671","id":"f9c6629c-f40e-11e6-bc64-92361f003671edit","type":"premissionEdit"},{"name":"对讲地址配置","pId":"6f720d14-095b-11e7-93ae-92361f002671","id":"6f72102a-095b-11e7-93ae-92361f002671"},{"name":"可写","pId":"6f72102a-095b-11e7-93ae-92361f002671","id":"6f72102a-095b-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"对讲设备配置","pId":"6f720d14-095b-11e7-93ae-92361f002671","id":"6f72126e-095b-11e7-93ae-92361f002671"},{"name":"可写","pId":"6f72126e-095b-11e7-93ae-92361f002671","id":"6f72126e-095b-11e7-93ae-92361f002671edit","type":"premissionEdit"},{"name":"平台信息设置","pId":"b2b25f96-3a09-11e7-a919-92ebcb67fe33","id":"753e4754-5635-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"753e4754-5635-11e7-907b-a6006ad3dba0","id":"753e4754-5635-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"监控对象图标","pId":"b2b25f96-3a09-11e7-a919-92ebcb67fe33","id":"753e4a9c-5635-11e7-907b-a6006ad3dba0"},{"name":"可写","pId":"753e4a9c-5635-11e7-907b-a6006ad3dba0","id":"753e4a9c-5635-11e7-907b-a6006ad3dba0edit","type":"premissionEdit"},{"name":"疲劳驾驶报警明细","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d515dbe-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d515dbe-25a1-11e8-b467-0ed5f89f718b","id":"7d515dbe-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"疲劳驾驶违章统计","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d515efe-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d515efe-25a1-11e8-b467-0ed5f89f718b","id":"7d515efe-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"超速报警明细","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d51602a-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d51602a-25a1-11e8-b467-0ed5f89f718b","id":"7d51602a-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"超速违章统计","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d516156-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d516156-25a1-11e8-b467-0ed5f89f718b","id":"7d516156-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"定位数据合格率","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d516480-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d516480-25a1-11e8-b467-0ed5f89f718b","id":"7d516480-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"漂移数据报表","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d5165c0-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d5165c0-25a1-11e8-b467-0ed5f89f718b","id":"7d5165c0-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"凌晨2-5点运行报表","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"7d5166e2-25a1-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"7d5166e2-25a1-11e8-b467-0ed5f89f718b","id":"7d5166e2-25a1-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"},{"name":"异常轨迹报表","pId":"eac86c12-25a0-11e8-b467-0ed5f89f718b","id":"1162a82c-25a3-11e8-b467-0ed5f89f718b"},{"name":"可写","pId":"1162a82c-25a3-11e8-b467-0ed5f89f718b","id":"1162a82c-25a3-11e8-b467-0ed5f89f718bedit","type":"premissionEdit"}]

    # ctree =[
    #         { id:1, pId:0, name:"随意勾选 1", open:true},
    #         { id:11, pId:1, name:"随意勾选 1-1", open:true},
    #         { id:111, pId:11, name:"随意勾选 1-1-1"},
    #         { id:112, pId:11, name:"随意勾选 1-1-2"},
    #         { id:12, pId:1, name:"随意勾选 1-2", open:true},
    #         { id:121, pId:12, name:"随意勾选 1-2-1"},
    #         { id:122, pId:12, name:"随意勾选 1-2-2"},
    #         { id:2, pId:0, name:"随意勾选 2", checked:true, open:true},
    #         { id:21, pId:2, name:"随意勾选 2-1"},
    #         { id:22, pId:2, name:"随意勾选 2-2", open:true},
    #         { id:221, pId:22, name:"随意勾选 2-2-1", checked:true},
    #         { id:222, pId:22, name:"随意勾选 2-2-2"},
    #         { id:23, pId:2, name:"随意勾选 2-3"}
    #     ]

    

    # return JsonResponse(dicts,safe=False)
    return HttpResponse(json.dumps(ctree))

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


class PersonalityView(TemplateView):
    """docstring for AuthStationView"""
    template_name = 'dma/personality.html'
        
    def get_context_data(self, **kwargs):
        context = super(PersonalityView, self).get_context_data(**kwargs)
        context['page_title'] = '个性化设置'
        return context       