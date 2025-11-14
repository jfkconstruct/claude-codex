#!/usr/bin/env bash
#
# Git Workflows for AI-Assisted Development
#
# Collection of git patterns for safe Claude Code usage
# Source: Claude Coding Master Playbook, Chapter 3
#
# Usage:
# Source this file in your shell: source git-workflows.sh
# Or copy individual functions to your .bashrc/.zshrc

set -euo pipefail

# ========================================
# CHECKPOINT WORKFLOW
# ========================================

# Create checkpoint before letting Claude make changes
claude_checkpoint() {
    local task_description="${1:-AI changes}"

    echo "📍 Creating checkpoint: $task_description"

    # Check if working directory is clean
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  Uncommitted changes detected. Committing first..."
        git add .
        git commit -m "WIP: Before $task_description"
    fi

    # Create checkpoint commit
    git add .
    git commit -m "Checkpoint: Before $task_description" --allow-empty

    echo "✅ Checkpoint created. Safe to let Claude work now."
}

# Commit AI-generated changes
claude_commit() {
    local description="${1:-AI generated changes}"

    echo "💾 Committing AI changes: $description"

    git add .
    git commit -m "AI: $description"

    echo "✅ Changes committed."
}

# Rollback to last checkpoint
claude_rollback() {
    echo "⏮️  Rolling back to last checkpoint..."

    # Show recent commits
    echo "Recent commits:"
    git log --oneline -5

    read -p "Confirm rollback to previous commit? (y/N) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git reset --hard HEAD^
        echo "✅ Rolled back successfully."
    else
        echo "❌ Rollback cancelled."
    fi
}

# ========================================
# COMPLETE WORKFLOW
# ========================================

# Complete Claude Code workflow with safety checks
claude_workflow() {
    local task_description="$1"

    echo "🤖 Starting Claude Code workflow for: $task_description"
    echo

    # Step 1: Create checkpoint
    claude_checkpoint "$task_description"
    echo

    # Step 2: Remind user to use Claude
    echo "🎯 Now:"
    echo "  1. Open Claude Code: claude"
    echo "  2. Work on: $task_description"
    echo "  3. Review changes: git diff HEAD"
    echo "  4. When done, run: claude_complete"
    echo
}

# Complete workflow - review and commit
claude_complete() {
    echo "🔍 Reviewing changes..."
    echo

    # Show diff
    git diff --stat HEAD

    echo
    read -p "Show detailed diff? (y/N) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git diff HEAD | less
    fi

    echo
    read -p "Accept these changes? (y/N) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit description: " description
        claude_commit "$description"
        echo "✅ Workflow complete!"
    else
        echo "❌ Changes not committed. Use 'claude_rollback' to discard."
    fi
}

# ========================================
# GRANULAR COMMITS
# ========================================

# Commit individual files (for fine-grained rollback)
claude_commit_file() {
    local file_path="$1"
    local description="${2:-Update $file_path}"

    if [[ ! -f "$file_path" ]]; then
        echo "❌ File not found: $file_path"
        return 1
    fi

    echo "💾 Committing $file_path..."

    git add "$file_path"
    git commit -m "AI: $description"

    echo "✅ Committed: $file_path"
}

# Interactive file-by-file commit
claude_commit_interactive() {
    local changed_files

    # Get list of changed files
    changed_files=$(git diff --name-only HEAD)

    if [[ -z "$changed_files" ]]; then
        echo "No changes to commit."
        return 0
    fi

    echo "Changed files:"
    echo "$changed_files" | nl
    echo

    while IFS= read -r file; do
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "File: $file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        git diff HEAD "$file" | head -20

        echo
        read -p "Commit this file? (y/n/q) " -n 1 -r
        echo

        case $REPLY in
            [Yy])
                read -p "Description: " desc
                claude_commit_file "$file" "$desc"
                ;;
            [Qq])
                echo "Remaining files not committed."
                break
                ;;
            *)
                echo "Skipped: $file"
                ;;
        esac

        echo
    done <<< "$changed_files"
}

# ========================================
# PARALLEL DEVELOPMENT (WORKTREES)
# ========================================

