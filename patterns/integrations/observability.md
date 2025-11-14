# Claude + Observability Platform Integration Patterns

## Overview

Observability platforms provide monitoring, tracing, and analytics for LLM applications. They help track costs, latency, quality, and user interactions with Claude-powered applications.

## Key Platforms

- **Langfuse**: Open-source LLM observability and prompt management
- **LangSmith**: LangChain ecosystem observability (paid)
- **Helicone**: Lightweight proxy-based observability
- **Phoenix**: Arize AI's open-source observability
- **Opik**: Full-stack LLM observability

## Platform Comparison

| Feature | Langfuse | LangSmith | Helicone |
|---------|----------|-----------|----------|
| **Open Source** | ✅ Yes | ❌ No | ✅ Yes |
| **Setup Complexity** | Medium | Low | Very Low (2 lines) |
| **Prompt Management** | ✅ Yes | ✅ Yes | ❌ Limited |
| **Evaluation** | ✅ Yes | ✅ Yes | ❌ No |
| **Self-Hosted** | ✅ Yes | ❌ No | ✅ Yes |
| **Proxy Mode** | ❌ No | ❌ No | ✅ Yes |
| **Best For** | Full observability | LangChain users | Quick setup |

## Langfuse Integration

### Setup & Installation

```bash
pip install langfuse
```

### Direct API Integration

```python
from langfuse import Langfuse
from anthropic import Anthropic

# Initialize clients
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # or self-hosted
)
anthropic = Anthropic()

# Create trace
trace = langfuse.trace(name="rag-query")

# Track Claude call
generation = trace.generation(
    name="claude-completion",
    model="claude-sonnet-4-5-20250929",
    input={"messages": [{"role": "user", "content": "Hello"}]},
)

# Make API call
response = anthropic.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)

# Update trace with response
generation.end(
    output=response.content[0].text,
    usage={
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    },
    metadata={
        "stop_reason": response.stop_reason
    }
)
```

### LangChain Integration

```python
from langfuse.callback import CallbackHandler
from langchain_anthropic import ChatAnthropic

# Create Langfuse callback
langfuse_handler = CallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
)

# Use with LangChain
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    callbacks=[langfuse_handler]
)

response = llm.invoke("What is RAG?")
```

### LlamaIndex Integration

```python
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler

# Setup callback
langfuse_callback = LlamaIndexCallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
)

Settings.callback_manager = CallbackManager([langfuse_callback])

# Now all LlamaIndex operations are tracked
query_engine = index.as_query_engine()
response = query_engine.query("What is this about?")
```

### Nested Tracing Pattern

```python
from langfuse.decorators import observe, langfuse_context

@observe()
def retrieve_documents(query: str):
    """Retrieval step"""
    # Vector search logic
    return documents

@observe()
def generate_response(query: str, context: str):
    """Generation step"""
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context: {context}\n\nQuestion: {query}"
        }]
    )
    return response.content[0].text

@observe()
def rag_pipeline(query: str):
    """Full RAG pipeline with nested traces"""
    docs = retrieve_documents(query)
    context = "\n".join(docs)
    response = generate_response(query, context)

    # Add custom metadata
    langfuse_context.update_current_trace(
        tags=["rag", "production"],
        user_id="user-123"
    )

    return response
```

### Prompt Management

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Fetch versioned prompt
prompt = langfuse.get_prompt("rag-system-prompt", version=2)

# Use in Claude call
response = anthropic.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=prompt.compile(),  # Get compiled prompt text
    messages=[{"role": "user", "content": user_query}]
)

# Track which prompt version was used
trace.generation(
    name="claude-call",
    prompt=prompt,
    input=user_query,
    output=response.content[0].text
)
```

### Langfuse Best Practices

✅ **Do's**:
- Use decorators for automatic tracing
- Tag traces by environment (dev, staging, prod)
- Track user IDs for user-level analytics
- Version prompts and track usage
- Set up alerts for cost/latency thresholds

```python
@observe(as_type="generation")
def call_claude(prompt: str):
    langfuse_context.update_current_observation(
        tags=["production", "critical"],
        metadata={"version": "v2.1"}
    )
    return response
```

❌ **Don'ts**:
- Don't log sensitive user data without consent
- Don't skip error handling in traces
- Don't create traces for every single token in streaming
- Don't forget to flush traces in serverless environments

```python
# In serverless/edge functions
langfuse.flush()  # Ensure traces are sent before shutdown
```

## LangSmith Integration

### Setup

```bash
pip install langsmith
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY="lsv2_..."
export LANGCHAIN_PROJECT="my-project"
```

### Automatic Tracing with LangChain

```python
from langchain_anthropic import ChatAnthropic

# Tracing happens automatically when env vars are set
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
response = llm.invoke("Hello")  # Automatically traced
```

### Manual Client Usage

```python
from langsmith import Client
from anthropic import Anthropic

ls_client = Client()
anthropic = Anthropic()

# Create run manually
with ls_client.trace(
    name="claude-call",
    run_type="llm",
    inputs={"messages": [{"role": "user", "content": "Hello"}]}
) as run:
    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )

    run.end(
        outputs={"response": response.content[0].text},
        extra={
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    )
```

### LangSmith Best Practices

✅ **Do's**:
- Use projects to organize different applications
- Tag runs with metadata for filtering
- Set up dataset evaluation for testing
- Use feedback API for quality tracking

❌ **Don'ts**:
- Don't use outside LangChain if possible (less friction)
- Don't mix multiple projects in same codebase
- Don't forget to set LANGCHAIN_PROJECT for multi-app setups

## Helicone Integration

### Setup (Simplest: 2 Lines)

```python
from anthropic import Anthropic

# Just change base URL
client = Anthropic(
    api_key="your-anthropic-key",
    base_url="https://anthropic.helicone.ai/",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-..."
    }
)

