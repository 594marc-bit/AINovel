import { api } from 'boot/axios';

export interface Novel {
  id: number;
  title: string;
  description?: string;
  author_id: number;
  status: string;
  is_public: boolean;
  created_at: string;
  updated_at?: string;
  chapters?: Chapter[];
  chapter_count?: number;
}

export interface Chapter {
  id: number;
  title: string;
  content: string;
  novel_id: number;
  chapter_number: number;
  is_ai_generated: boolean;
  created_at: string;
  updated_at?: string;
}

export interface NovelCreate {
  title: string;
  description?: string;
  status?: string;
  is_public?: boolean;
}

export interface ChapterCreate {
  title: string;
  content: string;
  chapter_number?: number;
  is_ai_generated?: boolean;
}


export const novelService = {
  async getNovels(): Promise<Novel[]> {
    const response = await api.get('/novels');
    return response.data;
  },

  async getNovel(id: number): Promise<Novel> {
    const response = await api.get(`/novels/${id}`);
    return response.data;
  },

  async createNovel(novel: NovelCreate): Promise<Novel> {
    const response = await api.post('/novels', novel);
    return response.data;
  },

  async updateNovel(id: number, novel: Partial<NovelCreate>): Promise<Novel> {
    const response = await api.put(`/novels/${id}`, novel);
    return response.data;
  },

  async deleteNovel(id: number): Promise<void> {
    await api.delete(`/novels/${id}`);
  },

  async getChapters(novelId: number): Promise<Chapter[]> {
    const response = await api.get(`/novels/${novelId}/chapters`);
    return response.data;
  },

  async createChapter(novelId: number, chapter: ChapterCreate): Promise<Chapter> {
    const response = await api.post(`/novels/${novelId}/chapters`, chapter);
    return response.data;
  },

  async updateChapter(chapterId: number, chapter: Partial<ChapterCreate>): Promise<Chapter> {
    const response = await api.put(`/novels/chapters/${chapterId}`, chapter);
    return response.data;
  },

  async deleteChapter(chapterId: number): Promise<void> {
    await api.delete(`/novels/chapters/${chapterId}`);
  }
};