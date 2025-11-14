---
pattern_name: MCP Servers for External Tool Integration
category: Tooling
difficulty: Intermediate
impact: High
date_created: 2025-11-14
last_updated: 2025-11-14
---

# Pattern: MCP Servers for External Tool Integration

> **TL;DR**: Use Model Context Protocol (MCP) servers to extend Claude's capabilities with access to live documentation, databases, file systems, browsers, and external APIs—eliminating stale information and enabling powerful integrations.

## Overview

The Model Context Protocol (MCP) is a standardized way to connect Claude to external tools and data sources beyond your codebase. Instead of relying on potentially outdated training data, MCP servers provide Claude with real-time access to:

- **Always-current documentation** from official sources
- **Database operations** to query production data directly
- **Browser automation** for research and data gathering
- **File system access** beyond your project directory
- **External API integrations** for specialized services

This dramatically extends Claude's capabilities from a code-focused assistant to a full-stack development partner that can research current best practices, query your database, automate web tasks, and integrate with your entire development ecosystem.

**Key Benefits:**
- Documentation is never out of date (pulled from official sources in real-time)
- Direct database access eliminates manual SQL running
- Automated research saves hours of manual web browsing
- Semantic code search finds relevant code by meaning, not just keywords

---

## Problem It Solves

### The Challenge

When coding with Claude, you often face limitations that break your flow:

1. **Stale Documentation**: Claude's training data has a cutoff date, meaning framework/library documentation may be outdated
2. **Limited Capabilities**: Claude can't natively access databases, browse the web, or interact with external services
3. **Manual Context Gathering**: You must manually copy-paste documentation, database query results, or research findings
4. **Time-Consuming Research**: Finding current best practices or API changes requires leaving the coding session

**Common Symptoms:**
- Claude provides outdated examples for frameworks (e.g., React Router v5 syntax when v6 is current)
- You need to manually run database queries and paste results back to Claude
- Research tasks require switching between browser, terminal, and Claude
- Can't access files or systems outside your project directory
- Missing context about current library versions and breaking changes

**Without This Pattern:**
- Claude provides generic or outdated solutions based on training data
- Constant context-switching between tools breaks development flow
- Manual data gathering is error-prone and time-consuming
- Limited to information explicitly provided in prompts
- Can't leverage Claude for data analysis or automation tasks

### Why Traditional Approaches Fall Short

**Copy-Paste Workflow**: Manually fetching documentation, running queries, and pasting results is:
- Time-consuming and breaks flow
- Error-prone (copy wrong version, miss important details)
- Not scalable for complex multi-step tasks

**Search Engines**: Using Google/Stack Overflow separately means:
- Context loss when switching tools
- Claude can't proactively research when needed
- You must synthesize findings and relay to Claude

**Static Context Files**: Storing documentation locally becomes:
- Quickly outdated as libraries update
- Massive file bloat in your project
- Still limited to what you anticipated needing

---

## The Solution

### Core Concept

MCP servers act as bridges between Claude and external systems. Each server exposes specific capabilities (called "tools") that Claude can invoke directly during conversations. When configured, Claude automatically:

1. Detects when external information/capabilities would help
2. Calls the appropriate MCP server
3. Processes the response
4. Incorporates results into its answer

You set up servers once in `.claude/mcp_settings.json`, and Claude handles all interactions transparently.

### Key Principles

1. **Transparent Integration**: Claude automatically uses MCP servers when relevant—you don't need special syntax
2. **Real-Time Data**: Information is fetched live, ensuring currency and accuracy
3. **Specialized Servers**: Each server focuses on one domain (docs, database, browser, etc.)
4. **Composable**: Multiple servers work together to solve complex tasks
5. **Secure**: Servers run locally with explicit permissions

### How It Works

1. **Install MCP servers** as npm packages (globally or locally)
2. **Configure** servers in `.claude/mcp_settings.json` with commands and arguments
3. **Claude detects** when a task would benefit from external tools
4. **Claude invokes** the appropriate MCP server
5. **Server executes** the request (fetch docs, query DB, etc.)
6. **Claude receives** results and integrates them into the response
7. **You get** accurate, current information without manual research

---

## Implementation

### Basic Implementation

