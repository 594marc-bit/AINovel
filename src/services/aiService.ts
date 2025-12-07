import { api } from 'boot/axios';

export interface AIResponse {
  content: string;
  is_success: boolean;
  error_message?: string;
}

export interface AIWriteRequest {
  novel_id: number;
  previous_content?: string;
  style_hint?: string;
  length_hint?: 'short' | 'medium' | 'long';
  chapter_id?: number;
  // 新增续写配置选项
  use_context?: boolean;
  context_depth?: number;
  character_consistency?: boolean;
  plot_continuity?: boolean;
  writing_style?: 'descriptive' | 'dialog_heavy' | 'action_focused' | 'introspective' | 'poetic' | 'minimalist';
  tone?: 'humorous' | 'serious' | 'romantic' | 'mysterious' | 'dramatic' | 'lighthearted';
  target_audience?: string;
  pov?: 'first_person' | 'third_person_limited' | 'third_person_omniscient';
}

export interface AIPolishRequest {
  content: string;
  instruction?: string;
  preserve_style?: boolean;
}

export interface AIChatRequest {
  message: string;
  novel_id?: number;
  conversation_history?: Array<{role: string; content: string}>;
}

export const aiService = {
  async continueWriting(request: AIWriteRequest): Promise<AIResponse> {
    const response = await api.post('/ai/write', request);
    return response.data;
  },

  async getWritingStyles() {
    const response = await api.get('/ai/writing-styles');
    return response.data;
  },

  async polishContent(request: AIPolishRequest): Promise<AIResponse> {
    const response = await api.post('/ai/polish', request);
    return response.data;
  },

  async chatWithAI(request: AIChatRequest): Promise<AIResponse> {
    const response = await api.post('/ai/chat', request);
    return response.data;
  },

  async suggestPlot(novelId: number): Promise<AIResponse> {
    const response = await api.post('/ai/suggest-plot', { novel_id: novelId });
    return response.data;
  },

  async testAI(): Promise<any> {
    const response = await api.post('/ai/test');
    return response.data;
  }
};