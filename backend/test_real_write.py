"""
测试实际的AI续写功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from app.services.ai_service import ai_service
from app.schemas.ai import AIWriteRequest
from app.db.database import get_db, engine, Base

async def test_real_write():
    """测试实际的AI续写功能"""
    print("开始测试实际AI续写功能...")

    # 创建测试请求
    request = AIWriteRequest(
        novel_id=1,
        previous_content="李明是一个普通的程序员，每天过着朝九晚五的生活。这一天，他像往常一样来到公司，却发现",
        length_hint="short",
        use_context=False,  # 不使用上下文，简化测试
        writing_style="descriptive"
    )

    # 获取数据库会话
    async for db in get_db():
        try:
            print(f"请求参数: {request}")
            print("正在调用AI服务...")

            # 调用AI服务
            content = await ai_service.generate_novel_content(request, db)

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
        finally:
            await db.close()
        break

if __name__ == "__main__":
    asyncio.run(test_real_write())