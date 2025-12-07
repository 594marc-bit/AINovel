from openai import AsyncOpenAI
from typing import List, Optional, Dict
from app.core.config import settings
from app.schemas.ai import AIWriteRequest, AIPolishRequest, AIChatRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import crud_chapter
import json
import asyncio
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying API calls on failure"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            raise last_exception
        return wrapper
    return decorator

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )

    async def get_novel_context(self, db: AsyncSession, request: AIWriteRequest) -> str:
        """获取小说上下文信息（仅使用数据库中的历史章节）"""
        if not request.use_context or not request.novel_id:
            return ""

        context_parts = []

        # 获取历史章节上下文
        if request.chapter_id:
            chapters = await crud_chapter.get_by_novel(
                db,
                request.novel_id,
                limit=request.context_depth,
                before_chapter_id=request.chapter_id
            )
        else:
            chapters = await crud_chapter.get_by_novel(
                db,
                request.novel_id,
                limit=request.context_depth
            )

        if chapters:
            context_parts.append("=== 近期章节内容 ===")
            for chapter in chapters:
                context_parts.append(f"第{chapter.chapter_number}章 {chapter.title}\n{chapter.content[:500]}...")

        return "\n\n".join(context_parts)

    def build_system_prompt(self, request: AIWriteRequest) -> str:
        """根据请求参数构建系统提示词"""
        base_prompt = """你是一个专业的小说作家。请根据用户提供的内容，续写下一段内容。

基本要求：
1. 保持文风和语调的一致性
2. 情节连贯，符合逻辑
3. 人物性格保持一致
4. 语言生动有趣"""

        # 根据长度要求调整提示
        length_guide = {
            "short": "200-300字",
            "medium": "400-600字",
            "long": "800-1000字"
        }
        base_prompt += f"\n5. 根据长度要求控制内容长度（{length_guide.get(request.length_hint, '400-600字')}）"

        # 添加角色一致性要求
        if request.character_consistency:
            base_prompt += "\n6. 确保已有角色的性格、说话方式和行为逻辑保持一致"

        # 添加情节连续性要求
        if request.plot_continuity:
            base_prompt += "\n7. 确保情节发展符合故事背景和已经建立的设定"

        # 添加写作风格指导
        if request.writing_style:
            style_guides = {
                "descriptive": "使用丰富的描述性语言，注重环境描写和感官细节",
                "dialog_heavy": "以对话为主，通过角色互动推进情节",
                "action_focused": "重点描述动作和情节发展，节奏较快",
                "introspective": "注重内心独白和心理描写",
                "poetic": "使用优美的语言和修辞手法",
                "minimalist": "语言简洁，留有想象空间"
            }
            if request.writing_style in style_guides:
                base_prompt += f"\n8. 写作风格：{style_guides[request.writing_style]}"

        # 添加语气要求
        if request.tone:
            base_prompt += f"\n9. 语气要求：{request.tone}"

        # 添加目标读者考虑
        if request.target_audience:
            base_prompt += f"\n10. 考虑目标读者：{request.target_audience}"

        # 添加视角要求
        if request.pov:
            pov_guide = {
                "first_person": "使用第一人称视角（我）",
                "third_person_limited": "使用第三人称有限视角，聚焦某个角色的体验",
                "third_person_omniscient": "使用第三人称全知视角，可以描述所有角色的想法"
            }
            if request.pov in pov_guide:
                base_prompt += f"\n11. 视角要求：{pov_guide[request.pov]}"

        return base_prompt

    async def generate_novel_content(
        self,
        request: AIWriteRequest,
        db: Optional[AsyncSession] = None
    ) -> str:
        """Generate novel continuation based on previous content with enhanced features"""
        try:
            print(f"收到续写请求: novel_id={request.novel_id}, length_hint={request.length_hint}")

            # 构建系统提示词
            system_prompt = self.build_system_prompt(request)
            print(f"系统提示词长度: {len(system_prompt)}")

            # 构建用户提示词
            user_prompt_parts = []

            # 添加上下文信息
            if db and request.use_context:
                context = await self.get_novel_context(db, request)
                if context:
                    user_prompt_parts.append(f"故事上下文：\n{context}")

            # 添加前文内容
            if request.previous_content:
                user_prompt_parts.append(f"前文内容：\n{request.previous_content}")
            else:
                user_prompt_parts.append("（这是小说的开头）")

            # 添加风格提示
            if request.style_hint:
                user_prompt_parts.append(f"风格提示：{request.style_hint}")

            # 添加续写要求
            user_prompt_parts.append("\n请续写下一段内容。")

            user_prompt = "\n\n".join(user_prompt_parts)
            print(f"用户提示词长度: {len(user_prompt)}")

            # 调整参数
            temperature = 0.8  # 默认创造性
            if request.writing_style == "introspective":
                temperature = 0.7  # 内省式风格稍低
            elif request.writing_style == "action_focused":
                temperature = 0.9  # 动作风格稍高

            max_tokens = {
                "short": 500,
                "medium": 1000,
                "long": 1500
            }.get(request.length_hint, 1000)

            print(f"调用API: model={settings.LLM_MODEL_NAME}, temperature={temperature}, max_tokens={max_tokens}")

            response = await self.client.chat.completions.create(
                model=settings.LLM_MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1
            )

            content = response.choices[0].message.content or ""
            print(f"API调用成功，生成内容长度: {len(content)}")
            return content

        except Exception as e:
            print(f"AI生成失败 - 错误类型: {type(e).__name__}, 错误信息: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"AI生成失败: {str(e)}")

    async def polish_content(self, content: str, instruction: Optional[str] = None) -> str:
        """Polish and improve the provided content"""
        system_prompt = """你是一个专业的编辑。请根据用户的要求润色和改进提供的内容。
要求：
1. 保持原文的核心思想和风格
2. 改善语言表达，使其更加流畅生动
3. 修正语法和标点错误
4. 优化句式结构"""

        user_prompt = f"""原文内容：
{content}

润色要求：{instruction if instruction else "请对原文进行全面的润色和改进"}

请提供润色后的内容。"""

        response = await self.client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )

        return response.choices[0].message.content

    async def chat_assistant(self, message: str, context: Optional[str] = None, history: Optional[List[dict]] = None) -> str:
        """AI chat assistant for writing help"""
        system_prompt = """你是一个写作助理，专门帮助用户进行小说创作。
你可以：
1. 讨论情节发展和故事结构
2. 提供人物塑造建议
3. 帮助解决写作瓶颈
4. 提供创作灵感
5. 讨论文学技巧和表达方式

请用友好、专业的语调与用户交流。"""

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({
                "role": "system",
                "content": f"当前小说背景：\n{context}"
            })

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": message})

        response = await self.client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

ai_service = AIService()