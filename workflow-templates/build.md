# Workflow: Build

## Description
Implement a software feature, script, or component. Writes code to files,
runs tests, and reports what was built with a summary of changes.

## Inputs
- `task`: Description of what to build
- `target_dir`: Directory to write output (default: /tmp/build-{timestamp}/)
- `language`: Programming language hint (default: auto-detect from task)
- `test`: Whether to run tests after build — true | false (default: true)

## Steps
1. **Understand requirements**
   - Parse the task description
   - Identify language, framework, dependencies
   - Check workspace for related existing code

2. **Plan implementation**
   - List files to create/modify
   - Identify external dependencies (pip, npm, etc.)
   - Flag any blockers or ambiguities

3. **Implement**
   - Write code files
   - Install dependencies if needed
   - Follow existing code style in the workspace

4. **Verify**
   - Run linter / syntax check
   - Run tests if test=true
   - Confirm output files exist

5. **Report**
   - List files created/modified
   - Summarise what was built
   - Note any caveats or follow-up needed

## Outputs
- `files_created`: List of created/modified file paths
- `summary`: What was built and how to use it
- `test_result`: Pass | Fail | Skipped

## Guardrails
- Do not modify files outside target_dir without explicit confirmation
- Max 500 lines of code per run
- If tests fail: report failure, do not auto-fix without approval
- No secrets or credentials in generated code
