# Deploy Service Skill

## Description
Deploys a service to Coolify with health checks and rollback capability.

## Generated Skill
This skill was automatically generated from a workflow template by the Dark Factory Engine.

## Usage

```bash
./skill.sh \
  --service_name <value> # required \
  --git_repo <value> # required \
  --branch <value> # default: main \
  --environment <value> # default: staging
```

## Inputs

- `service_name` (**Required**): Name of the service to deploy
- `git_repo` (**Required**): Repository URL (e.g., https://github.com/user/repo)
- `branch` (Optional) (default: `main`): Git branch (default: main)
- `environment` (Optional) (default: `staging`): Target environment (default: staging)

## Outputs

- `deployment_url`: Live service URL
- `health_status`: Service health check result
- `deployment_id`: Coolify deployment identifier
- `rollback_command`: Command to rollback deployment

## Execution Steps

1. **Validate Repository**

2. **Prepare Deployment**

3. **Deploy Application**

4. **Verify Deployment**

5. **Post-Deployment**

