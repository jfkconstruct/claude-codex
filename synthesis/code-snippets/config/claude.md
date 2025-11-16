# Project: [Your Project Name]

<!--
  .claude.md - Persistent Project Memory for Claude Code

  This file is automatically loaded at the start of every Claude Code session.
  It acts as a "system prompt" for your project, providing context, standards,
  and patterns that Claude should follow.

  Source: Claude Coding Master Playbook, Chapter 2
  Validation: High confidence pattern (7/11 sources)
-->

## Tech Stack

**Framework**: [e.g., Next.js 14]
**Language**: [e.g., TypeScript (strict mode)]
**Styling**: [e.g., Tailwind CSS]
**Database**: [e.g., PostgreSQL via Prisma]
**Authentication**: [e.g., NextAuth.js]
**Testing**: [e.g., Jest + React Testing Library]
**Deployment**: [e.g., Vercel]

**Key Dependencies**:
- React Query (data fetching)
- Zod (validation)
- React Hook Form (forms)
- [Add your specific libraries]

---

## Project Architecture

```
/app              # Next.js App Router
  /(auth)         # Auth pages (login, register)
  /(dashboard)    # Protected dashboard pages
  /api            # API routes
/components
  /ui             # Reusable UI components
  /features       # Feature-specific components
/lib
  /api            # API client functions
  /db             # Database utilities
  /utils          # Helper functions
/hooks            # Custom React hooks
/types            # Shared TypeScript types
```

---

## Coding Standards

### TypeScript

- ✅ **Always use explicit return types** on functions
- ✅ **Prefer `interface` over `type`** for object shapes
- ✅ **Use `const` assertions** for literal types
- ✅ **Enable strict mode** in tsconfig.json
- ❌ **Never use `any`** unless absolutely necessary (use `unknown` instead)

**Example**:
```typescript
// ✅ Good
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}

// ❌ Bad
export function formatDate(date) {  // No types
  return date.toISOString().split('T')[0];
}
```

### React Components

- ✅ **Use functional components** with hooks (no class components)
- ✅ **Extract custom hooks** when logic is reused 2+ times
- ✅ **Destructure props** with explicit types
- ✅ **Name event handlers**: `handleXxx` (e.g., `handleSubmit`, `handleClick`)
- ✅ **Co-locate tests** with components: `ComponentName.test.tsx`

**Component Structure**:
```typescript
interface Props {
  // Explicit prop types
  user: User;
  onUpdate: (user: User) => void;
}

export function UserCard({ user, onUpdate }: Props) {
  // 1. Hooks (state, queries, etc.)
  const [isEditing, setIsEditing] = useState(false);
  const { data } = useQuery(['user', user.id], fetchUser);

  // 2. Derived state
  const displayName = useMemo(() => `${user.firstName} ${user.lastName}`, [user]);

  // 3. Effects
  useEffect(() => {
    // Side effects
  }, [dependencies]);

  // 4. Event handlers
  const handleSave = useCallback(() => {
    // Handler logic
  }, [dependencies]);

  // 5. Render
  return (
    <div className="rounded-lg border p-4">
      {/* Component JSX */}
    </div>
  );
}
```

### Styling (Tailwind CSS)

- ✅ **Only use Tailwind classes** (no inline styles, no CSS modules)
- ✅ **Use responsive prefixes**: `sm:`, `md:`, `lg:`
- ✅ **Extract repeated patterns** into components (not `@apply`)
- ✅ **Use dark mode classes**: `dark:bg-gray-800`

**Example**:
```tsx
// ✅ Good
<button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
  Submit
</button>

// ❌ Bad
<button style={{ backgroundColor: 'blue', padding: '8px 16px' }}>
  Submit
</button>
```

### Database (Prisma)

- ✅ **Never use raw SQL** - always use Prisma client
- ✅ **All timestamps**: use `@default(now())` and `@updatedAt`
- ✅ **Soft delete pattern**: add `deletedAt DateTime?` field
- ✅ **Complex queries**: extract to `/lib/db/queries/*.ts`
- ✅ **Always handle errors** with try/catch

**Example**:
```typescript
// ✅ Good
async function getUsers() {
  try {
    return await prisma.user.findMany({
      where: { deletedAt: null },
      orderBy: { createdAt: 'desc' }
    });
  } catch (error) {
    logger.error('Failed to fetch users', { error });
    throw new Error('Unable to fetch users');
  }
}

// ❌ Bad
async function getUsers() {
  return await prisma.$queryRaw`SELECT * FROM users`;  // Raw SQL
}
```

### API Routes

- ✅ **Validate all inputs** with Zod
- ✅ **Return consistent format**:
  ```typescript
  { success: true, data: result }  // Success
  { success: false, error: message }  // Error
  ```
- ✅ **Proper HTTP status codes**:
  - 200: Success
  - 201: Created
  - 400: Bad Request (validation error)
  - 401: Unauthorized
  - 404: Not Found
  - 500: Server Error
- ✅ **Authentication**: verify session on protected routes
- ✅ **Error handling**: try/catch with logging

**Example**:
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2)
});

