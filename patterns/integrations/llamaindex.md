# Claude + LlamaIndex Integration Patterns

## Overview

LlamaIndex (formerly GPT Index) is a data framework designed specifically for building RAG (Retrieval-Augmented Generation) applications. It provides sophisticated indexing, querying, and data management capabilities optimized for LLM applications.

## Installation & Setup

### Basic Installation
```bash
pip install llama-index-llms-anthropic
```

### Full Installation with Dependencies
```bash
pip install llama-index
pip install llama-index-llms-anthropic
pip install llama-index-embeddings-openai  # For embeddings
```

## Basic Usage Patterns

### Initialize Claude with LlamaIndex
```python
from llama_index.llms.anthropic import Anthropic

# Basic setup
llm = Anthropic(
    model="claude-sonnet-4-0",
    api_key="your-api-key",  # Or set ANTHROPIC_API_KEY env var
    temperature=0.0,
    max_tokens=1024
)

# Simple completion
response = llm.complete("What is LlamaIndex?")
print(response)
```

### Chat Interface
```python
from llama_index.core.llms import ChatMessage

messages = [
    ChatMessage(role="system", content="You are a helpful assistant"),
    ChatMessage(role="user", content="Tell me about RAG")
]

response = llm.chat(messages)
print(response)
```

## Core Integration Patterns

### 1. Basic RAG Pipeline

**Complete RAG Setup** (from Anthropic Cookbook):

```python
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

# Step 1: Configure LLM and Embeddings
Settings.llm = Anthropic(model="claude-3-haiku-20240307")
Settings.embed_model = OpenAIEmbedding()

# Step 2: Load Documents
documents = SimpleDirectoryReader("./data").load_data()

# Step 3: Create Index
index = VectorStoreIndex.from_documents(documents)

# Step 4: Create Query Engine
query_engine = index.as_query_engine()

# Step 5: Query
response = query_engine.query("What is the main topic of these documents?")
print(response)
```

### 2. Agentic Tool Calling Pattern

```python
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.anthropic import Anthropic

# Define tools
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

tools = [
    FunctionTool.from_defaults(fn=multiply),
    FunctionTool.from_defaults(fn=add)
]

# Create agent
llm = Anthropic(model="claude-sonnet-4-0")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

# Use agent
response = agent.chat("What is (5 * 3) + 2?")
print(response)
```

### 3. Extended Thinking Mode (Claude 3.7+)

**Advanced Reasoning Pattern**:

```python
from llama_index.llms.anthropic import Anthropic

llm = Anthropic(
    model="claude-3-7-sonnet-20250219",
    thinking={
        "type": "enabled",
        "budget_tokens": 5000  # Allocate tokens for thinking
    }
)

# For complex reasoning tasks
response = llm.complete(
    "Solve this complex logic puzzle: [puzzle details]"
)
```

### 4. Multi-Modal Pattern

```python
from llama_index.core.schema import ImageDocument
from llama_index.multi_modal_llms.anthropic import AnthropicMultiModal

# Initialize multimodal LLM
mm_llm = AnthropicMultiModal(model="claude-3-opus-20240229")

# Process image with text
image_documents = [ImageDocument(image_path="./image.jpg")]
response = mm_llm.complete(
    prompt="What's in this image?",
    image_documents=image_documents
)
```

## Advanced Patterns

### Query Engine Customization

```python
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# Create custom retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5  # Return top 5 results
)

# Build query engine with custom settings
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=[...],  # Optional post-processing
)
```

### Streaming Responses

```python
# Stream completions
response = llm.stream_complete("Tell me a long story")
for token in response:
    print(token.delta, end="", flush=True)

# Stream chat
response = llm.stream_chat(messages)
for chunk in response:
    print(chunk.delta, end="", flush=True)
```

### Custom Prompt Templates

```python
from llama_index.core import PromptTemplate

qa_prompt_tmpl = PromptTemplate(
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context, answer: {query_str}\n"
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt_tmpl
)
```

## Best Practices

### ✅ Do's

1. **Use Settings for Global Configuration**
   ```python
   from llama_index.core import Settings

   Settings.llm = Anthropic(model="claude-sonnet-4-0")
   Settings.embed_model = OpenAIEmbedding()
   Settings.chunk_size = 512
   Settings.chunk_overlap = 50
   ```

