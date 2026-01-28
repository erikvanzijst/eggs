---
name: beads-sprint
description: Work through all available beads issues following the beads workflow. Use this skill when the user says "Start the sprint", "Execute the beads workflow", or something similar. 
---

# Main workflow

With the beads workflow you pick up one beads issue at a time and work on it
until completion. When a ticket has been resolved, you pick up the next one and the
cycle repeats until all issues have been resolved.

**MANDATORY SEQUENCE OF STEPS**

1. Use `bd ready` to grab an issue to work on
2. **Update the selected beads** issue status to in-progress
3. **Work on the issue** without bothering the user with questions, running tests,
   linters, etc, to ensure quality and working code
4. **File issues for remaining work** - Create issues for anything that needs follow-up --
   while staying focused on the task at hand
5. `git commit` the code, listing all changes in the commit message
6. After committing, ALWAYS FOLLOW the "Landing the Plane" instructions below ->


# Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

When all done, pick up the next bead and complete the cycle until all beads have been
resolved.
