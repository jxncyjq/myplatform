# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

IP_TYPES =(
    (0,u'外网'),
    (1,u'内网'),
    (2,u'远控'),
    (3,u'业务'),
)
RACK_SIZE = (
    (0,u'42U'),
    (1,u'34U'),
    (2,u'12U'),
)

SIDE_TYPE =(
    (0,u'甲方'),
    (1,u'乙方'),
)
SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)
SERVICE_TYPES = (
    ('moniter', u"Moniter"),
    ('lvs', u"LVS"),
    ('db', u"Database"),
    ('analysis', u"Analysis"),
    ('admin', u"Admin"),
    ('storge', u"Storge"),
    ('web', u"WEB"),
    ('email', u"Email"),
    ('mix', u"Mix"),
)
#公司
class Company(models.Model):
    """
    name        公司名
    address     公司地址
    telphone    公司电话
    person      业务负责人
    el_person   公司法人
    """
    name = models.CharField(max_length=64,verbose_name = '公司')
    address = models.TextField(verbose_name = '地址')
    telphone = models.CharField(max_length=32,blank=True,null=True,verbose_name='电话')
    person = models.CharField(max_length=20,verbose_name='联系人')
    el_person = models.CharField(max_length=20,verbose_name = '企业法人')

    def __unicode__(self):
        return '公司名称：%s\t地址：%s\t电话：%s' % (self.name,self.address,self.telphone)

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = verbose_name

#人员
class Person(models.Model):
    """
    name        人员名
    job         职位
    mobil       移动电话
    mail        邮箱
    im          即时聊天工具
    Company     所属公司
    side        甲方已言
    """
    name = models.CharField(max_length=64,verbose_name = '姓名')
    job = models.TextField(blank=True,verbose_name = '职位')
    telphone = models.CharField(max_length=20,blank=True,null=True,verbose_name = '电话')
    mobil = models.CharField(max_length=32,blank=True,null=True,verbose_name = '移动电话')
    mail = models.CharField(max_length=32,blank=True,null=True,verbose_name = '邮件')
    im =  models.CharField(max_length=32,blank=True,null=True,verbose_name = '聊天软件')
    company = models.ForeignKey(Company,related_name = 'company',verbose_name = '人员所在公司')
    side = models.SmallIntegerField(choices=SIDE_TYPE,verbose_name = '甲方乙方')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '人员'
        verbose_name_plural = verbose_name


#合同
class Contract(models.Model):
    """
    name        合同名
    description 合同描述
    startdate   合同开始日期
    enddate     合同结束日期
    createtime  合同添加日期
    corp        合同公司(多对多字段，一个公司可以有多份合同,但一份合同只能有一个公司)
    """
    name = models.CharField(max_length=64,verbose_name = '合同名')
    description = models.TextField(blank=True,null=True,verbose_name = '合同描述')
    startdate = models.DateField(verbose_name = '合同开始日期')
    enddate = models.DateField(verbose_name = '合同结束日期')
    corp = models.ForeignKey(Company,related_name='corp',verbose_name = '签订合同的乙方公司')
    create_time = models.DateField(verbose_name = '合同创建日期')

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = '合同'
        verbose_name_plural = verbose_name

#机房
class Idc(models.Model):
    """
    name        idc名
    description 机房描述
    telphone    电话
    address     机房地址
    create_time 机房添加时间
    """
    name = models.CharField(max_length=64,verbose_name = '机房名')
    description = models.TextField(blank=True,verbose_name = '机房描述')

    telphone = models.CharField(max_length=32,verbose_name = '机房电话')
    address = models.CharField(max_length=128,verbose_name = '机房地址')
    create_time = models.DateField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = verbose_name


