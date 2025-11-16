# Claude Integration Best Practices

## Overview

This document covers cross-cutting best practices for integrating Claude into production applications, including error handling, rate limiting, cost optimization, and security.

## Rate Limiting & Error Handling

### Understanding Claude's Rate Limits

Claude uses **token bucket algorithm** for rate limiting with three dimensions:

1. **Requests Per Minute (RPM)**: Number of API calls
2. **Input Tokens Per Minute (ITPM)**: Input tokens consumed
3. **Output Tokens Per Minute (OTPM)**: Output tokens generated

**Key Advantage**: Only **uncached** input tokens count toward ITPM for most models.

### Rate Limit Headers

Monitor these response headers:
```python
response = anthropic.messages.create(...)

# Check headers
headers = response.response.headers
rpm_limit = headers.get('anthropic-ratelimit-requests-limit')
rpm_remaining = headers.get('anthropic-ratelimit-requests-remaining')
rpm_reset = headers.get('anthropic-ratelimit-requests-reset')

# Log and monitor
logger.info(f"Rate limit: {rpm_remaining}/{rpm_limit} requests remaining")
```

### Exponential Backoff Pattern

**Primary Strategy** for handling 429 errors:

```python
import time
import random
from anthropic import RateLimitError, APIError

def call_claude_with_backoff(
    client,
    max_retries: int = 5,
    base_delay: float = 1.0,
    **kwargs
):
    """Call Claude with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)

            # Check retry-after header if available
            retry_after = getattr(e, 'retry_after', None)
            if retry_after:
                delay = max(delay, retry_after)

            logger.warning(f"Rate limited, retrying in {delay:.2f}s")
            time.sleep(delay)

        except APIError as e:
            # Handle other API errors
            logger.error(f"API error: {e}")
            raise
```

### Async Exponential Backoff

```python
import asyncio
from anthropic import AsyncAnthropic, RateLimitError

async def async_call_with_backoff(
    client: AsyncAnthropic,
    max_retries: int = 5,
    base_delay: float = 1.0,
    **kwargs
):
    """Async version with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await client.messages.create(**kwargs)

        except RateLimitError:
            if attempt == max_retries - 1:
                raise

            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            await asyncio.sleep(delay)
```

### Client-Side Rate Limiting

**Proactive Prevention**:

```python
import asyncio
from collections import deque
from time import time

class RateLimiter:
    """Client-side rate limiter"""
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.requests = deque()

    async def acquire(self):
        """Wait until a slot is available"""
        now = time()

        # Remove requests older than 1 minute
        while self.requests and self.requests[0] < now - 60:
            self.requests.popleft()

        # Wait if at limit
        if len(self.requests) >= self.rpm:
            sleep_time = 60 - (now - self.requests[0])
            await asyncio.sleep(sleep_time)
            return await self.acquire()

        self.requests.append(now)

# Usage
limiter = RateLimiter(requests_per_minute=50)

async def rate_limited_call():
    await limiter.acquire()
    return await client.messages.create(...)
```

### Request Queuing Pattern

```python
import asyncio
from queue import Queue
from threading import Thread

class RequestQueue:
    """Queue non-critical requests"""
    def __init__(self, worker_count: int = 3):
        self.queue = Queue()
        self.workers = []

        for _ in range(worker_count):
            worker = Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)

    def _worker(self):
        """Process queued requests"""
        while True:
            request_data, callback = self.queue.get()
            try:
                result = self._make_request(request_data)
                if callback:
                    callback(result)
            except Exception as e:
                logger.error(f"Request failed: {e}")
            finally:
                self.queue.task_done()

    def _make_request(self, data):
        return call_claude_with_backoff(client, **data)

    def enqueue(self, request_data, callback=None):
        """Add request to queue"""
        self.queue.put((request_data, callback))

    def wait_completion(self):
        """Wait for all requests to complete"""
        self.queue.join()
```

## Cost Optimization

### 1. Prompt Caching

**Save 90% on repeated content**:

```python
# Cache static content
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a helpful assistant...",  # Static system prompt
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": large_document,  # Large context
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": user_query  # Dynamic query
                }
            ]
        }
    ]
)

# Subsequent requests read from cache (90% cheaper)
```

