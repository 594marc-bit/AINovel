import psycopg
from sqlalchemy import create_engine, select, text
from app.core.config import settings
from app.models import User, Novel, Chapter

def test_connection():
    """测试数据库连接（同步版本）"""
    try:
        print("正在测试数据库连接...")

        # 使用同步方式测试连接
        sync_db_url = settings.DATABASE_URL.replace("+psycopg", "")

        # 直接使用 psycopg 测试连接
        with psycopg.connect(sync_db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print("[OK] 数据库连接成功！")
                print(f"  PostgreSQL 版本: {version[:50]}...")

                # 检查 pgvector 扩展
                cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
                if cur.fetchone():
                    print("[OK] pgvector 扩展已安装")
                else:
                    print("[WARN] pgvector 扩展未安装")

        # 使用 SQLAlchemy 查询数据
        engine = create_engine(sync_db_url)
        with engine.connect() as conn:
            print("[OK] SQLAlchemy 连接成功！")

            # 查询用户
            result = conn.execute(select(User).limit(1))
            user = result.first()
            if user:
                print(f"[OK] 找到测试用户: {user.username} ({user.email})")
            else:
                print("[WARN] 用户表中没有数据")

            # 查询小说
            result = conn.execute(select(Novel))
            novels = result.all()
            print(f"[OK] 小说表查询成功，共 {len(novels)} 部小说")

            # 显示小说和章节信息
            for novel in novels:
                result = conn.execute(
                    select(Chapter).where(Chapter.novel_id == novel.id)
                )
                chapters = result.all()
                print(f"  - 《{novel.title}》: {len(chapters)} 章节")

                if chapters:
                    for chapter in chapters:
                        content_preview = chapter.content[:50] if chapter.content else ""
                        print(f"    * {chapter.title}: {content_preview}...")

        print("\n[SUCCESS] 数据库测试全部通过！可以启动应用了。")
        return True

    except Exception as e:
        print(f"\n[ERROR] 数据库测试失败: {e}")
        return False

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    success = test_connection()
    sys.exit(0 if success else 1)