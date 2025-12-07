<template>
  <q-page class="q-pa-md">
    <div class="row q-mb-md">
      <div class="col">
        <div class="text-h4 text-weight-bold">我的小说</div>
        <div class="text-caption text-grey">创作和管理你的小说作品</div>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          label="新建小说"
          :to="{ name: 'novel-create' }"
        />
      </div>
    </div>

    <q-grid
      :cols="breakpoints"
      gutter="md"
    >
      <q-grid-item
        v-for="novel in novels"
        :key="novel.id"
      >
        <q-card
          flat
          bordered
          class="novel-card cursor-pointer"
          @click="goToNovel(novel.id)"
        >
          <q-card-section>
            <div class="text-h6">{{ novel.title }}</div>
            <div class="text-caption text-grey q-mt-sm">
              {{ novel.description || '暂无描述' }}
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div class="row items-center justify-between">
              <q-chip
                :color="getStatusColor(novel.status)"
                text-color="white"
                size="sm"
              >
                {{ getStatusText(novel.status) }}
              </q-chip>
              <div class="text-caption text-grey">
                {{ novel.chapter_count || 0 }} 章节
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              flat
              color="primary"
              icon="edit"
              @click.stop="editNovel(novel)"
            />
            <q-btn
              flat
              color="negative"
              icon="delete"
              @click.stop="deleteNovel(novel)"
            />
          </q-card-actions>
        </q-card>
      </q-grid-item>
    </q-grid>

    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>

    <!-- Empty State -->
    <div
      v-if="!loading && novels.length === 0"
      class="column items-center justify-center"
      style="height: 400px"
    >
      <q-icon
        name="menu_book"
        size="100px"
        color="grey-5"
      />
      <div class="text-h5 text-grey-6 q-mt-md">
        还没有小说
      </div>
      <div class="text-caption text-grey q-mt-sm">
        点击"新建小说"开始你的创作之旅
      </div>
    </div>

    <!-- Delete Dialog -->
    <q-dialog v-model="deleteDialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar
            icon="delete"
            color="negative"
            text-color="white"
          />
          <span class="q-ml-sm">
            确定要删除《{{ selectedNovel?.title }}》吗？<br>
            此操作不可恢复！
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn
            flat
            label="取消"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            label="删除"
            color="negative"
            @click="confirmDelete"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { novelService, type Novel } from 'src/services/novelService';

const router = useRouter();
const $q = useQuasar();

const novels = ref<Novel[]>([]);
const loading = ref(false);
const deleteDialog = ref(false);
const selectedNovel = ref<Novel | null>(null);

const breakpoints = computed(() => ({
  xs: 1,
  sm: 2,
  md: 3,
  lg: 4,
  xl: 5,
}));

onMounted(() => {
  void loadNovels();
});

async function loadNovels() {
  loading.value = true;
  try {
    novels.value = await novelService.getNovels();
  } catch {
    $q.notify({
      type: 'negative',
      message: '加载小说列表失败',
    });
  } finally {
    loading.value = false;
  }
}

function goToNovel(id: number) {
  void router.push(`/novel/${id}`);
}

function editNovel(novel: Novel) {
  // TODO: Implement edit novel dialog
  console.log('Edit novel:', novel);
}

function deleteNovel(novel: Novel) {
  selectedNovel.value = novel;
  deleteDialog.value = true;
}

async function confirmDelete() {
  if (!selectedNovel.value) return;

  try {
    await novelService.deleteNovel(selectedNovel.value.id);
    $q.notify({
      type: 'positive',
      message: '小说删除成功',
    });
    void loadNovels();
  } catch {
    $q.notify({
      type: 'negative',
      message: '删除小说失败',
    });
  } finally {
    deleteDialog.value = false;
    selectedNovel.value = null;
  }
}

function getStatusColor(status: string) {
  switch (status) {
    case 'draft':
      return 'grey';
    case 'published':
      return 'primary';
    case 'completed':
      return 'positive';
    default:
      return 'grey';
  }
}

function getStatusText(status: string) {
  switch (status) {
    case 'draft':
      return '草稿';
    case 'published':
      return '已发布';
    case 'completed':
      return '已完成';
    default:
      return '未知';
  }
}
</script>

<style lang="scss" scoped>
.novel-card {
  transition: transform 0.2s;
  height: 100%;

  &:hover {
    transform: translateY(-4px);
  }
}
</style>