Start with Context7 for always-current documentation:

**Step 1: Install Context7 MCP Server**
```bash
npm install -g @context7/mcp-server
```

**Step 2: Create MCP Configuration**

**File: `.claude/mcp_settings.json`**
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,tailwindcss"],
      "description": "Up-to-date documentation for popular libraries"
    }
  }
}
```

**Step 3: Use in Conversation**
```markdown
User: "How do I use React Query's useInfiniteQuery in v5?"

Claude: [Automatically fetches latest React Query v5 docs via Context7]
"According to the current React Query documentation (v5.0),
useInfiniteQuery works like this:

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

function Projects() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetching,
  } = useInfiniteQuery({
    queryKey: ['projects'],
    queryFn: ({ pageParam = 0 }) => fetchProjects(pageParam),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  })
}
```
[Continues with current, accurate documentation...]"
```

**Explanation:**
- Context7 maintains up-to-date caches of popular library documentation
- Claude automatically queries Context7 when documentation would help
- You get current information without leaving the conversation

### Advanced Implementation

Configure multiple MCP servers for comprehensive capabilities:

**File: `.claude/mcp_settings.json`**
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,tailwindcss,prisma,typescript"],
      "description": "Up-to-date documentation for popular libraries"
    },

    "serena": {
      "command": "npx",
      "args": ["-y", "@serena-ai/mcp-server"],
      "description": "Semantic code search and retrieval across codebase"
    },

    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Documents",
        "/Users/username/Projects"
      ],
      "description": "Access to local file system outside project"
    },

    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Browser automation for research and web scraping"
    },

    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server",
        "--supabase-url", "https://your-project.supabase.co",
        "--supabase-key", "your-service-role-key"
      ],
      "description": "Direct database access for queries and operations"
    }
  }
}
```

**Security Note**: For production databases, use read-only credentials or create a dedicated service account with limited permissions.

**Explanation:**
- **Context7**: Provides current documentation (React, Next.js, Tailwind, etc.)
- **Serena**: Semantic search finds code by meaning ("authentication logic" vs literal string matching)
- **Filesystem**: Access files outside project (design docs, shared libraries)
- **Browser**: Automated web research and data gathering
- **Supabase**: Direct database queries without leaving Claude

### Configuration

**Environment Variables for Security**

Instead of hardcoding credentials, use environment variables:

```bash
# .env (add to .gitignore!)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
GITHUB_TOKEN=ghp_your_token_here
```

**File: `.claude/mcp_settings.json`**
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server",
        "--supabase-url", "${SUPABASE_URL}",
        "--supabase-key", "${SUPABASE_KEY}"
      ],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_KEY}"
      },
      "description": "Database access with environment variables"
    }
  }
}
```

---

## Complete Code Example

### Scenario

You're building a SaaS application and need to:
1. Implement infinite scroll pagination using latest Next.js 14 patterns
2. Query the database to see current user growth metrics
3. Research how competitors implement similar features
4. Search your codebase for existing authentication patterns

**Requirements:**
- Use current Next.js 14 App Router patterns (not outdated Pages Router)
- Get real user metrics from production database
- Find relevant examples from competitor research
- Reuse existing auth patterns from codebase

### Implementation

**Setup: Install all required MCP servers**
```bash
# Documentation
npm install -g @context7/mcp-server

# Semantic code search
npm install -g @serena-ai/mcp-server

# Database access
npm install -g @supabase/mcp-server

# Browser automation
npm install -g @modelcontextprotocol/server-playwright
```

**File: `.claude/mcp_settings.json`**
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react-query,prisma"],
      "description": "Current Next.js, React Query, and Prisma docs"
    },
    "serena": {
      "command": "npx",
      "args": ["-y", "@serena-ai/mcp-server"],
      "description": "Semantic code search"
    },
    "supabase": {
      "command": "npx",
      "args": [
        "-y", "@supabase/mcp-server",
        "--supabase-url", "https://myapp.supabase.co",
        "--supabase-key", "your-key-here"
      ],
      "description": "Production database access"
    },
    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Web research automation"
    }
  }
}
```

**Usage Session:**

```markdown
User: "I need to implement infinite scroll for our user list.
First, show me how many users we have and recent growth.
Then find how we handle auth in the codebase, and give me
current best practices for infinite scroll in Next.js 14."

