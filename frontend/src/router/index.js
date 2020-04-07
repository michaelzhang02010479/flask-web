import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Ping from '@/components/Ping'
import Books from '@/components/Books'
import Order from '@/components/Order'

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
    },
    {
      path: '/order/:id',
      name: 'Order',
      component: Order,
    },
  ],
  mode: 'history'
})
