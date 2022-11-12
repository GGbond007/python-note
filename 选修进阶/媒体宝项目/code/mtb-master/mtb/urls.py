"""mtb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from apps.base.views import wx
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/base/', include('apps.base.urls')),
    path('api/msg/', include('apps.msg.urls')),
    path('api/task/', include('apps.task.urls')),

    path('<str:filename>.txt', wx.file_verify),  # 微信调用
    path('auth/', wx.component_verify_ticket),  # 微信调用
    path('<str:authorizer_app_id>/callback', wx.event_callback),  # 微信调用

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