**Pricing**:
- Cache writes: 25% more than base input
- Cache reads: 10% of base input (90% savings)
- Cache TTL: ~5 minutes, refreshed on use

### 2. Model Selection Strategy

```python
def select_model(task_complexity: str, task_type: str) -> str:
    """Smart model selection for cost optimization"""
    if task_type == "evaluation":
        return "claude-haiku-4-0"  # Cheapest for eval

    complexity_map = {
        "simple": "claude-haiku-4-0",      # $0.00025 input
        "moderate": "claude-sonnet-4-5-20250929",  # $0.003 input
        "complex": "claude-opus-4-0"       # Most expensive but best
    }

    return complexity_map.get(task_complexity, "claude-sonnet-4-5-20250929")

# Usage
model = select_model(task_complexity="simple", task_type="classification")
```

### 3. Token Management

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 chars)"""
    return len(text) // 4

def truncate_to_budget(text: str, max_tokens: int) -> str:
    """Truncate text to fit token budget"""
    estimated = estimate_tokens(text)
    if estimated <= max_tokens:
        return text

    # Truncate to approximate character count
    max_chars = max_tokens * 4
    return text[:max_chars] + "..."

# Apply budget constraints
context = truncate_to_budget(large_context, max_tokens=50000)
```

### 4. Streaming for Perceived Performance

```python
def stream_response(prompt: str):
    """Stream tokens for better UX without extra cost"""
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            # Display to user immediately

# No cost difference, but much better UX
```

### 5. Batch Similar Requests

```python
import asyncio

async def batch_process(prompts: list[str]) -> list[str]:
    """Process multiple requests in parallel"""
    tasks = [
        client.messages.create(
            model="claude-haiku-4-0",
            max_tokens=100,
            messages=[{"role": "user", "content": p}]
        )
        for p in prompts
    ]

    responses = await asyncio.gather(*tasks)
    return [r.content[0].text for r in responses]

# More efficient than sequential processing
```

## Security Best Practices

### 1. API Key Management

```python
import os
from anthropic import Anthropic

# ✅ Good: Use environment variables
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ❌ Bad: Hardcoded keys
# client = Anthropic(api_key="sk-ant-...")

# ✅ Better: Use secrets management
from google.cloud import secretmanager

def get_api_key():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/PROJECT_ID/secrets/anthropic-key/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### 2. Input Sanitization

```python
def sanitize_user_input(text: str) -> str:
    """Remove potential prompt injection attempts"""
    # Remove system-like instructions
    forbidden_patterns = [
        "ignore previous instructions",
        "system:",
        "assistant:",
        "<|im_start|>",
        "<|im_end|>"
    ]

    sanitized = text
    for pattern in forbidden_patterns:
        sanitized = sanitized.replace(pattern, "")

    return sanitized.strip()

# Use in prompts
user_input = sanitize_user_input(request.data)
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": user_input}]
)
```

### 3. PII Handling

```python
import re

def redact_pii(text: str) -> str:
    """Redact personally identifiable information"""
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                  '[EMAIL]', text)

    # Phone numbers (US format)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                  '[PHONE]', text)

    # SSN (US format)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b',
                  '[SSN]', text)

    # Credit card numbers
    text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                  '[CREDIT_CARD]', text)

    return text

# Use before sending to Claude (if needed)
safe_input = redact_pii(user_input)
```

### 4. Output Validation

```python
def validate_json_output(response: str, schema: dict) -> dict:
    """Validate structured output matches expected schema"""
    import json
    from jsonschema import validate, ValidationError

    try:
        data = json.loads(response)
        validate(instance=data, schema=schema)
        return data
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Invalid output: {e}")
        raise ValueError("Model output doesn't match expected schema")

# Usage
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
    },
    "required": ["name", "age"]
}

validated_data = validate_json_output(response.content[0].text, schema)
```

## Production Deployment Patterns

### 1. Health Checks

```python
from anthropic import Anthropic

def health_check() -> bool:
    """Check Claude API availability"""
    try:
        client = Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-0",  # Fastest, cheapest
            max_tokens=10,
            messages=[{"role": "user", "content": "test"}]
        )
        return True
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False

# Use in application startup and monitoring
```

### 2. Circuit Breaker

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    """Prevent cascading failures"""
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failures = 0
        self.state = "closed"

    def on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = "open"

# Usage
breaker = CircuitBreaker()
response = breaker.call(client.messages.create, **params)
```

### 3. Graceful Degradation

```python
def get_response_with_fallback(prompt: str) -> str:
    """Try Claude, fall back to simpler alternatives"""
    try:
        # Try primary model
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    except RateLimitError:
        # Fall back to faster, cheaper model
        logger.warning("Rate limited, using Haiku")
        response = client.messages.create(
            model="claude-haiku-4-0",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    except Exception as e:
        # Fall back to cached/default response
        logger.error(f"All models failed: {e}")
        return "I'm currently experiencing issues. Please try again later."
```

### 4. Monitoring & Alerting

```python
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class APIMetrics:
    """Track API performance metrics"""
    request_count: int = 0
    error_count: int = 0
    total_latency: float = 0.0
    total_cost: float = 0.0

metrics = APIMetrics()

def monitored_call(client, **kwargs):
    """Wrapper that tracks metrics"""
    start = time.time()

    try:
        response = client.messages.create(**kwargs)
        metrics.request_count += 1

        # Track latency
        latency = time.time() - start
        metrics.total_latency += latency

        # Track cost
        cost = calculate_cost(response.usage)
        metrics.total_cost += cost

        # Alert on high latency
        if latency > 10:
            logger.warning(f"High latency: {latency:.2f}s")

        return response

    except Exception as e:
        metrics.error_count += 1
        logger.error(f"Request failed: {e}")
        raise

def calculate_cost(usage) -> float:
    """Calculate request cost"""
    PRICING = {
        "input": 0.003,   # per 1K tokens
        "output": 0.015
    }
    return (
        (usage.input_tokens / 1000) * PRICING["input"] +
        (usage.output_tokens / 1000) * PRICING["output"]
    )
```

## Testing Best Practices

### 1. Mock Responses

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test without API calls"""
    mock_response = Mock()
    mock_response.content = [Mock(text="Mocked response")]
    mock_response.usage = Mock(input_tokens=10, output_tokens=20)

    with patch('anthropic.Anthropic.messages') as mock_messages:
        mock_messages.create.return_value = mock_response

        result = your_function()

        assert result == "Mocked response"
