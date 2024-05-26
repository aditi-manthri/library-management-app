import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../components/LoginPage.vue'
import SignupPage from '../components/SignupPage.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import UserDashboard from '../components/UserDashboard.vue'
import AdminStats from '../components/AdminStats.vue'
import AdminBooks from '@/components/AdminBooks.vue'
import UserStats from '@/components/UserStats.vue'
import UserBooks from '@/components/UserBooks.vue'
import AdminRequests from '@/components/AdminRequests.vue'
import SearchPage from '@/components/SearchPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LoginPage
  },
  {
    path: '/search',
    name: 'search',
    component: SearchPage
  },
  {
    path: '/admindashboard',
    name: 'adminDashboard',
    component: AdminDashboard,
    meta: {isAdmin:true}
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: UserDashboard,
    meta: {isUser:true}
  },
  {
    path: '/adminstats',
    name: 'adminstats',
    component: AdminStats,
    meta: {isAdmin:true}
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupPage
  },
  {
    path: '/adminbooks',
    name: 'adminbooks',
    component: AdminBooks,
    meta: {isAdmin:true}
  },
  {
    path: '/stats',
    name: 'stats',
    component: UserStats,
    meta: {isUser:true}
  },
  {
    path: '/mybooks',
    name: 'mybooks',
    component: UserBooks,
    meta: {isUser:true}
  },
  {
    path: '/adminrequests',
    name: 'adminrequests',
    component: AdminRequests,
    meta: {isAdmin:true}
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to,from,next) => {
  const userRole = localStorage.getItem('userRole') || 'user';

  if(to.meta.isAdmin && userRole !== 'admin'){
    next({path:'/login',query:{unauthorized:true}});
  } else if (to.meta.isUser && userRole !== 'user') {
    next({ path: '/login', query: { unauthorized: true } }); 
  }else {
    next();
  }
})

export default router
