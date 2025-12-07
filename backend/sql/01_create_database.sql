-- 创建数据库
CREATE DATABASE ainovel;

-- 连接到 ainovel 数据库
\c ainovel;

-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;