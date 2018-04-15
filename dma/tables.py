# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_tables2 as tables

from django.db import connection
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Stations

class StationsTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor="id")
    btn_del  = tables.Column(accessor="id")  #empty_values=()
    class Meta:
        model = Stations
        template_name = 'django_tables2/bootstrap.html'
        attrs = {
            'id':'tb_stations',
            'class':'table',
        }


    def render_selected(self,record):    
        return format_html('<input class="nameCheckBox" name="name[]" type="checkbox" />')
        # if record.id:
        #     return mark_safe('<input class="nameCheckBox" name="name[]" type="checkbox" checked/>')
        # else:   
        #     return mark_safe('<input class="nameCheckBox" name="name[]" type="checkbox"/>')

    def render_btn_del(self,value):
        return format_html('<button type = "button" value="{}" class = "btnAlter" data-toggle = "modal" data-target = "#myModal">Alter</button><button type = "button" class = "btnDelete">Delete</button>',value)

