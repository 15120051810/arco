from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User as Users

# Create your models here.
from django.utils import timezone

User = get_user_model()


class ActionLogManager(models.Manager):
    use_in_migrations = True

    # 执行者 动作 0 object字符串形式 客户id 改变信息
    def log_handler(self, actor, action, action_object, object_repr, client_ip, change_message=''):
        return self.model.objects.create(
            actor=actor,
            action=action,
            action_object=action_object,
            object_repr=object_repr,
            client_ip=client_ip,
            change_message=change_message
        )


class ActionLog(models.Model):
    """
    行为日志
    """
    ACTION_TYPE = (
        ('A', '添加了'),  # add
        ('E', '编辑了'),  # edit
        ('D', '删除了'),  # delete
    )
    action_time = models.DateTimeField(default=timezone.now, verbose_name='执行时间', editable=False, db_index=True)
    actor = models.ForeignKey(User, verbose_name='执行者', on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=ACTION_TYPE, verbose_name='动作')
    content_type = models.ForeignKey(ContentType, verbose_name='内容类型', related_name='action_logs', null=True,
                                     blank=True, on_delete=models.SET_NULL)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    object_repr = models.CharField(max_length=255, null=True, verbose_name='object字符串形式')
    action_object = GenericForeignKey()  # 或GenericForeignKey("content_type", "object_id")
    change_message = models.TextField(verbose_name='改变信息')
    client_ip = models.GenericIPAddressField(null=True, verbose_name='客户端IP')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = ActionLogManager()

    class Meta:
        verbose_name = '行为日志'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def __str__(self):
        if self.object_repr:
            return f'{self.created_at} {self.actor} {self.get_action_display()} {self.object_repr}'
        return f'{self.created_at} {self.actor} {self.get_action_display()}'


class ViewLogManager(models.Manager):
    use_in_migrations = True

    def log_handler(self, actor, action, page_desc, page_url, client_ip):
        return self.model.objects.create(
            actor=actor,
            action=action,
            page_desc=page_desc,
            page_url=page_url,
            client_ip=client_ip
        )


class ViewLog(models.Model):
    """
    浏览日志，记录用户浏览记录
    使用viewset 一个地址有多个请求，最好把请求方法也加到日志里
    """
    ACTION_TYPE = (
        ('V', '浏览'),
        ('D', '导出')
    )

    action_time = models.DateTimeField(default=timezone.now, verbose_name='执行时间', editable=False, db_index=True)
    actor = models.ForeignKey(User, verbose_name='执行者', on_delete=models.CASCADE)
    action = models.CharField(max_length=2, choices=ACTION_TYPE, verbose_name='动作')
    page_desc = models.CharField(max_length=255, null=True, verbose_name='页面描述')
    page_url = models.URLField(null=True, verbose_name='页面URL')
    client_ip = models.GenericIPAddressField(null=True, verbose_name='客户端IP')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    client_type = models.CharField(max_length=255, default='PC', verbose_name='客户端类型')

    objects = ViewLogManager()

    class Meta:
        verbose_name = '浏览日志'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)
        default_permissions = ()
        permissions = (
            ('view_viewlog', '查看浏览日志'),
        )

    def __str__(self):
        if self.page_desc:
            return f'{self.action_time} {self.actor} {self.get_action_display()} {self.page_desc}'
        return f'{self.created_at} {self.actor} {self.get_action_display()}'
