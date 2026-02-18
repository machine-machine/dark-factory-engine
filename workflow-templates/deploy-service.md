# Workflow: Deploy Service

## Description
Deploys a service to Coolify with health checks and rollback capability.

## Inputs
- `service_name` (required): Name of the service to deploy
- `git_repo` (required): Repository URL (e.g., https://github.com/user/repo)  
- `branch` (optional): Git branch (default: main)
- `environment` (optional): Target environment (default: staging)

## Steps

### 1. Validate Repository
- Clone the specified repository
- Checkout the target branch  
- Verify Dockerfile or docker-compose.yml exists
- Check for required environment variables

### 2. Prepare Deployment
- Generate Coolify application configuration
- Set environment variables from template
- Configure health check endpoints
- Set up logging and monitoring

### 3. Deploy Application
- Create or update Coolify application
- Trigger deployment from git repository
- Monitor deployment progress
- Wait for healthy status (max 10 minutes)

### 4. Verify Deployment
- Run health check against deployed service
- Execute basic smoke tests
- Verify service responds correctly
- Log deployment success metrics

### 5. Post-Deployment
- Update service registry
- Send notification to relevant channels
- Generate deployment report
- Create rollback script if needed

## Outputs
- `deployment_url`: Live service URL
- `health_status`: Service health check result  
- `deployment_id`: Coolify deployment identifier
- `rollback_command`: Command to rollback deployment

## Guardrails
- **Timeout**: Maximum deployment time of 10 minutes
- **Auto-rollback**: Automatic rollback on health check failure
- **Approval**: Production deployments require manual approval
- **Rate limiting**: Maximum 5 deployments per hour per service
- **Verification**: All deployments must pass health checks

## Error Handling
- **Repository errors**: Invalid repo, missing Dockerfile, branch not found
- **Deployment errors**: Build failures, resource constraints, timeout
- **Health check errors**: Service not responding, incorrect responses
- **Rollback errors**: Log and alert for manual intervention

## Example Usage

```yaml
inputs:
  service_name: "user-api"
  git_repo: "https://github.com/company/user-api"
  branch: "feature/new-auth"
  environment: "staging"
```

Expected outputs:
```yaml
outputs:
  deployment_url: "https://user-api-staging.machinemachine.ai"
  health_status: "healthy"  
  deployment_id: "clx1234567890"
  rollback_command: "coolify app:rollback clx1234567890 --to-previous"
```