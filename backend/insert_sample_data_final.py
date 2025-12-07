import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

def insert_data():
    """插入示例数据"""
    try:
        print("插入示例数据...")

        sync_db_url = settings.DATABASE_URL.replace("+psycopg", "")
        engine = create_engine(sync_db_url)

        with engine.connect() as conn:
            # 清空已有数据
            conn.execute(text("TRUNCATE TABLE chapters RESTART IDENTITY CASCADE"))
            conn.execute(text("TRUNCATE TABLE novels RESTART IDENTITY CASCADE"))
            print("[OK] 已清空小说和章节表")

            # 插入小说数据
            novels_data = [
                ('星辰之海', '一个关于星际探索和人类命运的科幻史诗', 1, 'draft'),
                ('江南烟雨', '古代江南的爱情故事，充满了诗意和忧伤', 1, 'published'),
                ('代码人生', '一个程序员的奋斗史和成长历程', 1, 'draft')
            ]

            for title, desc, author_id, status in novels_data:
                result = conn.execute(
                    text("INSERT INTO novels (title, description, author_id, status) VALUES (:title, :desc, :author_id, :status) RETURNING id"),
                    {'title': title, 'desc': desc, 'author_id': author_id, 'status': status}
                )
                novel_id = result.scalar()
                print(f"[OK] 插入小说: {title} (ID: {novel_id})")

                # 插入章节
                if title == '星辰之海':
                    chapters = [
                        ('第一章：启程', '在人类终于掌握了星际航行技术的第十年，巨大的探索者号宇宙飞船静静地停泊在月球轨道上。船长张明站在舰桥上，凝视着远方深邃的宇宙，心中充满了对未知世界的好奇和期待。', novel_id, 1),
                        ('第二章：星际跳跃', '探索者号的引擎开始预热，巨大的能量在反应堆中涌动。所有的船员都各就各位，紧张而兴奋地等待着那个历史性的时刻。', novel_id, 2)
                    ]
                elif title == '江南烟雨':
                    chapters = [
                        ('第一章：初遇', '春雨如丝，轻柔地打在油纸伞上。苏小曼走在青石板铺就的小巷里，雨滴顺着伞檐滑落，在地面溅起一朵朵小小的水花。', novel_id, 1)
                    ]
                elif title == '代码人生':
                    chapters = [
                        ('第一章：Hello World', '2005年的夏天，我第一次接触到了编程。那时的我还是一个懵懂的高中生，对计算机的世界充满了好奇。', novel_id, 1)
                    ]

                for chapter_title, content, nid, chapter_num in chapters:
                    conn.execute(
                        text("INSERT INTO chapters (title, content, novel_id, chapter_number) VALUES (:title, :content, :nid, :num)"),
                        {'title': chapter_title, 'content': content, 'nid': nid, 'num': chapter_num}
                    )
                    print(f"  [OK] 插入章节: {chapter_title}")

            conn.commit()

        print("\n[SUCCESS] 示例数据插入成功！")
        return True

    except Exception as e:
        print(f"\n[ERROR] 插入数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = insert_data()
    sys.exit(0 if success else 1)