Claude: "I'll gather all that information for you.

[Calls Supabase MCP to query database]
**User Growth Metrics:**
- Total users: 1,247
- Last 7 days: 89 new users
- Last 30 days: 342 new users
- Growth rate: +27.4% month-over-month

Daily breakdown (last 7 days):
- Nov 14: 15 users
- Nov 13: 12 users
- Nov 12: 18 users
- Nov 11: 11 users
- Nov 10: 14 users
- Nov 9: 10 users
- Nov 8: 9 users

[Calls Serena MCP for semantic code search]
**Authentication Patterns in Your Codebase:**

Found 4 relevant locations:

1. `/lib/auth.ts` (lines 23-67)
   - Main auth logic using NextAuth.js
   - JWT token generation and validation

2. `/middleware.ts` (lines 8-29)
   - Route protection middleware
   - Redirects to login if unauthenticated

3. `/app/api/auth/[...nextauth]/route.ts`
   - NextAuth configuration
   - Google and email providers

4. `/hooks/useAuth.ts`
   - React hook for auth state
   - Provides user info and logout function

[Calls Context7 MCP for latest Next.js docs]
**Current Next.js 14 Infinite Scroll Best Practices:**

According to the latest Next.js 14 documentation, here's the
recommended approach using App Router and React Query:

```typescript
'use client'

import { useInfiniteQuery } from '@tanstack/react-query'
import { useInView } from 'react-intersection-observer'
import { useEffect } from 'react'

export function UserList() {
  const { ref, inView } = useInView()

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetching,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['users'],
    queryFn: async ({ pageParam = 0 }) => {
      const res = await fetch(`/api/users?cursor=${pageParam}&limit=20`)
      return res.json()
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  })

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage()
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage])

  return (
    <div>
      {data?.pages.map((page) => (
        page.users.map((user) => (
          <UserCard key={user.id} user={user} />
        ))
      ))}

      {hasNextPage && (
        <div ref={ref} className="py-4">
          {isFetchingNextPage ? 'Loading more...' : 'Load more'}
        </div>
      )}
    </div>
  )
}
```

**API Route** (`/app/api/users/route.ts`):
```typescript
import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const cursor = searchParams.get('cursor') || '0'
  const limit = parseInt(searchParams.get('limit') || '20')

  const users = await prisma.user.findMany({
    take: limit + 1, // Fetch one extra to check if there's a next page
    skip: parseInt(cursor),
    orderBy: { createdAt: 'desc' },
  })

  const hasMore = users.length > limit
  const nextCursor = hasMore ? parseInt(cursor) + limit : null

  return NextResponse.json({
    users: users.slice(0, limit),
    nextCursor,
  })
}
```

This approach:
- ✅ Uses React Query v5 (latest stable)
- ✅ Implements cursor-based pagination
- ✅ Auto-loads on scroll with Intersection Observer
- ✅ Handles loading states properly
- ✅ Works with Next.js 14 App Router

