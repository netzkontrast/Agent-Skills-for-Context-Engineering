# Clean Code Checklist

Apply every item below during the task-reviewer's Step 2 validation. Each item must be explicitly confirmed as PASS or FAIL for the review to be considered complete.

## Functions and Methods

- [ ] No function exceeds 50 lines without documented justification in a comment
- [ ] Each function performs exactly one well-defined operation (Single Responsibility)
- [ ] Function names are imperative verbs describing what they do (`calculate_total`, not `data`)
- [ ] Functions have 0–3 parameters; objects/dataclasses used when more are needed
- [ ] No boolean trap parameters (prefer named enums or separate functions)
- [ ] No functions with side effects that are not clearly documented

## Naming

- [ ] Variable names describe their content, not their type (`user_count`, not `n` or `int_var`)
- [ ] No single-letter variables except in iteration contexts (`i`, `j` in loops are acceptable)
- [ ] No abbreviations that require domain knowledge to decode
- [ ] Constants are SCREAMING_SNAKE_CASE
- [ ] Boolean variables begin with `is_`, `has_`, `can_`, or `should_`

## Code Structure

- [ ] No commented-out code blocks (dead code must be deleted, not commented)
- [ ] No TODO comments in production paths (they belong in kanban_board.md)
- [ ] No magic numbers — all literals are named constants with explanatory names
- [ ] No deep nesting beyond 3 levels (extract into named functions)
- [ ] Early returns used to reduce nesting where applicable

## Error Handling

- [ ] Errors are handled only at system boundaries (user input, external APIs, file I/O)
- [ ] No empty catch/except blocks
- [ ] Error messages are descriptive and actionable (what went wrong + what to do)
- [ ] No silent failures — all error paths produce either an exception or a structured error object

## Security (OWASP Top 10)

- [ ] No hardcoded credentials, API keys, or passwords in source code
- [ ] All user input is validated before use (length, type, format, range)
- [ ] No SQL string concatenation — parameterized queries only
- [ ] No shell command construction from user input (command injection risk)
- [ ] No XSS vectors: output is escaped before rendering in HTML contexts
- [ ] No path traversal: file paths constructed from user input are sanitized
- [ ] Secrets loaded from environment variables or secure vaults only

## Testing

- [ ] New functions have corresponding test coverage
- [ ] Tests use descriptive names that explain the scenario (`test_returns_empty_list_when_no_users_found`)
- [ ] No tests that test implementation details rather than behavior
- [ ] Mock boundaries are at external system edges only (network, disk, time)

## Performance

- [ ] No N+1 query patterns in database access code
- [ ] No blocking I/O inside loops without explicit justification
- [ ] No unnecessary data copies in hot paths

## Dependencies

- [ ] No new dependencies added without corresponding entry in requirements/package.json
- [ ] No circular imports introduced
- [ ] No dependency on internal implementation details of external libraries

---

**Reviewer Note**: Every FAIL item must produce a specific Remediation Instruction in the rejection report. "Doesn't look right" is not a valid rejection reason — only checklist violations are.
