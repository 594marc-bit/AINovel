<template>
  <q-page class="q-pa-md">
    <!-- Header -->
    <div class="row q-mb-md">
      <div class="col">
        <q-breadcrumbs>
          <q-breadcrumbs-el label="我的小说" :to="{ name: 'novel-list' }" />
          <q-breadcrumbs-el :label="novel?.title" />
        </q-breadcrumbs>
      </div>
    </div>

    <template v-if="novel">
      <!-- Novel Info -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row items-center justify-between">
            <div class="col">
              <div class="text-h4 text-weight-bold">{{ novel.title }}</div>
              <div class="text-caption text-grey q-mt-sm">
                创建于 {{ formatDate(novel.created_at) }}
              </div>
            </div>
            <div class="col-auto">
              <q-btn
                color="primary"
                icon="add"
                label="新建章节"
                @click="createChapter"
              />
            </div>
          </div>

          <div class="q-mt-md">
            <p v-if="novel.description">{{ novel.description }}</p>
            <p v-else class="text-grey-6">暂无简介</p>
          </div>

          <div class="row q-mt-md q-gutter-sm">
            <q-chip
              :color="getStatusColor(novel.status)"
              text-color="white"
            >
              {{ getStatusText(novel.status) }}
            </q-chip>
            <q-chip
              v-if="novel.is_public"
              color="green"
              text-color="white"
              icon="public"
            >
              公开
            </q-chip>
            <q-chip color="blue" text-color="white">
              {{ chapters.length }} 章节
            </q-chip>
          </div>
        </q-card-section>
      </q-card>

      <!-- AI Assistant -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-h6 q-mb-md">AI 写作助理</div>
          <div class="row q-gutter-sm">
            <q-btn
              color="secondary"
              icon="lightbulb"
              label="情节建议"
              @click="suggestPlot"
              :loading="suggestingPlot"
            />
            <q-btn
              color="info"
              icon="chat"
              label="AI 对话"
              @click="openChatDialog"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Chapters List -->
      <q-card flat bordered>
        <q-card-section>
          <div class="text-h6 q-mb-md">章节列表</div>
          <q-list separator>
            <q-item
              v-for="chapter in chapters"
              :key="chapter.id"
              clickable
              @click="goToChapter(chapter.id)"
            >
              <q-item-section>
                <q-item-label class="text-weight-medium">
                  第{{ chapter.chapter_number }}章 - {{ chapter.title }}
                </q-item-label>
                <q-item-label caption>
                  {{ formatDate(chapter.created_at) }}
                  <span v-if="chapter.is_ai_generated" class="text-info q-ml-sm">
                    <q-icon name="smart_toy" size="sm" /> AI 生成
                  </span>
                </q-item-label>
                <q-item-label caption class="text-grey-7 q-mt-xs">
                  {{ chapter.content.slice(0, 100) }}...
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-btn
                  flat
                  round
                  color="negative"
                  icon="delete"
                  @click.stop="deleteChapter(chapter)"
                />
              </q-item-section>
            </q-item>

            <q-item v-if="chapters.length === 0">
              <q-item-section class="text-center text-grey-6">
                还没有章节，点击"新建章节"开始写作
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </template>

    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>

    <!-- Create Chapter Dialog -->
    <q-dialog v-model="createDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">新建章节</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="confirmCreateChapter" class="q-gutter-md">
            <q-input
              v-model="newChapterTitle"
              label="章节标题"
              outlined
              dense
              :rules="[val => !!val || '请输入章节标题']"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" color="primary" v-close-popup />
          <q-btn
            flat
            label="创建"
            color="primary"
            @click="confirmCreateChapter"
            :disable="!newChapterTitle.trim()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Delete Chapter Dialog -->
    <q-dialog v-model="deleteDialog">
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar
            icon="delete"
            color="negative"
            text-color="white"
          />
          <span class="q-ml-sm">
            确定要删除第{{ selectedChapter?.chapter_number }}章吗？
          </span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="取消" color="primary" v-close-popup />
          <q-btn flat label="删除" color="negative" @click="confirmDeleteChapter" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- AI Chat Dialog -->
    <q-dialog v-model="chatDialog" position="bottom">
      <q-card style="width: 700px; max-width: 90vw">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">AI 写作助理</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <div ref="chatContainer" style="height: 400px; overflow-y: auto">
            <div
              v-for="(msg, index) in chatHistory"
              :key="index"
              :class="msg.role === 'user' ? 'text-right' : 'text-left'"
              class="q-mb-md"
            >
              <q-chat-message
                :text="[msg.content]"
                :sent="msg.role === 'user'"
                :bg-color="msg.role === 'user' ? 'primary' : 'grey-4'"
              />
            </div>
          </div>

          <div class="row q-mt-md">
            <q-input
              v-model="chatMessage"
              outlined
              dense
              placeholder="询问AI关于情节、人物或写作的问题..."
              class="col"
              @keyup.enter="sendChatMessage"
            />
            <q-btn
              color="primary"
              icon="send"
              :disable="!chatMessage.trim()"
              @click="sendChatMessage"
              class="q-ml-sm"
            />
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useQuasar, date } from 'quasar';
import { novelService, type Novel, type Chapter } from 'src/services/novelService';
import { aiService } from 'src/services/aiService';

