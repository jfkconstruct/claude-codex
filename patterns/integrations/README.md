# Claude Integration Patterns

> Comprehensive guide to integrating Claude with popular frameworks, tools, and platforms

## Overview

This directory contains detailed documentation on integration patterns between Claude and various AI development tools, frameworks, and platforms. Each guide includes setup instructions, best practices, common gotchas, and production-ready code examples.

## 📚 Integration Guides

### Frameworks & Libraries

#### [LangChain Integration](./langchain.md)
**Last Updated**: November 2025 | **Difficulty**: ⭐⭐

Standardized framework for building LLM applications with Claude.

**Key Topics**:
- Chat agents and tool calling
- RAG implementation
- Streaming responses
- LangGraph for complex workflows

**When to Use**: Building multi-step LLM workflows, need provider flexibility, or using LangChain ecosystem tools.

---

#### [LlamaIndex Integration](./llamaindex.md)
**Difficulty**: ⭐⭐

Data framework optimized for RAG applications with Claude.

**Key Topics**:
- RAG pipeline setup
- Agentic tool calling
- Extended thinking mode (Claude 3.7+)
- Multi-modal capabilities
- Custom query engines

**When to Use**: Building RAG applications, document Q&A, knowledge management systems.

---

### Data & Storage

#### [Vector Database Integrations](./vector-databases.md)
**Difficulty**: ⭐⭐⭐

Complete guide to using Claude with vector databases for semantic search and RAG.

**Covered Platforms**:
- **Pinecone**: Fully managed, serverless
- **Weaviate**: Knowledge graphs + vector search
- **Qdrant**: Advanced filtering, high performance
- **Chroma**: Lightweight, embedded
- **Milvus, PgVector, Redis**: Additional options

**Key Topics**:
- RAG implementation patterns
- Embedding strategies (Voyage AI recommended)
- Performance optimization
- Comparison matrix

**When to Use**: Building RAG systems, semantic search, document retrieval.

---

### Observability & Monitoring

#### [Observability Platforms](./observability.md)
**Difficulty**: ⭐⭐

Monitor, trace, and analyze Claude-powered applications.

**Covered Platforms**:
- **Langfuse**: Open-source, full observability
- **LangSmith**: LangChain ecosystem (paid)
- **Helicone**: Proxy-based, 2-line setup

**Key Topics**:
- Request tracing
- Cost tracking
- Latency monitoring
- Quality evaluation
- Prompt management

**When to Use**: Production applications, cost optimization, quality monitoring, debugging.

---

### Development Tools

#### [AI Development Tools](./ai-dev-tools.md)
**Difficulty**: ⭐

IDE integrations, SDKs, and development workflows.

**Covered Tools**:
- **IDE Integrations**: VS Code, JetBrains, Cursor, Windsurf, Theia
- **Claude Code SDK**: Build custom agents
- **MCP Servers**: Extend capabilities
- **Enterprise**: Bedrock, Vertex AI

**Key Topics**:
- IDE setup and features
- Hooks and automation
- Subagent patterns
- Testing frameworks
- Prompt development

**When to Use**: Development workflows, custom agents, enterprise deployments.

---

### Cross-Cutting Guides

#### [Best Practices](./best-practices.md)
**Difficulty**: ⭐⭐

Essential patterns for production Claude applications.

**Key Topics**:
- Rate limiting & exponential backoff
- Cost optimization (prompt caching, model selection)
- Security (API keys, PII, input sanitization)
- Error handling & circuit breakers
- Testing strategies

**When to Use**: All production applications.

---

#### [RAG Patterns](./rag-patterns.md)
**Difficulty**: ⭐⭐⭐

Deep dive into Retrieval-Augmented Generation implementations.

**Key Topics**:
- Basic to advanced RAG patterns
- Cached RAG (90% cost reduction)
- Hybrid search
- Multi-hop RAG
- Agentic RAG
- Chunking strategies
- Evaluation methods

**When to Use**: Building any RAG application, from simple Q&A to complex multi-hop reasoning.

