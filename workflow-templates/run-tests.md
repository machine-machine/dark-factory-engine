# Workflow: Run Tests

## Description
Executes comprehensive test suite with coverage reporting and result notifications.

## Inputs
- `project_path` (required): Path to the project directory
- `test_type` (optional): Type of tests to run (default: all)
- `coverage_threshold` (optional): Minimum coverage percentage (default: 80)
- `notify_channels` (optional): Comma-separated list of notification channels

## Steps

### 1. Setup Test Environment
- Validate project structure and test directory exists
- Install test dependencies from requirements-test.txt
- Set up test database if needed
- Configure test environment variables

### 2. Execute Unit Tests
- Run unit tests with pytest
- Generate coverage report
- Capture test output and timing
- Save test artifacts

### 3. Execute Integration Tests
- Start required services (database, redis, etc.)
- Run integration test suite
- Monitor resource usage during tests
- Clean up test resources

### 4. Code Quality Checks
- Run linting with flake8/black
- Execute type checking with mypy
- Security scan with bandit
- Generate quality metrics report

### 5. Report Results
- Aggregate all test results
- Generate coverage report (HTML + JSON)
- Send notifications to specified channels
- Archive test artifacts

## Outputs
- `test_results`: Overall test success/failure status
- `coverage_percentage`: Code coverage percentage achieved
- `test_duration`: Total test execution time in seconds
- `artifacts_path`: Path to generated test artifacts and reports

## Guardrails
- **Timeout**: Maximum test execution time of 30 minutes
- **Coverage gate**: Fail if coverage below threshold
- **Resource limits**: Maximum 2GB memory usage during tests
- **Parallel execution**: Maximum 4 concurrent test processes
- **Retry policy**: Retry flaky tests up to 2 times

## Error Handling
- **Setup errors**: Missing dependencies, invalid project structure
- **Test failures**: Individual test failures, timeout exceeded
- **Coverage errors**: Coverage calculation failures, threshold not met
- **Notification errors**: Channel unavailable, credential issues

## Example Usage

```yaml
inputs:
  project_path: "/workspace/projects/user-api"
  test_type: "unit,integration"
  coverage_threshold: "85"
  notify_channels: "slack,email"
```

Expected outputs:
```yaml
outputs:
  test_results: "success"
  coverage_percentage: "87.3"
  test_duration: "142"
  artifacts_path: "/workspace/test-artifacts/user-api-20260218"
```