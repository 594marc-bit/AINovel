-- Rename metadata column to meta_data to avoid SQLAlchemy reserved keyword
-- This migration updates the novel_embeddings table

ALTER TABLE novel_embeddings RENAME COLUMN metadata TO meta_data;

-- Add comment to the column
COMMENT ON COLUMN novel_embeddings.meta_data IS 'JSON string for additional metadata';