Display the current workflow pipeline status.

Arguments: $ARGUMENTS  (optional: story ID for detail, or "all" for full board)

Show the current state of the `kanban_board.md`:

1. Read `kanban_board.md` from the repository root.
   If it does not exist, report "No active pipeline — run `/workflow:orchestrate` to start."

2. Display a formatted summary:

```
## Pipeline Status

### In Progress
[list stories with assignee]

### To Review
[list stories awaiting review]

### To Rework
[list rejected stories with rejection reason]

### Todo
[count of pending stories]

### Done
[count of completed stories this session]
```

3. If $ARGUMENTS is a specific story ID, show full story details including AC status and any
   rejection/rework history.

4. Highlight any `REWORK-LOOP` or `BLOCKED` markers that require human attention.

No file modifications. Read-only operation.