Would you like me to implement this following your existing auth
patterns from `/lib/auth.ts`?"
```

### Expected Output

When properly configured, Claude will:
1. ✅ Fetch current documentation (not outdated training data)
2. ✅ Query your database directly for real metrics
3. ✅ Search your codebase semantically for patterns
4. ✅ Provide working, current code examples
5. ✅ All without you leaving the conversation

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern when:**
- Working with rapidly evolving frameworks (Next.js, React, etc.) where docs change frequently
- Need to query production databases for metrics, debugging, or data analysis
- Researching current best practices or recent API changes
- Building features that require knowledge of your entire codebase (not just current files)
- Automating repetitive web research or data gathering tasks
- Integrating with external APIs (GitHub, Stripe, Slack, etc.)
- Need access to files or documentation outside your project directory

### Indicators You Need This Pattern

- Claude provides outdated syntax or deprecated APIs
- You frequently switch between browser (docs), database client, and Claude
- Copy-pasting documentation, query results, or research into prompts
- Asking "find all places where we handle X" requires manual grep/search
- Need to verify current library versions or breaking changes
- Spending significant time on manual research that could be automated

### Project Types

**Best For:**
- **Modern web apps** using frequently-updated frameworks (Next.js, React, Vue)
- **Full-stack applications** with database access needs
- **SaaS products** requiring user analytics and metrics
- **API integrations** needing current documentation
- **Large codebases** where semantic search helps find relevant code
- **Research-heavy projects** requiring current best practices

**Also Works For:**
- **Mobile development** (React Native, Flutter docs)
- **Backend services** (Node.js, Python framework docs)
- **Data analysis** (direct database querying)
- **DevOps/Infrastructure** (Terraform, Kubernetes docs)
- **Any project** where current information matters

---

## When NOT to Use

### Avoid This Pattern When

❌ **Don't use this pattern if:**
- Working with stable, rarely-updated technologies (HTML, CSS basics, vanilla JS)
- Project has no external dependencies or integrations
- Security policies prohibit external tool connections
- Working entirely offline or in air-gapped environments
- Project complexity doesn't justify setup overhead (simple scripts, one-off tools)
- Your company prohibits AI access to production databases

### Simpler Alternatives

If this pattern seems too complex, consider:

- **Manual Documentation Lookup**: For occasional needs, just search docs yourself
  - When: Using only 1-2 libraries, infrequent updates

- **Static Context Files**: Store key documentation in project
  - When: Small project, stable dependencies, team prefers local docs

- **README with Links**: Maintain curated list of current documentation URLs
  - When: Small team, everyone knows where to find docs

### Warning Signs

⚠️ **Red flags that suggest this pattern isn't right:**
- Setting up 5+ MCP servers but only using 1-2 regularly (over-engineering)
- Using database MCP with production write access (security risk)
- Installing every available MCP server "just in case" (complexity bloat)
- Team doesn't understand what MCP servers are doing (training gap)
- Experiencing frequent MCP server crashes or errors (compatibility issues)

---

## Variations & Related Patterns

### Common Variations

1. **Read-Only Database Access**
   - **When to use**: Production databases where writes are dangerous
   - **Trade-offs**: Safe but limited; can't test mutations
   ```json
   {
     "supabase": {
       "command": "npx",
       "args": ["--read-only", "true"],
       "description": "Read-only DB access for safety"
     }
   }
   ```

2. **Project-Specific MCP Servers**
   - **When to use**: Internal tools, proprietary systems
   - **Trade-offs**: Custom development effort vs perfect fit
   - **Example**: Custom MCP server for your company's design system or internal API

3. **Cached vs Live Documentation**
   - **When to use**: Balance freshness with performance
   - **Trade-offs**: Speed vs currency
   - **Context7** caches docs but refreshes daily for best of both

### Related Patterns

- **[Claude.md / Persistent Memory](../context/claude-md.md)**: Use together to store MCP server usage patterns
- **[Custom Commands](../workflow/custom-commands.md)**: Create commands that leverage specific MCP servers
- **[Sub-Agents](../architecture/sub-agents.md)**: Assign different MCP servers to specialized sub-agents

### Pattern Combinations

This pattern works especially well with:

- **Context Management + MCP** → Claude fetches only relevant docs based on current context
- **Plan Mode + MCP** → Claude researches during planning phase before coding
- **Code Review + MCP** → Claude checks against latest best practices during review

---

## Metrics & Results

### Expected Improvements

Based on reports from sources analyzing Claude Code workflows:

- **Time Savings**: 30-40% reduction in context-switching between tools
- **Accuracy**: Always current documentation eliminates deprecated API usage
- **Productivity**: Database queries in conversation vs manual SQL client switching
- **Research Speed**: Automated web research 5-10x faster than manual browsing

**Source**: YouTube tutorials "800+ hours of Learning Claude Code" and "A Complete Guide to Claude Code"

### Success Indicators

You'll know this pattern is working when:
- Claude provides current syntax/APIs without you requesting specific versions
- Database questions get answered instantly without leaving the conversation
- Research tasks complete in minutes instead of hours
- Semantic code search finds relevant patterns you didn't know existed
- Team velocity increases as documentation lookup becomes automatic

---

## Common Pitfalls & Solutions

### Pitfall 1: Exposing Production Database with Write Access

**Problem**: Configuring MCP with full production database access allows Claude to modify/delete data accidentally.

**Solution**: Use read-only credentials or separate analytics database.

```json
// ❌ Wrong: Full production access
{
  "supabase": {
    "args": ["--supabase-key", "service_role_key_with_write"]
  }
}

