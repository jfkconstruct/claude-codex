# RAG (Retrieval-Augmented Generation) Patterns with Claude

## Overview

RAG combines Claude's generation capabilities with external knowledge retrieval to build applications that can answer questions over custom data sources.

## Core RAG Architecture

```
┌─────────────┐
│   Documents │
└──────┬──────┘
       │ 1. Chunk & Embed
       ▼
┌─────────────┐
│Vector Store │
└──────┬──────┘
       │ 2. Similarity Search
       ▼
┌─────────────┐      ┌────────┐
│  Retrieved  │──3──▶│ Claude │
│   Context   │      └────┬───┘
└─────────────┘           │ 4. Generate
                          ▼
                   ┌─────────────┐
                   │   Response  │
                   └─────────────┘
```

## Implementation Patterns

### 1. Basic RAG Pattern

**Simple Document Q&A**:

```python
import voyageai
from anthropic import Anthropic
from pinecone import Pinecone

# Initialize clients
voyage = voyageai.Client()
anthropic = Anthropic()
pc = Pinecone(api_key="...")
index = pc.Index("documents")

def basic_rag(question: str) -> str:
    """Simple RAG implementation"""

    # 1. Embed query
    query_embedding = voyage.embed(
        [question],
        model="voyage-large-2",
        input_type="query"
    ).embeddings[0]

    # 2. Retrieve relevant documents
    results = index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    # 3. Build context
    context = "\n\n".join([
        f"Document {i+1}: {match['metadata']['text']}"
        for i, match in enumerate(results['matches'])
    ])

    # 4. Generate with Claude
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""
        }]
    )

    return response.content[0].text
```

### 2. Cached RAG Pattern

**Optimize for Repeated Queries**:

```python
def cached_rag(question: str, conversation_id: str) -> str:
    """RAG with prompt caching for multi-turn conversations"""

    # Retrieve context (same as basic RAG)
    query_embedding = voyage.embed([question], model="voyage-large-2").embeddings[0]
    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)
    context = "\n\n".join([m['metadata']['text'] for m in results['matches']])

    # Use caching for static context
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": "You are a helpful assistant that answers questions based on provided context.",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"Context:\n{context}",
                "cache_control": {"type": "ephemeral"}  # Cache the context
            }
        ],
        messages=[{
            "role": "user",
            "content": question
        }]
    )

    return response.content[0].text

# Subsequent questions in same conversation hit cache (90% cost reduction)
```

### 3. Hybrid Search RAG

**Combine Vector + Keyword Search**:

```python
from weaviate import Client

def hybrid_rag(question: str, alpha: float = 0.75) -> str:
    """RAG with hybrid search (vector + keyword)"""

    client = Client("https://your-instance.weaviate.network")

    # Hybrid search (alpha: 0=keyword, 1=vector)
    results = (
        client.query
        .get("Document", ["content", "title", "url"])
        .with_hybrid(
            query=question,
            alpha=alpha,  # Balance between keyword and vector
            properties=["content", "title"]  # Search these fields
        )
        .with_limit(5)
        .do()
    )

    documents = results["data"]["Get"]["Document"]

    # Build rich context with metadata
    context = "\n\n".join([
        f"Title: {doc['title']}\nSource: {doc['url']}\n{doc['content']}"
        for doc in documents
    ])

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

### 4. Multi-Hop RAG

**Answer Questions Requiring Multiple Retrieval Steps**:

```python
def multi_hop_rag(question: str, max_hops: int = 3) -> str:
    """RAG with multiple retrieval rounds"""

    anthropic_client = Anthropic()
    all_context = []
    current_query = question

    for hop in range(max_hops):
        # 1. Retrieve documents for current query
        query_embedding = voyage.embed([current_query], model="voyage-large-2").embeddings[0]
        results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

        # 2. Add to context
        hop_context = [m['metadata']['text'] for m in results['matches']]
        all_context.extend(hop_context)

        # 3. Check if we need more information
        check_response = anthropic_client.messages.create(
            model="claude-haiku-4-0",  # Fast model for checking
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": f"""Given this context, can you answer: {question}

Context so far:
{chr(10).join(all_context)}

Respond with:
1. "SUFFICIENT" if you can answer
2. "NEED_MORE: <specific info needed>" if you need more information"""
            }]
        )

        response_text = check_response.content[0].text

        if response_text.startswith("SUFFICIENT"):
            break

        # Extract what to search for next
        if response_text.startswith("NEED_MORE:"):
            current_query = response_text.split("NEED_MORE:")[1].strip()

    # Final generation with all context
    final_response = anthropic_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Context:\n{chr(10).join(all_context)}

Question: {question}

Answer:"""
        }]
    )

    return final_response.content[0].text
