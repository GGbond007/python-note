# Feed流系统

## Feed流的定义

Feed流是Feed + 流，Feed的本意是饲料，Feed流的本意就是有人一直在往一个地方投递新鲜的饲料，如果需要饲料，只需要盯着投递点就可以了，这样就能源源不断获取到新鲜的饲料。 在信息工程里面，Feed其实是一个信息单元，比如一条朋友圈状态、一条微博、一条咨询或一条短视频等，所以Feed流就是不停更新的信息单元，只要关注某些发布者就能获取到源源不断的新鲜信息，我们的用户也就可以在移动设备上逐条去浏览这些信息单元。

当前最流行的Feed流产品有微博、微信朋友圈、头条的资讯推荐、快手抖音的视频推荐等，还有一些变种，比如私信、通知等，这些系统都是Feed流系统，接下来我们会介绍如何设计一个Feed流系统架构。

## Feed流系统特点

Feed流本质上是数据流，是服务端系统将 “多个发布者的信息内容” 通过 “关注收藏等关系” 推送给 “多个接收者”。

![1579146889360](assets/1579146889360.png)

-   多账号内容流：Feed流系统中肯定会存在成千上万的账号，账号之间可以关注，取关，加好友和拉黑等操作。只要满足这一条，那么就可以当做Feed流系统来设计。
-   非稳定的账号关系：由于存在关注，取关等操作，所以系统中的用户之间的关系就会一直在变化，是一种非稳定的状态。
-   读写比例100:1：读写严重不平衡，读多写少。
-   消息必达性要求高：比如发送了一条朋友圈后，结果部分朋友看到了，部分朋友没看到，如果偏偏女朋友没看到，那么可能会产生很严重的感情矛盾，后果很严重。



## Feed流系统分类

Feed流的分类有很多种，但最常见的分类有两种：

-   Timeline：按发布的时间顺序排序，先发布的先看到，后发布的排列在最顶端，类似于微信朋友圈，微博等。这也是一种最常见的形式。产品如果选择Timeline类型，那么就是认为`Feed流中的Feed不多，但是每个Feed都很重要，都需要用户看到`。
-   Rank：按某个非时间的因子排序，一般是按照用户的喜好度排序，用户最喜欢的排在最前面，次喜欢的排在后面。这种一般假定用户可能看到的Feed非常多，而用户花费在这里的时间有限，那么就为用户选择出用户最想看的Top N结果，场景的应用场景有图片分享、新闻推荐类、商品推荐等。

上面两种是最典型，也是最常见的分类方式，另外的话，也有其他的分类标准，在其他的分类标准中的话，会多出两种类型：

-   Aggregate：聚合类型，比如好几个朋友都看了同一场电影，这个就可以聚合为一条Feed：A，B，C看了电影《你的名字》，这种聚合功能比较适合在客户端做。一般的Aggregate类型是Timeline类型 + 客户端聚合。
-   Notice：通知类型，这种其实已经是功能类型了，通知类型一般用于APP中的各种通知，私信等常见。这种也是Timeline类型，或者是Aggregate类型。



## 设计Feed流系统的2个核心

Feed流系统是一个数据流系统，如果要设计一个Feed流系统，最关键的两个核心，一个是数据存储(发布Feed)，一个是数据推送(读取Feed)。

这两个核心我们稍后再谈，我们先从数据层面看，数据分为三类，分别是：

-   发布者的数据：发布者发布数据，然后数据需要按照关注者进行组织，需要根据关注者查到所有数据，

    ​                          比如微博的个人页面、朋友圈的个人相册等。

-   关注关系：系统中个体间的关系，微博中是关注，是单向流，朋友圈是好友，是双向流。

    ​                   不管是单向还是双向，当发布者发布一条信息时，该条信息的流动永远是单向的。

-   粉丝的数据：从不同发布者那里获取到的数据，然后通过某种顺序（一般为时间timeline）组织到一起，

    ​                       比如微博首页、朋友圈首页等。

    ​                       这些数据具有时间热度属性，越新的数据越有价值，越新的数据就要排在最前面。

### Feed数据

针对这三类数据，我们可以定义为：

-   存储库：存储发布者的Feed数据，永久保存。我们已经存放到mysql中
-   关注表：用户关系表，永久保存。
-   同步库[未读池]:存储接收者的时间热度数据，只需要保留最近一段时间的数据即可。



### 数据存储

Feed消息的特点：

-   Feed信息的最大特点就是数据量大，而且在Feed流系统里面很多时候都会选择写扩散（推模式）模式，这时候数据量会再膨胀几个数量级，所以这里的数据量很容易达到100TB，甚至PB级别。

-   数据格式简单
-   数据不能丢失，可靠性要求高
-   自增主键功能，保证个人发的Feed的消息ID在个人发件箱中都是严格递增的，这样读取时只需要一个范围读取即可。由于个人发布的Feed并发度很低，这里用时间戳也能满足基本需求，但是当应用层队列堵塞，网络延迟变大或时间回退时，用时间戳还是无法保证严格递增。这里最好是有自增功能。



根据上述这些Feed数据的特征，最佳的系统应该是`具有主键自增功能的分布式NoSQL数据库`，但是在开源系统里面没有，所以常用的做法有两种：

-   关系型数据库 + 分库分表
-   关系型数据库 + 分布式NoSQL数据库：其中 关系型数据库提供主键自增功能。

目前业界大部分著名的Feed流产品，早期都是上面的2种模式之一，但是这会存在一个非常大的问题就是关系型数据库，比如开源MySQL数据库的主键自增功能性能差。不管是用MyISAM，还是InnoDB引擎，要保证自增ID严格递增，必须使用表锁，这个粒度非常大，会严重限制并发度，影响性能。

基于上述原因，部分技术公司早已经开始考虑使用表格存储(TableStore)。

表格存储是一个具有自增主键功能的分布式NoSQL数据库，这样就只需要使用一种系统即可，除此之外表格存储还有以下的特点：

-   天然分布式数据库，`无需分库分表`，单表可达10PB，10万亿行，可支持千万级TPS/QPS
-   号称SLA可用性可达到`10个9`，Feed内容不容易丢失。
-   主键自增功能性能极佳，其他所有系统在做自增功能的时候都需要加锁，但是表格存储的主键自增功能在写入自增列行的时候，完全不需要锁，既不需要表锁，也不需要行锁。



### 数据推送

数据推送的实现，有3种方案，分别是：

-   拉方案：也称为`读扩散`。很多Feed流产品的第一版会采用这种方案，但很快就抛弃了。
-   推方案：也成为`写扩散`。Feed流系统中最常用、有效的模式，用户关系数比较均匀，或者有上限，比较出名的有微信朋友圈。
-   推拉组合：大部分用户的账号关系都是几百个，但是有个别用户是1000万以上，比如微博。

| 类型         | 推模式      | 拉模式                               | 推拉结合模式 |
| :----------- | :---------- | :----------------------------------- | :----------- |
| 写放大       | 高          | 无                                   | 中           |
| 读放大       | 无          | 高                                   | 中           |
| 用户读取延时 | 毫秒        | 秒                                   | 秒           |
| 读写比例     | 1:99        | 99:1                                 | 50:50        |
| 系统要求     | 写能力强    | 读能力强                             | 读写都适中   |
| 常见系统     | 分布式NoSQL | 内存缓存或搜索系统<br>(推荐排序场景) | 两者结合     |
| 架构复杂度   | 简单        | 复杂                                 | 更复杂       |

-   如果产品中是双向关系，那么就采用推模式。
-   如果产品中是单向关系，且用户数少于1000万，那么也采用推模式，足够了。
-   如果产品是单向关系，单用户数大于1000万，那么采用推拉结合模式，这时候可以从推模式演进过来，不需要额外重新推翻重做。
-   永远不要只用拉模式。
-   如果是一个初创企业，先用推模式，快速把系统设计出来，然后让产品去验证、迭代，等客户数大幅上涨到1000万后，再考虑升级为推拉集合模式。

所以，接下来我们选择的是写扩散。

同步库表设计结构:

Table：user_message_table

| 主键列 | 第1列主键 | 第2列主键              | 第3列主键      | 第4列主键                                                    | 属性列                                     |
| :----- | :-------- | :--------------------- | :------------- | :----------------------------------------------------------- | :----------------------------------------- |
| 列名   | user_id   | sequence_id            | sender_id      | message_id                                                   | other                                      |
| 解释   | 接收者ID  | 消息顺序ID，要求自增。 | 发送者的用户ID | 消息ID。通过sender_id和message_id可以到存储库中查询到消息内容 | 其他字段内容，同步库中不需要包括消息内容。 |

关注或好友关系表设计结构：

Table：user_relation_table

| 主键顺序    | 第1列主键 | 第2列主键      | 属性列    | 属性列     |
| :---------- | :-------- | :------------- | :-------- | :--------- |
| Table字段名 | user_id   | follow_user_id | timestamp | other      |
| 备注        | 用户ID    | 粉丝用户ID     | 关注时间  | 其他属性列 |

未读池表设计结构：

Table: user_message_session_table

| 主键列顺序 | 第一列主键   | 属性列                                 |
| :--------- | :----------- | :------------------------------------- |
| 列名       | user_id      | last_sequence_id                       |
| 备注       | 接收者用户ID | 该接收者已经推送给客户端的最新的顺序ID |



# Feed流系统的实现前置准备

## tablestore

