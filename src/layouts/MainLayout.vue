<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          <q-icon name="auto_stories" class="q-mr-sm" />
          AI 小说创作
        </q-toolbar-title>

        <q-space />

        <!-- MVP阶段 - 固定显示admin用户信息 -->
        <q-btn
          flat
          dense
          icon="add"
          label="新建小说"
          :to="{ name: 'novel-create' }"
        />
        <q-btn flat round>
          <q-avatar size="32px">
            <q-icon name="person" />
          </q-avatar>
          <q-menu>
            <div class="row no-wrap q-pa-md">
              <div class="column">
                <div class="text-h6 q-mb-md">{{ authStore.userDisplayName }}</div>
                <q-btn
                  flat
                  color="secondary"
                  icon="settings"
                  label="设置"
                  class="full-width"
                />
              </div>
              <q-separator vertical inset class="q-mx-md" />
              <div class="column items-center">
                <q-avatar size="72px">
                  <q-icon name="account_circle" size="72px" />
                </q-avatar>
                <div class="text-subtitle1 q-mt-md">{{ authStore.user?.email }}</div>
                <div class="text-caption q-mt-sm">管理员</div>
              </div>
            </div>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header class="text-grey-8"> 导航菜单 </q-item-label>

        <q-item
          clickable
          :to="{ name: 'novel-list' }"
          exact
        >
          <q-item-section avatar>
            <q-icon name="menu_book" />
          </q-item-section>
          <q-item-section>
            <q-item-label>我的小说</q-item-label>
            <q-item-label caption>管理你的小说作品</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          clickable
          :to="{ name: 'novel-create' }"
          exact
        >
          <q-item-section avatar>
            <q-icon name="add_circle" />
          </q-item-section>
          <q-item-section>
            <q-item-label>创建小说</q-item-label>
            <q-item-label caption>开始新的创作</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <q-item-label header class="text-grey-8"> AI 助手 </q-item-label>

        <q-item clickable @click="showAIFeatures">
          <q-item-section avatar>
            <q-icon name="smart_toy" />
          </q-item-section>
          <q-item-section>
            <q-item-label>AI 功能</q-item-label>
            <q-item-label caption>AI 续写、润色、情节建议</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <q-item-label header class="text-grey-8"> 关于 </q-item-label>

        <q-item clickable @click="showAbout">
          <q-item-section avatar>
            <q-icon name="info" />
          </q-item-section>
          <q-item-section>
            <q-item-label>关于本应用</q-item-label>
            <q-item-label caption>版本信息</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth-store';

const $q = useQuasar();
const authStore = useAuthStore();
const leftDrawerOpen = ref(false);

// 初始化认证状态
void authStore.initAuth();

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

function showAIFeatures() {
  $q.dialog({
    title: 'AI 写作助手',
    message: `
      <div class="q-mt-md">
        <p><strong>AI 续写：</strong>当你写作遇到瓶颈时，AI 可以帮你继续创作。</p>
        <p><strong>AI 润色：</strong>让 AI 帮你优化文字表达，使文章更加生动。</p>
        <p><strong>情节建议：</strong>AI 可以根据已有内容提供故事发展建议。</p>
        <p><strong>AI 对话：</strong>与 AI 讨论情节、人物和写作技巧。</p>
      </div>
    `,
    html: true,
    ok: {
      label: '知道了',
      color: 'primary',
    },
  });
}

function showAbout() {
  $q.dialog({
    title: '关于 AI 小说创作',
    message: `
      <div class="q-mt-md">
        <p><strong>版本：</strong>1.0.0 (MVP)</p>
        <p><strong>技术栈：</strong></p>
        <ul>
          <li>前端：Quasar Vue 3</li>
          <li>后端：Python FastAPI</li>
          <li>数据库：PostgreSQL</li>
          <li>AI 服务：OpenAI GPT-4</li>
        </ul>
        <p class="q-mt-md">
          一个支持人机协作的小说创作平台，让 AI 成为你的创作伙伴。
        </p>
      </div>
    `,
    html: true,
    ok: {
      label: '关闭',
      color: 'primary',
    },
  });
}
</script>
