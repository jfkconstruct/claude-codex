/**
 * Claude API Integration Examples
 *
 * Reusable patterns for integrating with Anthropic's Claude API
 * Source: Claude Coding Master Playbook, Chapters 3-4
 *
 * Setup:
 * npm install @anthropic-ai/sdk
 *
 * Environment:
 * ANTHROPIC_API_KEY=your-api-key-here
 */

import Anthropic from '@anthropic-ai/sdk';

// Initialize client (singleton pattern)
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// ========================================
// BASIC REQUEST/RESPONSE
// ========================================

/**
 * Simple Claude API call
 *
 * @param prompt - User message to send to Claude
 * @param model - Claude model to use
 * @returns Claude's response text
 *
 * @example
 * const response = await callClaude('Explain React hooks');
 * console.log(response);  // => "React hooks are..."
 */
export async function callClaude(
  prompt: string,
  model: 'claude-sonnet-4' | 'claude-opus-4' = 'claude-sonnet-4'
): Promise<string> {
  try {
    const message = await anthropic.messages.create({
      model,
      max_tokens: 2048,
      temperature: 0.0,  // Consistency for code
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    // Extract text from response
    const textContent = message.content.find(block => block.type === 'text');
    return textContent?.type === 'text' ? textContent.text : '';

  } catch (error) {
    console.error('Claude API error:', error);
    throw error;
  }
}

// ========================================
// STREAMING RESPONSES
// ========================================

/**
 * Stream Claude's response in real-time
 *
 * @param prompt - User message
 * @param onChunk - Callback for each text chunk
 * @param model - Claude model to use
 *
 * @example
 * await callClaudeStreaming(
 *   'Explain async/await',
 *   (chunk) => process.stdout.write(chunk)
 * );
 */
export async function callClaudeStreaming(
  prompt: string,
  onChunk: (text: string) => void,
  model: 'claude-sonnet-4' | 'claude-opus-4' = 'claude-sonnet-4'
): Promise<void> {
  try {
    const stream = await anthropic.messages.stream({
      model,
      max_tokens: 2048,
      temperature: 0.0,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    for await (const chunk of stream) {
      if (
        chunk.type === 'content_block_delta' &&
        chunk.delta.type === 'text_delta'
      ) {
        onChunk(chunk.delta.text);
      }
    }

  } catch (error) {
    console.error('Streaming error:', error);
    throw error;
  }
}

// ========================================
// RETRY LOGIC WITH EXPONENTIAL BACKOFF
// ========================================

/**
 * Call Claude with automatic retry on rate limits
 *
 * @param prompt - User message
 * @param maxRetries - Maximum retry attempts
 * @returns Claude's response
 *
 * @example
 * const response = await callClaudeWithRetry('Generate code', 4);
 */
export async function callClaudeWithRetry(
  prompt: string,
  maxRetries: number = 4
): Promise<string> {
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      return await callClaude(prompt);

    } catch (error: any) {
      // Check if rate limit error
      if (error.code === 'rate_limit_exceeded' && attempt < maxRetries - 1) {
        attempt++;

        // Exponential backoff: 2s, 4s, 8s, 16s
        const delay = Math.pow(2, attempt) * 1000;
        console.log(`Rate limited. Retrying in ${delay}ms (attempt ${attempt}/${maxRetries})`);

        await sleep(delay);
      } else {
        throw error;  // Non-rate-limit error or max retries exceeded
      }
    }
  }

  throw new Error('Max retries exceeded');
}

// Helper: Sleep function
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ========================================
// STRUCTURED PROMPTS
// ========================================

/**
 * Create structured prompt with XML tags (30% accuracy boost)
 *
 * @param options - Prompt components
 * @returns Claude's response
 *
 * @example
 * const response = await callClaudeStructured({
 *   context: 'Next.js 14 app with TypeScript',
 *   task: 'Create a login form component',
 *   examples: ['export function LoginForm() { ... }'],
 *   constraints: ['Use React Hook Form', 'Tailwind CSS only']
 * });
 */
export async function callClaudeStructured(options: {
  context?: string;
  task: string;
  examples?: string[];
  constraints?: string[];
  format?: string;
  model?: 'claude-sonnet-4' | 'claude-opus-4';
}): Promise<string> {
  const {
    context,
    task,
    examples = [],
    constraints = [],
    format,
    model = 'claude-sonnet-4'
  } = options;

  // Build structured prompt
  let prompt = '';

  if (context) {
    prompt += `<context>\n${context}\n</context>\n\n`;
  }

  prompt += `<task>\n${task}\n</task>\n\n`;

  if (examples.length > 0) {
    prompt += `<examples>\n${examples.join('\n\n')}\n</examples>\n\n`;
  }

  if (constraints.length > 0) {
    prompt += `<constraints>\n${constraints.map(c => `- ${c}`).join('\n')}\n</constraints>\n\n`;
  }

  if (format) {
    prompt += `<format>\n${format}\n</format>\n\n`;
  }

  return callClaude(prompt, model);
}

// ========================================
// MULTI-TURN CONVERSATIONS
// ========================================

/**
 * Manage multi-turn conversation with Claude
 *
 * @example
 * const conversation = new ClaudeConversation();
 * const response1 = await conversation.send('Explain React');
 * const response2 = await conversation.send('Now explain hooks');
 * // Claude remembers previous context
 */
export class ClaudeConversation {
  private messages: Anthropic.MessageParam[] = [];
  private model: 'claude-sonnet-4' | 'claude-opus-4';

  constructor(model: 'claude-sonnet-4' | 'claude-opus-4' = 'claude-sonnet-4') {
    this.model = model;
  }

  /**
   * Send message and get response
   */
  async send(userMessage: string): Promise<string> {
    // Add user message to history
    this.messages.push({
      role: 'user',
      content: userMessage
    });

    try {
      const response = await anthropic.messages.create({
        model: this.model,
        max_tokens: 2048,
        temperature: 0.0,
        messages: this.messages
      });

      // Extract response text
      const textContent = response.content.find(block => block.type === 'text');
      const responseText = textContent?.type === 'text' ? textContent.text : '';

      // Add assistant response to history
      this.messages.push({
        role: 'assistant',
        content: responseText
      });

      return responseText;

    } catch (error) {
      console.error('Conversation error:', error);
      throw error;
    }
  }

  /**
   * Clear conversation history
   */
  clear(): void {
    this.messages = [];
  }

  /**
   * Get conversation history
   */
  getHistory(): Anthropic.MessageParam[] {
    return [...this.messages];
  }

  /**
   * Get token count (approximate)
   */
  getTokenCount(): number {
    // Rough estimate: 1 token ≈ 4 characters
    const totalChars = this.messages.reduce((sum, msg) => {
      const content = typeof msg.content === 'string'
        ? msg.content
        : msg.content.map(block =>
            block.type === 'text' ? block.text : ''
          ).join('');
      return sum + content.length;
    }, 0);

    return Math.ceil(totalChars / 4);
  }
}

// ========================================
// ERROR HANDLING PATTERNS
// ========================================

/**
 * Comprehensive error handling for Claude API
 *
 * @example
 * try {
 *   const response = await callClaudeWithErrorHandling(prompt);
 * } catch (error) {
 *   // Error already logged and classified
 *   console.error(error.message);
 * }
 */
export async function callClaudeWithErrorHandling(
  prompt: string
): Promise<string> {
  try {
    return await callClaude(prompt);

  } catch (error: any) {
    // Classify and handle different error types
    if (error.status === 429) {
      throw new Error('Rate limit exceeded. Please wait and retry.');
    }

    if (error.status === 401) {
      throw new Error('Invalid API key. Check ANTHROPIC_API_KEY environment variable.');
    }

    if (error.status === 400) {
      throw new Error(`Invalid request: ${error.message}`);
    }

    if (error.code === 'ENOTFOUND' || error.code === 'ETIMEDOUT') {
      throw new Error('Network error. Check your internet connection.');
    }

    // Generic error
    throw new Error(`Claude API error: ${error.message}`);
  }
}

// ========================================
// USAGE EXAMPLES
// ========================================

/**
 * Complete usage example
 */
export async function exampleUsage() {
  // Example 1: Simple call
  const simple = await callClaude('Explain TypeScript generics');
  console.log('Simple response:', simple);

  // Example 2: Streaming
  console.log('\nStreaming response:');
  await callClaudeStreaming(
    'Count from 1 to 5',
    (chunk) => process.stdout.write(chunk)
  );

  // Example 3: Structured prompt
  const structured = await callClaudeStructured({
    context: 'React 18 + TypeScript project',
    task: 'Create a custom useDebounce hook',
    examples: [
      'const debouncedValue = useDebounce(value, 500);'
    ],
    constraints: [
      'Use TypeScript generics',
      'Include JSDoc comments',
      'Add usage example'
    ]
  });
  console.log('\nStructured response:', structured);

  // Example 4: Conversation
  const conversation = new ClaudeConversation();
  const step1 = await conversation.send('What is React Query?');
  const step2 = await conversation.send('Show me an example of useQuery');
  console.log('Conversation:', { step1, step2 });

  // Example 5: With retry logic
  const withRetry = await callClaudeWithRetry('Generate API endpoint code');
  console.log('With retry:', withRetry);
}

// Run example if executed directly
if (require.main === module) {
  exampleUsage().catch(console.error);
}
