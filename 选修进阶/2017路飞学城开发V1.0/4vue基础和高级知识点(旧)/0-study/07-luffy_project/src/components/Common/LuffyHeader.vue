<template>
  <!-- element-ui -->
 <el-container>
      <el-header height = '80px' >
            <div class="header">
                <div class="nav-left">
                    <img src="https://hcdn2.luffycity.com/media/frontend/activity/head-logo_1564141048.3435316.svg" alt="">
                </div>
                <div class="nav-center">
                  	<ul>
                  		<li v-for = '(list,index) in headerList' :key = 'list.id'>
                  			<router-link :to = '{name:list.name}'>
                  			 {{list.title}}
                  			</router-link>
                  		</li>
                  	</ul>
                </div>
                
                <!-- <el-dropdown> -->

               <div class="nav-right " v-if = 'userInfo.access_token' @mouseenter = 'enterHandler' @mouseleave ='leaveHandler'>
                 <router-link :to="{name:'Study'}"> <span class = 'el-dropdown-link'>我的教室</span> </router-link>
                 	<span class="user">{{userInfo.username}}</span>
                 	<!-- <img :src="userInfo.avatar" alt=""> -->
                 	<img src="https://hcdn2.luffycity.com/media/frontend/head_portrait/f443b52920fa4a0d9d778a6813c5dcfb.png" alt="">
                  <ul class="my_account" v-show = 'isShow'>
                      <li>
                        我的账户
                        <i>></i>
                      </li>
                      <li>
                        我的订单
                        <i>></i>
                      </li>
                      <li>
                        我的优惠券
                        <i>></i>
                      </li>
                      <li>
                        我的消息<span class="msg">(40)</span>
                        <i>></i>
                      </li>
                      <li @click ='shopCartInfo'>
                       购物车<span class="count"></span>
                        <i>></i>
                      </li>
                      <li>
                       退出
                        <i>></i>
                      </li>
                  </ul>
                </div> 
              <!-- </el-dropdown> -->
                <div class="nav-right" v-else>
                  <router-link :to = '{name:"Login"}'> <span>登录</span> </router-link>
                  &nbsp;| &nbsp;
                  <router-link :to='{name:"Register"}'> <span>注册</span> </router-link>

                </div>
            </div>
      </el-header>
    </el-container>


</template>

<script>
export default {
  name: 'LuffyHeader',
  data(){
    return {
        headerList:[
              {id:'1',name:'Home',title:'首页'},
              {id:'2',name:'Course',title:'免费课程'},
              {id:'3',name:'LightCourse',title:'轻课'},
              {id:'4',name:'Micro',title:'就业课'}
          ],
    isShow:false
 
    }
  },
  methods:{
    shopCartInfo(){
        this.$router.push({
            name:'purchase.shop'
        })
    },
    enterHandler(){
      this.isShow = true;
    },
    leaveHandler(){
      this.isShow = false;
    }

  },
  computed:{
    userInfo(){
      console.log(this.$store.state.userInfo);
      return this.$store.state.userInfo;
    }
  }
};
</script>

<style lang="css" scoped>
.el-header{
  border-bottom: #c9c9c9;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
}
.header{
  width: 1200px;
  height: 80px;
  line-height: 80px;
  margin: 0 auto;
}
.nav-left{
  float: left;
 margin-top: 10px;
}
.nav-center{
  float: left;
  margin-left: 100px;
}
.nav-center ul{
	overflow: hidden;
}
.nav-center  ul li{
	float: left;
	margin: 0 5px;
	/*width: 100px;*/
	padding: 0 20px;
	height: 80px;
	line-height: 80px;
	text-align: center;
}
.nav-center ul li a{
	color: #4a4a4a;
	width: 100%;
	height: 60px;
	display: inline-block;

}
.nav-center ul li a:hover{
	color: #B3B3B3;
}
.nav-center ul li a.is-active{
	    color: #4a4a4a;
    	     border-bottom: 4px solid #ffc210;
}
.nav-right{
  float: right;
  position: relative;
  z-index: 100;
  
}
.nav-right span{
  cursor: pointer;
}
.nav-right .user{
	margin-left: 15px;
}
.nav-right img{
	width: 26px;
	height: 26px;
	border-radius: 50%;
	display: inline-block;
	vertical-align: middle;
	margin-left: 15px;
}
.nav-right  ul{
  position: absolute;
  width: 221px;
  z-index: 100;
  font-size: 12px;
  top: 80px;
  background: #fff;
  border-top: 2px solid #d0d0d0;
    box-shadow: 0 2px 4px 0 #e8e8e8;
}
.nav-right ul li{
    height: 40px;
    color: #4a4a4a;
    padding-left: 30px;
    padding-right: 20px;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    transition: all .2s linear;
}
.nav-right ul li span.msg{
  margin-left: -80px;
  color: red;
}
.nav-right ul li span.count{
  margin-left: -100px;
  color: red;
}

</style>