export async function POST(request: Request) {
  try {
    // 1. Validate input
    const body = await request.json();
    const validated = CreateUserSchema.parse(body);

    // 2. Check authentication
    const session = await getServerSession();
    if (!session) {
      return new Response(
        JSON.stringify({ success: false, error: 'Unauthorized' }),
        { status: 401 }
      );
    }

    // 3. Business logic
    const user = await prisma.user.create({
      data: validated
    });

    // 4. Return success
    return new Response(
      JSON.stringify({ success: true, data: user }),
      { status: 201 }
    );

  } catch (error) {
    if (error instanceof z.ZodError) {
      return new Response(
        JSON.stringify({ success: false, error: 'Invalid input', details: error.errors }),
        { status: 400 }
      );
    }

    logger.error('User creation failed', { error });
    return new Response(
      JSON.stringify({ success: false, error: 'Server error' }),
      { status: 500 }
    );
  }
}
```

### Testing

- ✅ **Minimum 80% coverage** for new code
- ✅ **Test file naming**: `ComponentName.test.tsx`
- ✅ **Describe blocks**: `describe('ComponentName')`
- ✅ **Test naming**: `it('should do X when Y')`
- ✅ **Mock external APIs** using MSW

**Example**:
```typescript
describe('UserCard', () => {
  it('should render user information', () => {
    const user = { id: '1', name: 'John Doe', email: 'john@example.com' };
    render(<UserCard user={user} onUpdate={jest.fn()} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('should call onUpdate when save button is clicked', async () => {
    const onUpdate = jest.fn();
    const user = { id: '1', name: 'John Doe', email: 'john@example.com' };

    render(<UserCard user={user} onUpdate={onUpdate} />);

    await userEvent.click(screen.getByRole('button', { name: /save/i }));

    expect(onUpdate).toHaveBeenCalledWith(user);
  });
});
```

---

## Error Handling Patterns

**All async operations MUST have try/catch**:

```typescript
// API Routes
try {
  const result = await someOperation();
  return res.json({ success: true, data: result });
} catch (error) {
  logger.error('Operation failed', { error, context });
  return res.status(500).json({
    success: false,
    error: 'Operation failed'
  });
}

// React Components (with error boundaries)
try {
  await mutation.mutateAsync(data);
  toast.success('Updated successfully');
} catch (error) {
  toast.error('Update failed. Please try again.');
  logger.error('Mutation failed', { error });
}
```

**User-facing error messages**:
- ✅ "Email is required"
- ✅ "Unable to save changes. Please try again."
- ❌ "Validation error: email.required"
- ❌ "[Object object]"
- ❌ Stack traces visible to users

---

## Security Requirements

- ❌ **Never expose API keys** in client-side code
- ✅ **All secrets** in environment variables
- ✅ **Validate all user input** (never trust client)
- ✅ **Parameterize database queries** (no string interpolation)
- ✅ **Sanitize HTML** before rendering (avoid `dangerouslySetInnerHTML`)
- ✅ **CSRF protection** on state-changing operations
- ✅ **Rate limiting** on authentication endpoints

**Security Checklist** (run before deploying):
- [ ] No hardcoded secrets (search for: `api_key`, `secret`, `password`)
- [ ] All SQL queries parameterized
- [ ] User input validated with Zod
- [ ] Authentication checked on protected routes
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] HTTPS enforced in production

---

## Before Starting Any Task

1. ✅ **Read relevant files first** - Don't assume, verify
2. ✅ **Use plan mode** (Shift+Tab) for complex tasks
3. ✅ **Ask clarifying questions** if anything is ambiguous
4. ✅ **Follow existing patterns** - Match the codebase style
5. ✅ **Write tests** for new features or bug fixes
6. ✅ **Update this file** if you discover new patterns

---

## Common Patterns

### Form Handling
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const form = useForm<FormData>({
  resolver: zodResolver(schema)
});
```

### Data Fetching
```typescript
import { useQuery } from '@tanstack/react-query';

const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers
});
```

### Mutations
```typescript
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: () => {
    queryClient.invalidateQueries(['users']);
    toast.success('Updated successfully');
  },
  onError: () => {
    toast.error('Update failed');
  }
});
```

---

## File Naming Conventions

- **Components**: `PascalCase.tsx` (e.g., `UserCard.tsx`)
- **Utilities**: `camelCase.ts` (e.g., `formatDate.ts`)
- **API routes**: `route.ts` (Next.js convention)
- **Types**: `camelCase.ts` or `types.ts`
- **Tests**: `FileName.test.tsx` or `FileName.spec.tsx`

---

## Git Commit Messages

```
feat: Add user authentication
fix: Resolve login redirect issue
refactor: Simplify user validation logic
test: Add tests for UserCard component
docs: Update API documentation
chore: Update dependencies
```

For AI-generated commits, prefix with `AI:`
```
AI: Implement user roles with RBAC
AI: Add pagination to users endpoint
```

---

## Deployment Checklist

Before deploying to production:

- [ ] All tests passing (`npm test`)
- [ ] TypeScript compiles (`npm run type-check`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security review completed
- [ ] Performance tested (Core Web Vitals)

---

## Resources

**Documentation**:
- Next.js: https://nextjs.org/docs
- React Query: https://tanstack.com/query/latest
- Prisma: https://prisma.io/docs
- Tailwind: https://tailwindcss.com/docs

**Internal**:
- API Documentation: `/docs/api.md`
- Architecture Decisions: `/docs/adr/`

---

<!--
  TODO: Customize this template for your project
  - Replace placeholder text with your actual tech stack
  - Add project-specific patterns
  - Update file paths to match your structure
  - Add domain-specific rules and constraints
-->
