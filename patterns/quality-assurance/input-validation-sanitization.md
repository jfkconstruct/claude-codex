---
pattern_name: Input Validation & Sanitization
category: Quality Assurance
difficulty: Beginner
impact: High
date_created: 2024-11-14
last_updated: 2024-11-14
---

# Pattern: Input Validation & Sanitization

> **TL;DR**: Never trust user input—validate format, sanitize content, and enforce constraints using Claude to generate comprehensive validation logic that prevents injection attacks and data corruption.

## Overview

Input Validation & Sanitization is the foundational security pattern that treats all external data as untrusted and potentially malicious. This pattern ensures that every piece of user input is validated against expected formats and sanitized to remove or escape potentially dangerous content before processing.

The principle is simple but critical: **validate input on arrival, sanitize for output context**. Whether data comes from user forms, APIs, file uploads, or URL parameters, it must be validated against strict rules and sanitized appropriately for how it will be used (database query, HTML output, shell command, etc.).

This pattern prevents the majority of web application vulnerabilities including SQL injection, XSS, command injection, and path traversal attacks. By implementing systematic validation and sanitization, you create a security boundary that blocks malicious input before it can cause damage.

---

## Problem It Solves

### The Challenge

Applications constantly receive data from untrusted sources: users, APIs, file uploads, URL parameters. Without proper validation and sanitization, this data can:
- Execute malicious SQL queries (SQL injection)
- Run unauthorized scripts in browsers (XSS)
- Execute system commands (command injection)
- Access unauthorized files (path traversal)
- Corrupt databases with invalid data
- Crash applications with unexpected formats

**Common Symptoms:**
- SQL injection vulnerabilities in search and filter functions
- XSS attacks through comment sections or profile fields
- Application crashes from unexpected input types
- Data corruption from invalid formats (wrong email, phone number)
- Security vulnerabilities from unescaped user content

**Without This Pattern:**
- Attackers inject malicious code through input fields
- Invalid data corrupts your database
- Applications crash from malformed input
- Cross-site scripting attacks steal user sessions
- Business logic errors from unexpected data formats

### Why Traditional Approaches Fall Short

Common but insufficient approaches:
- **Client-side validation only**: Trivially bypassed by attackers
- **Blacklist filtering**: Can't anticipate all malicious patterns
- **No validation**: Assuming frameworks handle everything
- **Output-only sanitization**: Too late if data is already in database
- **Regex-only validation**: Complex, error-prone, incomplete

These approaches fail because they're either too weak (client-side), incomplete (blacklists), or delayed (output-only).

---

## The Solution

### Core Concept

Implement defense-in-depth input handling:
1. **Validate on entry**: Check format, type, length, and allowed values
2. **Sanitize for storage**: Clean data before database insertion
3. **Escape for output**: Context-specific encoding when displaying
4. **Use allowlists**: Define what's allowed, reject everything else
5. **Fail securely**: Reject invalid input with clear error messages

This creates multiple security layers that protect against injection attacks and data corruption.

### Key Principles

1. **Never Trust Input**: All external data is guilty until proven innocent
2. **Validate Early**: Check input at application boundaries
3. **Allowlist Over Blacklist**: Define what's allowed, not what's forbidden
4. **Context-Specific Sanitization**: Escape differently for SQL, HTML, shell, etc.
5. **Fail Securely**: Invalid input should be rejected, not processed

### How It Works

1. **Input Arrival**: Data enters application (form, API, file, URL)
2. **Type Validation**: Verify data type matches expectation
3. **Format Validation**: Check against format rules (email, phone, date)
4. **Range Validation**: Ensure values within acceptable bounds
5. **Sanitization**: Remove or escape dangerous characters
6. **Storage**: Save validated, sanitized data
7. **Output Encoding**: Context-specific escaping when displaying

---

## Implementation

### Basic Implementation

Always validate and sanitize user input before use:

**Prompt Template for Claude:**
```markdown
I need input validation for [describe the input].

Requirements:
- Input source: [form field / API / file upload / URL parameter]
- Expected format: [email / phone / date / number / text / etc]
- Constraints: [length limits, allowed characters, range]
- Use case: [how the data will be used]

Please generate validation code that:
1. Validates format and type
2. Enforces constraints
3. Sanitizes for storage
4. Provides clear error messages
5. Includes examples of valid and invalid input

Use allowlist approach. Be strict.
```

