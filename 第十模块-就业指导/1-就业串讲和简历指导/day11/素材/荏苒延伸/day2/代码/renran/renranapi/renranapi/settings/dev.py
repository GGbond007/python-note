"""
Django settings for renranapi project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, os.path.join(BASE_DIR, "apps") )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '19q=^1v$qs$(=*-383oac&2sp)+wzb8ba7n87fs%r20awq+5o9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "api.renran.cn",
]

# CORS组的配置信息
CORS_ORIGIN_WHITELIST = (
    'http://www.renran.cn:8080',
    'http://www.moluo.net:8080',
)
CORS_ALLOW_CREDENTIALS = False  # 允许ajax跨域请求时携带cookie

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'xadmin',
    'crispy_forms',
    'reversion',
    'rest_framework',
    'haystack',

    'users',
    'home',
    'oauth',
    'article',
    'payments',
    'store', # 用于演示tableStore，后续删除掉即可

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'renranapi.urls'

# 模板引擎
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'renranapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "renran_user",
        "PASSWORD": "renran",
        "NAME": "renran",
    }
}

# 设置redis缓存
CACHES = {
    # 默认缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 项目上线时,需要调整这里的路径
        "LOCATION": "redis://127.0.0.1:6379/0",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供给xadmin或者admin的session存储
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供存储短信验证码
    "sms_code":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 提供存储文章内容
    "article":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 设置xadmin用户登录时,登录信息session保存到redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# 访问静态文件的url地址前缀
STATIC_URL = '/static/'
# 设置django的静态文件目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]

# 项目中存储上传文件的根目录[暂时配置]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT=os.path.join(BASE_DIR,"uploads")
# 访问上传文件的url地址前缀
MEDIA_URL ="/media/"



# log settings
# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { # 日志的处理格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/renran.log"),
            # 单个日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 备份日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose'
        },
    },
    # 日志对象
    'loggers': {
        'django': { # 固定，将来django内部也会有异常的处理，只会调用django下标的日志对象
            'handlers': ['console', 'file'],
            'propagate': True, # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}



# drf配置
REST_FRAMEWORK = {
    # 异常处理进行自定义设置
    'EXCEPTION_HANDLER': 'renranapi.utils.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]

# 腾讯防水墙配置
TENCENT_CAPTCHA = {
    "GATEWAY": "https://ssl.captcha.qq.com/ticket/verify",
    "APPID": "2086888489",
    "App_Secret_Key": "0TGMvQXvBZ54r9bOWrNYEhA**",
}

# 云通讯短信接口配置
SMS = {
    # 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
    "_accountSid":'8a216da863f8e6c20164139687e80c1b',

    # 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
    "_accountToken":'6dd01b2b60104b3dbc88b2b74158bac6',

    # 请使用管理控制台首页的APPID或自己创建应用的APPID
    "_appId":'8a216da863f8e6c20164139688400c21',

    # 说明：请求地址，生产环境配置成app.cloopen.com
    "_serverIP":'sandboxapp.cloopen.com',

    # 说明：请求端口 ，生产环境为8883
    "_serverPort": "8883",

    # 注册登录短信的发送模板ID,1为测试模板
    "_templateID": 1,
}

# 客户端的站点域名
CLIENT_HOST = "http://www.renran.cn:8080"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件服务器的地址
EMAIL_HOST = 'smtp.163.com'
#　邮件发送的协议端口, QQ的话，是465，还要配置另一个配置 EMAIL_USE_SSL 的选项的值为True
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'mooluoo@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'renranwang2020'
#收件人看到的发件人
EMAIL_FROM = 'renran<mooluoo@163.com>'


# QQ第三方登录相关配置
# QQ登录参数
QQ_APP_ID = '101403367'
QQ_APP_KEY = '93112df14c10d6fde74baa62f5de95ab'
QQ_REDIRECT_URL = 'http://www.moluo.net:8080/oauth_callback.html'
QQ_STATE = "/"  # 用于保存登录成功后的跳转页面路径


# 自定义存储类
DEFAULT_FILE_STORAGE = 'renranapi.utils.fastdfs.fdfs_storage.FastDFSStorage'
# FastDFS
FDFS_URL = 'http://192.168.252.136:8888/'  # 访问图片的路径域名 ip地址修改为自己机器的ip地址
FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')


ALIAPY_CONFIG = {
    # "gateway_url": "https://openapi.alipay.com/gateway.do?", # 真实支付宝网关地址
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?", # 沙箱支付宝网关地址
    "appid": "2016091600523592",
    "app_notify_url": None,
    "app_private_key_path": os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem"),
    "alipay_public_key_path": os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem"),
    "sign_type": "RSA2",
    "debug": False,
    "return_url": "http://www.moluo.net:8080/user/wallet", # 同步回调地址
    "notify_url": "http://api.renran.cn:8000/payments/alipay/result", # 异步结果通知
}


# 表格存储的配置
# tablestore
OTS_ID = "LTAIVQuOJe2aotE5"                    # access_key_id
OTS_SECRET = "bEFFuAi7gqGwECW2KtL2r4KuhamvZS"  # access_key_secret
OTS_INSTANCE = "szpython67"                    # 表格存储的实例
OTS_ENDPOINT = "https://szpython67.cn-hangzhou.ots.aliyuncs.com"  # 实例所在的公网地址


# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # elasticsearch运行的服务器ip地址，端口号默认为9200
        'URL': 'http://192.168.252.144:9200/',
        # elasticsearch建立的索引库的名称，一般使用项目名作为索引库
        'INDEX_NAME': 'renran',
    },
}

# 设置在Django运行时，如果有数据产生变化(添加、修改、删除)，
# haystack会自动让Elasticsearch实时生成新数据的索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'