# Claude + LangChain Integration Patterns

## Overview

LangChain provides a standardized framework for building applications with Large Language Models, allowing seamless provider swapping and avoiding vendor lock-in. The `langchain-anthropic` package offers first-class support for Claude models.

## Installation & Setup

### Python
```bash
# Full LangChain with Anthropic support
pip install -qU "langchain[anthropic]"

# Or just the Anthropic integration
pip install langchain-anthropic
```

### JavaScript/TypeScript
```bash
npm install @langchain/anthropic
```

**Last Updated**: November 12, 2025 (latest package version)

## Basic Usage Patterns

### Simple Chat Agent (Python)
```python
from langchain_anthropic import ChatAnthropic

# Initialize with latest model
llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    temperature=0,
    max_tokens=1024,
)

# Basic chat
response = llm.invoke("What is the capital of France?")
```

### Agent with Tools (<10 lines)
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[my_tool1, my_tool2],
    system_prompt="You are a helpful assistant"
)
```

## Integration Patterns

### 1. Standard Chat Pattern
**Use Case**: Direct conversational interactions
- Supports streaming responses
- Handles conversation history
- Temperature and token control

### 2. Tool/Function Calling Pattern
**Use Case**: Agentic workflows with external capabilities
```python
from langchain.tools import tool
from langchain_anthropic import ChatAnthropic

@tool
def get_weather(location: str) -> str:
    """Get weather for a location"""
    return f"Weather in {location}: Sunny"

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
llm_with_tools = llm.bind_tools([get_weather])
```

### 3. RAG (Retrieval-Augmented Generation)
**Use Case**: Question answering over documents
```python
from langchain.chains import RetrievalQA
from langchain_anthropic import ChatAnthropic
from langchain.vectorstores import Chroma

llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)
```

### 4. Multi-Step Chains
**Use Case**: Complex workflows with multiple LLM calls
```python
from langchain.chains import SequentialChain
from langchain_anthropic import ChatAnthropic

# Chain multiple operations
chain = first_chain | second_chain | third_chain
result = chain.invoke({"input": "data"})
```

## Best Practices

### ✅ Do's

1. **Version Compatibility**
   - Ensure all LangChain packages use the same `@langchain/core` instance
   - Pin versions in production to avoid breaking changes

2. **Model Selection**
   - Use Sonnet 4.5 (`claude-sonnet-4-5-20250929`) for best performance
   - Use Haiku for faster, cheaper operations
   - Use Opus for most complex reasoning tasks

3. **Streaming for Better UX**
   ```python
   for chunk in llm.stream("Tell me a story"):
       print(chunk.content, end="", flush=True)
   ```

4. **Error Handling**
   ```python
   from anthropic import RateLimitError

   try:
       response = llm.invoke(prompt)
   except RateLimitError:
       # Implement exponential backoff
       time.sleep(2 ** retry_count)
   ```

5. **Use LangGraph for Complex Workflows**
   - Deterministic + agentic workflows
   - Heavy customization needs
   - Latency-sensitive applications

### ❌ Don'ts

1. **Don't Mix LangChain Versions**
   - Mixing package versions can cause runtime errors
   - Always check `@langchain/core` compatibility

2. **Don't Ignore Rate Limits**
   - Implement proper retry logic with exponential backoff
   - Monitor rate limit headers

3. **Don't Over-Engineer Simple Tasks**
   - LangChain adds overhead; use direct API for simple calls
   - Evaluate if framework is needed for your use case

4. **Don't Forget Context Window Limits**
   - Track token usage across conversation history
   - Implement context pruning strategies

## Common Gotchas

### 1. Tool Calling Format Differences
**Issue**: Tool definitions must match Claude's expected schema
**Solution**: Use LangChain's `@tool` decorator for automatic schema generation

### 2. Async vs Sync Confusion
**Issue**: Mixing async and sync calls causes runtime errors
**Solution**:
```python
# Sync
response = llm.invoke(prompt)

# Async
response = await llm.ainvoke(prompt)
```

### 3. Conversation History Management
**Issue**: Context window overflow with long conversations
**Solution**: Implement sliding window or summarization
```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=5)  # Keep last 5 exchanges
```

### 4. Streaming Response Handling
**Issue**: Streaming requires different handling than standard responses
**Solution**:
```python
async for chunk in llm.astream("prompt"):
    print(chunk.content, end="", flush=True)
```

## Advanced Patterns

### Prompt Caching Integration
```python
# Use cache_control for large static prompts
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    # Enable caching for system prompts
    cache_control={"type": "ephemeral"}
)
```

### Multi-Modal Support
```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content=[
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": image_url}}
    ]
)
response = llm.invoke([message])
```

### Custom Callbacks for Observability
```python
from langchain.callbacks import StdOutCallbackHandler

llm = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    callbacks=[StdOutCallbackHandler()]
)
```

## Performance Optimization

1. **Batch Processing**: Process multiple requests in parallel
2. **Prompt Caching**: Cache static content (system prompts, examples)
3. **Model Selection**: Use Haiku for simple tasks, Sonnet for complex
4. **Streaming**: Reduce perceived latency for long responses

## Resources

- **Official Docs**: https://python.langchain.com/docs/integrations/providers/anthropic/
- **API Reference**: https://python.langchain.com/api_reference/anthropic/
- **NPM Package**: https://www.npmjs.com/package/@langchain/anthropic
- **PyPI Package**: https://pypi.org/project/langchain-anthropic/

## Related Patterns

- [Vector Databases](./vector-databases.md) - For RAG implementations
- [Observability](./observability.md) - For monitoring LangChain applications
- [Best Practices](./best-practices.md) - Cross-cutting concerns
