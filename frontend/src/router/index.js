import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: "/home/index",
    name: 'Home',
  },
  {
    path: "/home/index",
    name: "index",
    component: Home,
    children: [
      {
        path: "/home/test1",
        component: () => import("../views/About")
      },
      {
        path: "/home/index",
        component: () => import("../views/AllGenres")
      },
    ]
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: "/paper",
    name: "Paper",
    component: () => import("../views/Paper")
  },
  {
    path: "/user",
    name: "User Profile",
    redirect: "/user/index",
  },
  {
    path: "/user/index",
    component: () => import("../views/UserProfile"),
    children: [
      {
        path: "/user/index",
        component: () => import("../components/UserProfile/UserBasicInfo")
      },
      {
        path: "/user/index1"
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
