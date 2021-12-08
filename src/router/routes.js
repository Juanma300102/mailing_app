
const routes = [
  {
    path: '/',
    component: () => import('layouts/logInLayout.vue'),
    children: [
      { path: '', component: () => import('pages/logIn.vue') }
    ]
  },
  {
    path: '/h',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/main.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