---

## 🚀 Quick Start

### 1. Choose Your Use Case

```
Need to build...
├─ RAG / Document Q&A?
│  ├─ Simple setup → LlamaIndex
│  └─ Complex workflows → LangChain
│
├─ Production application?
│  ├─ Add observability → Langfuse/Helicone
│  └─ Review best practices → best-practices.md
│
├─ Vector search?
│  └─ Pick vector DB → vector-databases.md
│
└─ Development workflow?
   └─ IDE integration → ai-dev-tools.md
```

### 2. Essential Reading

For **all** integrations, read:
1. [Best Practices](./best-practices.md) - Rate limiting, error handling, security
2. Your specific integration guide
3. [RAG Patterns](./rag-patterns.md) - If building RAG

### 3. Basic Integration Template

```python
# 1. Install
pip install anthropic

# 2. Initialize (use env vars for API keys!)
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 3. Add error handling (from best-practices.md)
from anthropic import RateLimitError
import time

def call_with_retry(prompt: str, max_retries: int = 5):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# 4. Add observability (from observability.md)
from langfuse import Langfuse

langfuse = Langfuse()
trace = langfuse.trace(name="my-app")

# 5. Build your application
# ... rest of your code
```

## 📊 Integration Decision Matrix

| Need | Recommended Integration | Difficulty | Setup Time |
|------|------------------------|------------|------------|
| **Simple chat** | Direct API | ⭐ | 5 min |
| **RAG pipeline** | LlamaIndex | ⭐⭐ | 30 min |
| **Complex agents** | LangChain | ⭐⭐ | 1 hour |
| **Vector search** | Pinecone (managed) or Qdrant (self-hosted) | ⭐⭐ | 20 min |
| **Cost monitoring** | Helicone | ⭐ | 5 min |
| **Full observability** | Langfuse | ⭐⭐ | 30 min |
| **IDE integration** | VS Code extension | ⭐ | 10 min |
| **Enterprise** | Bedrock or Vertex AI | ⭐⭐⭐ | Varies |

## 🎯 Common Integration Scenarios

### Scenario 1: Document Q&A System

**Stack**: LlamaIndex + Pinecone + Langfuse

```
1. Read: llamaindex.md → RAG setup
2. Read: vector-databases.md → Pinecone integration
3. Read: observability.md → Langfuse monitoring
4. Read: rag-patterns.md → Optimization techniques
```

**Estimated Setup**: 2-3 hours

---

### Scenario 2: Production Chatbot

**Stack**: LangChain + Helicone + Prompt Caching

```
1. Read: langchain.md → Agent setup
2. Read: best-practices.md → Error handling + caching
3. Read: observability.md → Helicone setup
```

**Estimated Setup**: 1-2 hours

---

### Scenario 3: Development Workflow

**Stack**: Claude Code + VS Code + MCP

```
1. Read: ai-dev-tools.md → IDE setup
2. Configure: VS Code extension
3. Explore: MCP servers for your needs
```

**Estimated Setup**: 30 min

---

### Scenario 4: Enterprise RAG

**Stack**: LlamaIndex + Qdrant + AWS Bedrock + Langfuse

```
1. Read: ai-dev-tools.md → Bedrock setup
2. Read: vector-databases.md → Qdrant configuration
3. Read: llamaindex.md → RAG implementation
4. Read: observability.md → Production monitoring
5. Read: best-practices.md → Security & optimization
```

**Estimated Setup**: 1-2 days

---

## 🔑 Key Concepts

### Models

- **Sonnet 4.5** (`claude-sonnet-4-5-20250929`): Latest, best performance
- **Haiku 4** (`claude-haiku-4-0`): Fastest, cheapest
- **Opus 4** (`claude-opus-4-0`): Most capable for complex reasoning

### Embeddings

- **Voyage AI** (recommended by Anthropic): `voyage-large-2`, `voyage-2`
- **OpenAI**: `text-embedding-3-large`

### Rate Limits

