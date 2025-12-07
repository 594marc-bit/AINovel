"""
测试简化的续写功能
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

from openai import AsyncOpenAI
from app.core.config import settings

async def simple_write_test():
    """简化的续写测试，不依赖数据库"""
    print("开始简化续写测试...")

    client = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL
    )

    try:
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个小说作家，请续写下面的内容。"},
                {"role": "user", "content": "李明走进办公室，发现所有人的电脑都变成了蓝色屏幕。他惊恐地看到，屏幕中央显示着一行字："}
            ],
            max_tokens=200,
            temperature=0.8
        )

        content = response.choices[0].message.content
        print("续写成功！")
        print(f"生成内容：{content}")
        return True

    except Exception as e:
        print(f"续写失败：{e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(simple_write_test())
    print("\n测试结果：", "成功" if success else "失败")