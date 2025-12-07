import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  // 主应用路由 - MVP阶段不需要认证
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'novel-list', component: () => import('pages/NovelListPage.vue') },
      { path: 'novel/:id', name: 'novel-detail', component: () => import('pages/NovelDetailPage.vue'), props: true },
      { path: 'novel/:id/chapter/:chapterId', name: 'chapter-editor', component: () => import('pages/ChapterEditorPage.vue'), props: true },
      { path: 'new', name: 'novel-create', component: () => import('pages/NovelCreatePage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
