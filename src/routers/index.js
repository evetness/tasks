import {createRouter, createWebHistory} from 'vue-router';

const routes = [
  {
    path: "/",
    component: Page,
    name: "home",
    redirect: () => {
      return "/tasks"
    },
    children: [
      {
        path: "/tasks",
        children: [
          {
            path: "",
            name: "tasks",
          }
        ]
      },
      {
        path: "/wages",
        children: [
          {
            path: "",
            name: "wages"
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})