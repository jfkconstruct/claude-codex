# Claude + AI Development Tools Integration Patterns

## Overview

Modern AI development tools enhance productivity by integrating Claude directly into developer workflows. These tools span IDEs, prompt engineering platforms, testing frameworks, and development SDKs.

## IDE Integrations

### Supported IDEs

- **VS Code**: Native extension (beta)
- **JetBrains IDEs**: Claude Agent integration
- **Cursor**: Built-in Claude Code support
- **Windsurf**: Claude Code integration
- **VSCodium**: Claude Code support
- **Theia IDE**: First open-source native integration

### VS Code Integration

#### Installation

1. Install Claude Code CLI
```bash
npm install -g claude-code
```

2. Install VS Code extension (beta)
```bash
# Search for "Claude Code" in VS Code extensions
# Or install from marketplace
```

#### Key Features

**Inline Diffs**:
- See Claude's proposed changes directly in files
- Accept/reject changes individually
- Real-time diff viewing in sidebar panel

**Selection Context**:
```
1. Select code in editor
2. Right-click → "Ask Claude"
3. Claude sees selection as context
```

**File References**:
```
@filename.py - Reference specific files
#symbol - Reference symbols/functions
```

**Diagnostic Sharing**:
- Automatic error/warning sharing with Claude
- Context-aware debugging suggestions

**Setup Example**:
```json
// .vscode/settings.json
{
  "claude.model": "claude-sonnet-4-5-20250929",
  "claude.autoSuggestions": true,
  "claude.inlineDiff": true,
  "claude.diagnostics": true
}
```

### JetBrains Integration

#### Setup

1. Install AI Assistant plugin
2. Enable Claude Agent in AI chat settings
3. Configure API key in settings

#### Features

**AI Chat Integration**:
- Seamless Claude Agent in IDE chat
- Context-aware code suggestions
- Inline code generation

**Workflow Integration**:
```kotlin
// Claude understands project structure
// Can refactor across multiple files
// Maintains code style consistency
```

### Cursor Integration

**Native Claude Support**:
```
1. Cmd/Ctrl + K: Inline edit with Claude
2. Cmd/Ctrl + L: Chat with Claude
3. @-mentions for file context
```

**Best Practices**:
- Use Cmd+K for targeted edits
- Use Chat for exploratory questions
- Reference files with @ for context

### Theia IDE

**Open-Source Integration**:
- First native open-source Claude Code integration
- Full terminal and IDE integration
- Real-time collaboration features

## Claude Code SDK

### Overview

Extensible SDK for building custom agents and applications using Claude Code's core agent capabilities.

### Installation

```bash
npm install @anthropic-ai/claude-code-sdk
```

### Basic Agent Pattern

```typescript
import { ClaudeAgent } from '@anthropic-ai/claude-code-sdk';

const agent = new ClaudeAgent({
  model: 'claude-sonnet-4-5-20250929',
  tools: [
    // Custom tool definitions
    {
      name: 'run_tests',
      description: 'Run test suite',
      parameters: { /* schema */ },
      execute: async (params) => {
        // Tool implementation
      }
    }
  ]
});

// Use agent
const result = await agent.run('Refactor this module');
```

### Hooks Pattern

**Automatic Task Execution**:
```typescript
// .claude/hooks.json
{
  "onCodeChange": [
    "npm run lint",
    "npm test"
  ],
  "onCommit": [
    "npm run build"
  ]
}
```

**Hook Configuration**:
```typescript
agent.addHook('onCodeChange', async (files) => {
  // Run tests on changed files
  const testFiles = files.filter(f => f.endsWith('.test.ts'));
  await runTests(testFiles);
});
```

### Subagent Pattern

