from django.contrib import admin
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_menu', 'icon']


admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.UserInfo)
admin.site.register(models.Role)