1. [开通阿里云表格存储服务](https://www.aliyun.com/product/ots?spm=a2c4g.11186623.2.7.6f0b23a5RBru3P)

   ![1579170876748](assets/1579170876748.png)

2. 到阿里云控制台中[创建AccessKey](https://help.aliyun.com/document_detail/53045.html?spm=a2c4g.11186623.2.8.6f0b23a5RBru3P)

   直接使用AccessKey或者子账号都可以,

   ![1579171212028](assets/1579171212028.png)

3. 获取python操作TableStore的[SDK](https://github.com/aliyun/aliyun-tablestore-python-sdk)

   <https://help.aliyun.com/document_detail/31723.html?spm=a2c4g.11186623.6.891.563c3d76sdVMpI>

```bash
pip install tablestore
```

settings/dev.py，添加TableStore的API接口配置

```python
# tablestore
OTS_ID = "LTAIVQuOJe2aotE5"
OTS_SECRET = "bEFFuAi7gqGwECW2KtL2r4KuhamvZS"
OTS_INSTANCE = "moluo"
OTS_ENDPOINT = "https://moluo.cn-hangzhou.ots.aliyuncs.com"
```

Tablestore目前只支持四种数据类型：INTEGER、STRING、DOUBLE和BOOLEAN。其中DOUBLE类型不能做主键类型，BOOLEAN不可以做主键的第一列(分区键)。

为了方便演示,所以我们另外创建一个单独的子应用store来编写tablestore的代码.

```
cd renranapi/apps
python ../../manage.py startapp store
```

在settings/dev.py注册,

```
INSALL_APPS = [
    'store', # 用于演示tableStore，后续删除掉即可
]
```



### 表操作

视图代码:

```python
# Create your views here.
from tablestore import TableMeta,TableOptions,ReservedThroughput,CapacityUnit,OTSClient
from tablestore import PK_AUTO_INCR
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

class TableAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)
    def post(self,request):
        """创建表"""
        # 设置主键和字段
        table_name = "user_message_table"

        # schema_of_primary_key = [
        # ('字段名', '字段类型', PK_AUTO_INCR),
        # ('uid', 'STRING')
        # ]
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ('sequence_id', 'INTEGER',PK_AUTO_INCR),
            ("sender_id",'INTEGER'),
            ("message_id",'INTEGER')
        ]
        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)
        # 设置数据的有效型
        table_option = TableOptions(7*86400, 5)
        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        # 创建数据
        self.client.create_table(table_meta, table_option, reserved_throughput)

        return Response({"message":"ok"})


    def delete(self,request):
        """删除表"""
        table = "user_message_table"
        self.client.delete_table(table)
        return Response({"message":"ok"})

    def get(self,request):
        """列出所有的表"""
        table_list = self.client.list_table()
        for table in table_list:
            print(table)

        return Response({"message": "ok"})
```

 ```
注意：
1. 创建表后需要 1 分钟进行加载，在此期间对该表的读/写数据操作均会失败。
   应用程序应该等待表加载完毕后再进行数据操作。
2. 创建表格存储的表时必须指定表的主键。
   主键包含 1~4 个主键列，每一个主键列都有名字和类型。
 ```

路由:

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    path("table/", views.TableAPIView.as_view()),
]

# 总路由
    path('ots/', include("store.urls")),
```



### 一条数据的操作

```python
from datetime import datetime
from tablestore import Row
class DataAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def post(self,rquest):
        """添加数据到表格中"""
        table_name = "user_message_table"
        # 主键列
        primary_key = [
            # ('主键名', 值),
            ('user_id', 3), # 接收Feed的用户ID
            ('sequence_id', PK_AUTO_INCR), # 如果是自增主键，则值就是 PK_AUTO_INCR
            ("sender_id",1), # 发布Feed的用户ID
            ("message_id",4), # 文章ID
        ]

        attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
        row = Row(primary_key, attribute_columns)
        consumed, return_row = self.client.put_row(table_name, row)
        print(return_row)

        return Response({"message":"ok"})

    def get(self,request):
        """获取指定数据"""
        table_name = "user_message_table"

        primary_key = [('user_id', 3), ('sequence_id', 1579245502645000),("sender_id",1), ("message_id",4)]

        # 需要返回的属性列：。如果columns_to_get为[]，则返回所有属性列。
        columns_to_get = []
        # columns_to_get = ['recevice_time', 'read_status', 'age', 'sex']

        consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)

        print( return_row.attribute_columns )
        # [('read_status', False, 1579245502645), ('recevice_time', 1579245502137.347, 1579245502645)]

        return Response({"message":"ok"})
    
```

路由,代码:

```python
    path("data/", views.DataAPIView.as_view()),
```



### 多条数据的操作

```python
from tablestore import INF_MAX,INF_MIN,CompositeColumnCondition,LogicalOperator,SingleColumnCondition,ComparatorType,Direction,Condition,RowExistenceExpectation,PutRowItem
from tablestore import BatchWriteRowRequest,TableInBatchWriteRowItem
class RowAPIView(APIView):
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    """多行数据操作"""
    def get(self,request):
        """按范围获取多行数据"""

        table_name = "user_message_table"

        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', 3),
            ('sequence_id', INF_MIN),
            ('sender_id', INF_MIN),
            ('message_id', INF_MIN)
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', 3),
            ('sequence_id', INF_MAX),
            ('sender_id', INF_MAX),
            ('message_id', INF_MAX)
        ]

        # 查询所有列
        columns_to_get = [] # 表示返回所有列
        limit = 5

        # 设置多条件
        # cond = CompositeColumnCondition(LogicalOperator.AND) # 逻辑条件
        # cond = CompositeColumnCondition(LogicalOperator.OR)
        # cond = CompositeColumnCondition(LogicalOperator.NOT)

        # 多条件下的子条件
        # cond.add_sub_condition(SingleColumnCondition("read_status", False, ComparatorType.EQUAL)) #  比较运算符:　等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.NOT_EQUAL)) #  比较运算符:　不等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.GREATER_THAN)) #  比较运算符:　大于
        # cond.add_sub_condition(SingleColumnCondition("recevice_time", 1579246049, ComparatorType.GREATER_EQUAL)) #  比较运算符:　大于等于
        # cond.add_sub_condition(SingleColumnCondition("属性列", '属性值', ComparatorType.LESS_THAN)) #  比较运算符:　小于
        # cond.add_sub_condition(SingleColumnCondition("recevice_time", 1579246049, ComparatorType.LESS_EQUAL)) #  比较运算符:　小于等于

        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name, # 操作表明
            Direction.FORWARD, # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key, # 取值范围
            columns_to_get, # 返回字段列
            limit, #　结果数量
            # column_filter=cond, # 条件
            max_version=1         # 返回版本数量
        )

        print("一共返回了：%s" % len(row_list))

        for row in row_list:
            print ( row.primary_key, row.attribute_columns )

        return Response({"message":"ok"})

    def post(self,request):
        """添加多条数据"""

        table_name = "user_message_table"

        put_row_items = []

        for i in range(0, 10):
            # 主键列
            primary_key = [  # ('主键名', 值),
                ('user_id', i), # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR), # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id",1), # 发布Feed的用户ID
                ("message_id",5), # 文章ID
            ]

            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        print(result)
        print(result.is_all_succeed())

        return Response({"message":"ok"})
```

多行路由,代码:

```python
    path("row/", views.RowAPIView.as_view()),
```





## Django自定义终端命令

1.  在app子应用 home目录下创建`management`包，并在`management`包下面创建命令包目录`commands`，`commands`下面就可以创建命令模块文件了。【注意，app子应用必须注册到INSTALL_APPS应用列表中】

2. 在commands包下面创建命令文件，并在文件中声明命令类，例如：tablestore.py，代码：

   ```python
   from django.core.management import BaseCommand
   
   class Command(BaseCommand):
       help = """测试命令的帮助文档"""
   
       def add_arguments(self,parser):
           """参数设置"""
           parser.add_argument("argument",nargs="*", help="必填参数的说明") # 位置参数
           parser.add_argument("--option",'-p', default=None, help="可选参数的说明") # 选项参数
   
       def handle(self, *args, **options):
           """命令主方法
           options: 参数列表
           """
           argument = options.get("argument") # 获取位置参数
           option = options.get("option") # 获取位置参数
   
           self.stdout.write("argument: %s" % argument)
           self.stdout.write("option: %s" % option)
   
           if option is None:
               self.stdout.write("没有设置option选项参数")
   ```

   注意：

   ```
   1. 命令类必须继承于django.core.management.BaseCommand，并且类名必须叫Command。
   2. 命令名称就是文件名，例如，命令文件叫table，则终端下调用命令为： python manage.py table
   3. 命令参数左边加上--，则表示可选参数，可选参数建议设置默认值，方便在handle方法中判断进行默认处理。
   4. 命令参数如果没有--，则表示位置参数，则调用命令时，必须为当前命令传递参数，否则报错！
   ```

   

   接下来我们直接在项目中提供TableStore的操作用于创建Feed系统的表结构。

   ```python
   from django.core.management import BaseCommand
   from tablestore import *
   from django.conf import settings
   class Command(BaseCommand):
       help = """表格存储命令必须接收而且只接收1个命令参数，如下：
       create  表示创建项目使用的表格
       delete  表示删除项目使用的表格
       """
   
       def add_arguments(self,parser):
           """参数设置"""
           parser.add_argument("argument",nargs="*", help="操作类型") # 位置参数
   
       def handle(self, *args, **options):
           """表格存储的初始化"""
           argument = options.get("argument")
           if len(argument)==1:
               if argument[0] == "create":
                   """创建表格"""
                   self.create_table()
   
               elif argument[0] == "delete":
                   """删除表格"""
                   self.delete_table()
               else:
                   self.stdout.write(self.help)
           else:
               self.stdout.write(self.help)
   
       @property
       def client(self):
           return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)
   
       def set_table(self,table_name,schema_of_primary_key,time_to_live=-1):
           # 设置表的元信息
           table_meta = TableMeta(table_name, schema_of_primary_key)
           # 设置数据的有效型
           table_option = TableOptions(time_to_live=time_to_live, max_version=5)
           # 设置数据的预留读写吞吐量
           reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
           # 创建数据
           self.client.create_table(table_meta, table_option, reserved_throughput)
   
       def create_table(self):
           """创建表格"""
           # 创建存储库
           table_name = "user_message_table"
           schema_of_primary_key = [ # 主键列
               ('user_id', 'INTEGER'),
               ('sequence_id', 'INTEGER',PK_AUTO_INCR),
               ("sender_id",'INTEGER'),
               ("message_id",'INTEGER')
           ]
   
           self.set_table(table_name,schema_of_primary_key,time_to_live=7*86400)
           self.stdout.write("创建表格%s完成" % table_name)
   
           #　关系库
           table_name = "user_relation_table"
           # 主键列
           schema_of_primary_key = [
               ('user_id', 'INTEGER'),
               ("follow_user_id", 'INTEGER'),
           ]
           self.set_table(table_name, schema_of_primary_key)
           self.stdout.write("创建表格%s完成" % table_name)
   
           # 未读池
           table_name = "user_message_session_table"
           # 主键列
           schema_of_primary_key = [
               ('user_id', 'INTEGER'),
               ("last_sequence_id", 'INTEGER'),
           ]
           self.set_table(table_name, schema_of_primary_key)
           self.stdout.write("创建表格%s完成" % table_name)
   
       def delete_table(self):
           """删除表"""
           table_list = self.client.list_table()
           for table in table_list:
               self.client.delete_table(table)
               self.stdout.write("删除%s完成" % table)
   ```

   

以后,我们创建项目相关的表格,就可以使用`python manage.py create`,如果删除表格则`python manage.py delete`.



## 判断访问者是否关注了作者

在文章详情页中判断当前用户是否关注了文章作者

article/views.py,代码;

```python
from rest_framework.generics import RetrieveAPIView
from .serializers import ArticleInfoModelSerializer
from users.models import User
from tablestore import *
from django.conf import settings

