# Generated by Django 2.0 on 2018-05-22 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dma', '0002_auto_20180425_0937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dmabaseinfo',
            options={'managed': True, 'permissions': (('view_dmabaseinfo', 'View dmabaseinfo'),)},
        ),
    ]