# All calls automatically logged
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Advanced Configuration

```python
# Custom properties and user tracking
client = Anthropic(
    base_url="https://anthropic.helicone.ai/",
    default_headers={
        "Helicone-Auth": "Bearer sk-helicone-...",
        "Helicone-Property-Environment": "production",
        "Helicone-Property-App": "chatbot",
        "Helicone-User-Id": "user-123",
        "Helicone-Session-Id": "session-456",
        "Helicone-Prompt-Id": "welcome-prompt-v2"
    }
)
```

### Caching with Helicone

```python
# Enable response caching
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What is 2+2?"}],
    extra_headers={
        "Helicone-Cache-Enabled": "true"
    }
)
```

### Helicone Best Practices

✅ **Do's**:
- Use property headers for rich metadata
- Enable caching for repeated queries
- Set rate limits via dashboard
- Use user/session IDs for cohort analysis

❌ **Don'ts**:
- Don't skip authentication headers
- Don't use for extremely high-security applications (proxy pattern)
- Don't forget to handle Helicone downtime (have fallback)

## Common Observability Patterns

### 1. Cost Tracking

```python
def track_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Calculate cost based on Claude pricing"""
    pricing = {
        "claude-sonnet-4-5-20250929": {
            "input": 0.003,   # per 1K tokens
            "output": 0.015   # per 1K tokens
        },
        "claude-haiku-4-0": {
            "input": 0.00025,
            "output": 0.00125
        }
    }

    model_pricing = pricing.get(model, pricing["claude-sonnet-4-5-20250929"])
    cost = (
        (input_tokens / 1000) * model_pricing["input"] +
        (output_tokens / 1000) * model_pricing["output"]
    )

    # Log to observability platform
    langfuse.score(
        trace_id=trace_id,
        name="cost_usd",
        value=cost
    )

    return cost
```

### 2. Latency Monitoring

```python
import time

def monitor_latency(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        latency = time.time() - start

        # Track latency
        langfuse.score(
            trace_id=trace_id,
            name="latency_seconds",
            value=latency
        )

        # Alert if too slow
        if latency > 10:
            logger.warning(f"Slow request: {latency}s")

        return result
    return wrapper
```

### 3. Quality Evaluation

```python
# User feedback collection
def collect_feedback(trace_id: str, rating: int, comment: str = None):
    langfuse.score(
        trace_id=trace_id,
        name="user_rating",
        value=rating,
        comment=comment
    )

# Automated evaluation
def evaluate_response(question: str, response: str, context: str) -> float:
    """Use Claude to evaluate response quality"""
    eval_prompt = f"""
    Question: {question}
    Context: {context}
    Response: {response}

    Rate the response quality from 0-1 based on:
    - Accuracy
    - Relevance
    - Completeness

    Output only a number between 0 and 1.
    """

    eval_response = anthropic.messages.create(
        model="claude-haiku-4-0",  # Cheaper model for eval
        max_tokens=10,
        messages=[{"role": "user", "content": eval_prompt}]
    )

    score = float(eval_response.content[0].text.strip())

    langfuse.score(
        trace_id=trace_id,
        name="quality_score",
        value=score
    )

    return score
```

### 4. Error Tracking

```python
from langfuse.decorators import observe

@observe()
def safe_claude_call(prompt: str):
    try:
        response = anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        # Log error to observability
        langfuse_context.update_current_observation(
            level="ERROR",
            status_message=str(e),
            metadata={"error_type": type(e).__name__}
        )
        raise
```

## Multi-Platform Strategy

```python
# Use multiple platforms simultaneously
from langfuse.callback import CallbackHandler as LangfuseHandler
from langsmith.run_helpers import traceable

langfuse_handler = LangfuseHandler()

@traceable(name="claude-call")  # LangSmith
@observe()  # Langfuse
def call_claude_with_multi_tracking(prompt: str):
    # Also use Helicone via proxy
    client = Anthropic(
        base_url="https://anthropic.helicone.ai/",
        default_headers={"Helicone-Auth": "Bearer ..."}
    )

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
```

## Common Gotchas

### 1. Trace Flushing in Serverless
**Issue**: Traces not sent before function timeout
**Solution**:
```python
# Always flush before returning
try:
    result = process()
    return result
finally:
    langfuse.flush()  # Blocks until sent
```

### 2. PII Leakage
**Issue**: Accidentally logging sensitive data
**Solution**:
```python
def sanitize_input(text: str) -> str:
    # Remove emails, phone numbers, etc.
    return sanitized_text

trace.update(input=sanitize_input(user_input))
```

### 3. High Cardinality Tags
**Issue**: Too many unique tags hurt performance
**Solution**:
```python
# Bad: unique per request
tags=["request-" + uuid.uuid4()]

# Good: categorical
tags=["environment:prod", "app:chatbot", "version:v2"]
```

### 4. Nested Trace Overhead
**Issue**: Too many nested spans slow application
**Solution**: Only trace meaningful operations, not every function call

## Resources

- **Langfuse**: https://langfuse.com/integrations/model-providers/anthropic
- **LangSmith**: https://docs.smith.langchain.com/
- **Helicone**: https://www.helicone.ai/blog
- **Comparison**: http://blog.songhaban.com/2025/03/comparing-llm-observability-tools.html

## Related Patterns

- [Best Practices](./best-practices.md) - Error handling and monitoring
- [LangChain](./langchain.md) - LangChain callback integration
- [LlamaIndex](./llamaindex.md) - LlamaIndex callback integration
