<template>
  <q-page class="flex flex-center" style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <q-card class="login-card" flat bordered>
      <q-card-section class="text-center">
        <q-avatar size="100px" font-size="52px" color="primary" icon="auto_stories" />
        <div class="text-h4 q-mt-md text-weight-bold">AI 小说创作</div>
        <div class="text-caption text-grey-6 q-mt-sm">登录以开始你的创作之旅</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin" class="q-gutter-md">
          <q-input
            v-model="form.username"
            label="用户名"
            outlined
            dense
            :rules="[val => !!val || '请输入用户名']"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input
            v-model="form.password"
            label="密码"
            outlined
            dense
            :type="showPassword ? 'text' : 'password'"
            :rules="[val => !!val || '请输入密码']"
            lazy-rules
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
            <template v-slot:append>
              <q-icon
                :name="showPassword ? 'visibility_off' : 'visibility'"
                class="cursor-pointer"
                @click="showPassword = !showPassword"
              />
            </template>
          </q-input>

          <div class="row items-center justify-between">
            <q-checkbox v-model="rememberMe" label="记住我" />
            <q-btn flat color="primary" label="忘记密码？" />
          </div>

          <div>
            <q-btn
              type="submit"
              color="primary"
              class="full-width"
              label="登录"
              :loading="authStore.loading"
              size="md"
            />
          </div>
        </q-form>
      </q-card-section>

      <q-card-section class="text-center">
        <p class="text-grey-6">
          还没有账号？
          <q-btn flat color="primary" label="立即注册" @click="showRegisterDialog = true" />
        </p>
      </q-card-section>
    </q-card>

    <!-- 注册对话框 -->
    <q-dialog v-model="showRegisterDialog" persistent>
      <q-card style="min-width: 400px;">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">注册新账号</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="handleRegister" class="q-gutter-md">
            <q-input
              v-model="registerForm.username"
              label="用户名"
              outlined
              dense
              :rules="[val => !!val || '请输入用户名']"
            >
              <template v-slot:prepend>
                <q-icon name="person" />
              </template>
            </q-input>

            <q-input
              v-model="registerForm.email"
              label="邮箱"
              outlined
              dense
              type="email"
              :rules="[val => !!val || '请输入邮箱', val => /.+@.+\..+/.test(val) || '请输入有效的邮箱地址']"
            >
              <template v-slot:prepend>
                <q-icon name="email" />
              </template>
            </q-input>

            <q-input
              v-model="registerForm.password"
              label="密码"
              outlined
              dense
              :type="showRegisterPassword ? 'text' : 'password'"
              :rules="[val => !!val || '请输入密码', val => val.length >= 6 || '密码至少6位']"
            >
              <template v-slot:prepend>
                <q-icon name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showRegisterPassword ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="showRegisterPassword = !showRegisterPassword"
                />
              </template>
            </q-input>

            <q-input
              v-model="registerForm.confirmPassword"
              label="确认密码"
              outlined
              dense
              :type="showConfirmPassword ? 'text' : 'password'"
              :rules="[val => !!val || '请确认密码', val => val === registerForm.password || '两次输入的密码不一致']"
            >
              <template v-slot:prepend>
                <q-icon name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="showConfirmPassword = !showConfirmPassword"
                />
              </template>
            </q-input>

            <div class="row q-mt-lg">
              <q-btn
                flat
                label="取消"
                v-close-popup
              />
              <q-space />
              <q-btn
                type="submit"
                color="primary"
                label="注册"
                :loading="authStore.loading"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth-store';

const router = useRouter();
const $q = useQuasar();
const authStore = useAuthStore();

const form = ref({
  username: '',
  password: ''
});

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const showPassword = ref(false);
const showRegisterPassword = ref(false);
const showConfirmPassword = ref(false);
const rememberMe = ref(false);
const showRegisterDialog = ref(false);

async function handleLogin() {
  const result = await authStore.login(form.value);
  if (result.success) {
    $q.notify({
      type: 'positive',
      message: `欢迎回来，${authStore.user?.username}！`,
      position: 'top'
    });
    void router.push('/');
  } else {
    $q.notify({
      type: 'negative',
      message: result.error || '登录失败',
      position: 'top'
    });
  }
}

async function handleRegister() {
  const result = await authStore.register({
    username: registerForm.value.username,
    email: registerForm.value.email,
    password: registerForm.value.password
  });

  if (result.success) {
    $q.notify({
      type: 'positive',
      message: '注册成功！请登录',
      position: 'top'
    });
    showRegisterDialog.value = false;
    form.value.username = registerForm.value.username;
  } else {
    $q.notify({
      type: 'negative',
      message: result.error || '注册失败',
      position: 'top'
    });
  }
}
</script>

<style lang="scss" scoped>
.login-card {
  width: 100%;
  max-width: 400px;
  padding: 24px;
}
</style>