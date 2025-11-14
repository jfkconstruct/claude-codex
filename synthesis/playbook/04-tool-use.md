# Chapter 4: Tool Use & Function Calling

**Target Audience**: Developers ready to extend Claude's capabilities
**Reading Time**: 20-25 minutes
**Practice Time**: 3-4 hours
**Prerequisites**: Chapters 1-3, basic Claude Code proficiency

**Learning Objectives**:
- Understand when and why to use external tools
- Master MCP (Model Context Protocol) server integration
- Configure essential MCP servers (Context7, Supabase, Playwright)
- Design and integrate custom tools
- Handle tool responses and errors effectively
- Build multi-step tool chains
- Debug tool integrations

---

## 4.1 When to Use Tools

### Beyond Code Generation

Claude is excellent at writing code, but some tasks require real-time data, external systems, or capabilities beyond text generation.

**Tasks That Need Tools**:
- ✅ Accessing latest documentation (changes frequently)
- ✅ Querying databases (production data, analytics)
- ✅ Browser automation (testing, scraping, verification)
- ✅ File system operations outside project directory
- ✅ External API calls (GitHub, payment processors, cloud services)
- ✅ Real-time data (stock prices, weather, current events)

**Tasks That DON'T Need Tools**:
- ❌ Writing code (Claude's core competency)
- ❌ Code refactoring
- ❌ Explaining concepts
- ❌ Analyzing code within the project
- ❌ Planning and architecture

### The MCP Value Proposition

**Without MCP** (Context7 example):
```markdown
User: "Use the latest React Query documentation to implement data fetching"

Claude: [Uses training data from January 2025, may be outdated]
        "Based on React Query v4 patterns..."

User: "Actually we're on v5, and the API changed"
Claude: [Can't access latest docs, provides outdated advice]
```

**With MCP** (Context7 installed):
```markdown
User: "Use the latest React Query documentation to implement data fetching"

Claude: [Fetches current docs from tanstack.com via Context7 MCP]
        "According to React Query v5.0 documentation (current):

        \`\`\`typescript
        import { useQuery } from '@tanstack/react-query'

        function Component() {
          const { data, isLoading } = useQuery({
            queryKey: ['users'],
            queryFn: fetchUsers,
          })
        }
        \`\`\`

        [Accurate, up-to-date implementation]"
```

**15% Accuracy Improvement**: Using live documentation vs. relying on training data.

---

## 4.2 MCP (Model Context Protocol) Servers

### What is MCP?

**Model Context Protocol** is Anthropic's standard for extending Claude with external capabilities. Think of it as a plugin system that lets Claude interact with databases, browsers, APIs, file systems, and more.

**Architecture**:
```
Claude Code
    │
    ├─ MCP Protocol
    │     │
    │     ├─ Context7 Server (documentation)
    │     ├─ Supabase Server (database)
    │     ├─ Playwright Server (browser)
    │     ├─ GitHub Server (repository operations)
    │     └─ Custom MCP Server (your integration)
    │
    └─ Your Application
```

### Installing MCP Servers

**Installation Methods**:
```bash
# Method 1: Global NPM install (most common)
npm install -g @context7/mcp-server

# Method 2: NPX (no install, runs on-demand)
npx -y @modelcontextprotocol/server-playwright

# Method 3: Local project install
npm install @supabase/mcp-server
```

### Configuration File

MCP servers are configured in `.claude/mcp_settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,tailwindcss,prisma"],
      "description": "Up-to-date documentation for popular libraries"
    },

    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server",
        "--supabase-url", "https://xxx.supabase.co",
        "--supabase-key", "${SUPABASE_SERVICE_KEY}"
      ],
      "description": "Direct database access for queries and analytics"
    },

    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "description": "Browser automation for testing and web scraping"
    }
  }
}
```

**Environment Variables**: Use `${VAR_NAME}` syntax to reference environment variables for secrets.

---

## 4.3 Essential MCP Servers

### Context7: Live Documentation (Priority #1)

**Confidence**: ⭐⭐⭐⭐⭐ **VERY HIGH** (10/11 sources recommend)

**Why Essential**:
- Always uses latest library documentation
- Covers 1000+ popular libraries
- Eliminates outdated advice
- Universally recommended across all sources

**Installation**:
```bash
npm install -g @context7/mcp-server
```

**Configuration**:
```json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": [
        "--libraries",
        "nextjs,react,typescript,tailwindcss,prisma,react-query,zod,next-auth"
      ]
    }
  }
}
```

**Usage Example**:
```markdown
User: "Implement infinite scroll with React Query v5"

Claude: [Uses Context7 to fetch latest React Query v5 docs]
        "Based on the current React Query v5 documentation:

        \`\`\`typescript
        import { useInfiniteQuery } from '@tanstack/react-query'

        function Users() {
          const {
            data,
            fetchNextPage,
            hasNextPage,
            isFetchingNextPage,
          } = useInfiniteQuery({
            queryKey: ['users'],
            queryFn: async ({ pageParam = 0 }) => {
              const res = await fetch(\`/api/users?cursor=\${pageParam}\`)
              return res.json()
            },
            getNextPageParam: (lastPage) => lastPage.nextCursor,
          })
        }
        \`\`\`

        [Accurate implementation using current API]"
```

**Libraries Supported**: Next.js, React, Vue, Svelte, Tailwind, Prisma, TypeScript, and 1000+ more.

---

### Supabase: Database Access

**Confidence**: ⭐⭐⭐⭐ **HIGH** (7/11 sources)

**Why Valuable**:
- Query production data directly
- Get real analytics ("How many users signed up last week?")
- Debug data issues
- Analyze patterns

**Installation**:
```bash
npm install -g @supabase/mcp-server
```

**Configuration**:
```json
{
  "mcpServers": {
    "supabase": {
      "command": "supabase-mcp",
      "args": [
        "--supabase-url", "${SUPABASE_URL}",
        "--supabase-key", "${SUPABASE_SERVICE_KEY}"
      ]
    }
  }
}
```

**Environment Setup**:
```bash
# .env.local
SUPABASE_URL=https://xxxproject.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGci0iJI...  # Service role key (has full access)
```

**Usage Example**:
```markdown
User: "How many users signed up in the last 7 days? Show breakdown by day."

Claude: [Queries Supabase via MCP]
        "Querying your database...

        Result: 247 users signed up in the last 7 days.

        Breakdown by day:
        - Nov 14: 42 users
        - Nov 13: 38 users
        - Nov 12: 31 users
        - Nov 11: 45 users
        - Nov 10: 29 users
        - Nov  9: 35 users
        - Nov  8: 27 users

        SQL used:
        \`\`\`sql
        SELECT
          DATE(created_at) as signup_date,
          COUNT(*) as user_count
        FROM users
        WHERE created_at >= NOW() - INTERVAL '7 days'
        GROUP BY DATE(created_at)
        ORDER BY signup_date DESC;
        \`\`\`"
```

**Security Warning**: Service role key has full database access. Only use in secure environments. Never commit keys to git.

---

### Playwright: Browser Automation

**Confidence**: ⭐⭐⭐⭐ **HIGH** (8/11 sources)

**Why Valuable**:
- E2E testing automation
- Web scraping and research
- Screenshot generation
- UI verification
- Debugging rendering issues

**Installation**:
```bash
# No install needed, uses npx
# Or install globally:
npm install -g @modelcontextprotocol/server-playwright
```

**Configuration**:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

**Usage Example 1: E2E Testing**:
```markdown
User: "Test the login flow: navigate to /login, enter credentials,
       submit, verify redirect to /dashboard"

Claude: [Uses Playwright MCP to automate browser]
        "I'll test the login flow...

        \`\`\`typescript
        // Generated test
        test('login flow', async ({ page }) => {
          await page.goto('http://localhost:3000/login')

          await page.fill('[name=\"email\"]', 'test@example.com')
          await page.fill('[name=\"password\"]', 'password123')
          await page.click('button[type=\"submit\"]')

          await expect(page).toHaveURL('/dashboard')
          await expect(page.locator('h1')).toContainText('Dashboard')
        })
        \`\`\`

        Test result: ✅ Passed
        - Login form loaded successfully
        - Credentials accepted
        - Redirected to /dashboard as expected
        - Dashboard heading found"
```

**Usage Example 2: Web Research**:
```markdown
User: "Find the latest best practices for Next.js 14 App Router
       from articles published in 2025"

Claude: [Uses Playwright to search and scrape]
        "I searched for recent Next.js 14 App Router best practices.

        **Top findings from 3 recent articles**:

        1. **Server Components by Default** (vercel.com/blog)
           - Use 'use client' sparingly
           - Keep components on server when possible
           - Reduces bundle size by 40-60%

        2. **Parallel Routes for Complex Layouts** (leerob.io)
           - Use (@folder) convention for parallel routes
           - Enables sophisticated loading states
           - Example: @modal, @sidebar patterns

        3. **Streaming with Suspense** (nextjs.org)
           - Wrap slow components in <Suspense>
           - Stream content as it's ready
           - Dramatically improves perceived performance

        [Full sources provided]"
```

---

### GitHub CLI Integration

**Confidence**: ⭐ **LOW** (1/11 sources, but powerful)

**Why Valuable**:
- Automate issue → fix → PR workflow
- No context switching to browser
- End-to-end automation

**Installation**:
```bash
# Install GitHub CLI
brew install gh  # macOS
# or: https://cli.github.com/

# Authenticate
gh auth login
```

**Configuration**: No MCP server needed; Claude can use `gh` CLI directly via bash commands.

**Usage Example**:
```markdown
User: "Fix GitHub issue #47"

Claude: [Uses gh CLI to fetch issue]
        "Reading issue #47...

        Issue: \"User profile images not loading in production\"

        Let me investigate...
        [Analyzes code, identifies issue with S3 URL generation]

        I've found the bug in lib/storage.ts. The environment
        variable for S3 bucket name is undefined in production.

        Implementing fix...
        [Fixes code]

        Creating pull request...
        [Uses gh pr create]

        ✅ Pull Request created: #48
           \"Fix S3 bucket configuration for profile images\"
           https://github.com/user/repo/pull/48"
```

**Workflow Automation**: Combine with custom commands for `/fix-github-issue [number]` (see Chapter 5).

---

## 4.4 Designing Custom Tools

### When to Create Custom MCP Servers

**Build Custom MCP When**:
- ✅ Integrating proprietary internal APIs
- ✅ Connecting to company databases
- ✅ Accessing internal tools (Jira, Confluence, Slack)
- ✅ Domain-specific operations (financial calculations, scientific instruments)

**Don't Build Custom MCP When**:
- ❌ Existing MCP server already does it
- ❌ Can be done with bash commands
- ❌ One-off use case (not worth infrastructure)

### Custom MCP Server Structure

**Example: Custom Stripe MCP**:

```typescript
// stripe-mcp-server.ts
import { Server } from '@modelcontextprotocol/sdk/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

const server = new Server({
  name: 'stripe',
  version: '1.0.0',
});

// Define available tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'get_recent_charges',
        description: 'Get recent successful charges',
        inputSchema: {
          type: 'object',
          properties: {
            limit: { type: 'number', default: 10 }
          }
        }
      },
      {
        name: 'create_refund',
        description: 'Refund a charge',
        inputSchema: {
          type: 'object',
          properties: {
            charge_id: { type: 'string' },
            amount: { type: 'number', optional: true }
          },
          required: ['charge_id']
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'get_recent_charges') {
    const charges = await stripe.charges.list({
      limit: args.limit || 10,
      status: 'succeeded'
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(charges.data, null, 2)
      }]
    };
  }

  if (name === 'create_refund') {
    const refund = await stripe.refunds.create({
      charge: args.charge_id,
      amount: args.amount
    });

    return {
      content: [{
        type: 'text',
        text: `Refund created: ${refund.id}`
      }]
    };
  }
});

server.connect({
  type: 'stdio'
});
```

**Configuration** (`.claude/mcp_settings.json`):
```json
{
  "mcpServers": {
    "stripe": {
      "command": "node",
      "args": ["/path/to/stripe-mcp-server.js"],
      "env": {
        "STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}"
      }
    }
  }
}
```

---

## 4.5 Handling Tool Responses

### Parsing Tool Output

**Structured Responses**:
```typescript
// MCP returns structured data
{
  "content": [
    {
      "type": "text",
      "text": "{\"users\": 247, \"breakdown\": [...]}"
    }
  ]
}

// Claude parses and presents naturally:
"Your database shows 247 users signed up this week..."
```

### Error Recovery

**Tool Timeout**:
```markdown
User: "Query all users from the database"

Claude: [Supabase MCP times out after 30 seconds]
        "The query timed out (30 seconds). This table may be very large.

        Let's optimize:
        1. Add pagination: LIMIT 1000 OFFSET 0
        2. Add indexes on frequently queried columns
        3. Use materialized views for analytics queries

        Would you like me to:
        A) Retry with pagination?
        B) Analyze the table structure for optimization?
        C) Create a summary query instead (COUNT(*) by category)?"
```

**Tool Unavailable**:
```markdown
Claude: [Context7 MCP server not responding]
        "I couldn't fetch the latest documentation (Context7 MCP unavailable).

        I'll use my training data (current through January 2025).
        Please verify this implementation against the latest docs at:
        https://tanstack.com/query/latest/docs/react/overview

        [Provides implementation with caveat]"
```

### Rate Limiting

**Example: GitHub API**:
```typescript
// MCP handles rate limiting internally
try {
  const response = await mcpClient.callTool('github', 'list_issues');
} catch (error) {
  if (error.code === 'RATE_LIMITED') {
    // Wait and retry
    const retryAfter = error.retryAfter || 60;
    await sleep(retryAfter * 1000);
    // Retry...
  }
}
```

---

## 4.6 Multi-Step Tool Chains

### Orchestrating Multiple Tools

**Example: Full research → implementation workflow**:

```markdown
User: "Research best practices for React Server Components,
       then implement a server component for fetching user data"

Claude: [Step 1: Uses Playwright MCP to research]
        "Researching React Server Components best practices...

        Found 5 recent articles. Key patterns:
        - Async components (await in component body)
        - Direct database/API access (no client-side fetching)
        - No useState or useEffect
        - Automatic request deduplication

        [Step 2: Uses Context7 MCP for official docs]
        Checking official Next.js documentation...

        [Step 3: Implements based on research]
        Here's the server component following current best practices:

        \`\`\`typescript
        // app/users/UserList.tsx
        import { db } from '@/lib/database'

        // Server Component (async)
        export default async function UserList() {
          // Direct database access (no API layer needed)
          const users = await db.user.findMany({
            take: 50,
            orderBy: { createdAt: 'desc' }
          })

          return (
            <div>
              {users.map(user => (
                <div key={user.id}>{user.name}</div>
              ))}
            </div>
          )
        }
        \`\`\`

        This follows all current best practices from my research."
```

**Chain**: Playwright (research) → Context7 (docs) → Code Generation

### Transaction-Like Patterns

**Example: Multi-step database operation**:

```markdown
User: "Create a new subscription: charge customer, create record, send email"

Claude: [Uses Stripe MCP + Supabase MCP + Email MCP]
        "I'll perform this as a transaction-like sequence:

        Step 1: Charge customer via Stripe
        ✅ Charge successful: ch_abc123 ($29.99)

        Step 2: Create subscription record in database
        ✅ Record created: subscription_id = 847

        Step 3: Send confirmation email
        ✅ Email sent to user@example.com

        All steps completed successfully.

        Note: This isn't a true atomic transaction. If step 3 failed,
        we'd have charged the customer but not sent confirmation.
        Consider implementing:
        - Idempotency keys for Stripe
        - Database transactions
        - Email queue with retry logic

        Would you like me to add this safety infrastructure?"
```

---

## 4.7 Debugging Tool Integrations

### Common MCP Issues

**Issue #1: MCP Server Not Found**

**Symptom**:
```
Error: MCP server 'context7' not found
```

**Solutions**:
```bash
# 1. Verify installation
which context7-mcp
npm list -g @context7/mcp-server

# 2. Check configuration path
cat .claude/mcp_settings.json

# 3. Try full path in config
{
  "mcpServers": {
    "context7": {
      "command": "/usr/local/bin/context7-mcp",  // Full path
      "args": ["--libraries", "react"]
    }
  }
}

# 4. Restart Claude Code
exit
claude
```

---

**Issue #2: Authentication Failures**

**Symptom**:
```
Error: Supabase authentication failed
```

**Solutions**:
```bash
# 1. Verify environment variables
echo $SUPABASE_SERVICE_KEY

# 2. Check key validity (Supabase dashboard → Settings → API)

# 3. Use .env file
cat > .env.local <<EOF
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGci...
EOF

# 4. Load environment variables before running Claude
export $(cat .env.local | xargs)
claude
```

---

**Issue #3: Tool Timeout**

**Symptom**:
```
MCP tool call timed out after 30 seconds
```

**Solutions**:
```markdown
1. **Optimize the operation**:
   - Add pagination to large queries
   - Use indexes on database tables
   - Cache expensive computations

2. **Increase timeout** (in MCP server config):
   \`\`\`json
   {
     "mcpServers": {
       "supabase": {
         "command": "supabase-mcp",
         "args": ["--timeout", "60000"]  // 60 seconds
       }
     }
   }
   \`\`\`

3. **Break into smaller operations**:
   - Query in batches
   - Use streaming responses
   - Implement progress callbacks
```

---

## 4.8 MCP Cost-Benefit Analysis

### Armin Ronacher's Critique

**Finding** (from 800+ hours source): Some MCPs add unnecessary complexity without commensurate value.

**Guidelines**:

**High Value MCPs** (Worth the Complexity):
- ✅ **Context7**: Universal recommendation, always valuable
- ✅ **Database MCPs**: Direct access to production data
- ✅ **Browser MCPs**: Testing and research capabilities

**Evaluate Carefully**:
- ⚠️ **Niche MCPs**: Assess if bash commands suffice
- ⚠️ **Overcomplicated MCPs**: Look for simpler alternatives
- ⚠️ **Single-Use MCPs**: May not justify setup overhead

**Questions to Ask**:
1. Can I accomplish this with bash + existing tools?
2. Will I use this MCP regularly (weekly+)?
3. Does the value justify the configuration complexity?
4. Is there an existing, well-maintained MCP?

---

## 4.9 Key Takeaways

**Essential MCPs** (Start Here):
- ✅ **Context7**: Latest documentation (Priority #1)
- ✅ **Supabase/Database**: Production data access
- ✅ **Playwright**: Browser automation and testing

**When to Use Tools**:
- ✅ Real-time data, external APIs, database queries
- ❌ Code generation, refactoring, planning

**Best Practices**:
- ✅ Use environment variables for secrets
- ✅ Handle timeouts and errors gracefully
- ✅ Start with essential MCPs, add niche ones as needed
- ✅ Test MCP setup before relying on it

**Quick Reference**:
```bash
# Install Context7 (Priority #1)
npm install -g @context7/mcp-server

# Configure in .claude/mcp_settings.json
{
  "mcpServers": {
    "context7": {
      "command": "context7-mcp",
      "args": ["--libraries", "nextjs,react,typescript"]
    }
  }
}

# Restart Claude Code
exit && claude
```

---

## 4.10 Practice Exercises

**Exercise 1: Install Context7**
- Install Context7 MCP server
- Configure for your tech stack
- Ask Claude to use latest docs for a library you use
- Compare quality vs. without Context7

**Exercise 2: Database Queries**
- Set up Supabase MCP (or Postgres MCP)
- Ask Claude analytical questions about your data
- Practice error handling (query timeouts)

**Exercise 3: Browser Automation**
- Configure Playwright MCP
- Ask Claude to test a user flow
- Generate screenshots of different pages
- Research a technical topic via web search

**Exercise 4: Multi-Tool Chain**
- Combine Context7 + Database MCP
- Research a pattern, then query how it's used in your data
- Observe how Claude orchestrates multiple tools

**Exercise 5: Custom MCP (Advanced)**
- Build a simple custom MCP for an internal API
- Configure it in Claude Code
- Test with Claude

---

**Next Chapter**: [Chapter 5: Production Readiness](./05-production-readiness.md) - Deploy Claude-powered development safely with monitoring, security, testing, and deployment patterns.

---

**Word Count**: ~3,450 words
**Reading Time**: 22 minutes
**Hands-On Time**: 3-4 hours

**Validation**:
- MCP Servers: ⭐⭐⭐⭐⭐ VERY HIGH confidence (10/11 sources)
- Context7: Universally recommended
- Supabase: 7/11 sources
- Playwright: 8/11 sources

**Sources**:
- Pattern Confidence Matrix (11 sources analyzed)
- "A Complete Guide to Claude Code" (extensive MCP coverage)
- "800+ hours Learning Claude Code" (MCP evaluation)
- Armin Ronacher: MCP complexity analysis
- Anthropic: Tool use best practices
