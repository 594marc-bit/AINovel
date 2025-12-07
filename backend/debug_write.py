"""
调试AI续写问题
"""
import asyncio
import json
from openai import AsyncOpenAI
from app.core.config import settings

async def debug_write():
    """调试AI续写"""
    print("=== 调试AI续写 ===")
    print(f"LLM API Key: {settings.LLM_API_KEY[:10]}...")
    print(f"LLM Base URL: {settings.LLM_BASE_URL}")
    print(f"LLM Model: {settings.LLM_MODEL_NAME}")

    client = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL
    )

    # 构建系统提示词
    system_prompt = """你是一个专业的小说作家。请根据用户提供的内容，续写下一段内容。

基本要求：
1. 保持文风和语调的一致性
2. 情节连贯，符合逻辑
3. 人物性格保持一致
4. 语言生动有趣
5. 根据长度要求控制内容长度（400-600字）
6. 确保已有角色的性格、说话方式和行为逻辑保持一致
7. 确保情节发展符合故事背景和已经建立的设定"""

    # 构建用户提示词
    previous_content = "李明是一个普通的程序员，每天过着朝九晚五的生活。这一天，他像往常一样来到公司，却发现"
    user_prompt = f"""前文内容：
{previous_content}

请续写下一段内容。"""

    print("\n=== 调用API ===")
    print(f"System Prompt长度: {len(system_prompt)}")
    print(f"User Prompt长度: {len(user_prompt)}")

    try:
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1000,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )

        content = response.choices[0].message.content or ""
        print(f"\n=== 成功 ===")
        print(f"生成内容长度: {len(content)}")
        print(f"生成内容:\n{content}")

    except Exception as e:
        print(f"\n=== 失败 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_write())