**Example Implementation:**

```typescript
// ❌ DANGEROUS: No validation
app.post('/api/users', (req, res) => {
  const { email, age, bio } = req.body;
  db.query(`INSERT INTO users (email, age, bio) VALUES ('${email}', ${age}, '${bio}')`);
});

// ✅ SECURE: Comprehensive validation and sanitization
import validator from 'validator';
import { z } from 'zod';

// Define schema (allowlist approach)
const userSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .max(255, 'Email too long')
    .toLowerCase()
    .trim(),

  age: z.number()
    .int('Age must be an integer')
    .min(13, 'Must be at least 13 years old')
    .max(120, 'Invalid age'),

  bio: z.string()
    .max(500, 'Bio must be 500 characters or less')
    .trim()
    .optional()
});

app.post('/api/users', async (req, res) => {
  try {
    // Validate input
    const validatedData = userSchema.parse(req.body);

    // Additional sanitization for HTML context
    const sanitizedBio = validatedData.bio
      ? validator.escape(validatedData.bio)
      : null;

    // Parameterized query (prevents SQL injection)
    await db.query(
      'INSERT INTO users (email, age, bio) VALUES (?, ?, ?)',
      [validatedData.email, validatedData.age, sanitizedBio]
    );

    res.json({ success: true });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
    throw error;
  }
});
```

### Advanced Implementation

Create reusable validation utilities:

**File: `utils/validation.ts`**
```typescript
import validator from 'validator';
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

/**
 * Common validation schemas
 */
export const schemas = {
  email: z.string()
    .email()
    .max(255)
    .toLowerCase()
    .trim()
    .refine(
      email => validator.isEmail(email),
      'Invalid email format'
    ),

  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long')
    .refine(
      pwd => /[A-Z]/.test(pwd),
      'Must contain uppercase letter'
    )
    .refine(
      pwd => /[a-z]/.test(pwd),
      'Must contain lowercase letter'
    )
    .refine(
      pwd => /[0-9]/.test(pwd),
      'Must contain number'
    )
    .refine(
      pwd => /[^A-Za-z0-9]/.test(pwd),
      'Must contain special character'
    ),

  phone: z.string()
    .trim()
    .refine(
      phone => validator.isMobilePhone(phone, 'any'),
      'Invalid phone number'
    ),

  url: z.string()
    .url('Invalid URL')
    .refine(
      url => validator.isURL(url, {
        protocols: ['http', 'https'],
        require_protocol: true
      }),
      'URL must use HTTP or HTTPS'
    ),

  slug: z.string()
    .min(1)
    .max(100)
    .regex(/^[a-z0-9-]+$/, 'Only lowercase letters, numbers, and hyphens'),

  safeText: z.string()
    .max(10000)
    .trim()
    .transform(text => validator.escape(text)),

  richText: z.string()
    .max(50000)
    .transform(html => DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li'],
      ALLOWED_ATTR: ['href']
    }))
};

/**
 * Sanitization utilities
 */
export const sanitize = {
  /**
   * For HTML output - escapes HTML special characters
   */
  forHTML: (input: string): string => {
    return validator.escape(input);
  },

  /**
   * For SQL - use parameterized queries instead, but this strips null bytes
   */
  forSQL: (input: string): string => {
    return input.replace(/\0/g, '');
  },

  /**
   * For file paths - prevents path traversal
   */
  forFilePath: (input: string): string => {
    // Remove any path traversal attempts
    const cleaned = input.replace(/\.\./g, '');
    // Only allow alphanumeric, dash, underscore, and single dots
    return cleaned.replace(/[^a-zA-Z0-9._-]/g, '');
  },

  /**
   * For shell commands - AVOID if possible, use libraries instead
   * If you MUST use shell, this is the minimum
   */
  forShell: (input: string): string => {
    // WARNING: This is NOT foolproof. Avoid shell commands with user input!
    return input.replace(/[;&|`$()]/g, '');
  },

  /**
   * For rich text - allows safe HTML tags only
   */
  forRichText: (html: string): string => {
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3'],
      ALLOWED_ATTR: ['href', 'title'],
      ALLOWED_URI_REGEXP: /^https?:\/\//
    });
  }
};

