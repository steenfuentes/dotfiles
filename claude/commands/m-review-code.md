# Code Review Workflow: Comprehensive Analysis & Report Generation

**Target:** $ARGUMENTS (Default: latest commits of current branch)

**Scope:** Analyze code changes, architecture patterns, and implementation quality

## Execution Steps

1. **Architecture & Pattern Analysis**
   - Review repository patterns, service layers, and migration strategies
   - Assess system design decisions and structural changes

2. **Security & Multi-tenant Validation**
   - Check authentication, authorization, and tenant isolation
   - Identify potential security vulnerabilities and access control issues

3. **Functional Completeness Verification**
   - Ensure all requirements are implemented with proper edge case handling
   - Validate input validation, error handling, and boundary conditions

4. **Code Quality Assessment**
   - Identify code smells, anti-patterns, and duplicated logic
   - Detect potential runtime issues: race conditions, memory leaks, null pointer exceptions

5. **Test Coverage Evaluation**
   - Assess unit and integration test coverage gaps
   - Review test quality and edge case coverage

6. **Third-party Library Opportunities**
   - Suggest robust external libraries for current implementations
   - Identify opportunities to reduce custom code complexity

7. **Generate Report**
   - Compile findings into structured markdown format
   - Save to `docs/workspaces/review-MM-dd-HH-mm-ss.md`

## Output Format

Present findings in the following sections:

#### `functionalCompleteness`
- Requirements implementation status
- Edge case handling assessment
- Missing functionality identification

#### `criticalBugs`
- Potential crashes, panics, or system failures
- Security vulnerabilities and data exposure risks
- Performance bottlenecks and resource leaks

#### `badSmells`
- Code anti-patterns and design issues
- Duplicated or overly complex logic
- Maintainability concerns

#### `thirdPartyOpportunities`
- External library suggestions for current implementations
- Benefits and integration considerations
- Risk assessment for library adoption

#### `testCoverage`
- Coverage gaps in unit and integration tests
- Missing test scenarios and edge cases
- Test quality and reliability issues

#### `actionables`
- Prioritized improvement recommendations
- Specific code changes and refactoring suggestions
- Implementation guidance and best practices

## Final Output

Save the complete bilingual report to:
`docs/workspaces/review-MM-dd-HH-mm-ss.md`

Output the saved file path to confirm completion.
