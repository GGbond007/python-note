<template>
    <div class="sign">
    <div class="logo"><a href="/"><img src="/static/image/nav-logo.png" alt="Logo"></a></div>
    <div class="main">


      <h4 class="title">
        <div class="normal-title">
                <router-link class="active" to="/user/login">登录</router-link>
                <b>·</b>
                <router-link id="js-sign-up-btn" to="/user/register">注册</router-link>
        </div>
      </h4>
      <div class="js-sign-in-container">
        <form id="new_session" action="" method="post">
            <div class="input-prepend restyle js-normal">
              <input placeholder="登录账号或手机号或邮箱" type="text" v-model="username" id="session_email_or_mobile_number">
              <i class="iconfont ic-user"></i>
            </div>
            <!-- 海外登录登录名输入框 -->

            <div class="input-prepend">
              <input placeholder="密码" type="password" v-model="password" id="session_password">
              <i class="iconfont ic-password"></i>
            </div>
            <div class="remember-btn">
              <input type="checkbox" value="true" checked="checked" v-model="remember_me" id="session_remember_me"><span>记住我</span>
            </div>
            <div class="forget-btn">
              <router-link to="/find_password">通过邮箱找回密码?</router-link>
            </div>
            <button class="sign-in-button" id="sign-in-form-submit-btn" type="button" @click.prevent="show_captcha">
              <span id="sign-in-loading"></span>登录
            </button>
        </form>
        <!-- 更多登录方式 -->
        <div class="more-sign">
          <h6>社交帐号登录</h6>
          <ul>
        <li id="weibo-link-wrap" class="">
          <a class="weibo" id="weibo-link">
            <i class="iconfont ic-weibo"></i>
          </a>
        </li>
        <li><a id="weixin" class="weixin" target="_blank" href=""><i class="iconfont ic-wechat"></i></a></li>
        <li><a id="qq" class="qq" target="_blank" href="" @click.prevent="qq_login"><i class="iconfont ic-qq_connect"></i></a></li>
      </ul>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
    import "../../static/js/TCaptcha";
    export default {
        name: "Login",
        data(){
          return {
             username:"",
             password:"",
             remember_me: false,
          }
        },
        methods:{
          // 登录
          loginhander(){
            this.$axios.post(this.$settings.Host+"/users/login/",
              {
                "username":this.username,
                "password":this.password
              }).then(response=>{
                  // 使用浏览器本地存储保存token
                  if (this.remember_me) {
                    // 记住登录
                    sessionStorage.removeItem("user_token");
                    sessionStorage.removeItem("user_id");
                    sessionStorage.removeItem("user_name");
                    sessionStorage.removeItem("user_avatar");
                    sessionStorage.removeItem("user_nickname");
                    localStorage.user_token = response.data.token;
                    localStorage.user_id = response.data.id;
                    localStorage.user_name = response.data.username;
                    localStorage.user_avatar = response.data.avatar;
                    localStorage.user_nickname = response.data.nickname;
                  } else {
                    // 未记住登录
                    localStorage.removeItem("user_token");
                    localStorage.removeItem("user_id");
                    localStorage.removeItem("user_name");
                    localStorage.removeItem("user_avatar");
                    localStorage.removeItem("user_nickname");
                    sessionStorage.user_token = response.data.token;
                    sessionStorage.user_id = response.data.id;
                    sessionStorage.user_name = response.data.username;
                    sessionStorage.user_avatar = response.data.avatar;
                    sessionStorage.user_nickname = response.data.nickname;
                  }

                  this.$confirm('登录成功, 欢迎回来！', '提示', {
                    confirmButtonText: '返回首页',
                    cancelButtonText: '返回上一页',
                    type: 'success'
                  }).then(() => {
                    this.$router.push("/");
                  }).catch(() => {
                    this.$router.go(-1);
                  });

              }).catch(error=>{
                  this.$message.error("登录失败！账号或密码错误！");
                  this.username = "";
                  this.password = "";
              })
          },
          show_captcha(){

            // 判断手机号或者密码是否为空！
            if(this.username.length<1 || this.password.length<1){
              return false; // 阻止代码继续往下执行
            }

            // 验证码
            let self = this;
            // 生成一个验证码对象
            var captcha1 = new TencentCaptcha(this.$settings.TC_captcha.app_id, function(res) {
              console.log(res);
              // res（未通过验证）= {ret: 1, ticket: null}

              // ticket	验证成功的票据，当且仅当ret=0时ticket有值
              // res（验证成功） = {ret: 0, ticket: "String", randstr: "String"}
              if (res.ret === 0) {
                // 随机码
                // api服务端校验验证码的结果
                self.$axios.get(`${self.$settings.Host}/users/captcha/`,{
                  params:{
                    ticket: res.ticket,
                    randstr: res.randstr,
                  }
                }).then(response=>{
                  // 进行登录处理
                  self.loginhander();
                }).catch(error=>{
                  self.$message.error("验证码校验错误！");
                })
              }
            });

            // 显示验证码
            captcha1.show();
          },
          qq_login(){
            // 第三方登录
            this.$axios.get(`${this.$settings.Host}/oauth/qq/url/`,{
              params: {
                state: "/",
              }
            }).then(response=>{
              location.href = response.data;
            }).catch(error=>{
              this.$message.error("对不起，ＱＱ登录异常！");
            });
          }
        },
    }
