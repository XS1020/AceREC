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
    path: '/settings',
    component: () => import("../views/Settings")
  },
  {
    path: "/search",
    component: () => import("../views/Search")
  },
  {
    path: '/signup',
    component: () => import("../views/SignUp")
  },
  {
    path: "/signin",
    component: () => import("../views/SignIn")
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
    path: "/paper/:id",
    redirect: "/paper/:id/cited"
  },
  {
    path: "/paper/:id/cited",
    name: "Paper",
    component: () => import("../views/Paper"),
    children: [
      {
        path: "/paper/:id/cited",
        component: () => import("../components/Paper/CitedPaper")
      },
      {
        path: "/paper/:id/recommend",
        component: () => import("../components/Paper/CitedPaper")
      }
    ]
  },
  {
    path: "/profile/:id",
    name: "User Profile",
    redirect: to => {
      return to.fullPath + "/index"
    }
  },
  {
    path: "/profile/:id/index",
    component: () => import("../views/UserProfile"),
    children: [
      {
        path: "/profile/:id/index",
      },
      {
        path: "/profile/:id/index1"
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
router.beforeEach((to, from, next) => {
  if (to.path === '/signin' || to.path === "/signup")
    next()
  else {
    const token = localStorage.getItem('authorization')
    if (token === null || token === '')
      next('/signin')
    else {

      next()
    }
  }
})
export default router
