# Generated by Django 2.0 on 2018-04-14 22:48

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_time', models.DateTimeField(auto_now_add=True, verbose_name='报警时间')),
                ('alarm_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='报警类型')),
                ('process_status', models.CharField(blank=True, max_length=30, null=True, verbose_name='处理状态')),
                ('process_by', models.CharField(blank=True, max_length=30, null=True, verbose_name='处理人')),
                ('process_time', models.DateTimeField(blank=True, null=True, verbose_name='处理时间')),
                ('notes', models.CharField(blank=True, max_length=300, null=True, verbose_name='备注')),
            ],
            options={
                'managed': True,
                'db_table': 'alarms',
            },
        ),
        migrations.CreateModel(
            name='DMABaseinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dma_no', models.CharField(max_length=50, unique=True, verbose_name='分区编号')),
                ('pepoles_num', models.CharField(blank=True, max_length=50, null=True, verbose_name='服务人口')),
                ('acreage', models.CharField(blank=True, max_length=50, null=True, verbose_name='服务面积')),
                ('user_num', models.CharField(blank=True, max_length=50, null=True, verbose_name='用户数量')),
                ('pipe_texture', models.CharField(blank=True, max_length=50, null=True, verbose_name='管道材质')),
                ('pipe_length', models.CharField(blank=True, max_length=50, null=True, verbose_name='管道总长度(m)')),
                ('pipe_links', models.CharField(blank=True, max_length=50, null=True, verbose_name='管道连接总数(个)')),
                ('pipe_years', models.CharField(blank=True, max_length=50, null=True, verbose_name='管道最长服务年限(年)')),
                ('pipe_private', models.CharField(blank=True, max_length=50, null=True, verbose_name='私人拥有水管长度(m)')),
                ('ifc', models.CharField(blank=True, max_length=250, null=True, verbose_name='IFC参数')),
                ('aznp', models.CharField(blank=True, max_length=250, null=True, verbose_name='AZNP')),
                ('night_use', models.CharField(blank=True, max_length=50, null=True, verbose_name='正常夜间用水量')),
                ('cxc_value', models.CharField(blank=True, max_length=50, null=True, verbose_name='产销差目标值')),
                ('creator', models.CharField(blank=True, max_length=50, null=True, verbose_name='负责人')),
                ('create_date', models.DateField(blank=True, max_length=50, null=True, verbose_name='建立日期')),
            ],
            options={
                'db_table': 'dmabaseinfo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MeterFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comm_status', models.CharField(blank=True, max_length=30, null=True, verbose_name='状态')),
                ('read_time', models.DateTimeField(auto_now_add=True, verbose_name='最新采样时间')),
                ('read_interval', models.CharField(blank=True, max_length=128, null=True, verbose_name='采样间隔min')),
                ('report_interval', models.CharField(blank=True, max_length=128, null=True, verbose_name='上报间隔h')),
                ('instance_flow', models.CharField(blank=True, max_length=30, null=True, verbose_name='瞬时流量m³/h')),
                ('postive_flow', models.CharField(blank=True, max_length=30, null=True, verbose_name='正向流量m³')),
                ('reverse_flow', models.CharField(blank=True, max_length=30, null=True, verbose_name='反向流量m³')),
                ('base_power', models.CharField(blank=True, max_length=30, null=True, verbose_name='基表电量%')),
                ('trans_power', models.CharField(blank=True, max_length=30, null=True, verbose_name='远传电量%')),
                ('signals', models.CharField(blank=True, max_length=30, null=True, verbose_name='信号强度%')),
            ],
            options={
                'managed': True,
                'db_table': 'meterflow',
            },
        ),
        migrations.CreateModel(
            name='MeterPress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_time', models.DateTimeField(auto_now_add=True, verbose_name='最新采样时间')),
                ('read_interval', models.CharField(blank=True, max_length=128, null=True, verbose_name='采样间隔min')),
                ('report_interval', models.CharField(blank=True, max_length=128, null=True, verbose_name='上报间隔h')),
                ('press', models.CharField(blank=True, max_length=30, null=True, verbose_name='压力Mpa')),
            ],
            options={
                'managed': True,
                'db_table': 'meterpress',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='dma.Organization')),
            ],
            options={
                'managed': True,
                'db_table': 'organization',
            },
        ),
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=50, unique=True, verbose_name='站点名称')),
                ('station_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='类型')),
                ('meter_property', models.CharField(blank=True, max_length=50, null=True, verbose_name='用水性质')),
                ('meter_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='表具类型')),
                ('meter_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='表具编号')),
                ('simno', models.CharField(blank=True, max_length=50, null=True, verbose_name='SIM卡号')),
                ('caliber', models.CharField(blank=True, max_length=50, null=True, verbose_name='口径')),
                ('big_user', models.BooleanField(max_length=50, verbose_name='大用户')),
                ('focus', models.BooleanField(max_length=50, verbose_name='重点关注')),
                ('installed', models.DateField(blank=True, verbose_name='安装日期')),
                ('station_desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='站点描述')),
                ('longitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='经度')),
                ('latitude', models.CharField(blank=True, max_length=50, null=True, verbose_name='纬度')),
                ('geopos', models.CharField(blank=True, max_length=50, null=True, verbose_name='位置信息')),
                ('belongto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='station', to='dma.Organization', verbose_name='所属组织')),
            ],
            options={
                'db_table': 'stations',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='meterpress',
            name='stations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dma.Stations'),
        ),
        migrations.AddField(
            model_name='meterflow',
            name='stations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dma.Stations'),
        ),
        migrations.AddField(
            model_name='dmabaseinfo',
            name='dma',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dma.Organization'),
        ),
        migrations.AddField(
            model_name='alarms',
            name='stations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dma.Stations'),
        ),
        migrations.AlterUniqueTogether(
            name='stations',
            unique_together={('meter_code', 'simno')},
        ),
        migrations.AlterUniqueTogether(
            name='dmabaseinfo',
            unique_together={('dma_no',)},
        ),
    ]
