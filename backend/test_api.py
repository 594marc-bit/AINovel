"""
测试API配置
"""
import asyncio
from app.core.config import settings

def test_config():
    """测试配置是否正确加载"""
    print("测试配置...")
    print(f"LLM API Key: {settings.LLM_API_KEY[:10]}...")
    print(f"LLM Base URL: {settings.LLM_BASE_URL}")
    print(f"LLM Model: {settings.LLM_MODEL_NAME}")
    print(f"Embedding API Key: {settings.EMBEDDING_API_KEY[:10]}...")
    print(f"Embedding Base URL: {settings.EMBEDDING_BASE_URL}")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL_NAME}")

async def test_openai_client():
    """测试OpenAI客户端连接"""
    from openai import AsyncOpenAI

    print("\n测试大模型API连接...")
    client = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL
    )

    try:
        # 测试简单的chat completion
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "user", "content": "请说'测试成功'"}
            ],
            max_tokens=50
        )
        print(f"API响应: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"API连接失败: {e}")
        return False

if __name__ == "__main__":
    # 测试配置
    test_config()

    # 测试API连接
    success = asyncio.run(test_openai_client())

    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ API连接失败，请检查配置")