// ✅ Correct: Read-only key
{
  "supabase": {
    "args": ["--supabase-key", "anon_key_read_only"]
  }
}

// ✅ Better: Use replica or analytics DB
{
  "supabase": {
    "args": [
      "--supabase-url", "https://analytics-replica.supabase.co",
      "--supabase-key", "readonly_key"
    ]
  }
}
```

### Pitfall 2: Installing Every MCP Server Without Purpose

**Problem**: Over-configuring with 10+ MCP servers slows down Claude and adds complexity.

**Solution**: Start with 2-3 essential servers, add more only when needed.

```json
// ❌ Wrong: Kitchen sink approach
{
  "mcpServers": {
    "context7": {...},
    "serena": {...},
    "filesystem": {...},
    "browser": {...},
    "supabase": {...},
    "postgres": {...},
    "github": {...},
    "gitlab": {...},
    "slack": {...},
    "stripe": {...}
    // ... 10 more servers
  }
}

// ✅ Correct: Start essential, add as needed
{
  "mcpServers": {
    "context7": {...},    // Always need current docs
    "supabase": {...}     // Database for this project
    // Add more only when workflow requires them
  }
}
```

### Pitfall 3: Hardcoding Credentials in Config

**Problem**: Committing MCP config with API keys/database credentials to Git.

**Solution**: Use environment variables for all sensitive data.

```json
// ❌ Wrong: Hardcoded secrets
{
  "supabase": {
    "args": [
      "--supabase-url", "https://abc123.supabase.co",
      "--supabase-key", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    ]
  }
}

// ✅ Correct: Environment variables
{
  "supabase": {
    "args": [
      "--supabase-url", "${SUPABASE_URL}",
      "--supabase-key", "${SUPABASE_KEY}"
    ],
    "env": {
      "SUPABASE_URL": "${SUPABASE_URL}",
      "SUPABASE_KEY": "${SUPABASE_KEY}"
    }
  }
}
```

**Also add to `.gitignore`:**
```
.env
.claude/mcp_settings.json  # If it contains secrets
```

---

## Best Practices

### Do's ✅

- **Start with Context7**: Documentation is the most universally useful MCP server
- **Use read-only database credentials**: Prevent accidental data modifications
- **Configure environment variables**: Keep secrets out of version control
- **Test MCP servers individually**: Verify each works before adding more
- **Document MCP server purposes**: Help team understand what each server does
- **Monitor MCP performance**: Some servers are slower; optimize or disable if needed
- **Version pin MCP servers**: Use specific versions in package.json for consistency

### Don'ts ❌

- **Don't expose production write access**: Use read-only or dedicated accounts
- **Don't commit credentials**: Always use environment variables
- **Don't install servers you don't use**: Each adds overhead
- **Don't skip security review**: Understand what access each server has
- **Don't ignore errors**: Failed MCP calls indicate configuration issues
- **Don't use filesystem MCP for sensitive directories**: Limit to safe paths only

### Pro Tips 💡

- **Tip 1**: Context7 supports library aliases: `"nextjs,react,prisma"` automatically includes related packages
- **Tip 2**: Combine Serena (semantic search) with Context7 (docs) for "find auth code and show latest best practices"
- **Tip 3**: Use Browser MCP for competitive research: "How do [competitor] implement this feature?"
- **Tip 4**: Create custom MCP servers for internal tools—spec is open-source and well-documented
- **Tip 5**: MCP servers can be chained: Claude can use filesystem → read config → query database → update code
- **Tip 6**: Add MCP server setup to your project's onboarding docs for consistent team setup

---

## Real-World Examples

### Example 1: Next.js SaaS Application

**Context**: Building a subscription-based SaaS with Next.js 14, Prisma, and Stripe

**Challenge**:
- Next.js updates frequently; training data lags behind
- Need to query subscription metrics for debugging
- Must integrate Stripe API with current best practices

**Implementation**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,prisma,stripe"],
      "description": "Current docs for Next.js, Prisma, Stripe"
    },
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server", ...credentials],
      "description": "Production database (read-only)"
    }
  }
}
```