```

### 2. VCR for Replay Testing

```python
import vcr

# Record API responses once, replay in tests
@vcr.use_cassette('fixtures/claude_response.yaml')
def test_with_vcr():
    """Test with recorded responses"""
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=100,
        messages=[{"role": "user", "content": "test"}]
    )
    assert len(response.content[0].text) > 0
```

## Common Gotchas

### 1. Context Window Management
**Issue**: Exceeding model's context window
**Solution**: Track and limit total tokens
```python
MAX_CONTEXT = 200000  # Sonnet 4.5 limit
current_tokens = estimate_tokens(system + conversation_history + user_input)
if current_tokens > MAX_CONTEXT:
    # Truncate conversation history
    conversation_history = conversation_history[-10:]
```

### 2. Streaming Response Handling
**Issue**: Not properly closing streams
**Solution**:
```python
# Always use context manager
with client.messages.stream(**params) as stream:
    for text in stream.text_stream:
        process(text)
# Stream automatically closed
```

### 3. Rate Limit Header Parsing
**Issue**: Not checking all rate limit dimensions
**Solution**: Monitor RPM, ITPM, and OTPM separately

### 4. Caching Invalidation
**Issue**: Cache expires unexpectedly
**Solution**: Cache TTL is ~5 minutes; plan accordingly

## Resources

- **Rate Limits**: https://docs.claude.com/en/api/rate-limits
- **Prompt Caching**: https://docs.claude.com/en/docs/build-with-claude/prompt-caching
- **Streaming**: https://docs.claude.com/en/docs/build-with-claude/streaming

## Related Patterns

- [Observability](./observability.md) - Monitoring and tracking
- [RAG Patterns](./rag-patterns.md) - RAG-specific best practices
- [LangChain](./langchain.md) - Framework integration
- [LlamaIndex](./llamaindex.md) - LlamaIndex integration
