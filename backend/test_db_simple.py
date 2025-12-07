import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, select, text
from app.core.config import settings
from app.models import User, Novel, Chapter

def test_db():
    """测试数据库连接"""
    try:
        print("测试数据库连接...")

        # 使用同步数据库URL
        sync_db_url = settings.DATABASE_URL.replace("+psycopg", "")
        print(f"数据库URL: {sync_db_url}")

        # 创建引擎
        engine = create_engine(sync_db_url)

        # 测试连接
        with engine.connect() as conn:
            print("[OK] 数据库连接成功！")

            # 获取版本信息
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"PostgreSQL 版本: {version[:60]}...")

            # 检查表是否存在
            result = conn.execute(text("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            print(f"[OK] 找到表: {', '.join(tables)}")

            # 检查 pgvector 扩展
            result = conn.execute(text("""
                SELECT 1 FROM pg_extension WHERE extname = 'vector'
            """))
            if result.scalar():
                print("[OK] pgvector 扩展已安装")
            else:
                print("[WARN] pgvector 扩展未安装")

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
                    for chapter in chapters[:2]:  # 只显示前2章
                        content_preview = chapter.content[:50] if chapter.content else ""
                        print(f"    * {chapter.title}: {content_preview}...")

        print("\n[SUCCESS] 数据库测试全部通过！")
        return True

    except Exception as e:
        print(f"\n[ERROR] 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_db()
    sys.exit(0 if success else 1)