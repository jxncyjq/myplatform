# -*- coding: utf-8 -*-
# Create your views here.
import xadmin
from xadmin import views
from idc import models
from models import Idc, Host, MaintainLog, HostGroup, AccessRecord
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "绿岸IDC资产系统", "content": "<h3> 管理员欢迎您回来 <h3>"},
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {
                'o':'-guarantee_date'}},
        ],
        [
            {"type": "qbutton", "title": "Quick Start", "btns": [{'model': Host}, {'model':IDC}, {'title': "Google", 'url': "http://www.google.com"}]},
            {"type": "addform", "model": MaintainLog},
        ]
    ]

xadmin.site.register(views.website.IndexView,MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class HostGroupAdmin(object):
    list_display = ('name', 'description')
    list_display_links = ('name',)

    search_fields = ['name']
    style_fields = {'hosts': 'checkbox-inline'}

class MaintainLogAdmin(object):
    list_display = (
        'host', 'maintain_type', 'hard_type', 'time', 'operator', 'note')
    list_display_links = ('host',)

    list_filter = ['host', 'maintain_type', 'hard_type', 'time', 'operator']
    search_fields = ['note']

    form_layout = (
        Col("col2",
            Fieldset('Record data',
                     'time', 'note',
                     css_class='unsort short_label no_title'
                     ),
            span=9, horizontal=True
            ),
        Col("col1",
            Fieldset('Comm data',
                     'host', 'maintain_type'
                     ),
            Fieldset('Maintain details',
                     'hard_type', 'operator'
                     ),
            span=3
            )
    )
    reversion_enable = True



class GolbeSetting(object):
    globe_search_models = [models.Host, models.Idc]
    globe_models_icon = {
        models.Host: 'laptop', models.Idc: 'cloud'
    }
    site_title = u'上海绿岸网络'
xadmin.site.register(views.CommAdminView, GolbeSetting)

class IDCAdmin(object):
    list_display = ('name','description','create_time')
    list_display_links = ('name',)

class PersonAdmin(object):
    list_display = ('name','job','telphone','mobil','mail','im')
    list_display_links = ('name',)

class CompanyAdmin(object):
    list_display = ('name','address','telphone','person','el_person')
    list_display_links = ('name',)

class ContractAdmin(object):
    list_display = ('name','description','startdate','enddate','create_time','corp')
    list_display_links = ('name',)

class IdcAdmin(object):
    list_display = ('name','description','telphone','address')
    list_display_links = ('name',)

class RackAdmin(object):
    list_display = ('name','description','rackus','power')
    list_display_links = ('name',)

class HostAdmin(object):
    list_display = ('name','status','rack','model','cpu','core_num','hard_disk','hard_disk_size','memory')
    list_display_links = ('name',)
    search_fields = ['name', 'ip', 'description']
    list_filter = ['status', 'brand', 'model',
                   'cpu', 'core_num', 'hard_disk', 'memory', 'service_type']

class ContainerAdmin(object):
    list_display = ('name','description','hosts','person')
    list_display_links = ('name',)

class IPAddressAdmin(object):
    list_display = ('idc','ipaddr','ip_type','gateway')
    list_display_links = ('ipaddr',)



xadmin.site.register(models.Idc,IDCAdmin)
xadmin.site.register(models.Person,PersonAdmin)
xadmin.site.register(models.Company,CompanyAdmin)
xadmin.site.register(models.Contract,ContractAdmin)
xadmin.site.register(models.Rack,RackAdmin)
xadmin.site.register(models.Host,HostAdmin)
xadmin.site.register(models.IPAddress,IPAddressAdmin)
xadmin.site.register(models.Container,ContainerAdmin)
