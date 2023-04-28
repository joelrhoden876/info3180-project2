import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ExploreView from '../views/ExploreView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import RegisterForm from '../components/RegisterForm.vue'
import LoginForm from '../components/LoginForm.vue'
import PostForm from '../components/PostForm.vue'

const token = localStorage.getItem("token")
// console.log(token)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: "register",
      component: RegisterForm,
      meta: {auth: false}
    },
    {
      path: '/login',
      name: "login",
      component: LoginForm,
      meta: {auth: false}
    },
    {
      path: '/posts/new',
      name: "new post",
      component: PostForm,
      meta: {auth: true}
    },
    {
      path: '/logout',
      name: "logout",
      component: LoginForm,
    },
    {
      path: '/explore',
      name: "explore",
      component: ExploreView,
      meta: {auth: true}
      
    },
    {
      path: '/users/:id',
      name: "all posts",
      component: UserProfileView,
      meta: {auth: true}
    }
  ]
})

// routing and redirecting all users according to authentication
router.beforeEach((to, from, next) => {
  if (to.meta.auth && !token) {
    next("/login")
  } else if (!to.meta.auth && token) {
    next("/explore")
  } else {
    next()
  }
})

export default router