class ArticleInfoAPIView(RetrieveAPIView):
    """文章详情"""
    serializer_class = ArticleInfoModelSerializer
    queryset = Article.objects.exclude(pub_date=None)
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if isinstance(request.user, User):
            """用户登录了"""
            user = request.user                                    # 访问者
            author_id = response.data.get("user").get("id")        # 文章作者

            if author_id != user.id:
                # 到tablestore里面查询当前访问者是否关注了文章作者
                table_name = "user_relation_table"

                primary_key = [('user_id', author_id), ('follow_user_id', user.id)]

                columns_to_get = []

                consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)

                if return_row is None:
                    """没有关注"""
                    is_follow = 1
                else:
                    """已经关注了"""
                    is_follow = 2

            else:
                is_follow = 3 # 当前用户就是作者

        else:
            """用户未登录"""
            is_follow = 0  # 当前访问者未登录


        response.data["is_follow"] = is_follow
        return response

```

在客户端中根据返回的关注状态`is_follow`来判断显示关注按钮

```vue
         <div class="_3U4Smb">
          <span class="FxYr8x"><a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer">{{article.user.nickname}}</a></span>
          <button data-locale="zh-CN" type="button" class="_3kba3h _1OyPqC _3Mi9q9 _34692-" v-if="article.is_follow==2"><span>已关注</span></button>
          <button data-locale="zh-CN" type="button" class="_3kba3h _1OyPqC _3Mi9q9 _34692-" v-else-if="article.is_follow!=3"><span>关注</span></button>
         </div>
```

## 用户关注文章的作者

服务端实现用户关注作者的api接口

users/views.py,代码:

```python
from tablestore import *
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def post(self,request):
        """粉丝关注作者"""
        follow = request.user # 粉丝ID
        author_id = request.data.get("author_id") # 获取作者ID

        table_name = "user_relation_table"
        # 主键列
        primary_key = [('user_id', author_id), ('follow_user_id',follow.id)]
        attribute_columns = [('timestamp', datetime.now().timestamp())]
        row = Row(primary_key, attribute_columns)
        self.client.put_row(table_name, row)

        return Response({"message":"关注成功!"})

    def delete(self,request):
        """粉丝取关作者"""
        follow = request.user # 粉丝ID
        author_id = int(request.query_params.get("author_id")) # 获取作者ID
        table_name = "user_relation_table"
        # 主键列
        primary_key = [('user_id', author_id), ('follow_user_id',follow.id)]
        row = Row(primary_key)
        consumed, return_row = self.client.delete_row(table_name, row, None)
        return Response({"message": "取消关注成功!"})
```

路由代码:

```python
from django.urls import path,re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
	# ...
    path("follow/", views.FollowAPIView.as_view() ),
]
```

客户端发送请求,申请 关注/取消关注

```vue
<template>
  <div class="_21bLU4 _3kbg6I">
   <Header></Header>
   <div class="_3VRLsv" role="main">
    <div class="_gp-ck">
     <section class="ouvJEz">
      <h1 class="_1RuRku">{{article.title}}</h1>
      <div class="rEsl9f">
       <div class="_2mYfmT">
        <a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer"><img class="_13D2Eh" :src="article.user.avatar" alt="" /></a>
        <div style="margin-left: 8px;">
         <div class="_3U4Smb">
          <span class="FxYr8x"><a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer">{{article.user.nickname}}</a></span>
          <button data-locale="zh-CN" type="button" class="_3kba3h _1OyPqC _3Mi9q9 _34692-" v-if="article.is_follow==2" @click="follow_author(false)"><span>已关注</span></button>
          <button data-locale="zh-CN" type="button" class="_3kba3h _1OyPqC _3Mi9q9 _34692-" v-else-if="article.is_follow!=3" @click="follow_author(true)"><span>关注</span></button>
         </div>
         <div class="s-dsoj">
          <time>{{article.pub_date|dateformat}}</time>
          <span>字数 {{article.content.length}}</span>
          <span>阅读 {{article.read_count}}</span>
         </div>
        </div>
       </div>
      </div>
      <article class="_2rhmJa">
       <div class="image-package">
        <div class="image-container" style="max-width: 640px; max-height: 420px; background-color: transparent;">
         <div class="image-container-fill" style="padding-bottom: 65.63%;"></div>
         <div class="image-view" data-width="640" data-height="420">
          <img src="https://upload-images.jianshu.io/upload_images/18529254-f62fac0d998cff23?imageMogr2/auto-orient/strip|imageView2/2/w/640/format/webp" />
         </div>
        </div>
        <div class="image-caption"></div>
       </div>
       <p>文/小鸟飞过</p>
       <p>罗曼&middot;罗兰说：“生活中最沉重的负担不是工作，而是无聊。”</p>
       <div class="image-package">
        <div class="image-container" style="max-width: 700px; max-height: 152px; background-color: transparent;">
         <div class="image-container-fill" style="padding-bottom: 14.069999999999999%;"></div>
         <div class="image-view" data-width="1080" data-height="152">
          <img src="http://upload-images.jianshu.io/upload_images/18529254-a932f0ad8fbd51bb?imageMogr2/auto-orient/strip|imageView2/2/w/1080/format/webp" />
         </div>
        </div>
        <div class="image-caption"></div>
       </div>
       <p><strong>废掉一个人最快的方法</strong></p>
       <p><strong>就是让他闲着</strong></p>
       <p>这段时间，综艺节目《妻子的浪漫旅行第三季3》正在热播，四对明星夫妻的相处模式曝光，也让观众更了解了曾经饱受争议的女人唐一菲。</p>
       <p>有人很喜欢她大大咧咧的女侠性格，有人为她叫屈，当然还是有人骂她，说她旧事重提。</p>
       <p>而我，则是觉得非常惋惜。</p>
       <p>唐一菲是中央戏剧学院表演系毕业，真正的科班出身。</p>
       <p>从2003年到2011年，基本保证每年都有作品，要么拍电视剧、要么拍电影，2008年出演新版《红楼梦》的秦可卿也是颇为动人。</p>
       <div class="image-package">
        <div class="image-container" style="max-width: 533px; max-height: 510px; background-color: transparent;">
         <div class="image-container-fill" style="padding-bottom: 95.67999999999999%;"></div>
         <div class="image-view" data-width="533" data-height="510">
          <img src="http://upload-images.jianshu.io/upload_images/18529254-d92ace292d78aecb?imageMogr2/auto-orient/strip|imageView2/2/w/533/format/webp" />
         </div>
        </div>
        <div class="image-caption"></div>
       </div>
       <p>可是自2012年结婚后，8年时间里，只拍了一部电视剧，就再也没了一点儿消息，仿佛整个人生都停滞了。</p>
       <p>她在《妻子3》中展现出的婚姻状态是非常可悲的。</p>
       <p>一喝酒，就是吐槽自己的人生被毁了。</p>
       <div class="image-package">
        <div class="image-container" style="max-width: 532px; max-height: 394px;">
         <div class="image-container-fill" style="padding-bottom: 74.06%;"></div>
         <div class="image-view" data-width="532" data-height="394">
          <img data-original-src="//upload-images.jianshu.io/upload_images/18529254-5f20af5bb10bfa12" data-original-width="532" data-original-height="394" data-original-format="image/jpeg" data-original-filesize="17915" data-image-index="3" style="cursor: zoom-in;" class="image-loading" />
         </div>
        </div>
        <div class="image-caption"></div>
       </div>
       <p>要么直接形容老公凌潇肃是缩头乌龟。</p>
       <div class="image-package">
        <div class="image-container" style="max-width: 506px; max-height: 360px;">
         <div class="image-container-fill" style="padding-bottom: 71.15%;"></div>
         <div class="image-view" data-width="506" data-height="360">
          <img data-original-src="//upload-images.jianshu.io/upload_images/18529254-f2478cdc59c7e193" data-original-width="506" data-original-height="360" data-original-format="image/jpeg" data-original-filesize="23772" data-image-index="4" style="cursor: zoom-in;" class="image-loading" />
         </div>
        </div>
        <div class="image-caption"></div>
       </div>
       <p>作者简介：小鸟飞过，富小书的人，富书专栏作者，写温暖的文字，传递美好的情感；本文首发富小书（ID：fxsfrc），你身边最好的闺蜜，富书2018重磅推出新书《好好生活》。</p>
       <p><strong>注：本文章图片来源网络，如有侵权，请联系删除。</strong></p>
      </article>
      <div></div>
      <div class="_1kCBjS">
       <div class="_18vaTa">
        <div class="_3BUZPB">
         <div class="_2Bo4Th" role="button" tabindex="-1" aria-label="给文章点赞">
          <i aria-label="ic-like" class="anticon">
           <svg width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class="">
            <use xlink:href="#ic-like"></use>
           </svg></i>
         </div>
         <span class="_1LOh_5" role="button" tabindex="-1" aria-label="查看点赞列表">8人点赞<i aria-label="icon: right" class="anticon anticon-right">
           <svg viewbox="64 64 896 896" focusable="false" class="" data-icon="right" width="1em" height="1em" fill="currentColor" aria-hidden="true">
            <path d="M765.7 486.8L314.9 134.7A7.97 7.97 0 0 0 302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 0 0 0-50.4z"></path>
           </svg></i></span>
        </div>
        <div class="_3BUZPB">
         <div class="_2Bo4Th" role="button" tabindex="-1">
          <i aria-label="ic-dislike" class="anticon">
           <svg width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class="">
            <use xlink:href="#ic-dislike"></use>
           </svg></i>
         </div>
        </div>
       </div>
       <div class="_18vaTa">
        <a class="_3BUZPB _1x1ok9 _1OhGeD" href="/nb/38290018" target="_blank" rel="noopener noreferrer"><i aria-label="ic-notebook" class="anticon">
          <svg width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class="">
           <use xlink:href="#ic-notebook"></use>
          </svg></i><span>随笔</span></a>
        <div class="_3BUZPB ant-dropdown-trigger">
         <div class="_2Bo4Th">
          <i aria-label="ic-others" class="anticon">
           <svg width="1em" height="1em" fill="currentColor" aria-hidden="true" focusable="false" class="">
            <use xlink:href="#ic-others"></use>
           </svg></i>
         </div>
        </div>
       </div>
      </div>
      <div class="_19DgIp" style="margin-top:24px;margin-bottom:24px"></div>
      <div class="_13lIbp">
       <div class="_191KSt">
        &quot;小礼物走一走，来简书关注我&quot;
       </div>
       <button type="button" class="_1OyPqC _3Mi9q9 _2WY0RL _1YbC5u" @click="is_show_reward_window=true"><span>赞赏支持</span></button>
       <span class="_3zdmIj">还没有人赞赏，支持一下</span>
      </div>
      <div class="d0hShY">
       <a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer"><img class="_27NmgV" src="https://upload.jianshu.io/users/upload_avatars/18529254/.png?imageMogr2/auto-orient/strip|imageView2/1/w/100/h/100/format/webp" alt="  " /></a>
       <div class="Uz-vZq">
        <div class="Cqpr1X">
         <a class="HC3FFO _1OhGeD" href="/u/a70487cda447" title="書酱" target="_blank" rel="noopener noreferrer">書酱</a>
         <span class="_2WEj6j" title="你读书的样子真好看。">你读书的样子真好看。</span>
        </div>
        <div class="lJvI3S">
         <span>总资产0</span>
         <span>共写了78.7W字</span>
         <span>获得6,072个赞</span>
         <span>共1,308个粉丝</span>
        </div>
       </div>
       <button data-locale="zh-CN" type="button" class="_1OyPqC _3Mi9q9"><span>关注</span></button>
      </div>
     </section>
     <div id="note-page-comment">
      <div class="lazyload-placeholder"></div>
     </div>
    </div>
    <aside class="_2OwGUo">
     <section class="_3Z3nHf">
      <div class="_3Oo-T1">
       <a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer"><img class="_3T9iJQ" src="https://upload.jianshu.io/users/upload_avatars/18529254/.png?imageMogr2/auto-orient/strip|imageView2/1/w/90/h/90/format/webp" alt="" /></a>
       <div class="_32ZTTG">
        <div class="_2O0T_w">
         <div class="_2v-h3G">
          <span class="_2vh4fr" title="書酱"><a class="_1OhGeD" href="/u/a70487cda447" target="_blank" rel="noopener noreferrer">書酱</a></span>
         </div>
         <button data-locale="zh-CN" type="button" class="tzrf9N _1OyPqC _3Mi9q9 _34692-"><span>关注</span></button>
        </div>
        <div class="_1pXc22">
         总资产0
        </div>
       </div>
      </div>
      <div class="_19DgIp"></div>
     </section>
     <div>
      <div class="">
       <section class="_3Z3nHf">
        <h3 class="QHRnq8 QxT4hD"><span>推荐阅读</span></h3>
        <div class="cuOxAY" role="listitem">
         <div class="_3L5YSq" title="这些话没人告诉你，但必须知道的社会规则">
          <a class="_1-HJSV _1OhGeD" href="/p/a3e56a0559ff" target="_blank" rel="noopener noreferrer">这些话没人告诉你，但必须知道的社会规则</a>
         </div>
         <div class="_19haGh">
          阅读 5,837
         </div>
        </div>
        <div class="cuOxAY" role="listitem">
         <div class="_3L5YSq" title="浙大学霸最美笔记曝光：真正的牛人，都“变态”到了极致">
          <a class="_1-HJSV _1OhGeD" href="/p/d2a3724e2839" target="_blank" rel="noopener noreferrer">浙大学霸最美笔记曝光：真正的牛人，都“变态”到了极致</a>
         </div>
         <div class="_19haGh">
          阅读 12,447
         </div>
        </div>
        <div class="cuOxAY" role="listitem">
         <div class="_3L5YSq" title="征服一个女人最好的方式：不是讨好她，而是懂得去折腾她">
          <a class="_1-HJSV _1OhGeD" href="/p/f6acf67f039b" target="_blank" rel="noopener noreferrer">征服一个女人最好的方式：不是讨好她，而是懂得去折腾她</a>
         </div>
         <div class="_19haGh">
          阅读 5,311
         </div>
        </div>
        <div class="cuOxAY" role="listitem">
         <div class="_3L5YSq" title="告别平庸的15个小方法">
          <a class="_1-HJSV _1OhGeD" href="/p/cff7eb6b232b" target="_blank" rel="noopener noreferrer">告别平庸的15个小方法</a>
         </div>
         <div class="_19haGh">
          阅读 7,040
         </div>
        </div>
        <div class="cuOxAY" role="listitem">
         <div class="_3L5YSq" title="轻微抑郁的人，会说这3句“口头禅”，若你一个不占，偷着乐吧">
          <a class="_1-HJSV _1OhGeD" href="/p/2a0ca1729b4b" target="_blank" rel="noopener noreferrer">轻微抑郁的人，会说这3句“口头禅”，若你一个不占，偷着乐吧</a>
         </div>
         <div class="_19haGh">
          阅读 16,411
         </div>
        </div>
       </section>
      </div>
     </div>
    </aside>
   </div>
  <div class="_23ISFX-body" v-if="is_show_reward_window">
   <div class="_3uZ5OL">
    <div class="_2PLkjk">
     <img class="_2R1-48" src="https://upload.jianshu.io/users/upload_avatars/9602437/8fb37921-2e4f-42a7-8568-63f187c5721b.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/100/h/100/format/webp" alt="" />
     <div class="_2h5tnQ">
      给作者送糖
     </div>
    </div>
    <div class="_1-bCJJ">
     <div class="LMa6S_" :class="reward_money==item?'_1vONvL':''" @click="reward_money=item" v-for="item in reward_money_list">
      <span>{{item}}</span>
     </div>
    </div>
    <textarea class="_1yN79W" placeholder="给Ta留言..." v-model="reward_message"></textarea>
    <div class="_1_B577">
     选择支付方式
    </div>
    <div class="_1-bCJJ">
     <div class="LMa6S_ _3PA8BN" @click="reward_type=1" :class="reward_type==1?'_1vONvL':''">
      <span>支付宝</span>
     </div>
     <div class="LMa6S_ _3PA8BN" @click="reward_type=2" :class="reward_type==2?'_1vONvL':''">
      简书余额
     </div>
    </div>
    <button type="button" class="_3A-4KL _1OyPqC _3Mi9q9 _1YbC5u" @click="gotopay"><span>确认支付</span><span> ￥</span>{{reward_money}}</button>
   </div>
  </div>
   <Footer></Footer>
  </div>
