<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <div class="col-12 col-md-8 col-lg-6">
        <q-card flat bordered>
          <q-card-section>
            <div class="text-h5 text-weight-bold q-mb-md">创建新小说</div>
            <q-form @submit="createNovel" class="q-gutter-md">
              <q-input
                v-model="form.title"
                label="小说标题"
                outlined
                maxlength="100"
                :rules="[(val) => !!val || '请输入小说标题']"
              />

              <q-input
                v-model="form.description"
                label="小说简介"
                outlined
                type="textarea"
                rows="4"
                maxlength="500"
                hint="可选，简单描述你的小说内容"
              />

              <q-select
                v-model="form.status"
                :options="statusOptions"
                label="小说状态"
                outlined
                emit-value
                map-options
              />

              <q-toggle
                v-model="form.is_public"
                label="公开小说（其他用户可以阅读）"
                color="primary"
              />

              <div class="row justify-end q-mt-lg">
                <q-btn
                  flat
                  label="取消"
                  :to="{ name: 'novel-list' }"
                />
                <q-btn
                  type="submit"
                  color="primary"
                  label="创建"
                  :loading="loading"
                  class="q-ml-sm"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { novelService, type NovelCreate } from 'src/services/novelService';

const router = useRouter();
const $q = useQuasar();

const loading = ref(false);
const form = ref<NovelCreate>({
  title: '',
  description: '',
  status: 'draft',
  is_public: false,
});

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已完成', value: 'completed' },
];

async function createNovel() {
  loading.value = true;
  try {
    const novel = await novelService.createNovel(form.value);
    $q.notify({
      type: 'positive',
      message: `小说《${novel.title}》创建成功！`,
    });
    void router.push(`/novel/${novel.id}`);
  } catch {
    $q.notify({
      type: 'negative',
      message: '创建小说失败，请重试',
    });
  } finally {
    loading.value = false;
  }
}
</script>