Activate the `task-rework` skill (L3 Defect Repair Agent).

Arguments: $ARGUMENTS  (story ID of the rejected story)

You are the L3 Task Rework agent. A story has been rejected by the reviewer. Fix it:

1. Write a TodoWrite checklist as your first action.
2. Load the rejection report from `kanban_board.md` story comments (required before starting).
3. Load the original story acceptance criteria.
4. Read every file mentioned in the rejection report.
5. Apply targeted fixes in priority order: security → AC failures → clean code → regressions.
6. Run self-verification against all previously failed criteria.
7. Write a rework log documenting every change made.
8. Update `kanban_board.md`: set story status to `To Review`.
9. Signal story-executor that rework is complete.

**NON-COMMIT POLICY: You must never run `git commit`, `git add`, or `git push`.**

If this is the 3rd+ iteration, add `REWORK-LOOP` marker and escalate to human review.

For the full operational specification, load: `skills/task-rework/SKILL.md`
