from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.ai import AIWriteRequest, AIResponse, AIPolishRequest, AIChatRequest
from app.crud import crud_novel, crud_chapter
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/write", response_model=AIResponse)
async def ai_write(
    request: AIWriteRequest,
    db: AsyncSession = Depends(get_db)
):
    """AI continues writing the novel with direct API call"""
    try:
        print(f"[API] 收到AI续写请求: {request}")

        # Verify novel exists
        novel = await crud_novel.get(db, id=request.novel_id)
        if not novel:
            print(f"[API] 小说不存在: novel_id={request.novel_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Novel not found"
            )

        print(f"[API] 小说存在: {novel.title}")

        # 直接调用三方API
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )

        # 构建提示词
        system_prompt = """你是一个专业的小说作家。请根据用户提供的内容，续写下一段内容。

要求：
1. 保持文风和语调的一致性
2. 情节连贯，符合逻辑
3. 人物性格保持一致
4. 语言生动有趣"""

        # 根据长度要求调整
        length_guide = {
            "short": "200-300字",
            "medium": "400-600字",
            "long": "800-1000字"
        }
        system_prompt += f"\n5. 根据长度要求控制内容长度（{length_guide.get(request.length_hint, '400-600字')}）"

        # 构建用户提示词
        user_prompt_parts = []

        # 如果使用上下文，获取历史章节
        if request.use_context:
            chapters = await crud_chapter.get_by_novel(
                db,
                request.novel_id,
                limit=request.context_depth or 3
            )
            if chapters:
                context_text = "\n\n".join([
                    f"第{ch.chapter_number}章 {ch.title}\n{ch.content[:300]}..."
                    for ch in chapters
                ])
                user_prompt_parts.append(f"故事背景：\n{context_text}")

        # 添加前文内容
        if request.previous_content:
            user_prompt_parts.append(f"前文内容：\n{request.previous_content}")
        else:
            user_prompt_parts.append("（这是小说的开头）")

        # 添加风格提示
        if request.style_hint:
            user_prompt_parts.append(f"风格要求：{request.style_hint}")

        user_prompt_parts.append("请续写下一段内容。")
        user_prompt = "\n\n".join(user_prompt_parts)

        print(f"[API] 调用API生成内容...")

        # 调用API
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens={
                "short": 500,
                "medium": 1000,
                "long": 1500
            }.get(request.length_hint, 1000)
        )

        content = response.choices[0].message.content or ""
        print(f"[API] 生成内容长度: {len(content)}")

        return AIResponse(
            content=content,
            is_success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[API] 错误: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return AIResponse(
            content="",
            is_success=False,
            error_message=str(e)
        )

@router.post("/polish", response_model=AIResponse)
async def ai_polish(
    request: AIPolishRequest,
    db: AsyncSession = Depends(get_db)
):
    """AI polishes the provided content"""
    try:
        content = await ai_service.polish_content(
            content=request.content,
            instruction=request.instruction
        )

        return AIResponse(
            content=content,
            is_success=True
        )
    except Exception as e:
        return AIResponse(
            content="",
            is_success=False,
            error_message=str(e)
        )

@router.post("/chat", response_model=AIResponse)
async def ai_chat(
    request: AIChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """AI chat assistant for writing help"""
    try:
        # Get novel context if provided
        context = None
        if request.novel_id:
            novel = await crud_novel.get(db, id=request.novel_id)
            if novel:
                context = f"小说：{novel.title}\n描述：{novel.description or '无'}"

        content = await ai_service.chat_assistant(
            message=request.message,
            context=context,
            history=request.conversation_history
        )

        return AIResponse(
            content=content,
            is_success=True
        )
    except Exception as e:
        return AIResponse(
            content="",
            is_success=False,
            error_message=str(e)
        )

@router.post("/suggest-plot")
async def suggest_plot(
    novel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """AI suggests plot development based on existing content"""
    try:
        novel = await crud_novel.get(db, id=novel_id)
        if not novel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Novel not found"
            )

        # Get existing chapters for context
        chapters = await crud_chapter.get_by_novel(db, novel_id, limit=5)
        if not chapters:
            return AIResponse(
                content="请先写一些内容，我会基于这些内容为您建议情节发展。",
                is_success=True
            )

        # Combine recent chapters
        context = "\n\n".join([
            f"第{ch.chapter_number}章 {ch.title}\n{ch.content[:300]}..."
            for ch in chapters[-3:]
        ])

        message = f"""基于以下内容，请为小说《{novel.title}》提供3个可能的情节发展方向建议：

{context}

请以清晰的格式提供建议。"""

        content = await ai_service.chat_assistant(message=message)

        return AIResponse(
            content=content,
            is_success=True
        )
    except Exception as e:
        return AIResponse(
            content="",
            is_success=False,
            error_message=str(e)
        )

@router.get("/writing-styles")
async def get_writing_styles():
    """获取可用的写作风格选项"""
    return {
        "writing_styles": {
            "descriptive": "描述性 - 使用丰富的描述性语言，注重环境描写和感官细节",
            "dialog_heavy": "对话为主 - 以角色对话推进情节",
            "action_focused": "动作导向 - 重点描述动作和情节发展，节奏较快",
            "introspective": "内省式 - 注重内心独白和心理描写",
            "poetic": "诗意化 - 使用优美的语言和修辞手法",
            "minimalist": "极简主义 - 语言简洁，留有想象空间"
        },
        "tones": {
            "humorous": "幽默风趣",
            "serious": "严肃认真",
            "romantic": "浪漫温馨",
            "mysterious": "神秘悬疑",
            "dramatic": "戏剧性强",
            "lighthearted": "轻松愉快"
        },
        "pov_options": {
            "first_person": "第一人称（我）",
            "third_person_limited": "第三人称有限视角",
            "third_person_omniscient": "第三人称全知视角"
        },
        "length_options": {
            "short": "简短（200-300字）",
            "medium": "中等（400-600字）",
            "long": "长篇（800-1000字）"
        }
    }

@router.post("/test")
async def test_ai():
    """测试AI服务是否正常工作"""
    try:
        from app.schemas.ai import AIWriteRequest
        test_request = AIWriteRequest(
            novel_id=1,
            previous_content="这是一个测试请求。",
            length_hint="short",
            use_context=False  # 不使用上下文，简化测试
        )

        # 测试生成系统提示词
        system_prompt = ai_service.build_system_prompt(test_request)

        # 测试实际生成内容（不使用数据库）
        print("正在测试AI生成...")
        content = await ai_service.generate_novel_content(test_request)

        return {
            "status": "success",
            "message": "AI服务正常",
            "generated_content": content[:200] + "..." if len(content) > 200 else content,
            "system_prompt": system_prompt[:200] + "..." if len(system_prompt) > 200 else system_prompt,
            "config": {
                "llm_model": settings.LLM_MODEL_NAME,
                "llm_base_url": settings.LLM_BASE_URL
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"AI服务测试失败: {str(e)}"
        }


@router.post("/simple-write")
async def simple_write(request: dict):
    """简化的续写接口，不依赖数据库"""
    try:
        previous_content = request.get("previous_content", "")
        if not previous_content:
            previous_content = "这是一个故事的开头。"

        # 直接调用AI服务，不使用数据库
        from app.schemas.ai import AIWriteRequest
        write_request = AIWriteRequest(
            novel_id=1,  # 假设的ID
            previous_content=previous_content,
            length_hint=request.get("length_hint", "short"),
            use_context=False  # 不使用上下文
        )

        print(f"[SimpleWrite] 收到请求: {request}")
        content = await ai_service.generate_novel_content(write_request, None)
        print(f"[SimpleWrite] 生成内容长度: {len(content) if content else 0}")

        return {
            "status": "success",
            "content": content
        }

    except Exception as e:
        print(f"[SimpleWrite] 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"续写失败: {str(e)}"
        }
