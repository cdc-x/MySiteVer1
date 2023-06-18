import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login.vue'
import Home from '@/components/Home.vue'
import Index from '@/components/Index.vue'

Vue.use(Router)

const router =  new Router({
  routes: [
      { path: '/', component: Index},
      { path: '/admin', redirect: '/login'},
      { path: '/login', component: Login },
      { path: '/config', component: Home},
  ]
})


router.beforeEach((to, from, next)=>{
  if (to.path === "/login" || to.path === "/"){
      next()
  }else{
      // 获取token
      const tokenStr =  window.sessionStorage.getItem("AUTHORIZATION");
      if (tokenStr){
          next()
      }else{
          next("/login")
      }
  }
})

export default router