</script>

<style scoped>
input{
  outline: none;
}
*, :after, :before {
    box-sizing: border-box;
}
.sign {
	height: 100%;
	min-height: 750px;
	text-align: center;
	font-size: 14px;
	background-color: #f1f1f1
}

.sign:before {
	content: "";
	display: inline-block;
	height: 85%;
	vertical-align: middle
}

.sign .disable,.sign .disable-gray {
	opacity: .5;
	pointer-events: none
}

.sign .disable-gray {
	background-color: #969696
}

.sign .tooltip-error {
	font-size: 14px;
	line-height: 25px;
	white-space: nowrap;
	background: none
}

.sign .tooltip-error .tooltip-inner {
	max-width: 280px;
	color: #333;
	border: 1px solid #ea6f5a;
	background-color: #fff
}

.sign .tooltip-error .tooltip-inner i {
	position: static;
	margin-right: 5px;
	font-size: 20px;
	color: #ea6f5a;
	vertical-align: middle
}

.sign .tooltip-error .tooltip-inner span {
	vertical-align: middle;
	display: inline-block;
	white-space: normal;
	max-width: 230px
}

.sign .tooltip-error.right .tooltip-arrow-border {
	border-right-color: #ea6f5a
}

.sign .tooltip-error.right .tooltip-arrow-bg {
	left: 2px;
	border-right-color: #fff
}

.sign .slide-error {
	position: relative;
	padding: 10px 0;
	border: 1px solid #c8c8c8;
	border-radius: 4px
}

.sign .slide-error i {
	position: static!important;
	margin-right: 10px;
	color: #ea6f5a!important;
	vertical-align: middle
}

.sign .slide-error span {
	font-size: 15px;
	vertical-align: middle
}

.sign .slide-error div {
	margin-top: 10px;
	font-size: 13px
}

.sign .slide-error a {
	color: #3194d0
}

.sign .js-sign-up-forbidden {
	color: #999;
	padding: 80px 0 100px
}

.sign .js-sign-up-container .slide-error {
	border-bottom: none;
	border-radius: 0
}

.sign .logo {
	position: absolute;
	top: 56px;
	margin-left: 50px
}

.sign .logo img {
	width: 100px
}

.sign .main {
	width: 400px;
	margin: 60px auto 0;
	padding: 50px 50px 30px;
	background-color: #fff;
	border-radius: 4px;
	box-shadow: 0 0 8px rgba(0,0,0,.1);
	vertical-align: middle;
	display: inline-block
}

.sign .reset-title,.sign .title {
	margin: 0 auto 50px;
	padding: 10px;
	font-weight: 400;
	color: #969696
}

.sign .reset-title a,.sign .title a {
	padding: 10px;
	color: #969696
}

.sign .reset-title a:hover,.sign .title a:hover {
	border-bottom: 2px solid #ea6f5a
}

.sign .reset-title .active,.sign .title .active {
	font-weight: 700;
	color: #ea6f5a;
	border-bottom: 2px solid #ea6f5a
}

.sign .reset-title b,.sign .title b {
	padding: 10px
}

.sign .reset-title {
	color: #333;
	font-weight: 700
}

.sign form {
	margin-bottom: 30px
}

.sign form .input-prepend {
	position: relative;
	width: 100%
}