/**
 * Validation middleware generator
 */
export function validate(schema: z.ZodSchema) {
  return async (req, res, next) => {
    try {
      req.validatedData = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: 'Validation failed',
          details: error.errors.map(err => ({
            field: err.path.join('.'),
            message: err.message
          }))
        });
      }
      next(error);
    }
  };
}

/**
 * File upload validation
 */
export const fileValidation = {
  image: {
    allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    maxSize: 5 * 1024 * 1024, // 5MB

    validate(file: Express.Multer.File) {
      if (!this.allowedTypes.includes(file.mimetype)) {
        throw new Error('Invalid file type. Only JPEG, PNG, GIF, and WebP allowed');
      }
      if (file.size > this.maxSize) {
        throw new Error('File too large. Maximum size is 5MB');
      }
      // Sanitize filename
      file.filename = sanitize.forFilePath(file.originalname);
      return true;
    }
  },

  document: {
    allowedTypes: ['application/pdf', 'application/msword', 'text/plain'],
    maxSize: 10 * 1024 * 1024, // 10MB

    validate(file: Express.Multer.File) {
      if (!this.allowedTypes.includes(file.mimetype)) {
        throw new Error('Invalid file type. Only PDF, DOC, and TXT allowed');
      }
      if (file.size > this.maxSize) {
        throw new Error('File too large. Maximum size is 10MB');
      }
      file.filename = sanitize.forFilePath(file.originalname);
      return true;
    }
  }
};
```

### Configuration

**File: `.clauderc` - Custom command for validation generation**
```json
{
  "commands": {
    "generate-validation": {
      "description": "Generate validation schema for user input",
      "prompt": "Generate a comprehensive validation schema for the following input:\n\n- Field name: {field}\n- Type: {type}\n- Constraints: {constraints}\n- Use case: {useCase}\n\nInclude:\n1. Zod schema definition\n2. Sanitization logic\n3. Error messages\n4. Example valid and invalid inputs\n5. Security considerations\n\nBe strict with validation. Use allowlist approach."
    }
  }
}
```

---

## Complete Code Example

### Scenario

Building a blog platform where users can create posts with title, content, tags, and upload a cover image.

**Requirements:**
- Title: 1-200 characters, plain text
- Content: Rich text with safe HTML only
- Tags: Array of slugs (lowercase, alphanumeric, hyphens)
- Cover image: JPEG/PNG, max 5MB
- Must prevent XSS, SQL injection, and malicious uploads

### Implementation

**File: `api/posts.ts`**
```typescript
import { z } from 'zod';
import multer from 'multer';
import { schemas, sanitize, validate, fileValidation } from '../utils/validation';
import { db } from '../database';
import DOMPurify from 'isomorphic-dompurify';

// Validation schema for blog post
const createPostSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be 200 characters or less')
    .trim()
    .transform(title => sanitize.forHTML(title)), // Escape HTML

  content: z.string()
    .min(10, 'Content must be at least 10 characters')
    .max(50000, 'Content too long')
    .transform(html => sanitize.forRichText(html)), // Allow safe HTML only

  tags: z.array(
    z.string()
      .min(1)
      .max(30)
      .regex(/^[a-z0-9-]+$/, 'Tags must be lowercase alphanumeric with hyphens')
  )
    .max(5, 'Maximum 5 tags allowed')
    .optional()
    .default([]),

  slug: schemas.slug,

  publishedAt: z.string()
    .datetime('Invalid date format')
    .optional()
    .transform(date => date ? new Date(date) : null)
});

// File upload configuration
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    try {
      fileValidation.image.validate(file);
      cb(null, true);
    } catch (error) {
      cb(error);
    }
  }
});

/**
 * Create blog post
 */