</template>

<script>
    import Header from "./common/Header";
    import Footer from "./common/Footer";
    import '../../static/css/font-awesome/css/font-awesome.css';
    export default {
        name: "Article",
        data(){
          return {
             reward_money_list:[
                2,5,10,20,50
             ],
             reward_message: "", // 打赏的留言
             reward_money: 0, // 用户打赏金额
             reward_type: 1,  // 用户打赏的支付方式
             is_show_reward_window: false, // 是否显示文章打赏的窗口
             token: "",
             article:{
               content:"",
               user:{},
               collection:{},
             },
             article_id: 0,
             is_follow: false,
          }
        },
        components:{
          Header,
          Footer,
        },
        filters:{
          dateformat(date){
            date = new Date(date);
            return date.toLocaleDateString() + " " +date.toLocaleTimeString();
          }
        },
        created() {
          this.article_id = this.$route.params.id;
          this.token = this.get_login_user();
          this.get_article();
        },
        methods:{
           get_login_user(){
            // 获取登录用户
            return localStorage.user_token || sessionStorage.user_token;
          },
          get_article(){
            if(this.article_id<1){
              this.$message.error("参数有误！"); // 返回上一页
              return false;
            }

            let params = {};
            if(this.token){
              params = {
                Authorization: "jwt "+ this.token,
              }
            }

            this.$axios.get(`${this.$settings.Host}/article/${this.article_id}/`,{
              headers:params
            }).then(response=>{
              this.article = response.data;
            }).catch(error=>{
              this.$message.error("无法获取当前文章的内容！");
            })
          },
          gotopay(){
            // 发起请求，获取支付链接
            this.$axios.post(`${this.$settings.Host}/payments/alipay/`, {
                  "money": this.reward_money,
                  "article_id": this.article_id,
                  "type": this.reward_type,
                  "message": this.reward_message,
                },{
                    headers:{
                      Authorization: "jwt " + this.token
                    }
                }).then(response=>{
                  // 跳转到支付页面
                  this.$message.success("跳转支付页面中...请稍候")
                  setTimeout(()=>{
                    // 新建窗口打开
                    window.open(response.data,"_blank");
                    // 关闭打赏窗口
                    this.is_show_reward_window = false;
                  },2000);
                 }).catch(error=>{
                  this.$message.error("无法发起赞赏！");
                });
          },
          follow_author(opera){
             // 判断用户是否登录
            let self = this;　
            if(!this.token){
              this.$alert("对不起，您尚未登录，请登录后继续操作！","警告",{
                callback(){
                  self.$router.push("/user/login");
                }
              });
              return false;
            }

            if(opera){
                // 关注作者
                this.$axios.post(`${this.$settings.Host}/users/follow/`,{
                  author_id: this.article.user.id,
                },{
                  headers:{
                    Authorization: "jwt "+this.token,
                  }
                }).then(response=>{
                  this.article.is_follow = 2;
                }).catch(error=>{
                  this.$message.error("关注失败！请刷新页面以后重新操作！");
                });

            }else{
                // 取消关注
                this.$axios.delete(`${this.$settings.Host}/users/follow/`,{
                  params:{
                    author_id: this.article.user.id,
                  },
                  headers:{
                    Authorization: "jwt "+this.token,
                  }
                }).then(response=>{
                  this.article.is_follow = 1;

                }).catch(error=>{
                  this.$message.error("取消关注失败！请刷新页面以后重新操作！");
                });
            }
          }
        },
    }
</script>

<style scoped>
input,button{
  outline: 0;
}
</style>
```



作者发布文章以后, 推送Feed流

视图代码:

```python
# Create your views here.

