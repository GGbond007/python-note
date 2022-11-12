from django.db import models


class Host(models.Model):
    """
    主机表
    """
    host = models.CharField(verbose_name='主机名', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP')

    def __str__(self):
        return self.host


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)

    def __str__(self):
        return self.title


class Project(models.Model):
    """
    项目表
    """
    title = models.CharField(verbose_name='项目名称', max_length=32)
