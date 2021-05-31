import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import Trends from '../components/Trends.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/',
      name: 'Trends',
      component: Trends,
    },
  ],
});
