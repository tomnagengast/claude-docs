# PR

Generate and new GitHub PR and immediately merge. Use the PR summary to provide a insight on the changes being merged in an interesting way.

## Instructions

1. Read and execute the Context section to understand the scope of changes to the docs
2. Create a new PR
   - `gh pr create --title "Update Claude documentation - ${{ github.run_number }}" --body "<Read the Briefing section and follow it's instructions>" --label claude"`
3. Merge the PR
   - `gh pr merge $PR_NUMBER --merge --delete-branch`

## Context

- git add -A
- git ls-files docs/
- git log --stat --format="%h %an %ad %s" --date=short -15 docs/
- git diff docs/

## Briefing

You're a tech reporter writing a daily brief on documentation changes.

Write a conversational update highlighting what's new and interesting. Write like you're telling a colleague over coffee - natural, direct, informative.

Structure:

- **New News! 🎉** - What's the main story? (1-2 sentences)
- **What's New** - Key additions or changes worth knowing about
- **Watch Out** - Breaking changes, deprecations, or gotchas
- **Trends** - Where the action is: sections or files seeing the most edits recently
- **Deep Dive** - Links or sections to read if you want details

Tone: Casual but informative. Skip the fluff. If it's boring, say so. If something's a big deal, emphasize it.