- Measured in: RPM (requests), ITPM (input tokens), OTPM (output tokens)
- **Cached tokens don't count** toward ITPM
- Use exponential backoff for 429 errors

### Cost Optimization

1. **Prompt Caching**: 90% savings on repeated content
2. **Model Selection**: Use Haiku for simple tasks
3. **Streaming**: Better UX, same cost
4. **Batch Processing**: Parallel requests

## 📖 Reading Recommendations

### Beginner Path

1. Start: [Best Practices](./best-practices.md) - Error handling basics
2. Choose framework: [LangChain](./langchain.md) or [LlamaIndex](./llamaindex.md)
3. Add storage: [Vector Databases](./vector-databases.md) (if needed)
4. Monitor: [Observability](./observability.md) - Start with Helicone

### Advanced Path

1. Deep dive: [RAG Patterns](./rag-patterns.md) - Advanced techniques
2. Optimize: [Best Practices](./best-practices.md) - Cost & performance
3. Scale: [Vector Databases](./vector-databases.md) - Production setup
4. Monitor: [Observability](./observability.md) - Langfuse for full visibility

### Enterprise Path

1. Security: [Best Practices](./best-practices.md) - Security section
2. Deployment: [AI Dev Tools](./ai-dev-tools.md) - Bedrock/Vertex
3. Infrastructure: [Vector Databases](./vector-databases.md) - Self-hosted options
4. Governance: [Observability](./observability.md) - Complete tracing

## 🛠️ Development Workflow

### Recommended Setup

```bash
# 1. Core dependencies
pip install anthropic

# 2. Choose your stack
pip install langchain-anthropic  # OR
pip install llama-index-llms-anthropic

# 3. Vector storage (if needed)
pip install pinecone-client  # OR
pip install qdrant-client

# 4. Embeddings
pip install voyageai

# 5. Observability
pip install langfuse

# 6. Development
# Install Claude Code IDE extension
```

### Project Structure

```
your-project/
├── .env                    # API keys (never commit!)
├── requirements.txt
├── src/
│   ├── rag/
│   │   ├── embeddings.py  # Voyage AI integration
│   │   ├── retrieval.py   # Vector DB queries
│   │   └── generation.py  # Claude calls
│   ├── utils/
│   │   ├── errors.py      # Error handling + retry
│   │   └── monitoring.py  # Observability setup
│   └── main.py
└── tests/
    ├── test_rag.py
    └── fixtures/           # VCR cassettes for testing
```

## 🐛 Common Issues & Solutions

### Issue: Rate Limited (429 errors)
**Solution**: Implement exponential backoff (see [best-practices.md](./best-practices.md))

### Issue: High costs
**Solution**: Use prompt caching + model selection (see [best-practices.md](./best-practices.md))

### Issue: Poor retrieval quality
**Solution**: Improve chunking + use hybrid search (see [rag-patterns.md](./rag-patterns.md))

### Issue: Context overflow
**Solution**: Limit retrieved chunks + track tokens (see [rag-patterns.md](./rag-patterns.md))

### Issue: Slow responses
**Solution**: Use streaming + Haiku for simple tasks (see [best-practices.md](./best-practices.md))

## 📚 External Resources

### Official Documentation

- **Anthropic Docs**: https://docs.anthropic.com/
- **API Reference**: https://docs.anthropic.com/en/api/
- **Cookbook**: https://github.com/anthropics/anthropic-cookbook/

### Community

- **Discord**: Anthropic Developer Discord
- **GitHub Discussions**: https://github.com/anthropics/anthropic-sdk-python/discussions

### Tools

- **Claude Console**: https://console.anthropic.com/ (prompt testing)
- **Workbench**: https://console.anthropic.com/workbench (workflow design)

## 🤝 Contributing

Found an issue or have an improvement? These patterns are maintained as part of the Claude Codex research project.

## 📄 License

These patterns are documented for educational and reference purposes.

---

**Last Updated**: November 2025
**Claude Model**: Sonnet 4.5 (claude-sonnet-4-5-20250929)
