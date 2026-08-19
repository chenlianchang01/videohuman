import { createRouter, createWebHistory } from 'vue-router'
import JobList from './views/JobList.vue'
import JobNew from './views/JobNew.vue'
import JobDetail from './views/JobDetail.vue'
import Assets from './views/Assets.vue'
import Login from './views/Login.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: JobList },
    { path: '/new', component: JobNew },
    { path: '/jobs/:id', component: JobDetail, props: true },
    { path: '/assets', component: Assets },
    { path: '/login', component: Login },
  ],
})