**Results**:
- Claude provides current Next.js 14 App Router patterns (not outdated Pages Router)
- Database queries for subscription metrics happen in conversation
- Stripe integration uses latest API version (2024-11-20) automatically
- Development velocity increased ~35% (less context switching)

**Source**: Mentioned in "800+ hours of Learning Claude Code in 8 minutes" tutorial

### Example 2: Open Source Contributor Workflow

**Context**: Contributing to large open-source React libraries

**Challenge**:
- Unfamiliar codebase with 500+ files
- Need to understand architecture before contributing
- Must follow project's existing patterns

**Implementation**:
```json
{
  "mcpServers": {
    "serena": {
      "command": "npx",
      "args": ["-y", "@serena-ai/mcp-server"],
      "description": "Semantic code search across large codebase"
    },
    "browser": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Research similar PRs and issues"
    }
  }
}
```

**Results**:
- Semantic search finds all authentication-related code (not just grep matches)
- Browser automation researches similar feature implementations
- Quickly onboard to unfamiliar codebases
- Contributions follow existing patterns accurately

**Source**: "A Complete Guide to Claude Code Here are ALL the" tutorial showcasing Serena MCP

---

## Quick Reference

### Checklist

Before implementing this pattern, ensure:
- [ ] You have npm installed (required for npx and MCP server installation)
- [ ] You understand which MCP servers solve your specific problems
- [ ] You have read-only database credentials (if using database MCP)
- [ ] You've added `.env` and sensitive configs to `.gitignore`
- [ ] Your team knows how to set up MCP servers (document setup process)

### Implementation Steps (Quick)

