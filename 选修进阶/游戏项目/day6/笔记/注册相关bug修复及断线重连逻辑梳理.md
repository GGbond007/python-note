1. 简历注意事项:
a. 如果你学校不是很好(非211),不要写教育背景这个模块;
b. 格式间距,模块之间间距要比模块内部段落之间宽一些;
c. 技术名词格式统一,尽量都用首字母大写;
d. 专业技能里不要太谦虚,最好不要写"有...经验,会用...";
e. 不要写教育平台,不要写蘑菇街; 不要出现"基于保利威...实现..."

2. 断线重连
断线: game/room/handlers/user_offline.py
	游戏开始了,断线  匹配场用户不能退出
					好友场可以退出
	游戏尚未开始或者在大厅, 断线   则用户退出
	用户断线消息源头在proxy/protocol.py onClose() (连接断开时触发)

重连:    game/room/handlers/user_reconnect.py
	游戏现场信息
		玩家信息: 座位号,杠信息,出牌信息...
		游戏桌子信息:桌子号, 状态,庄家是谁, 还剩多少张牌
		等待|计时任务:  如吃碰杠等倒计时

	房间现场信息: 用户名,金币,昵称...

游戏代码和框架的设计原则: 高内聚, 低耦合
房间和游戏的逻辑拆开
	房间只做房间的事,和任何游戏无关
	各游戏做各游戏的事
	交互: bridge_controller.py

gamedesk.py  游戏逻辑控制

3. 棋牌游戏规则
代码中 一般用 十六进制表示牌 0x12    最后一位表示牌值, 倒数第二位表示花色
							二万
							1*16+2 = 18


预习:

所有玩家准备完之后--游戏自动开始--> 发生了什么?  (洗牌,定庄,发牌,补花,出牌,...游戏结束)

明天: 胡牌架构设计/ 听牌, 癞子|万能牌
	  胡牌算法: 
	  	基本胡: 
	  		平胡: 4(个数)*3(顺子或刻子)+1*2(对子)
	  		七小对: 7*2(对子)
	  		十三幺: 13*1 ,  一万,九万, 一饼,九饼, 一条,九条, 东南西北中发白 
	  	特殊胡:
	  		碰碰胡
	  		清一色
	  		豪华七小对

	  		九连宝灯:  一万,一万,一万,二万,三万,四万,五万,六万,七万,八万,九万,九万,九万

后天:
玩家操作实现

第三天:
系统操作

第四天:
结算

第五天:
模拟机器人



注册功能跑起来 --- 注册完之后能自动登录
1. 自己选定的小项目
2. 学习一些小的三方技术: k8s, elk(elasticsearch, logstash, kibana), zabbix及自定义接口...
3. 预习就业素材