export async function createPost(req, res) {
  try {
    // Validate input
    const validatedData = createPostSchema.parse(req.body);

    // Validate user is authenticated
    if (!req.userId) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    // Additional business logic validation
    const existingSlug = await db.query(
      'SELECT id FROM posts WHERE slug = ?',
      [validatedData.slug]
    );

    if (existingSlug) {
      return res.status(400).json({
        error: 'Validation failed',
        details: [{ field: 'slug', message: 'Slug already exists' }]
      });
    }

    // Insert post with parameterized query
    const result = await db.query(
      `INSERT INTO posts (user_id, title, content, slug, published_at)
       VALUES (?, ?, ?, ?, ?)`,
      [
        req.userId,
        validatedData.title,
        validatedData.content,
        validatedData.slug,
        validatedData.publishedAt
      ]
    );

    const postId = result.insertId;

    // Insert tags if provided
    if (validatedData.tags.length > 0) {
      const tagValues = validatedData.tags.map(tag => [postId, tag]);
      await db.query(
        'INSERT INTO post_tags (post_id, tag) VALUES ?',
        [tagValues]
      );
    }

    res.status(201).json({
      id: postId,
      slug: validatedData.slug,
      message: 'Post created successfully'
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message
        }))
      });
    }

    console.error('Error creating post:', error);
    res.status(500).json({ error: 'Failed to create post' });
  }
}

/**
 * Upload cover image
 */
export async function uploadCoverImage(req, res) {
  // Validate post ownership
  const post = await db.query(
    'SELECT user_id FROM posts WHERE id = ?',
    [req.params.postId]
  );

  if (!post || post.user_id !== req.userId) {
    return res.status(403).json({ error: 'Access denied' });
  }

  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    // Validate file
    fileValidation.image.validate(req.file);

    // Generate safe filename
    const safeFilename = `${Date.now()}-${sanitize.forFilePath(req.file.originalname)}`;
    const filepath = `uploads/covers/${safeFilename}`;

    // Save file (use cloud storage in production)
    await saveFile(filepath, req.file.buffer);

    // Update database with parameterized query
    await db.query(
      'UPDATE posts SET cover_image = ? WHERE id = ?',
      [filepath, req.params.postId]
    );

    res.json({
      url: `/api/images/${safeFilename}`,
      message: 'Cover image uploaded successfully'
    });

  } catch (error) {
    console.error('Error uploading cover image:', error);
    res.status(500).json({ error: 'Failed to upload image' });
  }
}

/**
 * Search posts (demonstrates query parameter validation)
 */
export async function searchPosts(req, res) {
  // Validate query parameters
  const searchSchema = z.object({
    q: z.string()
      .min(1, 'Search query required')
      .max(100, 'Query too long')
      .transform(q => sanitize.forSQL(q)),

    tag: z.string()
      .regex(/^[a-z0-9-]+$/, 'Invalid tag format')
      .optional(),

    page: z.string()
      .regex(/^\d+$/, 'Page must be a number')
      .transform(Number)
      .refine(n => n > 0, 'Page must be positive')
      .default('1'),

    limit: z.string()
      .regex(/^\d+$/, 'Limit must be a number')
      .transform(Number)
      .refine(n => n > 0 && n <= 100, 'Limit must be 1-100')
      .default('10')
  });

  try {
    const params = searchSchema.parse(req.query);

    const offset = (params.page - 1) * params.limit;

    // Use parameterized query with LIKE
    let query = 'SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?';
    let queryParams = [`%${params.q}%`, `%${params.q}%`];

    if (params.tag) {
      query += ' AND id IN (SELECT post_id FROM post_tags WHERE tag = ?)';
      queryParams.push(params.tag);
    }

    query += ' LIMIT ? OFFSET ?';
    queryParams.push(params.limit, offset);

    const posts = await db.query(query, queryParams);

    res.json({ posts, page: params.page, limit: params.limit });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        error: 'Invalid search parameters',
        details: error.errors
      });
    }
    throw error;
  }
}
```

**File: `frontend/components/PostForm.tsx`**
```typescript
// Client-side validation (UX only, not security)
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createPostSchema } from '../schemas';

export function PostForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(createPostSchema)
  });

  const onSubmit = async (data) => {
    // Data is validated client-side
    // Server will validate again (defense in depth)
    const response = await fetch('/api/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const error = await response.json();
      // Display server-side validation errors
      console.error('Server validation failed:', error.details);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('title')}
        placeholder="Post title"
        maxLength={200}
      />
      {errors.title && <span>{errors.title.message}</span>}

      {/* Client-side validation provides UX */}
      {/* Server-side validation provides security */}
    </form>
  );
}
```

### Expected Output

**Valid Request:**
```json
POST /api/posts
{
  "title": "My First Post",
  "content": "<p>This is <strong>safe HTML</strong> content.</p>",
  "slug": "my-first-post",
  "tags": ["tutorial", "beginners"]
}

