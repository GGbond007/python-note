from django.db import models


class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='一级菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text='null表示不是菜单;非null表示是二级菜单')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.name