1. Install MCP server packages: `npm install -g @context7/mcp-server`
2. Create `.claude/mcp_settings.json` with server configurations
3. Add credentials to `.env` file (don't commit!)
4. Test each server: ask Claude a question that requires that MCP
5. Iterate: add more servers as needs arise

### Key Commands/Code Snippets

```bash
# Install common MCP servers
npm install -g @context7/mcp-server                          # Documentation
npm install -g @serena-ai/mcp-server                        # Semantic search
npm install -g @modelcontextprotocol/server-filesystem      # File access
npm install -g @modelcontextprotocol/server-playwright      # Browser
npm install -g @supabase/mcp-server                         # Database

# Verify installation
context7-mcp --version
```

**Minimal Config:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react"],
      "description": "Current Next.js and React docs"
    }
  }
}
```

---

## FAQ

### Q: Do MCP servers send my code to external servers?

A: No. MCP servers run locally on your machine. Context7 fetches public documentation from official sources, but your code never leaves your machine. Always review the source code of MCP servers before installing (they're open source).

### Q: Which MCP server should I install first?

A: **Context7** is the most universally useful. It provides current documentation for popular libraries and frameworks, eliminating the most common source of outdated information.

### Q: Can I create custom MCP servers for internal tools?

A: Yes! The Model Context Protocol is open source. You can create custom servers for your company's design system, internal APIs, or proprietary tools. See the official MCP specification on GitHub.

### Q: How do I know if Claude is using an MCP server?

A: Claude will often mention the source: "According to the current Next.js documentation..." indicates Context7 usage. You can also ask: "Did you use an MCP server for that information?"

### Q: Are there performance impacts from many MCP servers?

A: Each MCP server adds slight overhead. Start with 2-3 essential servers and add more only as needed. If Claude becomes slow, reduce the number of active servers.

### Q: Can I use MCP servers with production databases safely?

A: Use read-only credentials or create a dedicated read-only replica database. Never give MCP servers write access to production data without extreme caution and safeguards.

---

## Further Reading

### Official Documentation
- [Model Context Protocol Specification](https://github.com/anthropics/mcp) - Official MCP standard and documentation
- [Anthropic MCP Announcement](https://www.anthropic.com/mcp) - Introduction and use cases

### Tutorials
- [Building Custom MCP Servers](https://github.com/anthropics/mcp/docs/custom-servers.md) - Guide to creating your own servers
- [MCP Server Directory](https://github.com/anthropics/mcp-servers) - Community-maintained list of available servers

### Case Studies
- Context7: [Official Context7 Documentation](https://context7.ai/docs) - In-depth usage examples
- Serena: [Semantic Code Search with MCP](https://serena.ai/mcp-guide) - Advanced code search patterns

### Related Patterns
- [Context Management & Codebase Understanding](../context/context-management.md) - Combines well with MCP for comprehensive context
- [Custom Commands](../workflow/custom-commands.md) - Create commands that leverage MCP servers
- [Claude.md / Persistent Memory](../context/claude-md.md) - Document MCP usage patterns for consistency

---

## Sources & References

### Primary Sources

1. **Armin Ronacher - Agentic Coding with Claude**
   - **File**: `/sources/youtube/armin-ronacher-agentic-coding-summary.md`
   - **Relevance**: Deep dive into MCP architecture and context sharing strategies
   - **Key Insights**: MCP enables agent-to-agent context sharing and external tool integration

2. **800+ Hours of Learning Claude Code in 8 Minutes**
   - **File**: `/sources/youtube/800+ hours of Learning Claude Code in 8 minutes 2.md`
   - **Relevance**: Practical examples of Context7 and Supabase MCP usage
   - **Key Insights**: Real-world workflows showing documentation lookup and database queries

3. **A Complete Guide to Claude Code**
   - **File**: `/sources/youtube/A Complete Guide to Claude Code Here are ALL the.md`
   - **Relevance**: Comprehensive coverage of Serena MCP for semantic code search
   - **Key Insights**: Semantic search dramatically improves code discovery in large codebases

### Research & Data

- Anthropic Official Documentation: Prompt Engineering Best Practices
- MCP Protocol Specification (Open Source): github.com/anthropics/mcp
- Context7 Performance Metrics: 30-40% reduction in documentation lookup time

### Community Resources

- [MCP Server Registry](https://github.com/anthropics/mcp-servers) - Community catalog of available servers
- [Context7 Examples](https://context7.ai/examples) - Real-world usage patterns
- [Serena Documentation](https://serena.ai/docs) - Semantic search integration guide

---

## Common MCP Servers Reference

| MCP Server | Purpose | Use Case | Installation |
|------------|---------|----------|--------------|
| **context7** | Live documentation | Get latest library docs | `npm install -g @context7/mcp-server` |
| **serena** | Semantic code search | Find code by meaning, not keywords | `npm install -g @serena-ai/mcp-server` |
| **filesystem** | File system access | Read/write files outside project | `npm install -g @modelcontextprotocol/server-filesystem` |
| **browser** | Web automation | Research, scraping, testing | `npm install -g @modelcontextprotocol/server-playwright` |
| **supabase** | Database access | Query/analyze production data | `npm install -g @supabase/mcp-server` |
| **github** | GitHub operations | Issues, PRs, repo management | `npm install -g @modelcontextprotocol/server-github` |
| **postgres** | PostgreSQL | Direct database queries | `npm install -g @modelcontextprotocol/server-postgres` |
| **gitlab** | GitLab operations | Issues, MRs, pipelines | `npm install -g @modelcontextprotocol/server-gitlab` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-14 | Initial documentation extracted from Top 10 Best Practices synthesis |

---

## Metadata

**Tags**: `mcp`, `tools`, `integration`, `documentation`, `database`, `automation`, `context7`, `serena`, `productivity`

**Prerequisites**:
- Basic understanding of npm and package installation
- Familiarity with JSON configuration files
- Understanding of environment variables for security

**Estimated Time to Implement**: 15-30 minutes for basic setup (Context7), 1-2 hours for comprehensive setup (multiple servers)

**Skill Level**: Intermediate (basic setup is beginner-friendly, advanced configurations require more experience)

---

## Contributing

Found an improvement or additional example? Please contribute:
1. Add your MCP server configurations in the "Real-World Examples" section
2. Share metrics if you've measured productivity improvements
3. Document additional MCP servers and their use cases
4. Submit custom MCP server examples for specialized domains

---

**Pattern Template Version**: 1.0
**Last Updated**: 2025-11-14
**Maintainer**: Claude Coding Knowledge Base Project
