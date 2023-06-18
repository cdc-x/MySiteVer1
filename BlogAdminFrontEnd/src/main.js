// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import * as echarts from 'echarts';
import store from './store'
import { 
  Button, 
  Form, 
  FormItem, 
  Input, 
  Message, 
  Container, 
  Header, 
  Aside, 
  Main, 
  Menu, 
  Submenu,
  MenuItem, 
  Breadcrumb, 
  BreadcrumbItem, 
  Card, 
  Row, 
  Col, 
  Table, 
  TableColumn, 
  Switch, 
  Tooltip, 
  Pagination, 
  Dialog, 
  MessageBox,
  Select, 
  Option,
  DatePicker,
  Scrollbar,
  Carousel,
  CarouselItem,
  Tag,
  Empty,
  Link
} from 'element-ui'
import axios from 'axios'

/* 导入全局样式 */
import '@/assets/css/global.css'
import '@/assets/fonts/iconfont.css'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'

// 配置根本请求路径
axios.defaults.baseURL = "http://127.0.0.1:8000/"

// 通过请求拦截器在请求头中添加Token，所有的请求都会先经过这个拦截器
axios.interceptors.request.use((config)=>{
  // config为一个请求对象，里面包含了 headers 等各种属性
  config.headers.Authorization = window.sessionStorage.getItem("AUTHORIZATION")
  // 最后必须返回请求对象
  return config
})

// 响应拦截器，判断用户登录是否已经过期
axios.interceptors.response.use(
  response => {
      return response;
  },
  error => {  
    const res = error.response;
    console.log(res);
    if (res.status === 403 || res.data.status_code === 1002){
        MessageBox.confirm('未登录或token已超时, 您可以停留在本页面或跳转登录登录页面', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          router.replace('/login');
        }).catch(() => {
          Message({
            type: 'info',
            message: '已取消'
          });          
      });
    }

    // return error
  }
)

Vue.use(mavonEditor)

Vue.config.productionTip = false
Vue.prototype.$http = axios
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$echarts = echarts;

Vue.use(Form)
Vue.use(FormItem)
Vue.use(Button)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(Submenu)
Vue.use(MenuItem)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Switch)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Dialog)
Vue.use(Select)
Vue.use(Option)
Vue.use(DatePicker)
Vue.use(Scrollbar)
Vue.use(Carousel)
Vue.use(CarouselItem)
Vue.use(Tag)
Vue.use(Empty)
Vue.use(Link)


// Message配置和其他组件配置不太一样，需要在全局挂载才能使用
Vue.prototype.$message = Message

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store
})