const props = defineProps<{
  id: string;
}>();

const router = useRouter();
const $q = useQuasar();

const novelId = Number(props.id);
const novel = ref<Novel | null>(null);
const chapters = ref<Chapter[]>([]);
const loading = ref(false);
const deleteDialog = ref(false);
const createDialog = ref(false);
const newChapterTitle = ref('');
const selectedChapter = ref<Chapter | null>(null);
const suggestingPlot = ref(false);
const chatDialog = ref(false);
const chatMessage = ref('');
const chatHistory = ref<Array<{role: string; content: string}>>([]);
const chatContainer = ref<HTMLElement | null>(null);

onMounted(() => {
  void loadNovel();
});

async function loadNovel() {
  loading.value = true;
  try {
    [novel.value, chapters.value] = await Promise.all([
      novelService.getNovel(novelId),
      novelService.getChapters(novelId),
    ]);
  } catch {
    $q.notify({
      type: 'negative',
      message: '加载小说详情失败',
    });
  } finally {
    loading.value = false;
  }
}

function createChapter() {
  newChapterTitle.value = '';
  createDialog.value = true;
}

async function confirmCreateChapter() {
  if (!newChapterTitle.value.trim()) return;

  try {
    loading.value = true;

    // 计算章节号
    const chapterNumber = chapters.value.length + 1;

    const newChapter = await novelService.createChapter(novelId, {
      title: newChapterTitle.value.trim(),
      content: '',
      chapter_number: chapterNumber,
      is_ai_generated: false,
    });

    $q.notify({
      type: 'positive',
      message: '章节创建成功',
    });

    // 创建后立即跳转到编辑页面
    await router.push(`/novel/${novelId}/chapter/${newChapter.id}`);
  } catch {
    $q.notify({
      type: 'negative',
      message: '创建章节失败',
    });
  } finally {
    loading.value = false;
    createDialog.value = false;
    newChapterTitle.value = '';
  }
}

function goToChapter(chapterId: number) {
  void router.push(`/novel/${novelId}/chapter/${chapterId}`);
}

function deleteChapter(chapter: Chapter) {
  selectedChapter.value = chapter;
  deleteDialog.value = true;
}

async function confirmDeleteChapter() {
  if (!selectedChapter.value) return;

  try {
    await novelService.deleteChapter(selectedChapter.value.id);
    $q.notify({
      type: 'positive',
      message: '章节删除成功',
    });
    void loadNovel();
  } catch {
    $q.notify({
      type: 'negative',
      message: '删除章节失败',
    });
  } finally {
    deleteDialog.value = false;
    selectedChapter.value = null;
  }
}

async function suggestPlot() {
  suggestingPlot.value = true;
  try {
    const response = await aiService.suggestPlot();
    if (response.is_success) {
      $q.dialog({
        title: 'AI 情节建议',
        message: response.content,
        html: true,
        ok: {
          label: '知道了',
          color: 'primary',
        },
      });
    } else {
      throw new Error(response.error_message);
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: '获取情节建议失败',
    });
  } finally {
    suggestingPlot.value = false;
  }
}

function openChatDialog() {
  chatDialog.value = true;
  chatHistory.value = [];
  chatMessage.value = '';
}

async function sendChatMessage() {
  if (!chatMessage.value.trim()) return;

  const userMessage = chatMessage.value;
  chatHistory.value.push({ role: 'user', content: userMessage });
  chatMessage.value = '';

  await nextTick();
  scrollToBottom();

  try {
    const response = await aiService.chatWithAI();

    if (response.is_success) {
      chatHistory.value.push({ role: 'assistant', content: response.content });
    } else {
      chatHistory.value.push({
        role: 'assistant',
        content: '抱歉，我现在无法回应。请稍后再试。',
      });
    }
  } catch {
    chatHistory.value.push({
      role: 'assistant',
      content: '抱歉，出现了一些问题。请稍后再试。',
    });
  }

  await nextTick();
  scrollToBottom();
}

function scrollToBottom() {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
}

function formatDate(dateString: string) {
  return date.formatDate(dateString, 'YYYY-MM-DD HH:mm');
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