# Set up parallel Claude Code instances using git worktrees
claude_parallel_setup() {
    local feature_name="$1"
    local num_instances="${2:-3}"

    echo "🌲 Setting up $num_instances parallel worktrees for: $feature_name"

    for i in $(seq 1 "$num_instances"); do
        local branch_name="claude/${feature_name}-approach-${i}"
        local worktree_path="../${PWD##*/}-approach-${i}"

        echo "Creating approach $i..."

        # Create branch and worktree
        git worktree add -b "$branch_name" "$worktree_path"

        echo "  ✅ Worktree: $worktree_path"
        echo "  ✅ Branch: $branch_name"
    done

    echo
    echo "🎯 Next steps:"
    echo "  1. Open Claude Code in each worktree:"
    for i in $(seq 1 "$num_instances"); do
        echo "     cd ../${PWD##*/}-approach-${i} && claude"
    done
    echo
    echo "  2. Give each the same prompt"
    echo "  3. Compare results with: claude_parallel_compare $feature_name"
}

# Compare parallel worktree implementations
claude_parallel_compare() {
    local feature_name="$1"

    echo "📊 Comparing parallel implementations..."

    for i in {1..3}; do
        local worktree_path="../${PWD##*/}-approach-${i}"

        if [[ -d "$worktree_path" ]]; then
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Approach $i:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

            (cd "$worktree_path" && git log --oneline -3)
            echo
        fi
    done

    echo "🎯 Review each implementation and choose the best one."
}

# Clean up parallel worktrees
claude_parallel_cleanup() {
    echo "🧹 Cleaning up worktrees..."

    git worktree list | grep "approach-" | while read -r path _; do
        echo "Removing: $path"
        git worktree remove "$path" --force
    done

    echo "✅ Cleanup complete."
}

# ========================================
# SAFETY CHECKS
# ========================================

# Verify changes before committing
claude_safety_check() {
    echo "🔒 Running safety checks..."

    local issues=0

    # Check 1: Uncommitted changes exist
    if git diff-index --quiet HEAD --; then
        echo "⚠️  No changes detected."
        ((issues++))
    else
        echo "✅ Changes detected."
    fi

    # Check 2: No merge conflicts
    if git ls-files -u | grep -q .; then
        echo "❌ Merge conflicts detected!"
        ((issues++))
    else
        echo "✅ No merge conflicts."
    fi

    # Check 3: Tests pass (if test command exists)
    if command -v npm &> /dev/null && [[ -f "package.json" ]]; then
        if grep -q "\"test\"" package.json; then
            echo "Running tests..."
            if npm test --silent; then
                echo "✅ Tests passed."
            else
                echo "❌ Tests failed!"
                ((issues++))
            fi
        fi
    fi

    # Check 4: TypeScript compiles (if applicable)
    if command -v tsc &> /dev/null && [[ -f "tsconfig.json" ]]; then
        echo "Checking TypeScript..."
        if tsc --noEmit; then
            echo "✅ TypeScript compiled successfully."
        else
            echo "❌ TypeScript errors found!"
            ((issues++))
        fi
    fi

    echo
    if [[ $issues -eq 0 ]]; then
        echo "🎉 All safety checks passed!"
        return 0
    else
        echo "⚠️  $issues issue(s) found. Review before committing."
        return 1
    fi
}

# ========================================
# ALIASES (Add to your .bashrc/.zshrc)
# ========================================

# Quick aliases for common workflows
alias ccp='claude_checkpoint'       # Create checkpoint
alias ccc='claude_commit'          # Commit AI changes
alias ccr='claude_rollback'        # Rollback to checkpoint
alias ccw='claude_workflow'        # Start full workflow
alias ccs='claude_safety_check'    # Run safety checks

# ========================================
# USAGE EXAMPLES
# ========================================

claude_examples() {
    cat << 'EOF'
Git Workflows for Claude Code - Usage Examples

1. Basic workflow:
   $ claude_workflow "Add user authentication"
   [Work with Claude...]
   $ claude_complete

2. Manual checkpoint and commit:
   $ claude_checkpoint "Implement new feature"
   [Claude makes changes...]
   $ git diff HEAD  # Review
   $ claude_commit "Implement user roles"

3. Rollback if needed:
   $ claude_rollback

4. Granular file-by-file commits:
   $ claude_commit_interactive

5. Parallel development (try 3 approaches):
   $ claude_parallel_setup "authentication" 3
   [Work in each worktree...]
   $ claude_parallel_compare "authentication"
   [Pick best approach]
   $ claude_parallel_cleanup

6. Safety checks before committing:
   $ claude_safety_check

7. Quick commit specific file:
   $ claude_commit_file src/auth.ts "Add JWT validation"

EOF
}

# Show examples if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    claude_examples
fi
