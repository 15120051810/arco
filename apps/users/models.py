from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


# 有外键的是从表，多对多没有主从之分

class Org(models.Model):
    org_type_choices = (
        (1, "大区"),
        (2, "省份"),
        (3, "城市"),
        (4, "片区"),
        (5, "电商"),
        (6, "门店"),
        (7, "作废闭店机构"),
        (8, "其他"),
        (9, "连锁总部"),

    )
    state_choices = (
        (0, "禁用"),
        (1, "正常")
    )

    ds_choices = (
        (0, "否"),
        (1, "是")
    )

    org_id = models.CharField(max_length=228, verbose_name='组织ID', unique=True, null=True)
    org_name = models.CharField(max_length=228, verbose_name='组织名称', blank=True)
    org_type = models.IntegerField(choices=org_type_choices, verbose_name='组织类型', null=True, blank=True)
    org_code = models.CharField(max_length=228, verbose_name='组织编码')
    order_index = models.IntegerField(default=1000, verbose_name='序号')
    parent = models.ForeignKey(to='self', to_field="org_id", null=True, blank=True, verbose_name='父组织',
                               related_name='children', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=state_choices, verbose_name="状态", default=1, null=True, blank=True)
    is_ds = models.SmallIntegerField(choices=ds_choices, verbose_name="是否是电商", default=0, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '组织管理'
        verbose_name_plural = verbose_name
        ordering = ('order_index',)
        default_permissions = ()
        permissions = (
            ('view_org', '查看组织'),
            ('add_org', '添加组织'),
            ('change_org', '编辑组织'),
            ('delete_org', '删除组织'),
        )
        indexes = [
            models.Index(fields=['org_name'])
        ]

    def __str__(self):
        return self.org_name


class ChannelShop(models.Model):
    channel_shop_type_choices = (
        (1, "渠道"),
        (2, "店铺"),
    )
    state_choices = (
        (0, "禁用"),
        (1, "正常")
    )

    channel_shop_id = models.CharField(max_length=228, verbose_name='渠道店铺ID', unique=True, null=True)
    name = models.CharField(max_length=228, verbose_name='渠道店铺名称', blank=True)
    type = models.IntegerField(choices=channel_shop_type_choices, verbose_name='渠道或者店铺类型', null=True,
                               blank=True)
    order_index = models.IntegerField(default=1000, verbose_name='序号')
    parent = models.ForeignKey(to='self', to_field="channel_shop_id", null=True, blank=True,
                               verbose_name='渠道店铺名称',
                               related_name='children', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=state_choices, verbose_name="状态", default=1, null=True, blank=True)

    class Meta:
        verbose_name = '渠道店铺管理'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class DepartmentalProject(models.Model):
    departmental_project_type_choices = (
        (1, "部门"),
        (2, "项目")
    )
    state_choices = (
        (0, "禁用"),
        (1, "正常")
    )

    departmental_project_id = models.CharField(max_length=228, verbose_name='部门或项目ID', unique=True, null=True)
    name = models.CharField(max_length=228, verbose_name='名称', blank=True)
    type = models.IntegerField(choices=departmental_project_type_choices, verbose_name='部门或项目', null=True,
                               blank=True)
    order_index = models.IntegerField(default=1000, verbose_name='序号')
    parent = models.ForeignKey(to='self', to_field="departmental_project_id", null=True, blank=True, verbose_name='父',
                               related_name='children', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=state_choices, verbose_name="状态", default=1, null=True, blank=True)

    class Meta:
        verbose_name = '部门项目'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class MedicalWorkerDP(models.Model):
    departmental_project_type_choices = (
        (1, "部门"),
        (2, "项目")
    )
    state_choices = (
        (0, "禁用"),
        (1, "正常")
    )

    departmental_project_id = models.CharField(max_length=228, verbose_name='部门或项目ID', unique=True, null=True)
    name = models.CharField(max_length=228, verbose_name='名称', blank=True)
    type = models.IntegerField(choices=departmental_project_type_choices, verbose_name='部门或项目', null=True,
                               blank=True)
    order_index = models.IntegerField(default=1000, verbose_name='序号')
    parent = models.ForeignKey(to='self', to_field="departmental_project_id", null=True, blank=True, verbose_name='父',
                               related_name='children', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=state_choices, verbose_name="状态", default=1, null=True, blank=True)

    class Meta:
        verbose_name = ' 圆心医工部门项目'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """用户"""
    name = models.CharField(blank=True, max_length=255, db_comment='姓名')
    email = models.EmailField(blank=True, max_length=128, db_comment='邮箱地址', null=True)

    roles = models.ManyToManyField('Role', blank=True, verbose_name='角色', related_name='role_users')
    orgs = models.ManyToManyField('Org', through='UserOrg', verbose_name='组织', related_name='org_users')
    channel_shop = models.ManyToManyField('ChannelShop', blank=True, verbose_name='渠道店铺',
                                          related_name='channel_shop')
    departmental_project = models.ManyToManyField('DepartmentalProject', blank=True, verbose_name='部门项目',
                                                  related_name='departmental_project')
    medical_worker_dp = models.ManyToManyField('MedicalWorkerDP', blank=True, verbose_name='医工部门项目',
                                               related_name='medical_worker_dp')
    staff_code = models.CharField(blank=True, max_length=128, db_comment='工号', null=True)
    home_page = models.ForeignKey('Router', blank=True, null=True, db_comment='首页', on_delete=models.SET_NULL)
    mobile = models.CharField(blank=True, max_length=128, db_comment='手机号', null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_comment='创建时间')
    updated_at = models.DateTimeField(auto_now=True, db_comment='更新时间')

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_user', '查看用户'),
            ('add_user', '添加用户'),
            ('change_user', '编辑用户'),
            ('delete_user', '删除用户'),
        )

        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name if self.name else self.username


