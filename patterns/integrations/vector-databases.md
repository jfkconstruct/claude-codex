# Claude + Vector Database Integration Patterns

## Overview

Vector databases enable semantic search and retrieval-augmented generation (RAG) by storing and querying embeddings. When integrated with Claude, they provide the foundation for knowledge-enhanced AI applications.

## Supported Vector Databases

- **Pinecone**: Fully managed, serverless vector database
- **Weaviate**: Open-source with knowledge graph capabilities
- **Qdrant**: Rust-based with advanced filtering
- **Chroma**: Lightweight, embedded database
- **Milvus**: Open-source, highly scalable
- **PgVector**: PostgreSQL extension
- **Redis**: In-memory with vector search

## Core Integration Pattern

### Standard RAG Workflow

```
1. Document Processing
   ├─> Chunk documents
   └─> Generate embeddings (Voyage AI, OpenAI, etc.)

2. Vector Storage
   ├─> Upload embeddings to vector DB
   └─> Store metadata alongside vectors

3. Query Processing
   ├─> Convert user query to embedding
   └─> Perform similarity search

4. Claude Generation
   ├─> Retrieve relevant context
   └─> Generate response with Claude
```

## Pinecone Integration

### Setup & Configuration

```python
import pinecone
from pinecone import ServerlessSpec
from anthropic import Anthropic

# Initialize Pinecone
pc = pinecone.Pinecone(api_key="YOUR_API_KEY")

# Create index
pc.create_index(
    name="claude-rag-index",
    dimension=1024,  # Match your embedding model
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-west-2"
    )
)

# Get index
index = pc.Index("claude-rag-index")
```

### RAG Implementation Pattern

```python
import voyageai
from anthropic import Anthropic

# Initialize clients
voyage = voyageai.Client(api_key="VOYAGE_API_KEY")
anthropic = Anthropic(api_key="ANTHROPIC_API_KEY")

# 1. Embed documents
documents = ["Doc 1 text...", "Doc 2 text...", "Doc 3 text..."]
embeddings = voyage.embed(
    documents,
    model="voyage-large-2",
    input_type="document"
).embeddings

# 2. Upload to Pinecone
vectors = [
    {
        "id": f"doc-{i}",
        "values": embedding,
        "metadata": {"text": doc}
    }
    for i, (embedding, doc) in enumerate(zip(embeddings, documents))
]
index.upsert(vectors=vectors)

# 3. Query workflow
def query_with_rag(question: str) -> str:
    # Embed query
    query_embedding = voyage.embed(
        [question],
        model="voyage-large-2",
        input_type="query"
    ).embeddings[0]

    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    # Build context
    context = "\n\n".join([
        match["metadata"]["text"]
        for match in results["matches"]
    ])

    # Generate with Claude
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )

    return response.content[0].text
```

### Best Practices for Pinecone

✅ **Do's**:
- Use namespaces to separate different datasets
- Implement metadata filtering for better retrieval
- Use serverless for variable workloads
- Monitor usage via Pinecone dashboard

```python
# Namespace usage
index.upsert(vectors=vectors, namespace="product-docs")
results = index.query(
    vector=query_embedding,
    namespace="product-docs",
    top_k=5
)

# Metadata filtering
results = index.query(
    vector=query_embedding,
    filter={"category": {"$eq": "technical"}},
    top_k=5
)
```

❌ **Don'ts**:
- Don't create too many indices (consolidate with namespaces)
- Don't skip batch upsert for large datasets
- Don't ignore dimension mismatches
- Don't forget to handle API rate limits

## Weaviate Integration

### Setup & Configuration

```python
import weaviate
from anthropic import Anthropic

# Initialize Weaviate
client = weaviate.Client(
    url="https://your-instance.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey("YOUR_API_KEY"),
    additional_headers={
        "X-OpenAI-Api-Key": "YOUR_OPENAI_KEY"  # For embeddings
    }
)

# Create schema
schema = {
    "class": "Document",
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "name": "content",
            "dataType": ["text"]
        },
        {
            "name": "category",
            "dataType": ["string"]
        }
    ]
}
client.schema.create_class(schema)
```

### RAG with GraphQL

```python
def query_weaviate_rag(question: str) -> str:
    # Weaviate performs embedding automatically with vectorizer
    results = (
        client.query
        .get("Document", ["content", "category"])
        .with_near_text({"concepts": [question]})
        .with_limit(5)
        .do()
    )

    documents = results["data"]["Get"]["Document"]
    context = "\n\n".join([doc["content"] for doc in documents])

    # Generate with Claude
    anthropic = Anthropic()
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )

    return response.content[0].text
```

### Weaviate Best Practices

✅ **Do's**:
- Leverage built-in vectorizers for convenience
- Use GraphQL for complex queries with filters
- Implement hybrid search (vector + keyword)
- Use cross-references for knowledge graphs

```python
# Hybrid search
results = (
    client.query
    .get("Document", ["content"])
    .with_hybrid(query=question, alpha=0.75)  # 0=keyword, 1=vector
    .with_limit(5)
    .do()
)
```

## Qdrant Integration

