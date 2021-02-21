import Vue from 'vue';
import VueRouter from 'vue-router';
import Ping from '../components/Ping.vue';
import Pessoas from '../components/Pessoas.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Pessoas',
    component: Pessoas,
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
