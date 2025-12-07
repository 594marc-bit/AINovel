# 数据库初始化指南

本文件夹包含了初始化 AI 小说创作平台数据库所需的所有 SQL 脚本。

## 执行步骤

### 1. 连接到 PostgreSQL

首先，使用 `psql` 或其他数据库管理工具连接到 PostgreSQL 服务器：

```bash
# 使用 psql 连接
psql -U postgres
```

### 2. 执行建库脚本

```sql
-- 执行第一个脚本创建数据库
\i 'e:/VSProjects/AINovel/ainovel/backend/sql/01_create_database.sql'
```

或者直接运行：
```bash
psql -U postgres -f backend/sql/01_create_database.sql
```

### 3. 创建表结构

连接到 ainovel 数据库后，执行建表脚本：

```sql
\c ainovel
\i 'e:/VSProjects/AINovel/ainovel/backend/sql/02_create_tables.sql'
```

或者直接运行：
```bash
psql -U postgres -d ainovel -f backend/sql/02_create_tables.sql
```

### 4. 插入示例数据（可选）

```sql
\i 'e:/VSProjects/AINovel/ainovel/backend/sql/03_sample_data.sql'
```

或者直接运行：
```bash
psql -U postgres -d ainovel -f backend/sql/03_sample_data.sql
```

## 数据库结构说明

### 表结构

1. **users** - 用户表
   - 存储用户基本信息
   - 默认创建了一个测试用户：admin/admin@example.com

2. **novels** - 小说表
   - 存储小说的基本信息
   - 包含状态：draft（草稿）、published（已发布）、completed（已完成）

3. **chapters** - 章节表
   - 存储小说章节内容
   - 支持AI生成标识

4. **novel_embeddings** - 向量嵌入表
   - 存储 AI 上下文的向量表示
   - 使用 pgvector 进行相似度搜索
   - 支持 HNSW 索引优化

### 索引

- 为提高查询性能，在关键字段上创建了 B-tree 索引
- 为向量搜索创建了 HNSW 索引
- 支持基于余弦相似度的向量搜索

## 测试数据

示例数据包含：
- 3本示例小说
- 每本小说包含1-2个章节
- 一个测试用户账号

## 注意事项

1. 确保 PostgreSQL 已安装 pgvector 扩展
2. 数据库默认编码使用 UTF-8
3. 所有时间戳字段都带有时区信息
4. 表之间的关系都设置了适当的 ON DELETE CASCADE