Response: 201 Created
{
  "id": 123,
  "slug": "my-first-post",
  "message": "Post created successfully"
}
```

**Invalid Request (XSS attempt):**
```json
POST /api/posts
{
  "title": "Hacked <script>alert('XSS')</script>",
  "content": "<p>Normal content</p>",
  "slug": "test-post",
  "tags": ["test"]
}

Response: 201 Created
{
  "id": 124,
  "slug": "test-post",
  "message": "Post created successfully"
}

// Title is stored as: "Hacked &lt;script&gt;alert('XSS')&lt;/script&gt;"
// XSS attack prevented through HTML escaping
```

**Invalid Request (validation error):**
```json
POST /api/posts
{
  "title": "",
  "content": "Short",
  "slug": "Invalid Slug!",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
}

Response: 400 Bad Request
{
  "error": "Validation failed",
  "details": [
    { "field": "title", "message": "Title is required" },
    { "field": "content", "message": "Content must be at least 10 characters" },
    { "field": "slug", "message": "Only lowercase letters, numbers, and hyphens" },
    { "field": "tags", "message": "Maximum 5 tags allowed" }
  ]
}
```

---

## When to Use

### Ideal Use Cases

✅ **Use this pattern for:**
- All user input (forms, APIs, uploads)
- URL parameters and query strings
- File uploads
- Search functionality
- User-generated content (comments, posts, profiles)
- Any data from external sources (APIs, webhooks)
- Configuration files loaded at runtime

### Indicators You Need This Pattern

- You accept user input
- You store data in a database
- You display user content
- You process files
- You execute queries
- You use data in shell commands
- You render HTML

### Project Types

**Best For:**
- Web applications
- APIs
- Content management systems
- Social platforms
- E-commerce sites
- Form processors

**Also Works For:**
- Command-line tools (validate CLI args)
- Data processing pipelines
- File processors

---

## When NOT to Use

### Avoid This Pattern When

❌ **Never skip validation for:**
- "Trusted" user input (admin users can be compromised)
- Internal APIs (still validate—defense in depth)
- "Quick prototypes" (prototypes become production)

⚠️ **Lower priority for:**
- Hardcoded constants
- Data from your own code
- System-generated values (but validate structure)

### Simpler Alternatives

For extremely simple cases:
- **Type checking only**: If you only need to verify data type
- **Framework defaults**: Some frameworks auto-escape (verify this!)

### Warning Signs

⚠️ **Red flags:**
- "Validation is too slow" (optimize, don't skip)
- "Users won't enter bad data" (attackers will)
- "Framework handles it" (verify this assumption)
- "It's just internal" (still validate)

---

## Variations & Related Patterns

### Common Variations

1. **Schema-Based Validation**
   - **When to use**: Complex nested objects
   - **Trade-offs**: More setup, comprehensive
   - **Libraries**: Zod, Yup, Joi

2. **Decorator-Based Validation**
   - **When to use**: TypeScript classes
   - **Trade-offs**: Nice syntax, framework-specific
   - **Example**: class-validator

3. **Middleware Validation**
   - **When to use**: Express/Koa apps
   - **Trade-offs**: Centralized, reusable
   - **Example**: express-validator

### Related Patterns

- **Security Review (OWASP)**: Comprehensive security including validation
- **Error Handling**: How to handle validation failures
- **API Design**: RESTful validation patterns
- **Type Safety**: TypeScript for compile-time validation

### Pattern Combinations

This pattern works especially well with:
- **Type Safety** → Compile-time + runtime validation
- **Error Handling** → Graceful validation error handling
- **Security Review** → Part of comprehensive security strategy

---

## Best Practices

### Do's ✅

- **Validate on server**: Client-side validation is UX, not security
- **Use allowlists**: Define what's allowed, reject everything else
- **Validate early**: At application boundaries
- **Use strong typing**: TypeScript + runtime validation
- **Be specific**: Different validation for different use cases
- **Sanitize for context**: HTML escaping ≠ SQL escaping
- **Provide clear errors**: Help users fix invalid input

### Don'ts ❌

- **Don't trust client-side validation**: Always validate on server
- **Don't use blacklists**: Can't anticipate all attacks
- **Don't validate output only**: Prevent bad data from entering
- **Don't rely on frameworks alone**: Verify what they actually do
- **Don't skip validation for "trusted" users**: Defense in depth
- **Don't use regex for HTML sanitization**: Use proven libraries

### Pro Tips 💡

- **Tip 1**: Use Zod schemas—they provide TypeScript types AND runtime validation
- **Tip 2**: Sanitize at the last moment before use (context-specific)
- **Tip 3**: Log validation failures—may indicate attack attempts
- **Tip 4**: Use CSP headers as additional XSS defense layer
- **Tip 5**: Validate data when reading from database too (defense in depth)

---

## Quick Reference

### Checklist

Before deploying:
- [ ] All user input validated on server
- [ ] Validation uses allowlist approach
- [ ] Input sanitized for storage context
- [ ] Output escaped for display context
- [ ] File uploads validated (type, size, content)
- [ ] URL parameters validated
- [ ] Parameterized queries used (not string concatenation)
- [ ] Clear error messages for invalid input
- [ ] No sensitive data in validation errors

### Key Libraries

```bash
# Schema validation
npm install zod