class UserOrg(models.Model):
    """
    定义中间模型 UserOrg，用来表示用户与组织之间的关系
    此模型允许我们为多对多关系添加额外的字段
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    # name = models.CharField(max_length=228, verbose_name='组织名称', blank=True)
    selected = models.BooleanField(default=False, verbose_name='选中')
    half_selected = models.BooleanField(default=False, verbose_name='半选')
    org_parent_id = models.IntegerField(null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='children')

    class Meta:
        unique_together = ('user', 'org')


class Api(models.Model):
    """
    API管理
    """
    name = models.CharField(max_length=150, verbose_name='API名称')
    abs_path = models.CharField(max_length=255, verbose_name='绝对路径', help_text='绝对路径，不包括域名')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父路径', related_name='children',
                               on_delete=models.CASCADE)
    order_index = models.IntegerField(default=1000, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'API管理'
        verbose_name_plural = verbose_name
        ordering = ('order_index',)
        default_permissions = ()
        permissions = (
            ('view_api', '查看API'),
            ('add_api', '增加API'),
            ('change_api', '编辑API'),
            ('delete_api', '删除API'),
        )

    def __str__(self):
        return f"{self.name}:{self.abs_path}"


class Router(models.Model):
    """
    菜单管理
    """
    type_choices = (
        (0, '目录'),
        (1, '页面'),
        (2, '按钮')
    )
    system_choices = (
        (0, 'PC端'),
        (1, '移动端'),
    )
    name = models.CharField(max_length=100, verbose_name='路由唯一名称', help_text='用来拼接path', null=True,
                            blank=True)
    title = models.CharField(max_length=255, verbose_name='菜单名称', help_text='显示的菜单名称')
    locale_title = models.CharField(max_length=100, verbose_name='前端需要的双语配置', help_text='前端需要的双语配置',
                                    null=True,
                                    blank=True)
    # abs_title = models.CharField(max_length=255, default='', verbose_name='菜单名称绝对路径', null=True, blank=True)
    component = models.CharField(max_length=100, verbose_name='组件名称', null=True, blank=True)
    redirect = models.CharField(max_length=150, null=True, blank=True, verbose_name='跳转路径')
    icon = models.CharField(max_length=60, null=True, blank=True, verbose_name='菜单图标')
    show = models.BooleanField(default=True, verbose_name='是否显示菜单')
    order_index = models.IntegerField(default=1000, verbose_name='排序')
    type = models.SmallIntegerField(choices=type_choices, default=0, verbose_name='类型')
    system = models.SmallIntegerField(choices=system_choices, default=0, verbose_name='系统')
    keyword = models.CharField(max_length=228, null=True, blank=True, verbose_name='权限关键字')
    apis = models.ManyToManyField(Api, blank=True, verbose_name='API接口', related_name='routers')
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='父路由',
                               related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '菜单管理'
        verbose_name_plural = verbose_name
        ordering = ('order_index',)
        default_permissions = ()
        permissions = (
            ('view_router', '查看菜单'),
            ('add_router', '增加菜单'),
            ('change_router', '编辑菜单'),
            ('delete_router', '删除菜单'),
        )


class Role(models.Model):
    """
        角色管理
    """
    system_choices = (
        (0, 'PC端'),
        (1, '移动端'),
    )

    name = models.CharField(max_length=150, unique=True, verbose_name='角色名称')
    routers = models.ManyToManyField(Router, blank=True, verbose_name='菜单', related_name='roles',
                                     help_text='左侧菜单，用来控制显示还是不显示')
    # apis = models.ManyToManyField(Api, blank=True, verbose_name='API', related_name='api_roles',
    #                               help_text='用做开放给外部程序调用接口的授权，可不填！')
    keyword = models.CharField(max_length=228, null=True, blank=True, verbose_name='角色关键字')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')
    type = models.SmallIntegerField(choices=system_choices, default=0, verbose_name='所属系统')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name
        default_permissions = ()
        permissions = (
            ('view_role', '查看角色'),
            ('add_role', '添加角色'),
            ('change_role', '编辑角色'),
            ('delete_role', '删除角色'),
        )

    def __str__(self):
        return f"{self.name}"
