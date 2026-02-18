# Dark Factory Engine
*Workflow-Driven Agentic Software Factory*

## Overview

The Dark Factory Engine converts human-readable workflow definitions (Markdown) into executable OpenClaw skills that can be deployed as Coolify apps.

**Core Concept**: `workflow.md` → `skill/` → Coolify deployment → Automated execution

## Architecture

```
┌─────────────────┐
│ Workflow.md     │ (Human-readable process definition)
│ (Templates)     │
└────────┬────────┘
         │ Compile
         ↓
┌─────────────────┐
│ OpenClaw Skill  │ (Executable code + metadata)
│ (Generated)     │
└────────┬────────┘
         │ Deploy
         ↓
┌─────────────────┐
│ Coolify App     │ (Running automation)
│ (Auto-scaled)   │
└─────────────────┘
```

## Quick Start

```bash
# Compile a workflow template
./bin/compile workflow-templates/deploy-service.md

# Deploy to Coolify (auto-generates app)
./bin/deploy output/deploy-service-skill/

# Monitor execution
./bin/monitor deploy-service
```

## Workflow Template Format

Workflows are written in Markdown with structured sections:

```markdown
# Workflow: Deploy Service

## Description
Deploys a service to Coolify with health checks and rollback capability.

## Inputs
- `service_name`: Name of the service to deploy
- `git_repo`: Repository URL
- `branch`: Git branch (default: main)

## Steps
1. **Clone Repository**
   - Checkout specified branch
   - Validate dockerfile exists

2. **Create Coolify App**
   - Generate app configuration
   - Set environment variables
   - Configure health checks

3. **Deploy & Verify**
   - Trigger deployment
   - Wait for healthy status
   - Run smoke tests

## Outputs
- `deployment_url`: Live service URL
- `health_status`: Service health check result
- `rollback_command`: Command to rollback if needed

## Guardrails
- Max deployment time: 10 minutes
- Auto-rollback on failure
- Requires manual approval for production
```

## Directory Structure

```
dark-factory-engine/
├── README.md                    # This file
├── bin/                        # Executable scripts
│   ├── compile                 # Workflow → Skill compiler
│   ├── deploy                  # Skill → Coolify deployer  
│   └── monitor                 # Execution monitor
├── workflow-templates/         # Sample workflows
│   ├── deploy-service.md
│   ├── run-tests.md
│   ├── backup-data.md
│   └── security-scan.md
├── compiler/                   # Compiler implementation
│   ├── parser.py              # Markdown parser
│   ├── generator.py           # Skill generator
│   └── templates/             # Code templates
├── examples/                   # Example generated skills
└── docs/                      # Documentation
```

## Features

### Phase 1 (Current)
- [x] Workflow template parsing
- [x] Basic skill generation
- [ ] Coolify integration
- [ ] Simple execution engine

### Phase 2 (Planned)
- [ ] Meta-agent monitoring
- [ ] Multi-workflow orchestration
- [ ] Visual workflow builder
- [ ] Compliance evidence generation

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test Compilation**
   ```bash
   python compiler/compile.py workflow-templates/deploy-service.md
   ```

3. **Deploy First Workflow**
   ```bash
   # TBD - Coolify integration
   ```

## Integration with MachineMachine

This engine integrates with our existing infrastructure:
- **OpenClaw**: Generated skills run as OpenClaw agents
- **Coolify**: Auto-deployment and scaling
- **Memory System**: Execution logs → Qdrant vector memory
- **Agent Spawning**: Multi-workflow parallel execution

---

*Part of the MachineMachine Dark Software Factory initiative*