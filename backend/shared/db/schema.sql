CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description_compressed TEXT NOT NULL,
    description_original BYTEA NOT NULL,
    compression_ratio REAL NOT NULL,
    semantic_similarity REAL NOT NULL,
    validation_score REAL NOT NULL,
    model_version TEXT NOT NULL,
    last_accessed TIMESTAMPTZ,
    access_count BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    specs JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    review_summary TEXT,
    sentiment_score REAL,
    fake_probability REAL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS embeddings (
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    embedding_original VECTOR(768),
    embedding_compressed VECTOR(384),
    embedding_aligned VECTOR(768),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (product_id)
);

CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw
ON embeddings USING hnsw (embedding_aligned vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_products_specs_gin
ON products USING gin (specs);

CREATE INDEX IF NOT EXISTS idx_products_hot
ON products (last_accessed)
WHERE last_accessed > NOW() - INTERVAL '30 days';