### Setup & Configuration

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize Qdrant
client = QdrantClient(
    url="https://your-cluster.qdrant.io",
    api_key="YOUR_API_KEY"
)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1024,  # Match embedding dimension
        distance=Distance.COSINE
    )
)
```

### Advanced Filtering Pattern

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

def query_qdrant_with_filters(question: str, category: str) -> str:
    # Embed query
    query_embedding = voyage.embed(
        [question],
        model="voyage-large-2",
        input_type="query"
    ).embeddings[0]

    # Search with filters
    results = client.search(
        collection_name="documents",
        query_vector=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category)
                )
            ]
        ),
        limit=5
    )

    context = "\n\n".join([hit.payload["text"] for hit in results])

    # Generate with Claude
    anthropic = Anthropic()
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )

    return response.content[0].text
```

### Qdrant Best Practices

✅ **Do's**:
- Use payload indexing for frequently filtered fields
- Leverage quantization for memory optimization
- Use scroll API for large result sets
- Implement multi-vector search for complex queries

```python
# Payload indexing
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema="keyword"
)

# Quantization for efficiency
from qdrant_client.models import ScalarQuantization, ScalarQuantizationConfig

client.update_collection(
    collection_name="documents",
    quantization_config=ScalarQuantizationConfig(
        scalar=ScalarQuantization(
            type="int8",
            quantile=0.99,
            always_ram=True
        )
    )
)
```

## Comparison Matrix

| Feature | Pinecone | Weaviate | Qdrant |
|---------|----------|----------|--------|
| **Deployment** | Fully managed | Managed or self-hosted | Cloud or self-hosted |
| **Scaling** | Automatic | Manual/Auto | Manual/Auto |
| **Filtering** | Basic metadata | GraphQL + filters | Advanced payload filters |
| **Hybrid Search** | No | Yes | Yes |
| **Best For** | Simplicity, scale | Knowledge graphs, complex queries | Advanced filtering, performance |
| **Pricing** | Usage-based | Varies | Usage-based |

## Common Gotchas Across All Vector DBs

### 1. Embedding Dimension Mismatch
**Issue**: Vector dimensions don't match index configuration
**Solution**:
```python
# Always verify embedding dimensions
embedding_dim = len(embedding_vector)
assert embedding_dim == index_dimension, "Dimension mismatch!"
```

### 2. Inconsistent Embedding Models
**Issue**: Switching embedding models breaks retrieval
**Solution**:
- Create new index when changing models
- Never mix embeddings from different models in same index
- Document which model was used

### 3. Context Window Overflow
**Issue**: Too many retrieved chunks exceed Claude's context
**Solution**:
```python
# Limit total context size
MAX_CONTEXT_TOKENS = 100000  # For Claude Sonnet

def truncate_context(chunks: list[str], max_tokens: int) -> str:
    total = 0
    selected = []
    for chunk in chunks:
        chunk_tokens = len(chunk) // 4  # Rough estimate
        if total + chunk_tokens > max_tokens:
            break
        selected.append(chunk)
        total += chunk_tokens
    return "\n\n".join(selected)
```

### 4. Cold Start Performance
**Issue**: First query after idle period is slow
**Solution**:
- Use serverless with auto-scaling
- Implement connection pooling
- Consider warm-up queries

### 5. Metadata Bloat
**Issue**: Large metadata slows retrieval
**Solution**:
```python
# Keep metadata lean
metadata = {
    "id": doc_id,
    "title": title,  # Store only what you need
    # Don't store entire document in metadata
}

# Retrieve full document separately if needed
```

## Embedding Model Selection

### Voyage AI (Recommended by Anthropic)
```python
import voyageai

vo = voyageai.Client()

# General purpose
embeddings = vo.embed(
    texts,
    model="voyage-large-2"  # Most powerful
)

# Domain-specific
embeddings = vo.embed(
    texts,
    model="voyage-code-2"  # For code
)
```

### OpenAI Embeddings
```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts,
    dimensions=1024  # Configurable
)
embeddings = [item.embedding for item in response.data]
```

## Performance Optimization

### 1. Batch Operations
```python
# Batch upsert (Pinecone example)
BATCH_SIZE = 100
for i in range(0, len(vectors), BATCH_SIZE):
    batch = vectors[i:i + BATCH_SIZE]
    index.upsert(vectors=batch)
```

### 2. Async Operations
```python
import asyncio
from anthropic import AsyncAnthropic

async def async_rag_query(question: str):
    # Parallel embedding and search
    query_embedding = await get_embedding_async(question)
    results = await vector_db.search_async(query_embedding)

    context = build_context(results)

    # Generate with Claude
    client = AsyncAnthropic()
    response = await client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{context}\n\n{question}"}]
    )

    return response.content[0].text
```

### 3. Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    """Cache embeddings for repeated queries"""
    return voyage.embed([text], model="voyage-large-2").embeddings[0]
```

## Resources

### Official Documentation
- **Pinecone + Claude**: https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb
- **Weaviate Docs**: https://weaviate.io/developers/weaviate
- **Qdrant Docs**: https://qdrant.tech/documentation/

### Integration Guides
- **Pipedream Pinecone + Anthropic**: https://pipedream.com/apps/pinecone/integrations/anthropic
- **AWS Bedrock + Pinecone**: RAG with Claude on Amazon Bedrock

## Related Patterns

- [RAG Patterns](./rag-patterns.md) - Detailed RAG implementation strategies
- [LangChain](./langchain.md) - LangChain vector store integrations
- [LlamaIndex](./llamaindex.md) - LlamaIndex vector store integrations
- [Best Practices](./best-practices.md) - Cross-cutting concerns
