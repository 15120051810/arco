from django.db import models
from users.models import User


# Create your models here.


class DownLoadCenter(models.Model):
    STATUS = (
        (1, "处理中"),
        (2, "可下载"),
        (3, "失败"),
    )
    name = models.CharField(max_length=228, verbose_name="名称")
    format = models.CharField(max_length=228, verbose_name="格式")
    data_number = models.IntegerField(null=True, blank=True, verbose_name="数据条数")
    data_size = models.CharField(max_length=228, null=True, blank=True, verbose_name="文件大小")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    status = models.SmallIntegerField(choices=STATUS, null=True, blank=True, default=1)
    download_link = models.TextField(null=True, blank=True, verbose_name="下载链接")
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="创建人")
    task_id = models.CharField(max_length=228, null=True, verbose_name="回调唯一标识")

    class Meta:
        verbose_name = '下载中心'
        verbose_name_plural = verbose_name