**Delegate Specialized Tasks**:
```typescript
const mainAgent = new ClaudeAgent({
  model: 'claude-sonnet-4-5-20250929',
  subagents: {
    'code-reviewer': {
      model: 'claude-sonnet-4-5-20250929',
      systemPrompt: 'You are a code review expert',
      tools: ['analyze_code', 'suggest_improvements']
    },
    'test-writer': {
      model: 'claude-haiku-4-0',  // Faster for simpler task
      systemPrompt: 'You generate comprehensive tests',
      tools: ['write_test', 'run_test']
    }
  }
});

// Delegate to subagent
await mainAgent.delegate('code-reviewer', {
  task: 'Review this pull request',
  files: changedFiles
});
```

### Background Tasks

**Long-Running Processes**:
```typescript
// Start background task
const task = agent.startBackgroundTask({
  command: 'npm run build:watch',
  onOutput: (data) => {
    console.log('Build output:', data);
  },
  onError: (err) => {
    console.error('Build error:', err);
  }
});

// Continue working while task runs
await agent.run('Add new feature');

// Stop when done
await task.stop();
```

## Prompt Development Tools

### Claude Console (Anthropic)

**Web-based Prompt Engineering**:
- Interactive prompt testing
- System prompt configuration
- Multi-turn conversation testing
- Cost estimation
- Model comparison

**Best Practices**:
1. Test prompts in Console before code
2. Use Workbench for complex workflows
3. Export prompts to code
4. Version prompts in code

### Prompt Management Platforms

#### Langfuse Prompts

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Fetch versioned prompt
prompt = langfuse.get_prompt("system-prompt", version=3)

# Use in Claude call
response = anthropic.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=prompt.compile(user_name="Alice"),
    messages=[{"role": "user", "content": query}]
)
```

#### PromptLayer

```python
import promptlayer
from anthropic import Anthropic

# Wrap client
anthropic = promptlayer.anthropic.Anthropic()

# Calls automatically logged
response = anthropic.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    pl_tags=["production", "chatbot"]  # PromptLayer tags
)
```

## Testing Frameworks

### Unit Testing Pattern

```python
import pytest
from anthropic import Anthropic

@pytest.fixture
def claude_client():
    return Anthropic()

def test_sentiment_analysis(claude_client):
    """Test Claude's sentiment analysis"""
    response = claude_client.messages.create(
        model="claude-haiku-4-0",  # Fast model for tests
        max_tokens=10,
        messages=[{
            "role": "user",
            "content": "Sentiment (positive/negative): I love this product!"
        }]
    )

    assert "positive" in response.content[0].text.lower()

def test_json_output(claude_client):
    """Test structured output"""
    response = claude_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Return JSON: {name: string, age: number} for John, 30"
        }]
    )

    import json
    result = json.loads(response.content[0].text)
    assert result["name"] == "John"
    assert result["age"] == 30
```

### Integration Testing with Mocks

```python
from unittest.mock import Mock, patch
import anthropic

def test_rag_pipeline_with_mock():
    """Test RAG without API calls"""
    mock_response = Mock()
    mock_response.content = [Mock(text="Mocked response")]
    mock_response.usage = Mock(input_tokens=100, output_tokens=50)

    with patch.object(anthropic.Anthropic, 'messages') as mock_messages:
        mock_messages.create.return_value = mock_response

        # Test your RAG pipeline
        result = rag_pipeline("test query")

        assert result == "Mocked response"
        mock_messages.create.assert_called_once()
```

### Evaluation Framework

```python
import anthropic
from typing import List, Dict

def evaluate_model(
    test_cases: List[Dict[str, str]],
    model: str
) -> Dict[str, float]:
    """Evaluate model on test cases"""
    client = anthropic.Anthropic()
    correct = 0
    total = len(test_cases)

    for case in test_cases:
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": case["prompt"]}]
        )

        if case["expected"] in response.content[0].text:
            correct += 1

    return {
        "accuracy": correct / total,
        "model": model,
        "total_cases": total
    }

# Compare models
results = {
    "haiku": evaluate_model(test_cases, "claude-haiku-4-0"),
    "sonnet": evaluate_model(test_cases, "claude-sonnet-4-5-20250929"),
}
```

## MCP (Model Context Protocol) Servers

### What is MCP?

MCP servers extend Claude Code's capabilities by providing additional tools and data sources.

### Installing MCP Servers

```bash
# GitHub MCP server
npm install @modelcontextprotocol/server-github