from .models import ArticleImage
from rest_framework.generics import CreateAPIView
from .serializers import ArticleImageModelSerializer
class ImageAPIView(CreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageModelSerializer


from .models import ArticleCollection
from .serializers import ArticleCollectionModelSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CollecionAPIView(CreateAPIView, ListAPIView):
    """文集的视图接口"""
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework.generics import UpdateAPIView
from .serializers import ArticleCollectionDetailModelSerializer
class CollecionDetailAPIView(UpdateAPIView):
    """文集的视图接口"""
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionDetailModelSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleModelSerializer
from rest_framework.decorators import action
from rest_framework import status
from django_redis import get_redis_connection
from datetime import datetime
from django.db import transaction

class ArticleAPIView(ModelViewSet):
    """文章的视图集接口"""
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    @action(methods=["PUT"], detail=True)
    def save_article(self,request,pk):
        # 接收文章内容，标题，编辑次数，文章ID
        content = request.data.get("content")
        title = request.data.get("title")
        save_id = int( request.data.get("save_id") )
        collection_id = request.data.get("collection_id")
        user = request.user
        if save_id is None:
            save_id = 1
        else:
            save_id += 1

        # 验证文章是否存在
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"message":"当前文章不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 写入到redis中[先配置redis库]
        redis_conn = get_redis_connection("article")
        """
        article_<user_id>_<article>_<save_id>:{
            "title":   title,
            "content": content,
            "update_time": 1929293,
            "collection_id":collection_id,
        }
        """
        new_timestamp = datetime.now().timestamp()
        data = {
            "title": title,
            "content": content,
            "updated_time": new_timestamp,
            "collection_id": collection_id,
        }
        redis_conn.hmset("article_%s_%s_%s" % (user.id, pk, save_id), data)
        # 把用户针对当前文章的最新编辑记录ID保存起来
        redis_conn.hset("article_history_%s" % (user.id), pk, save_id )
        # 实现查看当前文章的编辑历史的思路：
        # article_edit_history = redis_conn.keys("article_%s_%s*" % (user.id, pk) )
        # data_list = []
        # for item in article_edit_history:
        #     ret = redis_conn.hgetall(item)
        #     data_list.append({
        #         "title": ret.get("title".encode()).decode(),
        #         "content": ret.get("content".encode()).decode(),
        #         "updated_time": ret.get("updated_time".encode()).decode(),
        #     })
        # print(data_list)
        # 返回结果
        return Response({"message":"保存成功！","save_id": save_id})

    def list(self, request, *args, **kwargs):
        user = request.user
        collection_id = request.query_params.get("collection")
        try:
            ArticleCollection.objects.get(pk=collection_id)
        except ArticleCollection.DoesNotExist:
            return Response({"message":"对不起，当前文集不存在！"})

        # 先到redis中查询
        redis_conn = get_redis_connection("article")
        history_dist = redis_conn.hgetall("article_history_%s" % (user.id) )
        data = []
        exclude_id = []
        if history_dist is not None:
            for article_id, save_id in history_dist.items():
                article_id = article_id.decode()
                save_id = save_id.decode()
                article_data_byte = redis_conn.hgetall("article_%s_%s_%s" % (user.id, article_id, save_id) )
                if article_data_byte["collection_id".encode()].decode() == collection_id:
                    data.append({
                        "id": article_id,
                        "title": article_data_byte["title".encode()].decode(),
                        "content": article_data_byte["content".encode()].decode(),
                        "save_id": save_id,
                        "collection": collection_id,
                    })
                    exclude_id.append(article_id)

        # 然后把redis中已经编辑过的内容结果排除出来，然后到MySQL中查询

        queryset = self.filter_queryset(self.get_queryset().filter(user=user, collection_id=collection_id).exclude(id__in=exclude_id) )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data +=serializer.data

        return Response(data)

    @action(methods=["patch"],detail=True)
    def pub_article(self,request,pk):
        """发布文章"""
        user    = request.user
        status  = request.data.get("is_pub")

        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                article = Article.objects.get(user=user, pk=pk)
            except:
                transaction.savepoint_rollback(save_id)
                return Response({"message":"当前文章不存在或者您没有修改的权限！"})

            if status:
                """发布文章"""
                article.pub_date = datetime.now()

                # 先查询到当前作者的粉丝 user_relation_table中查询　
                fens_list = self.get_fens(user.id)

                # 循环结果，把Feed进行推送
                if len(fens_list) > 0:
                    ret = self.push_feed(fens_list, user.id, article.id)
                    if not ret:
                        transaction.savepoint_rollback(save_id)
                        message = {"message": "发布文章失败！"}
                    else:
                        message = {"message": "发布文章成功！"}
                else:
                    message = {"message":"发布文章成功"}
            else:
                """私密文章，取消发布"""
                article.pub_date = None
                message = {"message":"取消发布成功"}

            # 从redis的编辑记录中提取当前文章的最新记录
            redis_conn = get_redis_connection("article")
            user_history_dist = redis_conn.hgetall("article_history_%s" % user.id)
            save_id = user_history_dist.get(pk.encode()).decode()
            article_dict = redis_conn.hgetall("article_%s_%s_%s" % (user.id, pk, save_id) )
            if article_dict is not None:
                article.title = article_dict["title".encode()].decode()
                article.content = article_dict["content".encode()].decode()
                timestamp = datetime.fromtimestamp(int(float(article_dict["updated_time".encode()].decode())))
                article.updated_time = timestamp
                article.save_id = save_id
            article.save()

            return Response(message)

    def push_feed(self, fens_list,author_id, article_id):
        """推送Feed给粉丝"""
        table_name = "user_message_table"

        put_row_items = []

        for i in fens_list:
            # 主键列
            primary_key = [  # ('主键名', 值),
                ('user_id', i),  # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id", author_id),  # 发布Feed的用户ID
                ("message_id", article_id),  # 文章ID
            ]

            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)

        return result.is_all_succeed()

    def get_fens(self, user_id):
        """获取当前用户的所有粉丝，后面自己整理下这个方法到工具库中"""
        table_name = "user_relation_table"

        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', user_id),
            ('follow_user_id', INF_MIN)
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', user_id),
            ('follow_user_id', INF_MAX)
        ]

        # 查询所有列
        columns_to_get = [] # 表示返回所有列

        # 范围查询接口
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            max_version=1  # 返回版本数量
        )

        fens_list = []
        for row in row_list:
            fens_list.append( row.primary_key[1][1] )

        return fens_list

    @action(methods=["patch"], detail=True)
    def change_collection(self, request, pk):
        """切换当前文章的文集ID"""
        user = request.user
        collection_id = request.data.get("collection_id")
        try:
            article = Article.objects.get(user=user, pk=pk)
        except:
            return Response({"message": "当前文章不存在或者您没有修改的权限！"})

        try:
            ArticleCollection.objects.get(user=user, pk=collection_id)
        except:
            return Response({"message": "当前文集不存在或者您没有修改的权限！"})

        # 当前文章如果之前有曾经被编辑，则需要修改redis中的缓存
        redis_conn = get_redis_connection("article")
        save_id_bytes = redis_conn.hget("article_history_%s" % (user.id),pk)
        if save_id_bytes is not None:
            save_id = save_id_bytes.decode()
            redis_conn.hset("article_%s_%s_%s" % (user.id, pk, save_id ), "collection_id", collection_id )
        article.collection_id = collection_id
        article.save()

        return Response({"message":"切换文章的文集成功！"})

from .models import Special,SpecialArticle
from .serializers import SpecialModelSerializer
class SpecialListAPIView(ListAPIView):
    queryset = Special.objects.all()
    serializer_class = SpecialModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        ret = self.get_queryset().filter(mymanager__user=user)
        article_id = request.query_params.get("article_id")
        # 验证文章

        queryset = self.filter_queryset(ret)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 返回专题对于当前文章的收录状态
        data = []
        for special in serializer.data:
            try:
                SpecialArticle.objects.get(article_id=article_id, special_id=special.get("id"))
                special["post_status"] = True # 表示当前文章已经被专题收录了
            except SpecialArticle.DoesNotExist:
                special["post_status"] = False  # 表示当前文章已经被专题收录了
            data.append(special)
        return Response(data)

class ArticlePostSpecialAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        """收录到我管理的专题"""
        article_id = request.data.get("article_id")
        special_id = request.data.get("special_id")
        user = request.user
        try:
            Article.objects.get(user=user, pk=article_id)
        except Article.DoesNotExist:
            return Response({"message": "当前文章不存在或者您没有操作的权限！"})

        try:
            Special.objects.get(mymanager__user=user, pk=special_id)
        except Article.DoesNotExist:
            return Response({"message": "当前专题不存在或者您没有操作的权限！"})

        SpecialArticle.objects.create(article_id=article_id,special_id=special_id)

        return Response({"message":"收录成功！"})

from rest_framework.generics import RetrieveAPIView
from .serializers import ArticleInfoModelSerializer
from users.models import User
from tablestore import *
from django.conf import settings

class ArticleInfoAPIView(RetrieveAPIView):
    """文章详情"""
    serializer_class = ArticleInfoModelSerializer
    queryset = Article.objects.exclude(pub_date=None)
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if isinstance(request.user, User):
            """用户登录了"""
            user = request.user                                    # 访问者
            author_id = response.data.get("user").get("id")        # 文章作者

            if author_id != user.id:
                # 到tablestore里面查询当前访问者是否关注了文章作者
                table_name = "user_relation_table"

                primary_key = [('user_id', author_id), ('follow_user_id', user.id)]

                columns_to_get = []

                consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)

                if return_row is None:
                    """没有关注"""
                    is_follow = 1
                else:
                    """已经关注了"""
                    is_follow = 2

            else:
                is_follow = 3 # 当前用户就是作者

        else:
            """用户未登录"""
            is_follow = 0  # 当前访问者未登录


        response.data["is_follow"] = is_follow
        return response
```



## 首页数据内容展示

首页数据在Feed流系统中, 需要考虑2大问题:

针对没有登录的游客显示内容的问题:

1. 纯粹的游客
2. 已经注册但是没有关注过任何作者

```
解决:
   1. 从数据库查找到热门内容推送给用户[评论量高的, 赞赏量高的, 点赞量高的]
      如果是登录用户, 在查看了内容后, 针对用户ID保存查看记录, 哪一篇用户看过了就记录到tablestore里面
      如果是游客, 1. 在本地存储中,记录用户的浏览历史
                 2. 在tablestore里面记录当前IP的浏览历史
```



针对登录的用户显示内容的问题:

1. 用户关注了很多作者 
2. 用户关注了作者很少, 这些作者可能没有新的内容产生



```python
解决推送内容不足的情况, 接下来我们可以根据用户行为进行分析的实现基于物品的协同过滤算法来计算出用户的兴趣, 进行智能推荐.
```

综合上面所述,我们必须要显示首页的内容先然后对显示的内容进行一下步骤的过滤

```
1. 判断用户是否登录
   1.1. 用户登录了
        1.1.1 用户已经关注了其他作者
          1.1.1.1 用户关注作者中,有足够的内容展示给用户
          1.1.1.2 用户关注作者中,没有足够内容展示给用户
        1.1.2 用户没有关注任何的作者
          1.1.1.1 根据浏览历史查找内容进行热度推荐
   1.2. 用户未登录
        1.1.3 根据浏览历史查找内容进行热度推荐
