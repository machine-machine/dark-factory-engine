# Run Tests Skill

## Description
Executes comprehensive test suite with coverage reporting and result notifications.

## Generated Skill
This skill was automatically generated from a workflow template by the Dark Factory Engine.

## Usage

```bash
./skill.sh \
  --project_path <value> # required \
  --test_type <value> # default: all \
  --coverage_threshold <value> # default: 80 \
  --notify_channels <value>
```

## Inputs

- `project_path` (**Required**): Path to the project directory
- `test_type` (Optional) (default: `all`): Type of tests to run (default: all)
- `coverage_threshold` (Optional) (default: `80`): Minimum coverage percentage (default: 80)
- `notify_channels` (Optional): Comma-separated list of notification channels

## Outputs

- `test_results`: Overall test success/failure status
- `coverage_percentage`: Code coverage percentage achieved
- `test_duration`: Total test execution time in seconds
- `artifacts_path`: Path to generated test artifacts and reports

## Execution Steps

1. **Setup Test Environment**

2. **Execute Unit Tests**

3. **Execute Integration Tests**

4. **Code Quality Checks**

5. **Report Results**

