from stark.service.v1 import StarkHandler, StarkModelForm
from django.conf.urls import re_path
from django.shortcuts import HttpResponse
from django.utils.safestring import mark_safe
from web import models
from .base import PermissionHandler


class ConsultRecordModelForm(StarkModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = ['note', ]  # 只展示node字段


class ConsultRecordHandler(PermissionHandler, StarkHandler):
    change_list_template = 'consult_record.html'  # 默认用的changelist.html

    model_form_class = ConsultRecordModelForm

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "操作"
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">编辑</a> | <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=obj.pk, customer_id=customer_id),
            self.reverse_delete_url(pk=obj.pk, customer_id=customer_id))
        return mark_safe(tpl)

    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "操作"
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">编辑</a>' % (
            self.reverse_change_url(pk=obj.pk, customer_id=customer_id))
        return mark_safe(tpl)

    def display_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "操作"
        customer_id = kwargs.get('customer_id')
        tpl = '<a href="%s">删除</a>' % (
            self.reverse_delete_url(pk=obj.pk, customer_id=customer_id))
        return mark_safe(tpl)

    list_display = ['note', 'consultant', 'date']  # 自定义显示

    # 重构，url ， 每个用户 的跟进记录都有一条url
    def get_urls(self):  # 重写url
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$',
                    self.wrapper(self.changelist_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<customer_id>\d+)/$',
                    self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^change/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_change_url_name),
            re_path(r'^delete/(?P<customer_id>\d+)/(?P<pk>\d+)/$',
                    self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    # 重写,只能看到自己私户信息的记录
    def get_queryset(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')  # 取到具体哪个学员过滤
        # 获取session中的当前用户id，只有当前用户才能看自己的管理学员跟进
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)

    # 提交跟进记录视图
    def save(self, request, form, is_update, *args, **kwargs):
        """
        保存对象信息限制权限
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        # 必须是自己的客户才能添加，合法性校验
        object_exists = models.Customer.objects.filter(
            id=customer_id, consultant_id=current_user_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')
        if not is_update:
            # 因为隐藏了客户和顾问，所以默认给这两个参数赋值进去
            form.instance.customer_id = customer_id  # 客户id
            form.instance.consultant_id = current_user_id  # 销售id
        form.save()  # 设置上默认值后再save即可

    def get_change_object(self, request, pk, *args, **kwargs):
        """
        重构-修改页面，取对象
        查看对象信息限制选项
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        # 必须要当前用户，防止非法操作
        return models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                   customer__consultant_id=current_user_id).first()

    def get_delete_object(self, request, pk, *args, **kwargs):
        """
        删除对象信息限制权限
        """
        # 删除自定制
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        record_queryset = models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                              customer__consultant_id=current_user_id)
        if not record_queryset.exists():  # 过滤删除非法操作
            return HttpResponse('要删除的记录不存在，请重新选择')
        record_queryset.delete()