2. **Leverage Async for Better Performance**
   ```python
   response = await llm.acomplete("prompt")
   response = await llm.achat(messages)
   ```

3. **Use Appropriate Chunk Sizes**
   - Smaller chunks (256-512): Better for precise retrieval
   - Larger chunks (1024-2048): Better for context preservation

4. **Implement Proper Error Handling**
   ```python
   try:
       response = query_engine.query("question")
   except Exception as e:
       logger.error(f"Query failed: {e}")
       # Fallback logic
   ```

5. **Cache Embeddings for Development**
   ```python
   from llama_index.core import StorageContext

   # Save index
   index.storage_context.persist(persist_dir="./storage")

   # Load later
   from llama_index.core import load_index_from_storage
   storage_context = StorageContext.from_defaults(persist_dir="./storage")
   index = load_index_from_storage(storage_context)
   ```

### ❌ Don'ts

1. **Don't Skip Document Preprocessing**
   - Always clean and structure documents before indexing
   - Remove unnecessary whitespace and formatting

2. **Don't Ignore Retrieval Quality**
   - Monitor similarity scores
   - Tune similarity_top_k based on use case

3. **Don't Hardcode API Keys**
   - Use environment variables
   - Implement proper secrets management

4. **Don't Over-Index**
   - Index only relevant documents
   - Implement document filtering strategies

## Common Gotchas

### 1. Model Name Compatibility
**Issue**: Using outdated model names
**Solution**: Use current model names like `claude-sonnet-4-0`

### 2. Embedding Model Mismatch
**Issue**: Changing embedding models breaks existing indices
**Solution**: Re-index when changing embedding models, or maintain separate indices

### 3. Context Window Management
**Issue**: Retrieved context exceeds model's context window
**Solution**:
```python
query_engine = index.as_query_engine(
    similarity_top_k=3,  # Limit retrieved chunks
    response_mode="compact"  # Compact context
)
```

### 4. Async/Sync Mixing
**Issue**: Calling sync methods in async context
**Solution**: Use `acomplete`, `achat`, `aquery` variants consistently

### 5. Memory Consumption with Large Indices
**Issue**: Loading entire index into memory
**Solution**: Use vector databases for persistence
```python
from llama_index.vector_stores.pinecone import PineconeVectorStore

vector_store = PineconeVectorStore(...)
index = VectorStoreIndex.from_vector_store(vector_store)
```

## Performance Optimization

### 1. Chunk Size Optimization
- Test different chunk sizes (256, 512, 1024)
- Balance retrieval precision vs context quality

### 2. Retrieval Tuning
```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
    similarity_cutoff=0.7  # Filter low-quality matches
)
```

### 3. Batch Processing
```python
# Process multiple queries efficiently
queries = ["query1", "query2", "query3"]
responses = [query_engine.query(q) for q in queries]
```

### 4. Use Response Modes Wisely
- `compact`: Concatenate chunks, best for most cases
- `tree_summarize`: Hierarchical summarization for many chunks
- `simple_summarize`: Fast but may lose detail
- `no_text`: Only return source nodes

## Integration with Vector Databases

### Pinecone Integration
```python
import pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore

pc = pinecone.Pinecone(api_key="...")
index = pc.Index("my-index")

vector_store = PineconeVectorStore(pinecone_index=index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
```

## Resources

- **Official Docs**: https://docs.llamaindex.ai/en/stable/examples/llm/anthropic/
- **Anthropic Cookbook**: https://github.com/anthropics/anthropic-cookbook/tree/main/third_party/LlamaIndex
- **PyPI Package**: https://pypi.org/project/llama-index-llms-anthropic/
- **Function Calling Agent**: https://docs.llamaindex.ai/en/stable/examples/agent/anthropic_agent/
- **Multimodal Examples**: https://docs.llamaindex.ai/en/stable/examples/multi_modal/anthropic_multi_modal/

## Related Patterns

- [Vector Databases](./vector-databases.md) - Storage backends for LlamaIndex
- [RAG Patterns](./rag-patterns.md) - Detailed RAG implementation strategies
- [Best Practices](./best-practices.md) - Cross-cutting best practices
