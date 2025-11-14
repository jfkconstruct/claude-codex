# Claude Code Snippet Library

**Purpose**: Reusable code examples extracted from the Claude Coding Master Playbook
**Version**: 1.0
**Date**: 2025-11-14

---

## Directory Structure

```
code-snippets/
├── README.md (this file)
├── typescript/
│   ├── api-integration.ts       # Anthropic API integration examples
│   ├── mcp-servers.ts            # MCP server implementations
│   ├── error-handling.ts         # Error handling patterns
│   ├── streaming.ts              # Streaming response handling
│   └── validation.ts             # Input validation with zod
├── python/
│   ├── hooks.py                  # Claude Code hook examples
│   ├── api-client.py             # Python API client
│   └── retry-logic.py            # Exponential backoff implementation
├── bash/
│   ├── git-workflows.sh          # Git checkpoint patterns
│   ├── setup.sh                  # Environment setup scripts
│   └── deployment.sh             # Deployment automation
├── config/
│   ├── claude.md                 # Example .claude.md templates
│   ├── mcp_settings.json         # MCP server configurations
│   ├── commands/                 # Custom slash commands
│   └── subagents/                # Sub-agent configurations
└── markdown/
    ├── prompt-templates.md       # Reusable prompt templates
    └── code-review-checklists.md # Review checklists
```

---

## Quick Start

### 1. Copy What You Need

```bash
# Copy entire snippets directory to your project
cp -r code-snippets/ ~/my-project/.claude/snippets/

# Or copy individual files
cp code-snippets/config/claude.md ~/my-project/.claude/claude.md
cp code-snippets/typescript/api-integration.ts ~/my-project/src/lib/
```

### 2. Customize for Your Stack

All snippets include `TODO` comments marking areas to customize:
- Replace `YOUR_API_KEY` with your actual key
- Update file paths to match your project structure
- Adjust library imports for your dependencies
- Modify error messages and logging

### 3. Test Before Using in Production

```bash
# For TypeScript snippets
tsc --noEmit snippet-file.ts  # Type check

# For Python snippets
python3 -m py_compile snippet-file.py  # Syntax check

# For bash snippets
shellcheck snippet-file.sh  # Linting
bash -n snippet-file.sh     # Syntax check
```

---

## Snippet Categories

### API Integration (`typescript/api-integration.ts`)
- Basic Claude API call
- Streaming responses
- Error handling with retry logic
- Message formatting
- Token counting

### MCP Servers (`typescript/mcp-servers.ts`)
- Custom MCP server structure
- Tool definition schemas
- Tool call handling
- Authentication patterns

### Error Handling (`typescript/error-handling.ts`)
- Try/catch patterns
- Graceful degradation
- Error logging
- User-friendly error messages

### Hooks (`python/hooks.py`)
- Post-tool-use hooks
- Type checking automation
- Linting automation
- Custom validation gates

### Git Workflows (`bash/git-workflows.sh`)
- Checkpoint before/after AI changes
- Granular commits
- Rollback procedures
- Worktree setup for parallel development

### Configurations (`config/`)
- `.claude.md` templates for different project types
- MCP server configurations
- Custom command examples
- Sub-agent definitions

---

## Usage Examples

### Example 1: Set Up Claude Code for New Project

```bash
# 1. Copy base configuration
cp code-snippets/config/claude.md ./

# 2. Install recommended MCP server
npm install -g @context7/mcp-server

# 3. Copy MCP configuration
cp code-snippets/config/mcp_settings.json .claude/

# 4. Customize for your stack
# Edit .claude.md and mcp_settings.json
```

### Example 2: Add API Integration

```typescript
// Copy and customize the API integration snippet
import { callClaude, callClaudeStreaming } from './lib/claude-api';

// Basic usage
const response = await callClaude({
  model: 'claude-sonnet-4',
  messages: [{
    role: 'user',
    content: 'Explain React hooks'
  }]
});

// Streaming usage
await callClaudeStreaming({
  model: 'claude-sonnet-4',
  messages: [/* ... */]
}, (chunk) => {
  console.log(chunk);  // Handle each chunk
});
```

### Example 3: Set Up Type Checking Hook

```bash
# 1. Copy hook script
cp code-snippets/python/hooks.py .claude/hooks/type-check.py

# 2. Make executable
chmod +x .claude/hooks/type-check.py

# 3. Configure in Claude Code settings
# (Hook will auto-run after file edits)
```

---

## Snippet Standards

All snippets in this library follow these standards:

### Documentation
- Clear purpose statement at top
- Usage instructions in comments
- Parameter descriptions
- Return value documentation

### Error Handling
- All async operations wrapped in try/catch
- Meaningful error messages
- Graceful degradation where possible

### Type Safety
- TypeScript snippets have explicit types
- No `any` types unless absolutely necessary
- Interfaces defined for complex structures

### Security
- No hardcoded secrets (use environment variables)
- Input validation examples included
- Security notes in comments

### Testability
- Functions are pure where possible
- Dependencies injected where practical
- Test examples included (where applicable)

---

## Contributing Your Own Snippets

If you develop useful patterns, consider adding them:

**Format**:
```typescript
/**
 * Brief description of what this does
 *
 * @param paramName - Description
 * @returns Description
 *
 * @example
 * const result = functionName(args);
 * // => expected output
 *
 * @see Related documentation link
 */
export function functionName(paramName: Type): ReturnType {
  // Implementation with comments
}
```

**File Naming**:
- Use kebab-case: `my-snippet-name.ts`
- Group related snippets in same file
- Keep files focused (< 300 lines)

---

## Integration with Claude Code

These snippets work great with Claude Code:

**Ask Claude to Use Them**:
```markdown
"Use the API integration pattern from code-snippets/typescript/api-integration.ts
to implement [your feature]"
```

**Reference in .claude.md**:
```markdown
## Code Patterns

For API integration, follow examples in:
- .claude/snippets/typescript/api-integration.ts

For error handling, use patterns from:
- .claude/snippets/typescript/error-handling.ts
```

**Custom Commands**:
```markdown
---
description: Create new API endpoint using our standard pattern
---

Use the API pattern from code-snippets/typescript/api-integration.ts
to create a new endpoint at [user specifies path]
```

---

## Maintenance

**Keeping Snippets Updated**:
- Review snippets quarterly
- Update for new Claude features
- Add snippets for new patterns discovered
- Remove deprecated patterns
- Update dependencies to latest versions

**Version Compatibility**:
- TypeScript: 5.0+
- Node.js: 18+
- Python: 3.8+
- Claude Code: Latest version

---

## Additional Resources

**Official Documentation**:
- Anthropic API Docs: docs.anthropic.com/claude/reference
- MCP SDK: github.com/anthropics/anthropic-sdk-typescript

**Related Files**:
- Quick Reference: `../QUICK-REFERENCE.md`
- Decision Trees: `../decision-trees.md`
- Full Playbook: `../playbook/`

**Community**:
- Share useful snippets
- Request missing examples
- Report issues with snippets

---

**License**: MIT (or your organization's license)
**Maintained By**: Claude Codex Project
**Last Updated**: 2025-11-14
