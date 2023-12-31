[TOC]

# DRF框架中常用的组件

为了方便接下来的学习，我们创建一个新的子应用 opt

```python
python manage.py startapp opt
```

提前在总路由和配置文件中注册子应用和配置总路由。

```python

# settings.py中注册子应用：
INSTALLED_APPS = [
	# ....
	'opt',        # drf的常用组件
]


# 总路由中加上：
	path("opt/",include("opt.urls")),
```



因为接下来的功能中需要使用到登陆功能，所以我们使用django内置admin站点并创建一个管理员.

```shell
python manage.py createsuperuser
```

![1557276390641](assets/1557276390641.png)

创建管理员以后，访问admin站点，先修改站点的语言配置

settings.py

```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

![1553043081445](assets/1553043081445.png)



访问admin 站点效果：

![1553043054133](assets/1553043054133.png)





# 1. 认证Authentication

可以在配置文件中配置全局默认的认证方案

/rest_framework/settings.py

```python
# 可以在项目的主应用的settings.py配置文件中加入以下配置覆盖全局默认的配置方案。
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # session认证
        'rest_framework.authentication.BasicAuthentication',    # 基本认证
    )
}
```

也可以在每个视图中通过设置authentication_classess类属性来设置

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView

class ExampleView(APIView):
    # 类属性
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self,request):
        pass
    
```

认证失败会有两种可能的返回值，这个需要我们配合权限组件来使用：

- 401 Unauthorized 未认证
- 403 Permission Denied 权限被禁止







# 2. 权限Permissions

权限控制可以限制用户对于视图的访问和对于具体数据模型对象的访问。

- 在执行视图的as_view()方法的dispatch()方法前，会先进行视图访问权限的判断
- 在通过get_object()获取具体模型对象时，会进行模型对象访问权限的判断

### 提供的权限

-   AllowAny 允许所有用户
-   IsAuthenticated 仅通过登录认证的用户
-   IsAdminUser 仅管理员用户
-   IsAuthenticatedOrReadOnly 已经登陆认证的用户可以对数据进行增删改操作，没有登陆认证的只能查看数据。

### 配置使用

chorme浏览器进入无痕模式的快捷键，Ctrl+Shift+N

可以在配置文件settings.py中全局设置默认的权限管理类，如

```python
# drf的配置信息，需要卸载django的配置文件，而且必须写在REST_FRAMEWORK的字典中，才能被drf识别
REST_FRAMEWORK = {
    ....
    #  权限[全局配置，所有的视图都会被影响到]
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # 已经登录认证的用户才能访问
    )
}
```

如果未指明，则采用如下默认配置

```python
'DEFAULT_PERMISSION_CLASSES': (
   'rest_framework.permissions.AllowAny',
)
```

也可以在具体的视图中通过permission_classes属性来设置，如

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ExampleView(APIView):
    permission_classes = (IsAuthenticated,)
    ...
```



### 举例

```python
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

class StudentAPIView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
```



### 自定义权限

如需自定义权限，需继承rest_framework.permissions.BasePermission父类，并实现以下两个任何一个方法或全部

- `.has_permission(self, request, view)`

  是否可以访问视图， view表示当前视图对象

- `.has_object_permission(self, request, view, obj)`

  是否可以访问数据模型对象， view表示当前视图， obj为模型数据对象

例如：

在当前子应用下，创建一个权限文件permissions.py中声明自定义权限类:

```python
from rest_framework.permissions import BasePermission

class IsXiaoMingPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.username == "xiaoming":
            return True
```

```python
from .permissions import IsXiaoMingPermission
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsXiaoMingPermission]
```





# 3. 限流Throttling

可以对接口访问的频次进行限制，以减轻服务器压力，或者实现特定的业务。

一般用于付费购买次数,投票等场景使用.

### 可选限流类

1） AnonRateThrottle

限制所有匿名未认证用户，使用IP区分用户。

使用`DEFAULT_THROTTLE_RATES['anon']` 来设置频次

2）UserRateThrottle

限制认证用户，使用User id 来区分。

使用`DEFAULT_THROTTLE_RATES['user']` 来设置频次

3）ScopedRateThrottle

限制用户对于每个视图的访问频次，使用ip或user id。

例如：

```
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...

class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```



## 使用

可以在配置文件中，使用`DEFAULT_THROTTLE_CLASSES` 和 `DEFAULT_THROTTLE_RATES`进行全局配置，

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ( # 启用的限制类
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {   # 限制频率
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

`DEFAULT_THROTTLE_RATES` 可以使用 `second`, `minute`, `hour` 或`day`来指明周期。

也可以在具体视图中通过throttle_classess属性来配置，如

```python
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = (UserRateThrottle,)
    ...
