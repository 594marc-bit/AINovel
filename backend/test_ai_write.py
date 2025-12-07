"""
测试AI续写功能的简单脚本
"""
import asyncio
from app.services.ai_service import ai_service
from app.schemas.ai import AIWriteRequest

async def test_ai_write():
    """测试AI续写功能"""
    print("开始测试AI续写功能...")

    # 创建测试请求
    request = AIWriteRequest(
        novel_id=1,
        previous_content="李明是一个普通的程序员，每天过着朝九晚五的生活。这一天，他像往常一样来到公司，却发现...",
        length_hint="short",
        use_context=False,  # 不使用上下文，直接测试
        writing_style="descriptive",
        tone="serious"
    )

    try:
        # 生成续写内容
        print("正在生成续写内容...")
        content = await ai_service.generate_novel_content(request)

        print("=" * 50)
        print("续写成功！")
        print("=" * 50)
        print("前文内容：")
        print(request.previous_content)
        print("\nAI续写内容：")
        print(content)
        print("=" * 50)

    except Exception as e:
        print(f"续写失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_write())