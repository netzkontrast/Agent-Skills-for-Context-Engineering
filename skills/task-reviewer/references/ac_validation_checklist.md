# Acceptance Criteria Validation Checklist

This checklist governs how the task-reviewer validates each acceptance criterion (AC) in a story. Apply every item for each AC item to ensure complete verification.

## Pre-Validation Setup

- [ ] All acceptance criteria from the story definition are listed (none omitted)
- [ ] Each criterion is binary — has a clear pass/fail state
- [ ] The validation method for each criterion is identified before executing

## Validation Methods by Criterion Type

### Behavioral Criteria (e.g., "The API returns 200 when given valid input")
```bash
# Run the relevant test or invoke the behavior
pytest tests/test_api.py::test_valid_input -v
# or
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/endpoint
```
- [ ] Test or invocation executed and output captured
- [ ] Expected output matches actual output
- [ ] Edge cases mentioned in the criterion are also tested

### Structural Criteria (e.g., "The function is in the utils/ module")
```bash
# Use Glob or Grep to verify structure
glob("utils/*.py")
grep("def function_name", "utils/")
```
- [ ] File location verified with tool output
- [ ] No duplicate implementations elsewhere in codebase

### Content Criteria (e.g., "SKILL.md contains the allowed-tools field")
```bash
# Read the file and verify presence
grep("allowed-tools", "path/to/SKILL.md")
```
- [ ] Field/content presence confirmed
- [ ] Content format matches specification (not just presence)

### Negative Criteria (e.g., "No CLAUDE_PLUGIN_ROOT variables remain")
```bash
grep("CLAUDE_PLUGIN_ROOT", output_dir, recursive=True)
# Must return zero results
```
- [ ] Absence confirmed with an explicit search
- [ ] Searched in all relevant file types, not just the obvious ones

### Performance Criteria (e.g., "Response time under 200ms")
- [ ] Measurement methodology documented
- [ ] Measurement taken under representative load conditions
- [ ] P95 (not just average) meets the criterion

## Acceptance Criterion Status Record

For each AC, record:
```
AC-01: {criterion text}
  Method: {validation method used}
  Evidence: {output, file path, or command result}
  Status: ✅ PASS | ❌ FAIL
  Failure Detail: {if FAIL: specific mismatch between expected and actual}
```

## Aggregate Validation Decision

The story passes validation ONLY if:
- [ ] Every AC item is marked `✅ PASS`
- [ ] No AC items are skipped or marked as "N/A" without explicit justification
- [ ] The justification for any "N/A" item is approved by the orchestrator

If any AC is `❌ FAIL`:
- The story goes to `To Rework`
- All failed criteria and their specific failure details are included in the rejection report
- A remediation instruction is provided for each failed criterion

## Mandatory Pre-Commit Verification

Before any git commit, confirm:
- [ ] `git diff --name-only HEAD` shows only the expected files
- [ ] No unrelated files are staged
- [ ] `git status` shows no untracked secret files (.env, *.key, *.pem)
- [ ] The commit message includes the story ID and a clear imperative description

---

**Note**: Acceptance criteria validate user-facing behavior and system properties. The clean_code_checklist.md validates implementation quality. Both must pass before a story reaches `Done`.
