import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

declare module 'vue-router' {
  interface RouteMeta {
    headline?: string;
    description?: string;
    parentName?: string;
  }
}

export const default_route_name = "home";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: () => import("@/layouts/MainLayout.vue"),
      children: [
        {
          path: "",
          name: default_route_name,
          components: {
            default: () => import('../views/HomeView.vue'),
          },
          meta: {
            headline: "Dotazy na karcinom prsu - demo"
          }
        },
      ]
    },
    {
      path: '/',
      name: default_route_name,
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
