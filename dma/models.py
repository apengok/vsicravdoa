# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Organization(MPTTModel):
    name    = models.CharField(max_length=50, unique=True)
    parent  = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True)
    # slug    = models.SlugField()
    
    # def get_absolute_url(self):
    #     return reverse('sub_dma', kwargs={'path': self.get_path()})

    def get_absolute_url(self): #get_absolute_url
        return "/organ/{}".format(self.pk)
        # return reverse('dma:detail', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        managed=True
        # unique_together = ('slug', 'parent')
        db_table = 'organization'

        permissions = (
            # 数据监控 sub
            ('perms_datamonitor','数据监控'),
            ('mapmonitor_perms_datamonitor','地图监控'),
            ('mapmonitor_perms_datamonitor_edit','地图监控_可写'),
            ('realcurlv_perms_datamonitor','实时曲线'),
            ('realcurlv_perms_datamonitor_edit','实时曲线_可写'),
            ('realdata_perms_datamonitor','实时数据'),
            ('realdata_perms_datamonitor_edit','实时数据_可写'),
            ('dmaonline_perms_datamonitor','DMA在线监控'),
            ('dmaonline_perms_datamonitor_edit','DMA在线监控_可写'),

            # 数据分析 sub
            ('perms_datanalys','数据分析'),
            ('dailyuse_perms_datanalys','日用水分析'),
            ('dailyuse_perms_datanalys_edit','日用水分析_可写'),
            ('monthlyuse_perms_datanalys','月用水分析'),
            ('monthlyuse_perms_datanalys_edit','月用水分析_可写'),
            ('dmacxc_perms_datanalys','DMA产销差分析'),
            ('dmacxc_perms_datanalys_edit','DMA产销差分析_可写'),
            ('flownalys_perms_datanalys','流量分析'),
            ('flownalys_perms_datanalys_edit','流量分析_可写'),
            ('comparenalys_perms_datanalys','对比分析'),
            ('comparenalys_perms_datanalys_edit','对比分析_可写'),
            ('peibiao_perms_datanalys','配表分析'),
            ('peibiao_perms_datanalys_edit','配表分析_可写'),
            ('rawdata_perms_datanalys','原始数据'),
            ('rawdata_perms_datanalys_edit','原始数据_可写'),
            ('mnf_perms_datanalys','夜间最小流量'),
            ('mnf_perms_datanalys_edit','夜间最小流量_可写'),

            # 报警中心 sub
            ('perms_alarmcenter','报警中心'),
            ('stationalarm_perms_alarmcenter','站点报警设置'),
            ('stationalarm_perms_alarmcenter_edit','站点报警设置_可写'),
            ('dmaalarm_perms_alarmcenter','DMA报警设置'),
            ('dmaalarm_perms_alarmcenter_edit','DMA报警设置_可写'),
            ('queryalarm_perms_alarmcenter','报警查询'),
            ('queryalarm_perms_alarmcenter_edit','报警查询_可写'),

            # 基础管理 sub
            ('perms_basemanager','基础管理'),
            ('dmamanager_perms_basemanager','dma管理'),
            ('dmamanager_perms_basemanager_edit','dma管理_可写'),
            ('stationmanager_perms_basemanager','站点管理'),
            ('stationmanager_perms_basemanager_edit','站点管理_可写'),

            # 企业管理 sub
            ('perms_firmmanager','企业管理'),
            ('rolemanager_perms_firmmanager','角色管理'),
            ('rolemanager_perms_firmmanager_edit','角色管理_可写'),
            ('organusermanager_perms_basemanager','组织和用户管理'),
            ('organusermanager_perms_basemanager_edit','组织和用户管理_可写'),

            # 设备管理 sub
            ('perms_devicemanager','设备管理'),
            ('meters_perms_devicemanager','表具管理'),
            ('meters_perms_devicemanager_edit','表具管理_可写'),
            ('simcard_perms_devicemanager','SIM卡管理'),
            ('simcard_perms_devicemanager_edit','SIM卡管理_可写'),
            ('params_perms_devicemanager','参数指令'),
            ('params_perms_devicemanager_edit','参数指令_可写'),

            # 基准分析 sub
            ('perms_basenalys','基准分析'),
            ('dma_perms_basenalys','DMA基准分析'),
            ('dma_perms_basenalys_edit','DMA基准分析_可写'),
            ('mf_perms_basenalys','最小流量分析'),
            ('mf_perms_basenalys_edit','最小流量分析_可写'),
            ('day_perms_basenalys','日基准流量分析'),
            ('day_perms_basenalys_edit','日基准流量分析_可写'),

            # 统计报表 sub
            ('perms_reporttable','统计报表'),
            ('querylog_perms_reporttable','日志查询'),
            ('querylog_perms_reporttable_edit','日志查询_可写'),
            ('alarm_perms_reporttable','报警报表'),
            ('alarm_perms_reporttable_edit','报警报表_可写'),
            ('dmastatics_perms_reporttable','DMA统计报表'),
            ('dmastatics_perms_reporttable_edit','DMA统计报表_可写'),
            ('biguser_perms_reporttable','大用户报表'),
            ('biguser_perms_reporttable_edit','大用户报表_可写'),
            ('flows_perms_reporttable','流量报表'),
            ('flows_perms_reporttable_edit','流量报表_可写'),
            ('waters_perms_reporttable','水量报表'),
            ('waters_perms_reporttable_edit','水量报表_可写'),
            ('biaowu_perms_reporttable','表务报表'),
            ('biaowu_perms_reporttable_edit','表务报表_可写'),
            ('bigdata_perms_reporttable','大数据报表'),
            ('bigdata_perms_reporttable_edit','大数据报表_可写'),

            # 系统管理 sub
            ('perms_systemconfig','系统管理'),
            ('personality_perms_systemconfig','平台个性化管理'),
            ('personality_perms_systemconfig_edit','平台个性化管理_可写'),
            ('system_perms_systemconfig','系统设置'),
            ('system_perms_systemconfig_edit','系统设置_可写'),
            ('retransit_perms_systemconfig','转发设置'),
            ('retransit_perms_systemconfig_edit','转发设置_可写'),
            ('icons_perms_systemconfig','图标配置'),
            ('icons_perms_systemconfig_edit','图标配置_可写'),
            ('querylog_perms_systemconfig','日志查询'),
            ('querylog_perms_systemconfig_edit','日志查询_可写'),
        )   
    

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class DMABaseinfo(models.Model):
    dma_no        = models.CharField('分区编号',max_length=50, unique=True)
    pepoles_num   = models.CharField('服务人口',max_length=50, null=True,blank=True)
    acreage       = models.CharField('服务面积',max_length=50, null=True,blank=True)
    user_num      = models.CharField('用户数量',max_length=50, null=True,blank=True)
    pipe_texture  = models.CharField('管道材质',max_length=50, null=True, blank=True)
    pipe_length   = models.CharField('管道总长度(m)',max_length=50, null=True, blank=True)
    pipe_links    = models.CharField('管道连接总数(个)',max_length=50,null=True, blank=True)
    pipe_years    = models.CharField('管道最长服务年限(年)',max_length=50,null=True, blank=True)
    pipe_private  = models.CharField('私人拥有水管长度(m)',max_length=50,blank=True,null=True)
    ifc           = models.CharField('IFC参数',max_length=250, null=True, blank=True)
    aznp          = models.CharField('AZNP',max_length=250,null=True, blank=True)
    night_use     = models.CharField('正常夜间用水量',max_length=50,null=True, blank=True)
    cxc_value     = models.CharField('产销差目标值',max_length=50, null=True, blank=True)

    creator     = models.CharField('负责人',max_length=50, null=True, blank=True) 
    create_date  = models.DateField('建立日期',max_length=50, null=True, blank=True) 

    dma = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        # primary_key=True,
    )

    class Meta:
        managed=True
        unique_together = ('dma_no', )
        db_table = 'dmabaseinfo'

        permissions = (
            ('view_dmabaseinfo', 'View dmabaseinfo'),
        )

    def get_absolute_url(self): #get_absolute_url
        # return "/organ/{}".format(self.pk)
        return reverse('dma:dma_manager', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.dma_no

    def __str__(self):
        return self.dma_no


class Stations(models.Model):
    station_name    = models.CharField('站点名称',max_length=50, unique=True)
    station_type    = models.CharField('类型',max_length=50, null=True, blank=True)
    meter_property  = models.CharField('用水性质',max_length=50,  null=True, blank=True)
    meter_type      = models.CharField('表具类型',max_length=50,  null=True, blank=True)
    meter_code      = models.CharField('表具编号',max_length=50,  null=True, blank=True)
    simno           = models.CharField('SIM卡号',max_length=50,  null=True, blank=True)
    caliber         = models.CharField('口径',max_length=50,  null=True, blank=True)
    big_user        = models.BooleanField('大用户',max_length=50, blank=True)
    focus           = models.BooleanField('重点关注',max_length=50, blank=True)
    installed       = models.DateField('安装日期',auto_now=False,null=True,blank=True)

    belongto        = models.ForeignKey(Organization,verbose_name='所属组织',related_name='station',on_delete=models.CASCADE) #class_instance.model_set.all()

    station_desc    = models.CharField('站点描述',max_length=50, null=True, blank=True)
    longitude       = models.CharField('经度',max_length=50, null=True, blank=True)
    latitude        = models.CharField('纬度',max_length=50, null=True, blank=True)
    geopos          = models.CharField('位置信息',max_length=50, null=True, blank=True)

    class Meta:
        managed=True
        unique_together = ('meter_code', 'simno')
        db_table = 'stations'

    def get_absolute_url(self): #get_absolute_url
        # return "/organ/{}".format(self.pk)
        return reverse('dma:stations_list_manager', kwargs={'dma_id': self.belongto.id})

    def __unicode__(self):
        return self.station_name

    def __str__(self):
        return self.station_name
    

class MeterFlow(models.Model):
    stations        = models.ForeignKey(Stations,blank=True, null=True,on_delete=models.CASCADE) 
    comm_status     = models.CharField('状态', max_length=30, blank=True, null=True)  # Field name made lowercase.
    read_time       = models.DateTimeField('最新采样时间', auto_now_add=True )  # Field name made lowercase.
    read_interval   = models.CharField('采样间隔min', max_length=128, blank=True, null=True)  # Field name made lowercase.
    report_interval = models.CharField('上报间隔h', max_length=128, blank=True, null=True)  # Field name made lowercase.
    instance_flow   = models.CharField('瞬时流量m³/h', max_length=30, blank=True, null=True)  # Field name made lowercase.
    postive_flow    = models.CharField('正向流量m³', max_length=30, blank=True, null=True)  # Field name made lowercase.
    reverse_flow    = models.CharField('反向流量m³', max_length=30, blank=True, null=True)  # Field name made lowercase.
    base_power      = models.CharField('基表电量%', max_length=30, blank=True, null=True)  # Field name made lowercase.
    trans_power     = models.CharField('远传电量%', max_length=30, blank=True, null=True)  # Field name made lowercase.
    signals         = models.CharField('信号强度%', max_length=30, blank=True, null=True)  # Field name made lowercase.
    
    
    class Meta:
        managed = True
        db_table = 'meterflow'
        

    def __unicode__(self):
        return '%s_flow'%(self.stations.station_name)

    def __str__(self):
        return '%s_flow'%(self.stations.station_name)


class MeterPress(models.Model):
    stations        = models.ForeignKey(Stations,blank=True, null=True,on_delete=models.CASCADE) 
    read_time       = models.DateTimeField('最新采样时间', auto_now_add=True )  # Field name made lowercase.
    read_interval   = models.CharField('采样间隔min', max_length=128, blank=True, null=True)  # Field name made lowercase.
    report_interval = models.CharField('上报间隔h', max_length=128, blank=True, null=True)  # Field name made lowercase.
    press           = models.CharField('压力Mpa', max_length=30, blank=True, null=True)  # Field name made lowercase.
    
    
    
    class Meta:
        managed = True
        db_table = 'meterpress'
        

    def __unicode__(self):
        return '%s_press'%(self.stations.station_name)       

    def __str__(self):
        return '%s_flow'%(self.stations.station_name) 


class Alarms(models.Model):
    stations        = models.ForeignKey(Stations,blank=True, null=True,on_delete=models.CASCADE) 
    report_time     = models.DateTimeField('报警时间',auto_now_add=True)
    alarm_type      = models.CharField('报警类型',max_length=30,null=True,blank=True)
    process_status  = models.CharField('处理状态',max_length=30,null=True,blank=True)
    process_by      = models.CharField('处理人',max_length=30,null=True,blank=True)
    process_time    = models.DateTimeField('处理时间',auto_now=False,null=True,blank=True)
    notes           = models.CharField('备注',max_length=300,null=True,blank=True)


    class Meta:
        managed = True
        db_table = 'alarms'

    def __unicode__(self):
        return '%s_alarms'%(self.stations.station_name)       

    def __str__(self):
        return '%s_alarms'%(self.stations.station_name) 