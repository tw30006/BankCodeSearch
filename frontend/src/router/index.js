import { createRouter, createWebHistory } from 'vue-router';
import Detail from '../components/Detail.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/:headOfficeCode/:branchOfficeCode/:headOffice-:branchOffice.html',
      name: 'Detail',
      component: Detail,
      props: true
    }
  ]
});

export default router;