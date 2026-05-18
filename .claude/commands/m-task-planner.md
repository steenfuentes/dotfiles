# Dev Task Plan Workflow: Structure Implementation & Tests

**Target:** $ARGUMENTS (Default: requirement document(s) discovered in the project)

**Scope:** Analyze requirements and generate structured implementation plan with tests

## Execution Steps

1. **Requirements Analysis**
   - Parse target documents and extract functional requirements
   - Identify technical constraints and dependencies
   - Document ambiguities and unclear specifications

2. **Implementation Strategy Design**
   - Define architecture patterns and system design
   - Plan API structures and data models
   - Outline testing strategy and coverage approach

3. **Task Decomposition**
   - Break down features into actionable implementation tasks
   - Create corresponding test tasks for each feature
   - Define task types (feature, test, refactor, documentation)

4. **Dependency Mapping**
   - Identify task prerequisites and blocking relationships
   - Sequence tasks based on logical dependencies
   - Optimize for parallel development opportunities

5. **Plan Visualization**
   - Generate Mermaid diagram showing task flow
   - Illustrate critical path and milestone dependencies
   - Highlight testing integration points

6. **Generate Task Plan Report**
   - Compile findings into structured markdown format
   - Save to `docs/workspaces/task-plan-MM-dd-HH-mm-ss.md`

## Output Format

### English Report

#### `overview`
- High-level implementation strategy and architectural approach
- Testing methodology and coverage targets
- Key technical decisions and assumptions

#### `tasks`
Array of task objects with structure:
```json
{
  "id": "string",
  "description": "string",
  "type": "feature|test|refactor|docs",
  "status": "pending|in-progress|completed",
  "dependencies": ["task_id_1", "task_id_2"]
}
```

#### `diagram`
Mermaid diagram code illustrating:
- Task dependencies and flow
- Critical path identification
- Parallel execution opportunities

#### `clarifications`
Array of questions for requirement ambiguities:
- Unclear functional requirements
- Missing technical specifications
- Integration and compatibility concerns

## Final Output

Save the complete bilingual task plan to:
`docs/workspaces/task-plan-MM-dd-HH-mm-ss.md`

Output the saved file path to confirm completion.