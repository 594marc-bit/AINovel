import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

def reset_data():
    """重置数据并重新插入"""
    try:
        print("重置数据库数据...")

        sync_db_url = settings.DATABASE_URL.replace("+psycopg", "")
        engine = create_engine(sync_db_url)

        with engine.connect() as conn:
            # 删除所有数据
            conn.execute(text("TRUNCATE TABLE chapters RESTART IDENTITY CASCADE"))
            conn.execute(text("TRUNCATE TABLE novels RESTART IDENTITY CASCADE"))
            print("[OK] 已清空小说和章节表")

            # 重新插入示例数据
            novels_sql = """
            INSERT INTO novels (title, description, author_id, status) VALUES
            ('星辰之海', '一个关于星际探索和人类命运的科幻史诗', 1, 'DRAFT'),
            ('江南烟雨', '古代江南的爱情故事，充满了诗意和忧伤', 1, 'PUBLISHED'),
            ('代码人生', '一个程序员的奋斗史和成长历程', 1, 'DRAFT')
            RETURNING id, title
            """
            result = conn.execute(text(novels_sql))
            novels = result.fetchall()
            print(f"[OK] 插入了 {len(novels)} 部小说")

            # 插入章节
            chapters_sql = """
            INSERT INTO chapters (title, content, novel_id, chapter_number) VALUES
            ('第一章：启程', '在人类终于掌握了星际航行技术的第十年，巨大的探索者号宇宙飞船静静地停泊在月球轨道上。船长张明站在舰桥上，凝视着远方深邃的宇宙，心中充满了对未知世界的好奇和期待。

明天，他们就要踏上前往半人马座阿尔法星的征程，这是人类历史上第一次如此深远的星际探索。

"船长，一切准备就绪。"大副李娜的声音从通讯器中传来。

张明深吸了一口气，"收到，通知所有船员，明天一早准时出发。"

这是人类文明的新篇章，也是他个人梦想的实现。', 1, 1),

            ('第二章：星际跳跃', '探索者号的引擎开始预热，巨大的能量在反应堆中涌动。所有的船员都各就各位，紧张而兴奋地等待着那个历史性的时刻。

"十、九、八......"倒计时的声音在舰桥回响。

"三、二、一，启动！"

瞬间，飞船周围的空间开始扭曲，一个巨大的虫洞在飞船前方形成。探索者号缓缓驶入虫洞，消失在原地。

几分钟后，飞船出现在距离太阳系4.3光年的地方。透过舷窗，可以看到半人马座阿尔法星正在前方闪耀。

"我们成功了！"舰桥上爆发出欢呼声。', 1, 2),

            ('第一章：初遇', '春雨如丝，轻柔地打在油纸伞上。苏小曼走在青石板铺就的小巷里，雨滴顺着伞檐滑落，在地面溅起一朵朵小小的水花。

这是她第一次来苏州，这座传说中的江南水乡。雨水洗过的青瓦白墙，倒映在水中的石拱桥，还有偶尔划过的小船，一切都如诗如画。

突然，一阵悠扬的古筝声从巷子深处传来。苏小曼停下脚步，循声望去，只见一位白衣公子坐在窗前，素手抚琴，神情专注。

雨声、琴声，交织在一起，构成了这江南最美的画卷。', 2, 1),

            ('第一章：Hello World', '2005年的夏天，我第一次接触到了编程。那时的我还是一个懵懂的高中生，对计算机的世界充满了好奇。

"hello.c"，这是我创建的第一个C语言文件。按照书本上的教程，我小心翼翼地敲下了每一行代码：

#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}

编译、运行，当屏幕上出现"Hello, World!"的那一刻，我的世界被彻底改变了。

原来，代码可以如此神奇，可以让机器听从人的指令。从那时起，我知道了这就是我想要的人生。', 3, 1)
            """
            result = conn.execute(text(chapters_sql))
            print(f"[OK] 插入了 {result.rowcount} 个章节")

            conn.commit()

        print("\n[SUCCESS] 数据重置成功！")
        return True

    except Exception as e:
        print(f"\n[ERROR] 重置数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_data()
    sys.exit(0 if success else 1)