.sign form .input-prepend input {
	width: 100%;
	height: 50px;
	margin-bottom: 0;
	padding: 4px 12px 4px 35px;
	border: 1px solid #c8c8c8;
	border-radius: 0 0 4px 4px;
	background-color: hsla(0,0%,71%,.1);
	vertical-align: middle
}

.sign form .input-prepend i {
	position: absolute;
	top: 14px;
	left: 10px;
	font-size: 18px;
	color: #969696
}

.sign form .input-prepend span {
	color: #333
}

.sign form .input-prepend .ic-show {
	top: 18px;
	left: auto;
	right: 8px;
	font-size: 12px
}

.sign form .geetest-placeholder {
	height: 44px;
	border-radius: 4px;
	background-color: hsla(0,0%,71%,.1);
	text-align: center;
	line-height: 44px;
	font-size: 14px;
	color: #999
}

.sign form .restyle {
	margin-bottom: 0
}

.sign form .restyle input {
	border-bottom: none;
	border-radius: 4px 4px 0 0
}

.sign form .no-radius input {
	border-radius: 0
}

.sign form .slide-security-placeholder {
	height: 32px;
	background-color: hsla(0,0%,71%,.1);
	border-radius: 4px
}

.sign form .slide-security-placeholder p {
	padding-top: 7px;
	color: #999;
	margin-right: -7px
}

.sign .overseas-btn {
	font-size: 14px;
	color: #999
}

.sign .overseas-btn:hover {
	color: #2f2f2f
}

.sign .remember-btn {
	float: left;
	margin: 15px 0
}

.sign .remember-btn span {
	margin-left: 5px;
	font-size: 15px;
	color: #969696;
	vertical-align: middle
}

.sign .forget-btn {
	float: right;
	position: relative;
	margin: 15px 0;
	font-size: 14px
}

.sign .forget-btn a {
	color: #999
}

.sign .forget-btn a:hover {
	color: #333
}

.sign .forget-btn .dropdown-menu {
	top: 20px;
	left: auto;
	right: 0;
	border-radius: 4px
}

.sign .forget-btn .dropdown-menu a {
	padding: 10px 20px;
	color: #333
}

.sign #sign-in-loading {
	position: relative;
	width: 20px;
	height: 20px;
	vertical-align: middle;
	margin-top: -4px;
	margin-right: 2px;
	display: none
}

.sign #sign-in-loading:after {
	content: "";
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background-color: transparent
}

.sign #sign-in-loading:before {
	content: "";
	position: absolute;
	top: 50%;
	left: 50%;
	width: 20px;
	height: 20px;
	margin: -10px 0 0 -10px;
	border-radius: 10px;
	border: 2px solid #fff;
	border-bottom-color: transparent;
	vertical-align: middle;
	-webkit-animation: rolling .8s infinite linear;
	animation: rolling .8s infinite linear;
	z-index: 1
}

.sign .sign-in-button,.sign .sign-up-button {
	margin-top: 20px;
	width: 100%;
	padding: 9px 18px;
	font-size: 18px;
	border: none;
	border-radius: 25px;
	color: #fff;
	background: #42c02e;
	cursor: pointer;
	outline: none;
	display: block;
	clear: both
}

.sign .sign-in-button:hover,.sign .sign-up-button:hover {
	background: #3db922
}

.sign .sign-in-button {
	background: #3194d0
}

.sign .sign-in-button:hover {
	background: #187cb7
}

.sign .btn-in-resend,.sign .btn-up-resend {
	position: absolute;
	top: 7px;
	right: 7px;
	width: 100px;
	height: 36px;
	font-size: 13px;
	color: #fff;
	background-color: #42c02e;
	border-radius: 20px;
	line-height: 36px
}

.sign .btn-in-resend {
	background-color: #3194d0
}

.sign .sign-up-msg {
	margin: 10px 0;
	padding: 0;
	text-align: center;
	font-size: 12px;
	line-height: 20px;
	color: #969696
}

.sign .sign-up-msg a,.sign .sign-up-msg a:hover {
	color: #3194d0
}

.sign .overseas input {
	padding-left: 110px!important
}

.sign .overseas .overseas-number {
	position: absolute;
	top: 0;
	left: 0;
	width: 100px;
	height: 50px;
	font-size: 18px;
	color: #969696;
	border-right: 1px solid #c8c8c8
}

