import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.core.config import settings
from app.db.database import async_session_maker, engine
from app.models import User, Novel, Chapter

async def test_connection():
    """测试数据库连接和数据查询"""
    try:
        # 测试数据库连接
        print("正在测试数据库连接...")

        # 创建异步引擎
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✓ 数据库连接成功！PostgreSQL 版本: {version}")

        # 测试会话创建
        async with async_session_maker() as session:
            print("✓ 数据库会话创建成功！")

            # 查询用户表
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()
            if user:
                print(f"✓ 找到测试用户: {user.username} ({user.email})")
            else:
                print("⚠ 用户表中没有数据")

            # 查询小说表
            result = await session.execute(select(Novel))
            novels = result.scalars().all()
            print(f"✓ 小说表查询成功，共 {len(novels)} 部小说")

            # 显示小说列表
            for novel in novels:
                result = await session.execute(
                    select(Chapter).where(Chapter.novel_id == novel.id)
                )
                chapters = result.scalars().all()
                print(f"  - 《{novel.title}》: {len(chapters)} 章节")

            # 测试 pgvector 扩展
            result = await session.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            vector_ext = result.scalar_one_or_none()
            if vector_ext:
                print("✓ pgvector 扩展已安装")
            else:
                print("⚠ pgvector 扩展未安装")

        print("\n🎉 数据库测试全部通过！可以启动应用了。")

    except Exception as e:
        print(f"\n❌ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())