```

### 5. Filtered RAG

**Apply Metadata Filters for Better Retrieval**:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

def filtered_rag(
    question: str,
    category: str = None,
    date_range: tuple = None
) -> str:
    """RAG with metadata filtering"""

    client = QdrantClient("https://your-cluster.qdrant.io")
    query_embedding = voyage.embed([question], model="voyage-large-2").embeddings[0]

    # Build filters
    filter_conditions = []

    if category:
        filter_conditions.append(
            FieldCondition(key="category", match=MatchValue(value=category))
        )

    if date_range:
        start_date, end_date = date_range
        filter_conditions.append(
            FieldCondition(
                key="date",
                range={
                    "gte": start_date,
                    "lte": end_date
                }
            )
        )

    # Search with filters
    results = client.search(
        collection_name="documents",
        query_vector=query_embedding,
        query_filter=Filter(must=filter_conditions) if filter_conditions else None,
        limit=5
    )

    context = "\n\n".join([hit.payload["text"] for hit in results])

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

### 6. Agentic RAG

**Let Claude Decide When to Retrieve**:

```python
def agentic_rag(question: str) -> str:
    """Claude decides when to use retrieval"""

    tools = [{
        "name": "search_documents",
        "description": "Search the knowledge base for relevant information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant documents"
                }
            },
            "required": ["query"]
        }
    }]

    def search_documents(query: str) -> str:
        """Actual retrieval implementation"""
        query_embedding = voyage.embed([query], model="voyage-large-2").embeddings[0]
        results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
        return "\n\n".join([m['metadata']['text'] for m in results['matches']])

    # Initial message
    messages = [{
        "role": "user",
        "content": question
    }]

    while True:
        response = anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            tools=tools,
            messages=messages
        )

        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Execute tool
            tool_use = next(block for block in response.content if block.type == "tool_use")

            if tool_use.name == "search_documents":
                search_result = search_documents(tool_use.input["query"])

                # Add tool result to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": search_result
                    }]
                })

        else:
            # Claude is done, return final answer
            return response.content[0].text
