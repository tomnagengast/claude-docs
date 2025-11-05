# PR

Generate and new GitHub PR and immediately merge. Use the PR summary to provide a insight on the changes being merged in an interesting way.

## Instructions

1. Setup a new working branch
   - `git checkout -b sync-docs-$GITHUB_RUN_NUMBER`
   - `git push -u origin sync-docs-$GITHUB_RUN_NUMBER`
2. Understand the scope of changes to the docs
   - Review existing docs: `git ls-files docs/`
   - Review what has been a focus recently: `git log --stat --format=$'\n%h %an %ad %s' --date=short -15 docs/`
   - Inspect the new changes: `git diff docs/`
3. Commit the new changes
   - `git add -A`
   - `git commit -m 'docs: <Add a high-level summary of the changes>'`
4. Create a new PR
   - `gh pr create --title "Update Claude documentation - $GH_RUN_NUMBER" --body "<Read the Briefing section and follow it's instructions>" --label claude"`
5. Merge the PR
   - `gh pr merge $PR_NUMBER --merge --delete-branch`

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