#机架
class Rack(models.Model):
    """
    name        机架名，机架编号可重复
    description 机柜描述
    idc         机柜所在idc关联(多对1关系)
    power       机柜电力
    rackus      机柜u数
    Contract    合同(多个机柜对应一份合同属于多对1关系)
    bandwidth   机柜带宽
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    idc = models.ForeignKey(Idc,related_name = 'rack_idc',verbose_name = '机柜所在的IDC名字')
    contact = models.ForeignKey(Contract,related_name = 'contact',verbose_name='机柜对应的合同')
    bandwidth = models.IntegerField(verbose_name = '带宽')

    power=models.TextField(verbose_name='电力（安培）')
    rackus=models.SmallIntegerField(choices=RACK_SIZE,verbose_name = '机架U数')

    def __unicode__(self):
        return '%s,%s' % (self.name,self.description)
    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = verbose_name

#IP地址
class IPAddress(models.Model):
    """
    idc         ip 所以在机房关联
    ipaddr      ip地址
    ip_type     地址类型（内网、外网、业务、远控）
    """
    idc = models.ForeignKey(Idc,related_name = 'idc' ,verbose_name = 'IP地址所在机房')
    ipaddr = models.IPAddressField(verbose_name = 'IP地址')
    ip_type = models.SmallIntegerField(choices = IP_TYPES,verbose_name = 'IP类型')
    gateway = models.IPAddressField(verbose_name = '网关')

    def __unicode__(self):
        return self.ipaddr

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = verbose_name


#主机
class Host(models.Model):
    """
    Name        主机名
    rack        所在机架
    status      主机状态
    macaddr1    mac地址1
    macaddr2    mac地址2
    macaddr3    mac地址3
    macaddr4    mac地址4
    brand       服务器品牌
    model
    cpu         服务器CPU型号
    core_num    服务器核数
    hard_disk   服务器硬盘数
    raid_card   RAID卡型号
    memory      内存大小
    buydate     购买日期
    first_rack  首次上架
    last_rack   最后一次上架
    system      系统类型
    system_version  系统版本
    system_arch     系统架构
    create_time     主机录入时间
    guarantee_date  过保日期
    service_type    应用类型
    description     描述
    """
    name = models.CharField(u"主机名字",max_length=64)
    rack = models.ForeignKey(Rack,related_name = 'rack',verbose_name = '主机所在机柜')

    status = models.SmallIntegerField(choices=SERVER_STATUS)
    ipaddr1 = models.ForeignKey(IPAddress,related_name = 'ipaddrs1',verbose_name = 'IP地址1',blank = True,null=True)
    macadd1 = models.CharField(u"Mac地址1",max_length=18,blank = True,null=True)
    ipaddr2 = models.ForeignKey(IPAddress,related_name = 'ipaddrs2',verbose_name = 'IP地址2',blank = True,null=True)
    macadd2 = models.CharField(u"Mac地址2",max_length=18,blank = True,null=True)
    ipaddr3 = models.ForeignKey(IPAddress,related_name = 'ipaddrs3',verbose_name = 'IP地址3',blank = True,null=True)
    macadd3 = models.CharField(u"Mac地址3",max_length=18,blank = True,null=True)
    ipaddr4 = models.ForeignKey(IPAddress,related_name = 'ipaddrs4',verbose_name = 'IP地址4',blank = True,null=True)
    macadd4 = models.CharField(u"Mac地址4",max_length=18,blank = True,null=True)

    brand = models.CharField(max_length=64, choices=[(i, i) for i in (u"DELL", u"HP", u"Other")],verbose_name = '品牌')
    model = models.CharField(max_length=64,verbose_name = '型号')
    cpu = models.CharField(max_length=64,verbose_name = 'cpu')
    core_num = models.SmallIntegerField(choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 15)],verbose_name ='核数')
    hard_disk = models.IntegerField(verbose_name = '硬盘个数')
    hard_disk_size = models.IntegerField(verbose_name = '硬盘容量')
    raid_card = models.TextField(verbose_name = 'raid卡型号')
    memory = models.IntegerField(verbose_name = '内存（MB）')
    buydate = models.DateField(verbose_name = '购买日期')
    guarantee_date = models.DateField(verbose_name = '过保日期')

    first_rack = models.DateField(verbose_name = '首次上架时间')
    last_rack = models.DateField(verbose_name = '最后一次上架时间')

    system = models.CharField(u"操作系统类型", max_length=32, choices=[(i, i) for i in (u"CentOS", u"FreeBSD", u"Ubuntu",u"Windows")])
    system_version = models.CharField(u"系统版本",max_length=32)
    system_arch = models.CharField(u"系统架构",max_length=32, choices=[(i, i) for i in (u"x86_64", u"i386")])

    create_time = models.DateField(verbose_name='入录时间')
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPES,verbose_name = '服务类型')
    description = models.TextField(verbose_name = '描述')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = verbose_name


#业务组
class Container(models.Model):
    """
    name            业务组名字
    description     业务描述
    hosts           业务中存在的主机表，多对多字段
    person          业务负责人
    """
    name = models.CharField(max_length=64,verbose_name = '业务组名')
    description = models.TextField(u"描述")
    hosts = models.ManyToManyField(Host,blank=True,verbose_name='主机成员')
    person = models.ForeignKey(Person,verbose_name = '管理人')

    def __unicode__(self):
        return '%s,%s' % (self.name,self.description)

    class Meta:
        verbose_name = '业务容器'
        verbose_name_plural = verbose_name


class MaintainLog(models.Model):
    host = models.ForeignKey(Host)
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __unicode__(self):
        return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                               self.maintain_type, self.hard_type)

    class Meta:
        verbose_name = u"Maintain Log"
        verbose_name_plural = verbose_name


class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField()
    hosts = models.ManyToManyField(
        Host, verbose_name=u'Hosts', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"Host Group"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"Access Record"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')