```



### 客户端根据用户的登录状态发起请求获取数据

```vue
<template>
  <div id="home">
    <Header></Header>
    <div class="container">
      <div class="row">
        <div class="main">
          <!-- Banner -->
          <div class="banner">
            <el-carousel height="272px" indicator-position="none" interval="2000">
              <el-carousel-item v-for="item in 4" :key="item">
                <h3 class="small">{{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div id="list-container">
            <!-- 文章列表模块 -->
            <ul class="note-list">
              <li class="">
                <div class="content">
                  <a class="title" target="_blank" href="">常做此运动，让你性福加倍</a>
                  <p class="abstract">运动，是人类在发展过程中有意识地对自己身体素质的培养的各种活动 运动的方式多种多样 不仅仅是我们常知的跑步，球类，游泳等 今天就为大家介绍一种男...</p>
                  <div class="meta">
                    <span class="jsd-meta">
                      <img src="/static/image/paid1.svg" alt=""> 4.8
                    </span>
                    <a class="nickname" target="_blank" href="">上班族也健身</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> 4
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> 31</span>
                  </div>
                </div>
              </li>
              <li class="have-img">
                <a class="wrap-img" href="" target="_blank">
                  <img class="img-blur-done" src="/static/image/10907624-107943365323e5b9.jpeg" />
                </a>
                <div class="content">
                  <a class="title" target="_blank" href="">“不耻下问”，正在毁掉你的人生</a>
                  <p class="abstract">
                    在过去，遇到不懂的问题，你不耻下问，找个人问问就行；在现在，如果你还这么干，多半会被认为是“搜商低”。 昨天，35岁的表姐把我拉黑了。 表姐是医...
                  </p>
                  <div class="meta">
                    <span class="jsd-meta">
                      <img src="/static/image/paid1.svg" alt=""> 6.7
                    </span>
                    <a class="nickname" target="_blank" href="">_飞鱼</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> 33
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> 113</span>
                    <span><img src="/static/image/shang.svg" alt=""> 2</span>
                  </div>
                </div>
              </li>
            </ul>
            <!-- 文章列表模块 -->
          </div>
        <a href="" class="load-more">阅读更多</a></div>
        <div class="aside">
          <!-- 推荐作者 -->
          <div class="recommended-author-wrap">
            <!---->
            <div class="recommended-authors">
              <div class="title">
                <span>推荐作者</span>
                <a class="page-change"><img class="icon-change" src="/static/image/exchange-rate.svg" alt="">换一批</a>
              </div>
              <ul class="list">
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>

              </ul>
              <a href="" target="_blank" class="find-more">查看全部 ></a>
              <!---->
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
  export default {
      name:"Home",
      data(){
          return {
            token:{},
            article_list:[]
          }
      },
      created(){
        this.token = this.get_login_user();
        this.get_article_list()
      },
      methods:{
          get_login_user(){
            // 获取登录用户
            return localStorage.user_token || sessionStorage.user_token;
          },
          get_article_list(){
            // 获取推送文章
            let headers = {};
            if(this.token){
              headers = {
                Authorization:"jwt " +this.token,
              }
            }
            this.$axios.get(`${this.$settings.Host}/home/article/`,{
              headers
            }).then(response=>{
              this.article_list = response.data;
            }).catch(eror=>{
              this.$message.error("获取推送文章失败！");
            });
          }
      },
      components:{
        Header,
        Footer,
      }
  }
</script>

```



### 服务端提供推送文章的内容

home/views.py,代码:

```python
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from article.models import Article
from .serializers import ArticleListModelSerializer
from .paginations import HomeArticlePageNumberPagination
from django.db.models import QuerySet
class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListModelSerializer
    pagination_class = HomeArticlePageNumberPagination

    def get_queryset(self):
        queryset = Article.objects.exclude(pub_date=None,).order_by("-reward_count","-comment_count","-like_count","-id")
        return queryset   
```

home/paginations.py,代码:

```python
from rest_framework.pagination import PageNumberPagination
class HomeArticlePageNumberPagination(PageNumberPagination):
    """首页推送文章的分页器"""
    page_query_param = "page" # 地址上面代表页码的参数名
    max_page_size = 20 # 每一页显示的最大数据量
    page_size = 10     # 默认每一页显示的数据量
    page_size_query_param = "size" # 地址上面代表数据量的参数名
```

home/serializers.py,代码:

```python
from rest_framework import serializers
from article.models import Article
from users.models import User
class ArticleAuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","nickname"]
        model = User
class ArticleListModelSerializer(serializers.ModelSerializer):
    user = ArticleAuthorModelSerializer()
    class Meta:
        model = Article
        fields = ["id","title","content","user","like_count","reward_count","comment_count"]
```

home/urls.py 子应用路由和总路由

```python
from django.urls import path
from . import views
urlpatterns = [
    path("article/", views.ArticleListAPIView.as_view() ),
]

# 总路由
    path('home/', include("home.urls")),
```



客户端展示内容 

```vue
<template>
  <div id="home">
    <Header></Header>
    <div class="container">
      <div class="row">
        <div class="main">
          <!-- Banner -->
          <div class="banner">
            <el-carousel height="272px" indicator-position="none" :interval="2000">
              <el-carousel-item v-for="item in 4" :key="item">
                <h3 class="small">{{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div id="list-container">
            <!-- 文章列表模块 -->
            <ul class="note-list">
<!--              <li class="">-->
<!--                <div class="content">-->
<!--                  <a class="title" target="_blank" href="">常做此运动，让你性福加倍</a>-->
<!--                  <p class="abstract">运动，是人类在发展过程中有意识地对自己身体素质的培养的各种活动 运动的方式多种多样 不仅仅是我们常知的跑步，球类，游泳等 今天就为大家介绍一种男...</p>-->
<!--                  <div class="meta">-->
<!--                    <span class="jsd-meta">-->
<!--                      <img src="/static/image/paid1.svg" alt=""> 4.8-->
<!--                    </span>-->
<!--                    <a class="nickname" target="_blank" href="">上班族也健身</a>-->
<!--                    <a target="_blank" href="">-->
<!--                      <img src="/static/image/comment.svg" alt=""> 4-->
<!--                    </a>-->
<!--                    <span><img src="/static/image/like.svg" alt=""> 31</span>-->
<!--                  </div>-->
<!--                </div>-->
<!--              </li>-->
              <li :class="check_img(article.content)?'have-img':''" v-for="article in article_list">
                <a class="wrap-img" href="" target="_blank" v-if="check_img(article.content)">
                  <img class="img-blur-done" :src="check_img(article.content)" />
                </a>
                <div class="content">
                  <router-link class="title" target="_blank" :to="`/article/${article.id}`">{{article.title}}</router-link>
                  <p class="abstract"　v-html="subtext(article.content,120)">
                  </p>
                  <div class="meta">
                    <a class="nickname" target="_blank" href="">{{article.user.nickname}}</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> {{article.comment_count}}
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> {{article.like_count}}</span>
                    <span v-if="article.reward_count>0"><img src="/static/image/shang.svg" alt=""> {{article.reward_count}}</span>
                  </div>
                </div>
              </li>
            </ul>
            <!-- 文章列表模块 -->
          </div>
        <a href="" class="load-more">阅读更多</a></div>
        <div class="aside">
          <!-- 推荐作者 -->
          <div class="recommended-author-wrap">
            <!---->
            <div class="recommended-authors">
              <div class="title">
                <span>推荐作者</span>
                <a class="page-change"><img class="icon-change" src="/static/image/exchange-rate.svg" alt="">换一批</a>
              </div>
              <ul class="list">
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>

              </ul>
              <a href="" target="_blank" class="find-more">查看全部 ></a>
              <!---->
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
  export default {
      name:"Home",
      data(){
          return {
            token:{},
            article_list:[
              {
                "user":{

                }
              }
            ]
          }
      },
      created(){
        this.token = this.get_login_user();
        this.get_article_list()
      },
      methods:{
          subtext(content,len=100){
            // 如果文章开头有图片，则过滤图片
            if(content){
              while (content.search("<img") != -1){
                content = content.replace(/<img.*?src="(.*?)".*?>/,"")
              }
              return content.split("").slice(0,len).join("")+'...';
            }
            return "";
          },
          check_img(content){
            if(content){
              let ret = content.match(/<img.*?src="(.*?)".*?>/)
              if(ret){
                return ret[1];
              }
            }

            return false;

          },
          get_login_user(){
            // 获取登录用户
            return localStorage.user_token || sessionStorage.user_token;
          },
          get_article_list(){
            // 获取推送文章
            let headers = {};
            if(this.token){
              headers = {
                Authorization:"jwt " +this.token,
              }
            }
            this.$axios.get(`${this.$settings.Host}/home/article/`,{
              headers
            }).then(response=>{
              this.article_list = response.data.results;
              this.article_count = response.data.count;
              this.new_article_list = response.data.next;
            }).catch(eror=>{
              this.$message.error("获取推送文章失败！");
            });
          }
      },
      components:{
        Header,
        Footer,
      }
  }
</script>
```

使用函数节流, 在用户频繁点击ajax按钮时, 阻止点击

```vue
<template>
  <div id="home">
    <Header></Header>
    <div class="container">
      <div class="row">
        <div class="main">
          <!-- Banner -->
          <div class="banner">
            <el-carousel height="272px" indicator-position="none" :interval="2000">
              <el-carousel-item v-for="item in 4" :key="item">
                <h3 class="small">{{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div id="list-container">
            <!-- 文章列表模块 -->
            <ul class="note-list">
<!--              <li class="">-->
<!--                <div class="content">-->
<!--                  <a class="title" target="_blank" href="">常做此运动，让你性福加倍</a>-->
<!--                  <p class="abstract">运动，是人类在发展过程中有意识地对自己身体素质的培养的各种活动 运动的方式多种多样 不仅仅是我们常知的跑步，球类，游泳等 今天就为大家介绍一种男...</p>-->
<!--                  <div class="meta">-->
<!--                    <span class="jsd-meta">-->
<!--                      <img src="/static/image/paid1.svg" alt=""> 4.8-->
<!--                    </span>-->
<!--                    <a class="nickname" target="_blank" href="">上班族也健身</a>-->
<!--                    <a target="_blank" href="">-->
<!--                      <img src="/static/image/comment.svg" alt=""> 4-->
<!--                    </a>-->
<!--                    <span><img src="/static/image/like.svg" alt=""> 31</span>-->
<!--                  </div>-->
<!--                </div>-->
<!--              </li>-->
              <li :class="check_img(article.content)?'have-img':''" v-for="article in article_list">
                <a class="wrap-img" href="" target="_blank" v-if="check_img(article.content)">
                  <img class="img-blur-done" :src="check_img(article.content)" />
                </a>
                <div class="content">
                  <router-link class="title" target="_blank" :to="`/article/${article.id}`">{{article.title}}</router-link>
                  <p class="abstract"　v-html="subtext(article.content,120)">
                  </p>
                  <div class="meta">
                    <a class="nickname" target="_blank" href="">{{article.user.nickname}}</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> {{article.comment_count}}
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> {{article.like_count}}</span>
                    <span v-if="article.reward_count>0"><img src="/static/image/shang.svg" alt=""> {{article.reward_count}}</span>
                  </div>
                </div>
              </li>
            </ul>
            <!-- 文章列表模块 -->
          </div>
        <a @click="get_next_article" class="load-more" v-if="new_article_list">阅读更多</a></div>
        <div class="aside">
          <!-- 推荐作者 -->
          <div class="recommended-author-wrap">
            <!---->
            <div class="recommended-authors">
              <div class="title">
                <span>推荐作者</span>
                <a class="page-change"><img class="icon-change" src="/static/image/exchange-rate.svg" alt="">换一批</a>
              </div>
              <ul class="list">
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>

              </ul>
              <a href="" target="_blank" class="find-more">查看全部 ></a>
              <!---->
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
  export default {
      name:"Home",
      data(){
          return {
            get_article_url:"",
            new_article_list:"",
            is_send_get_article_request:false, // 函数节流，判断当前ajax是否执行过程中
            token:{},
            article_list:[
              {
                "user":{

                }
              }
            ]
          }
      },
      created(){
        this.token = this.get_login_user();
        this.get_article_url = `${this.$settings.Host}/home/article/`;
        this.get_article_list()
      },
      methods:{
          subtext(content,len=100){
            // 如果文章开头有图片，则过滤图片
            if(content){
              while (content.search("<img") != -1){
                content = content.replace(/<img.*?src="(.*?)".*?>/,"")
              }
              return content.split("").slice(0,len).join("")+'...';
            }
            return "";
          },
          check_img(content){
            if(content){
              let ret = content.match(/<img.*?src="(.*?)".*?>/)
              if(ret){
                return ret[1];
              }
            }

            return false;

          },
          get_login_user(){
            // 获取登录用户
            return localStorage.user_token || sessionStorage.user_token;
          },
          get_article_list(){

            // 判断当前ajax是否正在执行
            if(this.is_send_get_article_request){
              this.$message.error("点击过于频繁！");
              return false;
            }

            this.is_send_get_article_request = true;

            // 获取推送文章
            let headers = {};
            if(this.token){
              headers = {
                Authorization:"jwt " +this.token,
              }
            }
            this.$axios.get(this.get_article_url,{
              headers
            }).then(response=>{
              if(!this.new_article_list){
                this.article_list = response.data.results;
              }else{
                this.article_list = this.article_list.concat(response.data.results);
              }
              this.article_count = response.data.count;
              this.new_article_list = response.data.next;

              // 开启再次执行ajax的状态
              this.is_send_get_article_request = false;
            }).catch(eror=>{
              this.$message.error("获取推送文章失败！");
            });
          },
          get_next_article(){
            this.get_article_url = this.new_article_list;
            this.get_article_list();
          }
      },
      components:{
        Header,
        Footer,
      }
  }
</script>

```

```
1. 判断用户是否登录
   1.1. 用户登录了
        1.1.1 用户已经关注了其他作者
          1.1.1.1 用户关注作者中,有足够的内容展示给用户
          1.1.1.2 用户关注作者中,没有足够内容展示给用户
        1.1.2 用户没有关注任何的作者
          1.1.1.1 根据浏览历史查找内容进行热度推荐
   1.2. 用户未登录
        1.1.3 根据浏览历史查找内容进行热度推荐
```

因为用户查看首页时, 显示的文章是不能重复的,所以接下来我们需要在每次推送文章给用户的时候,必须要进行记录:

## 实现用户和Feed内容的日志记录

用户和文章的推送日志

表格: user_message_log_table

| 第一主键 | (第二主键) | 属性列                                          |
| -------- | ---------- | ----------------------------------------------- |
| user_id  | message_id | is_push, is_read, is_like,is_reward, is_comment |

在home/management/commands/tablestore.py,自定义命令中,新增创建日志的命令:

```python
from django.core.management import BaseCommand
from tablestore import *
from django.conf import settings
class Command(BaseCommand):
    help = """表格存储命令必须接收而且只接收1个命令参数，如下：
    create  表示创建项目使用的表格
    delete  表示删除项目使用的表格
    """

    def add_arguments(self,parser):
        """参数设置"""
        parser.add_argument("argument",nargs="*", help="操作类型") # 位置参数

    def handle(self, *args, **options):
        """表格存储的初始化"""
        argument = options.get("argument")
        if len(argument)==1:
            if argument[0] == "create":
                """创建表格"""
                self.create_table()

            elif argument[0] == "delete":
                """删除表格"""
                self.delete_table()
            else:
                self.stdout.write(self.help)
        else:
            self.stdout.write(self.help)

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def set_table(self,table_name,schema_of_primary_key,time_to_live=-1):
        # 设置表的元信息
        table_meta = TableMeta(table_name, schema_of_primary_key)
        # 设置数据的有效型
        table_option = TableOptions(time_to_live=time_to_live, max_version=5)
        # 设置数据的预留读写吞吐量
        reserved_throughput = ReservedThroughput(CapacityUnit(0, 0))
        # 创建数据
        self.client.create_table(table_meta, table_option, reserved_throughput)

    def create_table(self):
        """创建表格"""
        # 创建存储库
        table_name = "user_message_table"
        schema_of_primary_key = [ # 主键列
            ('user_id', 'INTEGER'),
            ('sequence_id', 'INTEGER',PK_AUTO_INCR),
            ("sender_id",'INTEGER'),
            ("message_id",'INTEGER'),
        ]

        self.set_table(table_name,schema_of_primary_key,time_to_live=7*86400)
        self.stdout.write("创建表格%s完成" % table_name)

        #　关系库
        table_name = "user_relation_table"
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ("follow_user_id", 'INTEGER'),
        ]
        self.set_table(table_name, schema_of_primary_key)
        self.stdout.write("创建表格%s完成" % table_name)

        # 未读池
        table_name = "user_message_session_table"
        # 主键列
        schema_of_primary_key = [
            ('user_id', 'INTEGER'),
            ("last_sequence_id", 'INTEGER'),
        ]
        self.set_table(table_name, schema_of_primary_key)
        self.stdout.write("创建表格%s完成" % table_name)


        # 用户对文章的访问操作日志
        table_name = "user_message_log_table"
        schema_of_primary_key = [ # 主键列
            ('user_id', 'INTEGER'),
            ("message_id",'INTEGER'),
        ]
        self.set_table(table_name, schema_of_primary_key)
        self.stdout.write("创建表格%s完成" % table_name)

    def delete_table(self):
        """删除表"""
        table_list = self.client.list_table()
        for table in table_list:
            self.client.delete_table(table)
            self.stdout.write("删除%s完成" % table)
```

在首页获取推送内容时, 直接查询推送内容:

```python
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from article.models import Article
from .serializers import ArticleListModelSerializer
from .paginations import HomeArticlePageNumberPagination
from tablestore import *
from django.conf import settings
from users.models import User
from datetime import datetime
class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListModelSerializer
    pagination_class = HomeArticlePageNumberPagination

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def get_queryset(self):
        week_timestamp = datetime.now().timestamp() - 7 * 86400
        week_date = datetime.fromtimestamp(week_timestamp) # 获取一周前的时间对象
        queryset = Article.objects.filter(pub_date__gte=week_date).exclude(pub_date=None,).order_by("-reward_count","-comment_count","-like_count","-id")

        # 记录本次给用户推送文章的记录
        user = self.request.user

        if isinstance(user, User):
            # 判断tablestore中是否曾经推送过当前当前文章给用户
            queryset = self.check_user_message_log(user, queryset)

            if len(queryset)>0:
                article_id_list = []
                for item in queryset:
                    article_id_list.append(item.id)
                self.push_log(user.id, article_id_list)

        return queryset

    def check_user_message_log(self, user, queryset):
        """判断系统是否曾经推送过文章给用户"""
        columns_to_get = []
        rows_to_get = []
        for article in queryset:
            primary_key = [('user_id', user.id), ('message_id', article.id)]
            rows_to_get.append(primary_key)
        request = BatchGetRowRequest()
        table_name = "user_message_log_table"

        cond = CompositeColumnCondition(LogicalOperator.OR)
        cond.add_sub_condition(SingleColumnCondition("is_read", True, ComparatorType.EQUAL))
        cond.add_sub_condition(SingleColumnCondition("is_like", True, ComparatorType.EQUAL))

        request.add(TableInBatchGetRowItem(table_name, rows_to_get, columns_to_get,column_filter=cond, max_version=1))
        result = self.client.batch_get_row(request)
        table_result = result.get_result_by_table(table_name)
        push_id_list = []
        for item in table_result:
            if item.row is not None:
                push_id_list.append(item.row.primary_key[1][1])

        return queryset.exclude(id__in=push_id_list)

    def push_log(self, user_id, article_id_list):
        """推送文章给用户的记录"""
        table_name = "user_message_log_table"

        put_row_items = []

        for i in article_id_list:
            # 主键列
            primary_key = [
                ('user_id', user_id),  # 用户ID
                ("message_id", i),  # 文章ID
            ]

            attribute_columns = [('is_push', True), ('is_read', False), ('is_like', False), ('is_reward',False), ('is_comment',False)]

            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        return result.is_all_succeed()
```

在用户点击阅读文章以后, 更新阅读记录

```python
# Create your views here.

from .models import ArticleImage
from rest_framework.generics import CreateAPIView
from .serializers import ArticleImageModelSerializer
class ImageAPIView(CreateAPIView):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageModelSerializer


from .models import ArticleCollection
from .serializers import ArticleCollectionModelSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CollecionAPIView(CreateAPIView, ListAPIView):
    """文集的视图接口"""
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

from rest_framework.generics import UpdateAPIView
from .serializers import ArticleCollectionDetailModelSerializer
class CollecionDetailAPIView(UpdateAPIView):
    """文集的视图接口"""
    queryset = ArticleCollection.objects.all()
    serializer_class = ArticleCollectionDetailModelSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.viewsets import ModelViewSet
from .models import Article
from .serializers import ArticleModelSerializer
from rest_framework.decorators import action
from rest_framework import status
from django_redis import get_redis_connection
from datetime import datetime
from django.db import transaction

class ArticleAPIView(ModelViewSet):
    """文章的视图集接口"""
    queryset = Article.objects.all()
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]

    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    @action(methods=["PUT"], detail=True)
    def save_article(self,request,pk):
        # 接收文章内容，标题，编辑次数，文章ID
        content = request.data.get("content")
        title = request.data.get("title")
        save_id = int( request.data.get("save_id") )
        collection_id = request.data.get("collection_id")
        user = request.user
        if save_id is None:
            save_id = 1
        else:
            save_id += 1

        # 验证文章是否存在
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"message":"当前文章不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 写入到redis中[先配置redis库]
        redis_conn = get_redis_connection("article")
        """
        article_<user_id>_<article>_<save_id>:{
            "title":   title,
            "content": content,
            "update_time": 1929293,
            "collection_id":collection_id,
        }
        """
        new_timestamp = datetime.now().timestamp()
        data = {
            "title": title,
            "content": content,
            "updated_time": new_timestamp,
            "collection_id": collection_id,
        }
        redis_conn.hmset("article_%s_%s_%s" % (user.id, pk, save_id), data)
        # 把用户针对当前文章的最新编辑记录ID保存起来
        redis_conn.hset("article_history_%s" % (user.id), pk, save_id )
        # 实现查看当前文章的编辑历史的思路：
        # article_edit_history = redis_conn.keys("article_%s_%s*" % (user.id, pk) )
        # data_list = []
        # for item in article_edit_history:
        #     ret = redis_conn.hgetall(item)
        #     data_list.append({
        #         "title": ret.get("title".encode()).decode(),
        #         "content": ret.get("content".encode()).decode(),
        #         "updated_time": ret.get("updated_time".encode()).decode(),
        #     })
        # print(data_list)
        # 返回结果
        return Response({"message":"保存成功！","save_id": save_id})

    def list(self, request, *args, **kwargs):
        user = request.user
        collection_id = request.query_params.get("collection")
        try:
            ArticleCollection.objects.get(pk=collection_id)
        except ArticleCollection.DoesNotExist:
            return Response({"message":"对不起，当前文集不存在！"})

        # 先到redis中查询
        redis_conn = get_redis_connection("article")
        history_dist = redis_conn.hgetall("article_history_%s" % (user.id) )
        data = []
        exclude_id = []
        if history_dist is not None:
            for article_id, save_id in history_dist.items():
                article_id = article_id.decode()
                save_id = save_id.decode()
                article_data_byte = redis_conn.hgetall("article_%s_%s_%s" % (user.id, article_id, save_id) )
                if article_data_byte["collection_id".encode()].decode() == collection_id:
                    data.append({
                        "id": article_id,
                        "title": article_data_byte["title".encode()].decode(),
                        "content": article_data_byte["content".encode()].decode(),
                        "save_id": save_id,
                        "collection": collection_id,
                    })
                    exclude_id.append(article_id)

        # 然后把redis中已经编辑过的内容结果排除出来，然后到MySQL中查询

        queryset = self.filter_queryset(self.get_queryset().filter(user=user, collection_id=collection_id).exclude(id__in=exclude_id) )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data +=serializer.data

        return Response(data)

    @action(methods=["patch"],detail=True)
    def pub_article(self,request,pk):
        """发布文章"""
        user    = request.user
        status  = request.data.get("is_pub")

        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                article = Article.objects.get(user=user, pk=pk)
            except:
                transaction.savepoint_rollback(save_id)
                return Response({"message":"当前文章不存在或者您没有修改的权限！"})

            if status:
                """发布文章"""
                article.pub_date = datetime.now()

                # 先查询到当前作者的粉丝 user_relation_table中查询　
                fens_list = self.get_fens(user.id)

                # 循环结果，把Feed进行推送
                if len(fens_list) > 0:
                    ret = self.push_feed(fens_list, user.id, article.id)
                    if not ret:
                        transaction.savepoint_rollback(save_id)
                        message = {"message": "发布文章失败！"}
                    else:
                        message = {"message": "发布文章成功！"}
                else:
                    message = {"message":"发布文章成功"}
            else:
                """私密文章，取消发布"""
                article.pub_date = None
                message = {"message":"取消发布成功"}

            # 从redis的编辑记录中提取当前文章的最新记录
            redis_conn = get_redis_connection("article")
            user_history_dist = redis_conn.hgetall("article_history_%s" % user.id)
            save_id = user_history_dist.get(pk.encode()).decode()
            article_dict = redis_conn.hgetall("article_%s_%s_%s" % (user.id, pk, save_id) )
            if article_dict is not None:
                article.title = article_dict["title".encode()].decode()
                article.content = article_dict["content".encode()].decode()
                timestamp = datetime.fromtimestamp(int(float(article_dict["updated_time".encode()].decode())))
                article.updated_time = timestamp
                article.save_id = save_id
            article.save()

            return Response(message)

    def push_feed(self, fens_list,author_id, article_id):
        """推送Feed给粉丝"""
        table_name = "user_message_table"

        put_row_items = []

        for i in fens_list:
            # 主键列
            primary_key = [  # ('主键名', 值),
                ('user_id', i),  # 接收Feed的用户ID
                ('sequence_id', PK_AUTO_INCR),  # 如果是自增主键，则值就是 PK_AUTO_INCR
                ("sender_id", author_id),  # 发布Feed的用户ID
                ("message_id", article_id),  # 文章ID
            ]

            attribute_columns = [('recevice_time', datetime.now().timestamp()), ('read_status', False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)

        return result.is_all_succeed()

    def get_fens(self, user_id):
        """获取当前用户的所有粉丝，后面自己整理下这个方法到工具库中"""
        table_name = "user_relation_table"

        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', user_id),
            ('follow_user_id', INF_MIN)
        ]

        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', user_id),
            ('follow_user_id', INF_MAX)
        ]

        # 查询所有列
        columns_to_get = [] # 表示返回所有列

        # 范围查询接口
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            max_version=1  # 返回版本数量
        )

        fens_list = []
        for row in row_list:
            fens_list.append( row.primary_key[1][1] )

        return fens_list

    @action(methods=["patch"], detail=True)
    def change_collection(self, request, pk):
        """切换当前文章的文集ID"""
        user = request.user
        collection_id = request.data.get("collection_id")
        try:
            article = Article.objects.get(user=user, pk=pk)
        except:
            return Response({"message": "当前文章不存在或者您没有修改的权限！"})

        try:
            ArticleCollection.objects.get(user=user, pk=collection_id)
        except:
            return Response({"message": "当前文集不存在或者您没有修改的权限！"})

        # 当前文章如果之前有曾经被编辑，则需要修改redis中的缓存
        redis_conn = get_redis_connection("article")
        save_id_bytes = redis_conn.hget("article_history_%s" % (user.id),pk)
        if save_id_bytes is not None:
            save_id = save_id_bytes.decode()
            redis_conn.hset("article_%s_%s_%s" % (user.id, pk, save_id ), "collection_id", collection_id )
        article.collection_id = collection_id
        article.save()

        return Response({"message":"切换文章的文集成功！"})

from .models import Special,SpecialArticle
from .serializers import SpecialModelSerializer
class SpecialListAPIView(ListAPIView):
    queryset = Special.objects.all()
    serializer_class = SpecialModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        ret = self.get_queryset().filter(mymanager__user=user)
        article_id = request.query_params.get("article_id")
        # 验证文章

        queryset = self.filter_queryset(ret)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # 返回专题对于当前文章的收录状态
        data = []
        for special in serializer.data:
            try:
                SpecialArticle.objects.get(article_id=article_id, special_id=special.get("id"))
                special["post_status"] = True # 表示当前文章已经被专题收录了
            except SpecialArticle.DoesNotExist:
                special["post_status"] = False  # 表示当前文章已经被专题收录了
            data.append(special)
        return Response(data)

class ArticlePostSpecialAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        """收录到我管理的专题"""
        article_id = request.data.get("article_id")
        special_id = request.data.get("special_id")
        user = request.user
        try:
            Article.objects.get(user=user, pk=article_id)
        except Article.DoesNotExist:
            return Response({"message": "当前文章不存在或者您没有操作的权限！"})

        try:
            Special.objects.get(mymanager__user=user, pk=special_id)
        except Article.DoesNotExist:
            return Response({"message": "当前专题不存在或者您没有操作的权限！"})

        SpecialArticle.objects.create(article_id=article_id,special_id=special_id)

        return Response({"message":"收录成功！"})

from rest_framework.generics import RetrieveAPIView
from .serializers import ArticleInfoModelSerializer
from users.models import User
from tablestore import *
from django.conf import settings

class ArticleInfoAPIView(RetrieveAPIView):
    """文章详情"""
    serializer_class = ArticleInfoModelSerializer
    queryset = Article.objects.exclude(pub_date=None)
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if isinstance(request.user, User):
            """用户登录了"""
            user = request.user                                    # 访问者
            author_id = response.data.get("user").get("id")        # 文章作者

            # 用户对文章的阅读记录
            article_id = kwargs.get("pk")
            self.read_log(user.id, article_id)

            if author_id != user.id:
                # 到tablestore里面查询当前访问者是否关注了文章作者
                table_name = "user_relation_table"

                primary_key = [('user_id', author_id), ('follow_user_id', user.id)]

                columns_to_get = []

                consumed, return_row, next_token = self.client.get_row(table_name, primary_key, columns_to_get)

                if return_row is None:
                    """没有关注"""
                    is_follow = 1
                else:
                    """已经关注了"""
                    is_follow = 2

            else:
                is_follow = 3 # 当前用户就是作者

        else:
            """用户未登录"""
            is_follow = 0  # 当前访问者未登录

        response.data["is_follow"] = is_follow
        return response

    def read_log(self,user_id, article_id):
        """更新用户对文章的阅读记录"""
        table_name = "user_message_log_table"
        primary_key = [('user_id', int(user_id)), ('message_id', int(article_id))]
        update_of_attribute_columns = {
            'PUT': [('is_read', True)],
        }
        row = Row(primary_key, update_of_attribute_columns)
        condition = Condition(RowExistenceExpectation.IGNORE,
                              SingleColumnCondition("is_read", False, ComparatorType.EQUAL))  # update row on\
        consumed, return_row = self.client.update_row(table_name, row, condition)

```