# String validation and sanitization
npm install validator

# HTML sanitization
npm install isomorphic-dompurify

# Form validation (React)
npm install react-hook-form @hookform/resolvers
```

### Quick Code Snippets

```typescript
// Email validation
const email = z.string().email().max(255);

// Safe HTML
import DOMPurify from 'isomorphic-dompurify';
const clean = DOMPurify.sanitize(dirty);

// SQL (use parameterized queries)
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// File upload
if (!['image/jpeg', 'image/png'].includes(file.mimetype)) {
  throw new Error('Invalid file type');
}
```

---

## FAQ

### Q: Should I validate and sanitize, or just one?

A: **Both**. Validate first (reject invalid input), then sanitize what remains for safe storage/display. Validation prevents bad data; sanitization ensures safe data.

### Q: Is client-side validation enough?

A: **No**. Client-side validation improves UX but provides zero security. Attackers bypass it easily. Always validate on the server.

### Q: What's the difference between escaping and sanitization?

A:
- **Escaping**: Convert dangerous characters (`<` → `&lt;`) - use for output
- **Sanitization**: Remove or strip dangerous content - use for input
Both are needed at different stages.

### Q: Should I validate data coming from my own database?

A: **Yes** (defense in depth). Databases can be compromised, or old data may not meet new validation rules. Validate at application boundaries, including database.

---

## Further Reading

### Official Documentation
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Zod Documentation](https://zod.dev/)
- [DOMPurify](https://github.com/cure53/DOMPurify)

### Tools
- [validator.js](https://github.com/validatorjs/validator.js) - String validation library
- [express-validator](https://express-validator.github.io/) - Express middleware
- [class-validator](https://github.com/typestack/class-validator) - Decorator-based validation

### Related Patterns
- [Security Review (OWASP Top 10)](./security-review-owasp.md)
- [Code Review & Validation](./code-review.md)

---

## Sources & References

### Primary Sources

1. **OWASP Input Validation Cheat Sheet**
   - **Source**: https://cheatsheetseries.owasp.org/
   - **Relevance**: Industry standard for input validation
   - **Key Insights**: Allowlist approach, context-specific sanitization

2. **Pattern Index Research**
   - **File**: `/synthesis/pattern-index.md`
   - **Relevance**: Community patterns for validation
   - **Key Insights**: Validation gates, type checking

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-11-14 | Initial documentation |

---

## Metadata

**Tags**: `security`, `validation`, `sanitization`, `injection`, `xss`, `input-validation`

**Prerequisites**: Basic understanding of web security, SQL injection, XSS

**Estimated Time to Implement**:
- Initial setup: 1-2 hours
- Per endpoint: 10-15 minutes
- Learning curve: 1 week

**Skill Level**: Beginner - Fundamental security pattern

---

**Pattern Template Version**: 1.0
**Last Updated**: 2024-11-14
**Maintainer**: Claude Coding Knowledge Base Project
