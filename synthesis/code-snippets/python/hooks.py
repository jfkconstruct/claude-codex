#!/usr/bin/env python3
"""
Claude Code Hooks - Event-Driven Automation

Hooks allow you to run custom scripts at specific points in Claude Code workflow.
Source: Claude Coding Master Playbook, Chapter 9

Setup:
1. Create .claude/hooks/ directory
2. Add hook scripts with descriptive names
3. Make executable: chmod +x hook-script.py
4. Configure in Claude Code settings

Hook Types:
- post-tool-use: After Claude edits/writes files
- stop: When Claude completes a task
- pre-message: Before user sends message
- compress-history: When conversation context is compressed
- sub-agent-complete: After sub-agent finishes

Exit Codes:
- 0: Success, continue
- 2: Blocking error, Claude must fix before continuing
- Other: Non-blocking feedback
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


# ========================================
# TYPE CHECKING HOOK
# ========================================

def type_check_hook():
    """
    Auto-run TypeScript type checker after file edits

    Usage:
    Save as: .claude/hooks/type-check.py
    chmod +x .claude/hooks/type-check.py

    Configure to run on: post-tool-use (edit, write events)

    This replicates Cursor's auto-lint feature
    """
    # Read hook event data from stdin
    try:
        event_data: Dict[str, Any] = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(1)

    # Extract file path from event
    tool_input = event_data.get('tool_input', {})
    file_path = tool_input.get('path', '')

    # Only check TypeScript files
    if not file_path.endswith(('.ts', '.tsx')):
        sys.exit(0)  # Success, continue

    print(f"Running type check on {file_path}...", file=sys.stderr)

    # Run TypeScript compiler in check mode
    result = subprocess.run(
        ['tsc', '--noEmit'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # Type errors found - blocking error
        print("❌ Type checking failed:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(2)  # Exit code 2 = blocking error

    print("✅ Type checking passed", file=sys.stderr)
    sys.exit(0)  # Success


# ========================================
# LINTING HOOK
# ========================================

def eslint_hook():
    """
    Auto-run ESLint after file modifications

    Usage:
    Save as: .claude/hooks/eslint.py
    Configure to run on: post-tool-use (edit, write events)
    """
    event_data: Dict[str, Any] = json.loads(sys.stdin.read())
    tool_input = event_data.get('tool_input', {})
    file_path = tool_input.get('path', '')

    # Only lint JavaScript/TypeScript files
    if not file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
        sys.exit(0)

    print(f"Running ESLint on {file_path}...", file=sys.stderr)

    # Run ESLint with --fix to auto-fix issues
    result = subprocess.run(
        ['npx', 'eslint', '--fix', file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("⚠️  ESLint warnings/errors:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        # Don't block on lint errors, just warn
        sys.exit(0)

    print("✅ ESLint passed", file=sys.stderr)
    sys.exit(0)


# ========================================
# TEST RUNNER HOOK
# ========================================

def test_runner_hook():
    """
    Auto-run tests after code changes

    Usage:
    Save as: .claude/hooks/test-runner.py
    Configure to run on: post-tool-use (edit, write events)

    Only runs tests related to changed files
    """
    event_data: Dict[str, Any] = json.loads(sys.stdin.read())
    tool_input = event_data.get('tool_input', {})
    file_path = tool_input.get('path', '')

    # Find related test file
    test_file = find_test_file(file_path)

    if not test_file or not Path(test_file).exists():
        print(f"No test file found for {file_path}", file=sys.stderr)
        sys.exit(0)

    print(f"Running tests: {test_file}...", file=sys.stderr)

    # Run Jest on specific test file
    result = subprocess.run(
        ['npm', 'test', '--', test_file, '--passWithNoTests'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("❌ Tests failed:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        sys.exit(2)  # Blocking error

    print("✅ Tests passed", file=sys.stderr)
    sys.exit(0)


def find_test_file(source_file: str) -> str:
    """Find corresponding test file"""
    path = Path(source_file)

    # Common test file patterns
    patterns = [
        path.with_suffix('.test' + path.suffix),  # file.test.ts
        path.with_suffix('.spec' + path.suffix),  # file.spec.ts
        Path('tests') / path.name.replace(path.suffix, f'.test{path.suffix}'),  # tests/file.test.ts
        Path('__tests__') / path.name,  # __tests__/file.ts
    ]

    for test_path in patterns:
        if test_path.exists():
            return str(test_path)

    return ''


# ========================================
# NOTIFICATION HOOK
# ========================================

def notification_hook():
    """
    Send notification when Claude completes a task

    Usage:
    Save as: .claude/hooks/notify.py
    Configure to run on: stop event

    Requires:
    macOS: terminal-notifier (brew install terminal-notifier)
    Linux: notify-send (usually pre-installed)
    """
    import platform

    event_data: Dict[str, Any] = json.loads(sys.stdin.read())

    system = platform.system()

    if system == 'Darwin':  # macOS
        subprocess.run([
            'terminal-notifier',
            '-title', 'Claude Code',
            '-message', 'Task completed!',
            '-sound', 'default'
        ])
    elif system == 'Linux':
        subprocess.run([
            'notify-send',
            'Claude Code',
            'Task completed!'
        ])
    else:
        print("✅ Task completed!", file=sys.stderr)

    sys.exit(0)


# ========================================
# SECURITY SCAN HOOK
# ========================================

def security_scan_hook():
    """
    Run security checks on code changes

    Usage:
    Save as: .claude/hooks/security-scan.py
    Configure to run on: post-tool-use

    Checks for:
    - Hardcoded API keys
    - SQL injection patterns
    - XSS vulnerabilities
    """
    import re

    event_data: Dict[str, Any] = json.loads(sys.stdin.read())
    tool_input = event_data.get('tool_input', {})
    file_path = tool_input.get('path', '')

    if not Path(file_path).exists():
        sys.exit(0)

    print(f"Running security scan on {file_path}...", file=sys.stderr)

    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Check for hardcoded API keys
    api_key_patterns = [
        r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9_-]+["\']',
        r'sk_live_[a-zA-Z0-9]+',  # Stripe live keys
        r'pk_live_[a-zA-Z0-9]+',  # Stripe publishable keys
    ]

    for pattern in api_key_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"⚠️  Possible hardcoded API key found (pattern: {pattern})")

    # Check for SQL injection vulnerabilities
    sql_injection_patterns = [
        r'SELECT.*FROM.*\$\{',  # String interpolation in SQL
        r'INSERT INTO.*VALUES.*\$\{',
        r'UPDATE.*SET.*\$\{',
        r'DELETE FROM.*WHERE.*\$\{',
    ]

    for pattern in sql_injection_patterns:
        if re.search(pattern, content):
            issues.append(f"⚠️  Possible SQL injection vulnerability (pattern: {pattern})")

    # Check for XSS vulnerabilities
    if 'dangerouslySetInnerHTML' in content:
        issues.append("⚠️  dangerouslySetInnerHTML used - ensure input is sanitized")

    if issues:
        print("\n❌ Security issues found:", file=sys.stderr)
        for issue in issues:
            print(f"  {issue}", file=sys.stderr)
        sys.exit(2)  # Blocking error

    print("✅ Security scan passed", file=sys.stderr)
    sys.exit(0)


# ========================================
# DOCUMENTATION HOOK
# ========================================

def documentation_hook():
    """
    Auto-update documentation when code changes

    Usage:
    Save as: .claude/hooks/update-docs.py
    Configure to run on: post-tool-use

    Updates README.md with function signatures when API changes
    """
    event_data: Dict[str, Any] = json.loads(sys.stdin.read())
    tool_input = event_data.get('tool_input', {})
    file_path = tool_input.get('path', '')

    # Only update docs for API files
    if 'api' not in file_path.lower():
        sys.exit(0)

    print("📝 Updating documentation...", file=sys.stderr)

    # Run documentation generator (adjust for your setup)
    result = subprocess.run(
        ['npm', 'run', 'docs:generate'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Documentation updated", file=sys.stderr)
    else:
        print("⚠️  Documentation update failed (non-blocking)", file=sys.stderr)

    sys.exit(0)  # Don't block even if docs fail


# ========================================
# MAIN ENTRY POINT
# ========================================

if __name__ == '__main__':
    # Determine which hook to run based on script name or argument
    import os

    script_name = os.path.basename(__file__)

    if 'type-check' in script_name:
        type_check_hook()
    elif 'eslint' in script_name or 'lint' in script_name:
        eslint_hook()
    elif 'test' in script_name:
        test_runner_hook()
    elif 'notify' in script_name:
        notification_hook()
    elif 'security' in script_name:
        security_scan_hook()
    elif 'docs' in script_name:
        documentation_hook()
    else:
        print("Unknown hook type. Check script name.", file=sys.stderr)
        sys.exit(1)
