<template>
  <q-page class="q-pa-md">
    <div class="row justify-center">
      <div class="col-12 col-lg-10">
        <!-- Breadcrumbs -->
        <q-breadcrumbs class="q-mb-md">
          <q-breadcrumbs-el label="我的小说" :to="{ name: 'novel-list' }" />
          <q-breadcrumbs-el :label="novel?.title" :to="`/novel/${props.id}`" />
          <q-breadcrumbs-el :label="chapter?.title" />
        </q-breadcrumbs>

        <template v-if="chapter && novel">
          <!-- Chapter Info -->
          <q-card flat bordered class="q-mb-md">
            <q-card-section>
              <div class="row items-center q-gutter-md">
                <q-input
                  v-model="chapter.title"
                  label="章节标题"
                  outlined
                  class="col"
                  :readonly="!isEditing"
                />
                <div class="col-auto">
                  <q-badge
                    v-if="chapter.is_ai_generated"
                    color="info"
                    class="q-mr-sm"
                  >
                    <q-icon name="smart_toy" class="q-mr-xs" />
                    AI 生成
                  </q-badge>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Editor -->
          <q-card flat bordered class="q-mb-md">
            <q-card-section>
              <div class="row items-center justify-between q-mb-md">
                <div class="text-h6">章节内容</div>
                <div class="row q-gutter-sm">
                  <q-btn
                    v-if="!isEditing"
                    flat
                    color="primary"
                    icon="edit"
                    label="编辑"
                    @click="startEditing"
                  />
                  <q-btn
                    v-if="isEditing"
                    flat
                    color="secondary"
                    icon="auto_fix_high"
                    label="AI润色"
                    @click="openPolishDialog"
                  />
                  <q-btn
                    v-if="isEditing"
                    flat
                    color="info"
                    icon="smart_toy"
                    label="AI续写"
                    @click="aiContinueWriting"
                    :loading="aiWriting"
                  />
                  <q-btn
                    v-if="isEditing"
                    flat
                    color="negative"
                    icon="cancel"
                    label="取消编辑"
                    @click="cancelEditing"
                  />
                </div>
              </div>

              <q-input
                v-model="chapter.content"
                type="textarea"
                rows="20"
                outlined
                :readonly="!isEditing"
                :placeholder="isEditing ? '开始写作...' : '点击编辑按钮开始编辑'"
              />
            </q-card-section>
          </q-card>

          <!-- Previous Chapters Context -->
          <q-card flat bordered class="q-mb-md" v-if="previousChapters.length > 0">
            <q-card-section>
              <div class="text-h6 q-mb-md">前文回顾</div>
              <q-expansion-item
                v-for="(prevChapter, index) in previousChapters"
                :key="prevChapter.id"
                :label="`第${prevChapter.chapter_number}章 - ${prevChapter.title}`"
                :default-opened="index === previousChapters.length - 1"
              >
                <q-card flat bordered>
                  <q-card-section>
                    <pre class="text-body1">{{ prevChapter.content }}</pre>
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </q-card-section>
          </q-card>

          <!-- Actions -->
          <div class="row justify-end q-gutter-sm">
            <q-btn
              flat
              label="返回"
              :to="`/novel/${props.id}`"
            />
            <q-btn
              color="primary"
              label="保存"
              @click="saveChapter"
              :loading="saving"
            />
          </div>
        </template>

        <q-inner-loading :showing="loading">
          <q-spinner-gears size="50px" color="primary" />
        </q-inner-loading>

        <!-- AI Polish Dialog -->
        <q-dialog v-model="polishDialog" persistent>
          <q-card style="min-width: 600px">
            <q-card-section>
              <div class="text-h6">AI 润色</div>
            </q-card-section>

            <q-card-section>
              <q-input
                v-model="polishInstruction"
                label="润色要求"
                outlined
                type="textarea"
                rows="3"
                hint="例如：让语言更生动、修正语法错误、调整语调等"
              />
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="取消" v-close-popup />
              <q-btn
                color="primary"
                label="开始润色"
                @click="polishContent"
                :loading="polishing"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>

        <!-- Polish Result Dialog -->
        <q-dialog v-model="polishResultDialog" persistent>
          <q-card style="min-width: 800px">
            <q-card-section>
              <div class="text-h6">润色结果</div>
            </q-card-section>

            <q-card-section>
              <div class="q-mb-md">
                <q-badge color="primary" label="原文" />
              </div>
              <q-card flat bordered class="q-mb-md">
                <q-card-section>
                  <pre>{{ originalContent }}</pre>
                </q-card-section>
              </q-card>

              <div class="q-mb-md">
                <q-badge color="secondary" label="润色后" />
              </div>
              <q-card flat bordered class="q-mb-md">
                <q-card-section>
                  <pre>{{ polishedContent }}</pre>
                </q-card-section>
              </q-card>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn flat label="取消" v-close-popup />
              <q-btn
                flat
                color="negative"
                label="保留原文"
                v-close-popup
              />
              <q-btn
                color="primary"
                label="使用润色版本"
                @click="applyPolishedContent"
                v-close-popup
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import { novelService, type Novel, type Chapter } from 'src/services/novelService';
import { aiService } from 'src/services/aiService';

