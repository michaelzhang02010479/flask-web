import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Ping from '@/components/Ping'
import Books from '@/components/Books'

Vue.use(Router)

export default new Router({
  routes: [
    //{
    //  path: '/',
    //  name: 'HelloWorld',
    //  component: HelloWorld
    //},
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    },
    {
      path: '/',
      name: 'Books',
      component: Books
    }
  ],
  mode: 'history'
})