```

## 实例

全局配置中设置访问频率，settings.py代码：

```python
REST_FRAMEWORK = {
    # 权限[全局配置，会被局部配置覆盖]
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),

    # 限流
    # 'DEFAULT_THROTTLE_CLASSES': (  # 全局启用的限制类
    #     'rest_framework.throttling.AnonRateThrottle', # 匿名用户,游客
    #     'rest_framework.throttling.UserRateThrottle'  # 登录用户
    # ),
    'DEFAULT_THROTTLE_RATES': {  # 限制频率
        'anon': '3/minute',
        'user': '10/minute',
        'access': '5/minute', # 这个是自定义限流的频率配置
    }
}
```

视图代码：

```python
from students.models import Student
from students.serializers import StudentModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from .permission import ISMingGe
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
class Students8APIView(ModelViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()
    # 权限配置
    permission_classes = [AllowAny]
    # 限流配置
    # throttle_classes = [AnonRateThrottle,UserRateThrottle]
    # 自定义限流配置
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'access'
```



# 4. 过滤Filtering

对于列表数据可能需要根据字段进行过滤，我们可以通过添加django-fitlter扩展来增强支持。

```shel
pip install django-filter
```

在配置文件settings.py中增加过滤组件的设置：

```python
INSTALLED_APPS = [
    ...
    'django_filters',  # 需要注册应用，
]

REST_FRAMEWORK = {
    ...
    # 全局配置，也可以使用局部配置
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
```

在视图类中添加类属性filter_fields，指定可以过滤的字段

```python
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_fields = ('age', 'sex')

# 127.0.0.1:8000/opt/students/?sex=true  #单个过滤条件
# http://127.0.0.1:8000/opt/students/?sex=false&age=27 # 多个并列的过滤条件
```



# 5. 排序

对于列表数据，REST framework提供了**OrderingFilter**过滤器来帮助我们快速指明数据按照指定字段进行排序。

使用方法：

在类视图中设置filter_backends，使用`rest_framework.filters.OrderingFilter`过滤器，REST framework会在请求的查询字符串参数中检查是否包含了ordering参数，如果包含了ordering参数，则按照ordering参数指明的排序字段对数据集进行排序。

前端可以传递的ordering参数的可选字段值需要在ordering_fields中指明。

示例：

```python
class StudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('id', 'age')

# 127.0.0.1:8000/books/?ordering=-age
# -id 表示针对id字段进行倒序排序
# id  表示针对id字段进行升序排序
```



如果需要在过滤以后再次进行排序，则需要两者同步。要么一起写在全局配置中，要么一起写在视图类中。

```python
from rest_framework.generics import ListAPIView
from students.models import Student
from .serializers import StudentModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
class Student3ListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_fields = ('age', 'sex')
    # 因为排序配置和过滤配置使用同一个类属性，所以当视图中需要使用排序和过滤时，
    # 要么大家一起在视图类中局部配置，要么大家一起在全局中配置，否则会出现过滤组件使用无效的情况
    # filter_backends = [DjangoFilterBackend,OrderingFilter]
    ordering_fields = ('id', 'age')
   
```

配置文件：

```python
    # 过滤组件[全局引入]
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.OrderingFilter')

```





# 6. 分页Pagination

REST framework提供了分页的支持。

我们可以在配置文件中设置全局的分页方式，如：

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':  'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100  # 每页数目
}
```

```python
如果在配置settings.py文件中， 设置了全局分页，那么在drf中凡是调用了ListModelMixin的list()，都会自动分页。如果项目中出现大量需要分页的数据，只有少数部分的分页，则可以在少部分的视图类中关闭分页功能。
class 视图类(ListAPIView):
	pagination_class = None
```



也可通过自定义Pagination类，来为视图添加不同分页行为。在视图中通过`pagination_clas`属性来指明。

```python
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
class BookDetailView(RetrieveAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    pagination_class = LargeResultsSetPagination
```



## 可选分页器

1） **PageNumberPagination**

前端访问网址形式：

```http
GET  http://127.0.0.1:8000/students/?page=4
```

可以在子类中定义的属性：

- page_size 每页数目
- page_query_param 前端发送的页数关键字名，默认为"page"
- page_size_query_param 前端发送的每页数目关键字名，默认为None
- max_page_size 前端最多能设置的每页数量

```python
# 声明分页的配置类
from rest_framework.pagination import PageNumberPagination
class StandardPageNumberPagination(PageNumberPagination):
    # 默认每一页显示的数据量
    page_size = 2
    # 允许客户端通过get参数来控制每一页的数据量
    page_size_query_param = "size"
    max_page_size = 10
    # 自定义页码的参数名
    page_query_param = "p"

class StudentAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    pagination_class = StandardPageNumberPagination

# 127.0.0.1/four/students/?p=1&size=5
```

2）**LimitOffsetPagination**

前端访问网址形式：

```http
GET http://127.0.0.1/four/students/?limit=100&offset=100
```

可以在子类中定义的属性：

- default_limit 默认限制，默认值与`PAGE_SIZE`设置一直
- limit_query_param limit参数名，默认'limit'
- offset_query_param offset参数名，默认'offset'
- max_limit 最大limit限制，默认None

```python
from rest_framework.pagination import LimitOffsetPagination
class StandardLimitOffsetPagination(LimitOffsetPagination):
    # 默认每一页查询的数据量,类似上面的page_size
    default_limit = 2
    limit_query_param = "size"
    offset_query_param = "start"

class StudentAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    # 调用页码分页类
    # pagination_class = StandardPageNumberPagination
    # 调用查询偏移分页类
    pagination_class = StandardLimitOffsetPagination
```





# 7. 异常处理 Exceptions

REST framework提供了自定义异常处理，我们可以自定义的方式来编写异常处理函数。例如我们想在要创建一个自定义异常函数，

这个函数，我们保存到当前主应用中[注意在实际工作中，我们可以设置一个单独的独立的公共目录来保存这种公共的函数/工具/类库]。

drfdemo/exceptions.py，代码；

```python
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework import status
def custom_exception_handler(exc, context):
    """
    自定义异常处理函数
    :param exc: 异常对象，本次发生的异常对象
    :param context: 字典，异常出现时的执行上下文环境
    :return:
    """
    # 先让drf进行异常判断
    response = drf_exception_handler(exc, context)

    # 判断response对象是否为None
    if response is None:
        """出现drf不能处理的异常"""
        if isinstance(exc, DatabaseError):
            view = context.get("view")
            print('数据库报错，[%s]: %s' % (view, exc))
            return Response({"detail":"服务器内部错误!"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        if isinstance(exc, ZeroDivisionError):
            view = context.get("view")
            print("0不能作为除数! [%s]: %s" % (view, exc) )
            return Response({"detail":"服务器内部错误!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
```

在主应用的配置文件settings.py中声明自定义的异常处理

```python
REST_FRAMEWORK = {
    # 异常处理
    'EXCEPTION_HANDLER': 'drfdemo.exceptions.custom_exception_handler',
}
```

如果未声明，会采用默认的方式，如下

rest_frame/settings.py

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```



### REST framework定义的异常

- APIException drf中所有异常的父类
- ParseError 解析错误
- AuthenticationFailed 认证失败
- NotAuthenticated 尚未认证
- PermissionDenied 权限受限
- NotFound 未找到
- MethodNotAllowed 请求方式不支持
- NotAcceptable 要获取的数据格式不支持
- Throttled 超过限流次数
- ValidationError 校验失败

也就是说，很多的没有在上面列出来的异常，就需要我们在自定义异常中自己处理了。







# 8. 自动生成接口文档

官方文档：http://core-api.github.io/python-client/

REST framework可以自动帮助我们生成接口文档。

接口文档以网页的方式呈现。

自动接口文档能生成的是继承自`APIView`及其子类的视图。

## 8.1. 安装依赖

REST framewrok生成接口文档需要`coreapi`库的支持。

```python
pip install coreapi
```

## 8.2. 设置接口文档访问路径

在settings.py中配置接口文档。

```python
REST_FRAMEWORK = {
    # 。。。 其他选项
    # 接口文档
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}
```



在总路由中添加接口文档路径。

文档路由对应的视图配置为`rest_framework.documentation.include_docs_urls`，

参数`title`为接口文档网站的标题。

```python
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='站点页面标题'))
]
```



8.3. 文档描述说明的定义位置

1） 单一方法的视图，可直接使用类视图的文档字符串，如

```python
class BookListView(generics.ListAPIView):
    """
    返回所有图书信息.
    """
```

2）包含多个方法的视图，在类视图的文档字符串中，分开方法定义，如

```python
class BookListCreateView(generics.ListCreateAPIView):
    """
    get:
    返回所有图书信息.

    post:
    新建图书.
    """
```

3）对于视图集ViewSet，仍在类视图的文档字符串中封开定义，但是应使用action名称区分，如

```python
class BookInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    list:
    返回图书列表数据

    retrieve:
    返回图书详情数据

    latest:
    返回最新的图书数据

    read:
    修改图书的阅读量
    """
```

## 8.4. 访问接口文档网页

浏览器访问 127.0.0.1:8000/docs/，即可看到自动生成的接口文档。

![æ¥å£ææ¡£ç½é¡µ](assets/接口文档页面.png)

#### 两点说明：

1） 视图集ViewSet中的retrieve名称，在接口文档网站中叫做read

2）参数的Description需要在模型类或序列化器类的字段中以help_text选项定义，如：

```python
class Student(models.Model):
    ...
    age = models.IntegerField(default=0, verbose_name='年龄', help_text='年龄')
    ...
```

或

```python
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {
            'age': {
                'required': True,
                'help_text': '年龄'
            }
        }
```
