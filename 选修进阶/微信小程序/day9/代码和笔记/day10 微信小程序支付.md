# day10 微信小程序支付

## 1.沙箱环境

一个用于开发测试的环境。

## 2.微信小程序支付

### 2.1 微信小程序平台

- 个人
- 企业（微信支付）

### 2.2 商户平台账号（企业）

- 开通商户平台
- 小程序 和 商户平台账号关联

### 2.3 账号

- AppID
- 商户号
- 商户key（关键）



## 3. 微信支付的步骤

- 登录，获取用户openid
- 挑选商品去支付
  - 生成订单（待支付）
  - 用户扫码支付给微信
  - 微信通知咱们系统，咱们系统更改订单状态。 



## 4.案例

### 4.1 用户登录

- 小程序

  ```
  wx.login
  ```

- 后端

  ```
  通过wx_code获取openid
  ```



### 4.2 支付

- 小程序

  - 请求

- 后端

  - 统一下单-> prepay_id
  - prepay_id + 再签名，给前端返回

- 小程序

  ```
  wx.requestPayment
  ```

### 4.3 微信通知

- 向指定接口发送POST

  - 校验是否合法
  - 更改订单状态

- 问题

  - 为什么要再次进行校验？

  - 通知时服务器宕机如何解决？

    ```
    微信的通知如果没有执行成功，那么他会在24小时内向我们的服务器一直请求。
    ```

    

## 任务

1. 保证金页面

2. 集成微信支付的功能（支付宝支付）