# Configure in .claude/mcp_config.json
```

### Example MCP Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### Using MCP Tools

```typescript
// Claude Code automatically discovers MCP tools
// Use in prompts like:
"Create a pull request using GitHub MCP"
"Query database for user stats using database MCP"
```

## Enterprise Integration

### Amazon Bedrock

```python
import boto3
from anthropic import AnthropicBedrock

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

client = AnthropicBedrock(
    aws_region="us-west-2",
    # Uses AWS credentials from environment
)

# Use like standard Anthropic client
response = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v2:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Bedrock Prompt Caching**:
```python
# Enable caching on Bedrock
response = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v2:0",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Query"}]
)
```

### Google Cloud Vertex AI

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    region="us-central1",
    project_id="my-project",
)

response = client.messages.create(
    model="claude-sonnet-4-5-20250929@20250301",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Best Practices

### ✅ Do's

1. **Use IDE Extensions for Development**
   - Faster iteration with inline diffs
   - Better context sharing
   - Integrated debugging

2. **Test Prompts Before Production**
   - Use Claude Console for experimentation
   - Version prompts in code/Langfuse
   - A/B test different approaches

3. **Implement Proper Testing**
   - Unit tests for prompt outputs
   - Integration tests for workflows
   - Mock API calls in CI/CD

4. **Use Hooks for Automation**
   - Auto-run tests on code changes
   - Auto-format before commits
   - Auto-deploy on successful builds

5. **Leverage MCP for Extensibility**
   - Add domain-specific tools
   - Integrate with internal systems
   - Avoid reinventing capabilities

### ❌ Don'ts

1. **Don't Skip Version Control for Prompts**
   - Prompts are code, version them
   - Document changes and rationale

2. **Don't Ignore IDE Integration Limits**
   - Not all features work in all IDEs
   - Test integration before relying on it

3. **Don't Over-Automate with Hooks**
   - Too many hooks slow development
   - Only automate what adds value

4. **Don't Test Against Production API in CI**
   - Use mocks to avoid costs
   - Save real API tests for staging

## Common Gotchas

### 1. IDE Extension Conflicts
**Issue**: Multiple AI extensions interfere
**Solution**: Disable conflicting extensions or use separate profiles

### 2. API Key Management in IDEs
**Issue**: Accidentally committing API keys
**Solution**:
```bash
# Use environment variables
export ANTHROPIC_API_KEY="sk-..."

# Or IDE secret storage
# VS Code: Settings → Claude → API Key (stored in keychain)
```

### 3. Hook Execution Failures
**Issue**: Hooks fail silently
**Solution**: Enable verbose logging
```json
{
  "hooks": {
    "verbose": true,
    "onError": "notify"
  }
}
```

### 4. Model Availability in Enterprise
**Issue**: Latest models not available on Bedrock/Vertex
**Solution**: Check model catalog, use model aliases

### 5. Context Size in IDE
**Issue**: Sending too much code context
**Solution**: Use file references strategically, not entire codebase

## Resources

### Official Documentation
- **Claude Code**: https://www.anthropic.com/claude-code
- **IDE Integrations**: https://docs.anthropic.com/en/docs/claude-code/ide-integrations
- **SDK**: https://skywork.ai/blog/claude-code-sdk-api-reference-explained/
- **Bedrock**: https://aws.amazon.com/bedrock/claude/
- **Vertex AI**: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/claude

### Integration Guides
- **JetBrains**: https://blog.jetbrains.com/ai/2025/09/introducing-claude-agent-in-jetbrains-ides/
- **VS Code**: https://apidog.com/blog/claude-code-ide-integrations/
- **Theia**: https://eclipsesource.com/blogs/2025/10/14/its-released-your-native-claude-code-ide-integration-in-theia/

## Related Patterns

- [Best Practices](./best-practices.md) - Cross-cutting development practices
- [Observability](./observability.md) - Monitoring and debugging
- [LangChain](./langchain.md) - Framework integration