```

## Chunking Strategies

### 1. Fixed-Size Chunking

```python
def chunk_by_tokens(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """Simple token-based chunking"""
    # Rough estimation: 1 token ≈ 4 characters
    char_chunk_size = chunk_size * 4
    char_overlap = overlap * 4

    chunks = []
    start = 0

    while start < len(text):
        end = start + char_chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - char_overlap

    return chunks
```

### 2. Semantic Chunking

```python
def semantic_chunk(text: str, max_chunk_size: int = 1000) -> list[str]:
    """Chunk by semantic boundaries (paragraphs, sentences)"""
    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(para)

        if current_size + para_size > max_chunk_size and current_chunk:
            # Save current chunk
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size

    # Add remaining
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks
```

### 3. Recursive Chunking (LangChain Style)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def recursive_chunk(text: str) -> list[str]:
    """Chunk with recursive splitting on multiple separators"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
```

## Document Processing Pipeline

```python
class DocumentProcessor:
    """Complete document processing pipeline"""

    def __init__(self, voyage_client, vector_index):
        self.voyage = voyage_client
        self.index = vector_index

    def process_and_index(self, documents: list[dict]):
        """Process documents and add to vector store"""
        all_chunks = []

        for doc in documents:
            # 1. Extract text
            text = self.extract_text(doc)

            # 2. Clean
            text = self.clean_text(text)

            # 3. Chunk
            chunks = semantic_chunk(text, max_chunk_size=1000)

            # 4. Add metadata
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": doc["url"],
                    "title": doc["title"],
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                })

        # 5. Embed in batches
        BATCH_SIZE = 100
        for i in range(0, len(all_chunks), BATCH_SIZE):
            batch = all_chunks[i:i+BATCH_SIZE]
            texts = [c["text"] for c in batch]

            embeddings = self.voyage.embed(
                texts,
                model="voyage-large-2",
                input_type="document"
            ).embeddings

            # 6. Upload to vector store
            vectors = [
                {
                    "id": f"chunk-{i+j}",
                    "values": embedding,
                    "metadata": chunk
                }
                for j, (embedding, chunk) in enumerate(zip(embeddings, batch))
            ]

            self.index.upsert(vectors=vectors)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        # Remove special characters if needed
        # Add domain-specific cleaning
        return text

    def extract_text(self, doc: dict) -> str:
        """Extract text from various document formats"""
        # Implement format-specific extraction
        # PDF, DOCX, HTML, etc.
        return doc.get("content", "")
```

## Evaluation Patterns

### 1. Retrieval Quality

```python
def evaluate_retrieval(
    test_queries: list[dict]  # {"query": "...", "relevant_doc_ids": [...]}
) -> dict:
    """Evaluate retrieval quality"""
    metrics = {
        "precision_at_5": [],
        "recall_at_5": [],
        "mrr": []  # Mean Reciprocal Rank
    }

    for item in test_queries:
        query_embedding = voyage.embed([item["query"]], model="voyage-large-2").embeddings[0]
        results = index.query(vector=query_embedding, top_k=5)

        retrieved_ids = [r["id"] for r in results["matches"]]
        relevant_ids = set(item["relevant_doc_ids"])

        # Precision@5
        precision = len(set(retrieved_ids) & relevant_ids) / 5
        metrics["precision_at_5"].append(precision)

        # Recall@5
        recall = len(set(retrieved_ids) & relevant_ids) / len(relevant_ids)
        metrics["recall_at_5"].append(recall)

        # MRR
        for i, rid in enumerate(retrieved_ids):
            if rid in relevant_ids:
                metrics["mrr"].append(1 / (i + 1))
                break
        else:
            metrics["mrr"].append(0)

    # Average metrics
    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

### 2. End-to-End RAG Quality

```python
def evaluate_rag_quality(test_cases: list[dict]) -> dict:
    """Evaluate complete RAG pipeline"""
    # test_cases: [{"question": "...", "expected_answer": "...", "context": [...]}]

    anthropic_client = Anthropic()
    scores = []

    for case in test_cases:
        # Get RAG answer
        answer = basic_rag(case["question"])

        # Use Claude to evaluate
        eval_prompt = f"""Compare the generated answer to the expected answer.

Question: {case["question"]}

Expected Answer: {case["expected_answer"]}

Generated Answer: {answer}

Rate the generated answer from 0-10 based on:
- Correctness
- Completeness
- Relevance

Output only a number 0-10."""

        eval_response = anthropic_client.messages.create(
            model="claude-haiku-4-0",
            max_tokens=10,
            messages=[{"role": "user", "content": eval_prompt}]
        )

        score = float(eval_response.content[0].text.strip())
        scores.append(score)

    return {
        "average_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores)
    }
```

## Common Gotchas

### 1. Context Window Overflow
**Issue**: Too many retrieved chunks exceed Claude's context
**Solution**:
```python
def smart_context_builder(chunks: list[str], max_tokens: int = 100000) -> str:
    """Build context that fits in context window"""
    context_parts = []
    total_tokens = 0

    for chunk in chunks:
        chunk_tokens = len(chunk) // 4  # Rough estimate
        if total_tokens + chunk_tokens > max_tokens:
            break
        context_parts.append(chunk)
        total_tokens += chunk_tokens

    return "\n\n".join(context_parts)
```

### 2. Low-Quality Retrieval
**Issue**: Retrieved documents not relevant
**Solutions**:
- Use hybrid search (vector + keyword)
- Add metadata filters
- Improve chunking strategy
- Use better embedding model (voyage-large-2)
- Add similarity score threshold

```python
# Filter by similarity score
results = index.query(vector=query_embedding, top_k=10)
filtered_results = [r for r in results["matches"] if r["score"] > 0.7]
```

### 3. Stale Document Updates
**Issue**: Updated documents not reflected
**Solution**: Implement versioning and update strategy
```python
def update_document(doc_id: str, new_content: str):
    """Update document in vector store"""
    # 1. Delete old chunks
    index.delete(filter={"doc_id": doc_id})

    # 2. Re-process and index new content
    chunks = semantic_chunk(new_content)
    # ... embed and upload
```

### 4. Embedding Model Mismatch
**Issue**: Query embedding different model than documents
**Solution**: Always use same model for queries and documents

## Best Practices Summary

### ✅ Do's
1. Use Voyage AI embeddings (recommended by Anthropic)
2. Implement prompt caching for repeated contexts
3. Add metadata to chunks (source, date, category)
4. Use semantic chunking over fixed-size
5. Monitor retrieval quality metrics
6. Implement fallback strategies

### ❌ Don'ts
1. Don't mix embedding models
2. Don't skip chunking optimization
3. Don't ignore context window limits
4. Don't forget to handle edge cases (no results, too many results)
5. Don't skip evaluation

## Resources

- **Anthropic RAG Guide**: https://www.anthropic.com/learn/build-with-claude
- **Cookbook**: https://github.com/anthropics/anthropic-cookbook/
- **Voyage AI**: https://docs.voyageai.com/
- **Vector DB Comparison**: See [vector-databases.md](./vector-databases.md)

## Related Patterns

- [Vector Databases](./vector-databases.md) - Storage backends
- [Best Practices](./best-practices.md) - General integration patterns
- [LangChain](./langchain.md) - RAG with LangChain
- [LlamaIndex](./llamaindex.md) - RAG with LlamaIndex