.sign .overseas .overseas-number span {
	margin-top: 17px;
	padding-left: 35px;
	text-align: left;
	font-size: 14px;
	display: block
}

.sign .overseas .dropdown-menu {
	width: 100%;
	max-height: 285px;
	font-size: 14px;
	border-radius: 0 0 4px 4px;
	overflow-y: auto
}

.sign .overseas .dropdown-menu li .nation-code {
	width: 65px;
	display: inline-block
}

.sign .overseas .dropdown-menu li a {
	padding: 6px 20px;
	font-size: 14px;
	line-height: 20px
}

.sign .overseas .dropdown-menu li a::hover {
	color: #fff;
	background-color: #f5f5f5
}

.sign .more-sign {
	margin-top: 50px
}

.sign .more-sign h6 {
	position: relative;
	margin: 0 0 10px;
	font-size: 12px;
	color: #b5b5b5
}

.sign .more-sign h6:before {
	left: 30px
}

.sign .more-sign h6:after,.sign .more-sign h6:before {
	content: "";
	border-top: 1px solid #b5b5b5;
	display: block;
	position: absolute;
	width: 60px;
	top: 5px
}

.sign .more-sign h6:after {
	right: 30px
}

.sign .more-sign ul {
	margin-bottom: 10px;
	list-style: none
}

.sign .more-sign ul li {
	margin: 0 5px;
	display: inline-block
}

.sign .more-sign ul a {
	width: 50px;
	height: 50px;
	line-height: 50px;
	display: block
}

.sign .more-sign ul i {
	font-size: 28px
}

.sign .more-sign .ic-weibo {
	color: #e05244
}

.sign .more-sign .ic-wechat {
	color: #00bb29
}

.sign .more-sign .ic-qq_connect {
	color: #498ad5
}

.sign .more-sign .ic-douban {
	color: #00820f
}

.sign .more-sign .ic-more {
	color: #999
}

.sign .more-sign .weibo-loading {
	pointer-events: none;
	cursor: pointer;
	position: relative
}

.sign .more-sign .weibo-loading:after {
	content: "";
	position: absolute;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background-color: #fff
}

body.reader-night-mode .sign .more-sign .weibo-loading:after {
	background-color: #3f3f3f
}

.sign .more-sign .weibo-loading:before {
	content: "";
	position: absolute;
	top: 50%;
	left: 50%;
	width: 20px;
	height: 20px;
	margin: -10px 0 0 -10px;
	border-radius: 10px;
	border: 2px solid #e05244;
	border-bottom-color: transparent;
	vertical-align: middle;
	-webkit-animation: rolling .8s infinite linear;
	animation: rolling .8s infinite linear;
	z-index: 1
}

@keyframes rolling {
	0% {
		-webkit-transform: rotate(0deg);
		transform: rotate(0deg)
	}

	to {
		-webkit-transform: rotate(1turn);
		transform: rotate(1turn)
	}
}

@-webkit-keyframes rolling {
	0% {
		-webkit-transform: rotate(0deg)
	}

	to {
		-webkit-transform: rotate(1turn)
	}
}

.sign .reset-password-input {
	border-radius: 4px!important
}

.sign .return {
	margin-left: -8px;
	color: #969696
}

.sign .return:hover {
	color: #333
}

.sign .return i {
	margin-right: 5px
}

.sign .icheckbox_square-green {
	display: inline-block;
	*display: inline;
	vertical-align: middle;
	margin: 0;
	padding: 0;
	width: 18px;
	height: 18px;
	background: url(/static/image/green.png) no-repeat;
	border: none;
	cursor: pointer;
	background-position: 0 0
}

.sign .icheckbox_square-green.hover {
	background-position: -20px 0
}

.sign .icheckbox_square-green.checked {
	background-position: -40px 0
}

.sign .icheckbox_square-green.disabled {
	background-position: -60px 0;
	cursor: default
}

.sign .icheckbox_square-green.checked.disabled {
	background-position: -80px 0
}


.geetest_panel_box>* {
	box-sizing: content-box
}

@media (max-width:768px) {
	body {
		min-width: 0
	}

	.sign {
		height: auto;
		min-height: 0;
		background-color: transparent
	}

	.sign .logo {
		display: none
	}

	.sign .main {
		position: absolute;
		left: 50%;
		margin: 0 0 0 -200px;
		box-shadow: none
	}
}
</style>
