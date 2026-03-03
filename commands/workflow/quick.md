Fast path: execute a single self-contained task without the full pipeline.

Arguments: $ARGUMENTS  (concise task description)

Use this for simple, atomic tasks that do not require Epic decomposition or multi-story planning.

1. Write a TodoWrite checklist as your first action (3–5 steps maximum).
2. Identify affected files — read them before modifying.
3. Implement the change described in $ARGUMENTS with minimal footprint.
4. Verify the change produces the expected outcome.
5. Output a brief summary: files modified, what changed, verification result.

**NON-COMMIT POLICY: Leave all changes uncommitted.**
After completion, run `/workflow:review` to validate and commit.

**When NOT to use quick:**
- Tasks affecting more than 3 files
- Tasks with multiple dependent steps
- Tasks that require test suite creation
- Any architectural change

For those, use `/workflow:orchestrate` → `/workflow:plan` → `/workflow:execute`.
