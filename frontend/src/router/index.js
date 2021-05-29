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
    path: "/paper",
    redirect: "/paper/cited"
  },
  {
    path: "/paper/cited",
    name: "Paper",
    component: () => import("../views/Paper"),
    children: [
      {
        path: "/paper/cited",
        component: () => import("../components/Paper/CitedPaper")
      }
    ]
  },
  {
    path: "/user/:id",
    name: "User Profile",
    redirect: to => {
      return to.fullPath + "/index"
    }
  },
  {
    path: "/user/:id/index",
    component: () => import("../views/UserProfile"),
    children: [
      {
        path: "/user/:id/index",
      },
      {
        path: "/user/:id/index1"
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