const props = defineProps<{
  id: string;
  chapterId: string;
}>();

const router = useRouter();
const $q = useQuasar();

const novel = ref<Novel | null>(null);
const chapter = ref<Chapter | null>(null);
const chapters = ref<Chapter[]>([]);
const previousChapters = ref<Chapter[]>([]);
const loading = ref(false);
const saving = ref(false);
const aiWriting = ref(false);
const isEditing = ref(false);

// AI Polish
const polishDialog = ref(false);
const polishInstruction = ref('');
const polishing = ref(false);
const polishResultDialog = ref(false);
const originalContent = ref('');
const polishedContent = ref('');

onMounted(async () => {
  await loadData();
});

async function loadData() {
  loading.value = true;
  const novelId = Number(props.id);
  const chapterId = Number(props.chapterId);

  try {
    [novel.value, chapter.value, chapters.value] = await Promise.all([
      novelService.getNovel(novelId),
      novelService.getChapters(novelId).then(chs => chs.find(c => c.id === chapterId) || null),
      novelService.getChapters(novelId),
    ]);

    if (!chapter.value) {
      $q.notify({
        type: 'negative',
        message: '章节不存在',
      });
      void router.push(`/novel/${novelId}`);
      return;
    }

    // Get previous chapters
    previousChapters.value = chapters.value
      .filter(c => c.chapter_number < chapter.value!.chapter_number)
      .slice(-3); // Last 3 chapters
  } catch {
    $q.notify({
      type: 'negative',
      message: '加载数据失败',
    });
  } finally {
    loading.value = false;
  }
}

function startEditing() {
  if (!chapter.value) return;
  originalContent.value = chapter.value.content;
  isEditing.value = true;
}

function cancelEditing() {
  if (!chapter.value) return;
  chapter.value.content = originalContent.value;
  isEditing.value = false;
}

async function saveChapter() {
  if (!chapter.value) return;

  saving.value = true;
  const chapterId = Number(props.chapterId);

  try {
    await novelService.updateChapter(chapterId, {
      title: chapter.value.title,
      content: chapter.value.content,
    });
    $q.notify({
      type: 'positive',
      message: '保存成功',
    });
    isEditing.value = false;
  } catch {
    $q.notify({
      type: 'negative',
      message: '保存失败',
    });
  } finally {
    saving.value = false;
  }
}

async function aiContinueWriting() {
  if (!chapter.value || !novel.value) return;

  aiWriting.value = true;
  const novelId = Number(props.id);

  try {
    // Get context from previous content
    const context = previousChapters.value
      .map(c => `第${c.chapter_number}章：${c.content.slice(-500)}`)
      .join('\n\n');

    const response = await aiService.continueWriting({
      novel_id: novelId,
      previous_content: context + '\n\n' + chapter.value.content.slice(-1000),
      length_hint: 'medium',
    });

    if (response.is_success && response.content) {
      // Append AI content
      chapter.value.content += '\n\n' + response.content;

      // Mark as AI generated if it was empty before
      if (!chapter.value.content.trim()) {
        chapter.value.is_ai_generated = true;
      }

      $q.notify({
        type: 'positive',
        message: 'AI 续写成功',
      });
    } else {
      throw new Error(response.error_message || 'AI 续写失败');
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: 'AI 续写失败，请重试',
    });
  } finally {
    aiWriting.value = false;
  }
}

function openPolishDialog() {
  if (!chapter.value) return;
  originalContent.value = chapter.value.content;
  polishDialog.value = true;
  polishInstruction.value = '';
}

async function polishContent() {
  if (!chapter.value) return;

  polishing.value = true;
  try {
    const response = await aiService.polishContent({
      content: originalContent.value,
      instruction: polishInstruction.value,
    });

    if (response.is_success && response.content) {
      polishedContent.value = response.content;
      polishDialog.value = false;
      polishResultDialog.value = true;
    } else {
      throw new Error(response.error_message || '润色失败');
    }
  } catch {
    $q.notify({
      type: 'negative',
      message: '润色失败，请重试',
    });
  } finally {
    polishing.value = false;
  }
}

function applyPolishedContent() {
  if (!chapter.value) return;
  chapter.value.content = polishedContent.value;
}
</script>

<style lang="scss" scoped>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: inherit;
}
</style>