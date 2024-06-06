import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SimulationListView from '../views/SimulationListView.vue'
import MainPageLayoutViewVue from '@/views/MainPageLayoutView.vue'
import auth from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainPageLayoutViewVue,

      children: [
        { name: 'home-view', path: '', component: HomeView },
        {
          name: 'simulation-list',
          path: 'list',
          component: SimulationListView
        },
        {
          path: '/brief/:id',
          name: 'brief',
          component: () => import('../views/BriefView.vue')
        },
        {
          path: 'scenario/:id',
          name: 'scenario',
          component: () => import('../views/ScenarioView.vue')
        },
        {
          name: 'simulation-chat',
          path: 'list/:id',
          component: () => import('../views/SimulationChatView.vue')
        },
        {
          path: '/login',
          name: 'login',
          meta: { requiresAuth: false },
          component: () => import('../views/LoginView.vue')
        },
        {
          path: '/generate',
          name: 'generate',
          component: () => import('../views/Select_scenario.vue')
        },
        {
          path: '/open-list',
          name: 'openlist',
          component: () => import('../views/OpenList.vue')
        }
      ]
    },
  
    {
      path: '/logout',
      name: 'logout',
      meta: { requiresAuth: true },
      component: () => import('../views/LogoutView.vue')
    }
  ]
})

router.beforeEach((to) => {
  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  if (to.meta.requiresAuth && !auth.isLoggedIn()) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: '/login',
      // save the location we were at to come back later
      query: { redirect: to.fullPath }
    }
  }
  if (to.meta.requiresAuth === false && auth.isLoggedIn()) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    return {
      path: '404'
    }
  }
})

export default router
