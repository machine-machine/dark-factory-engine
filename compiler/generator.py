#!/usr/bin/env python3
"""
Dark Factory Skill Generator
Converts parsed workflows into OpenClaw skills
"""

import os
import json
from pathlib import Path
from typing import Dict, Any
from .parser import Workflow, WorkflowInput, WorkflowStep


class SkillGenerator:
    """Generates OpenClaw skills from parsed workflows"""
    
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        self.templates_dir = Path(templates_dir)
    
    def generate_skill(self, workflow: Workflow, output_dir: str) -> str:
        """Generate a complete OpenClaw skill from workflow"""
        skill_dir = Path(output_dir) / f"{self._normalize_name(workflow.name)}-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate skill files
        self._generate_skill_file(workflow, skill_dir)
        self._generate_config_file(workflow, skill_dir)
        self._generate_readme(workflow, skill_dir)
        self._generate_executor_script(workflow, skill_dir)
        
        return str(skill_dir)
    
    def _normalize_name(self, name: str) -> str:
        """Normalize workflow name for filesystem"""
        return name.lower().replace(' ', '-').replace(':', '').strip()
    
    def _generate_skill_file(self, workflow: Workflow, skill_dir: Path):
        """Generate the main skill.sh file"""
        script_content = self._build_skill_script(workflow)
        
        skill_file = skill_dir / "skill.sh"
        with open(skill_file, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(skill_file, 0o755)
    
    def _build_skill_script(self, workflow: Workflow) -> str:
        """Build the main skill execution script"""
        script_parts = [
            "#!/bin/bash",
            f'# Generated skill for workflow: {workflow.name}',
            f'# Description: {workflow.description.strip()}',
            "",
            "set -euo pipefail",
            "",
            "# Skill metadata",
            f'SKILL_NAME="{self._normalize_name(workflow.name)}"',
            f'SKILL_VERSION="1.0.0"',
            f'WORKFLOW_NAME="{workflow.name}"',
            "",
            "# Source common functions",
            'SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"',
            'source "$SCRIPT_DIR/functions.sh" 2>/dev/null || true',
            "",
            "# Logging setup",
            'LOG_FILE="${SCRIPT_DIR}/execution.log"',
            'exec 1> >(tee -a "$LOG_FILE")',
            'exec 2> >(tee -a "$LOG_FILE" >&2)',
            "",
            "# Start execution",
            'log_info "Starting workflow: $WORKFLOW_NAME"',
            'log_info "Timestamp: $(date -Iseconds)"',
            "",
        ]
        
        # Add input validation
        script_parts.extend(self._generate_input_validation(workflow))
        
        # Add step execution
        for i, step in enumerate(workflow.steps, 1):
            script_parts.extend(self._generate_step_execution(step, i))
        
        # Add completion
        script_parts.extend([
            "",
            "# Workflow completed successfully", 
            'log_info "Workflow completed successfully"',
            'log_info "Outputs stored in: $SCRIPT_DIR/outputs.json"',
            "",
            "exit 0"
        ])
        
        return "\n".join(script_parts)
    
    def _generate_input_validation(self, workflow: Workflow) -> list:
        """Generate input validation code"""
        validation_lines = [
            "# Input validation",
            "declare -A INPUTS",
            "declare -A OUTPUTS",
            "",
            "# Parse command line arguments",
            "while [[ $# -gt 0 ]]; do",
            "  case $1 in"
        ]
        
        for inp in workflow.inputs:
            validation_lines.extend([
                f"    --{inp.name})",
                f'      INPUTS[{inp.name}]="$2"',
                "      shift 2",
                "      ;;"
            ])
        
        validation_lines.extend([
            "    *)",
            '      echo "Unknown argument: $1" >&2',
            "      exit 1",
            "      ;;",
            "  esac",
            "done",
            ""
        ])
        
        # Validate required inputs
        for inp in workflow.inputs:
            if inp.required:
                validation_lines.extend([
                    f'if [[ -z "${{INPUTS[{inp.name}]:-}}" ]]; then',
                    f'  log_error "Required input missing: {inp.name}"',
                    '  exit 1',
                    'fi',
                    ""
                ])
            elif inp.default:
                validation_lines.extend([
                    f'INPUTS[{inp.name}]="${{INPUTS[{inp.name}]:-{inp.default}}}"',
                    ""
                ])
        
        return validation_lines
    
    def _generate_step_execution(self, step: WorkflowStep, step_num: int) -> list:
        """Generate execution code for a workflow step"""
        lines = [
            f"# Step {step_num}: {step.title}",
            f'log_info "Executing step {step_num}: {step.title}"',
            "",
            f"execute_step_{step_num}() {{",
        ]
        
        # Add step description as comment if available
        if step.description:
            lines.append(f'  # {step.description.strip()}')
            lines.append("")
        
        # Convert actions to bash commands
        for action in step.actions:
            # This is a simplified conversion - in real implementation, 
            # we'd have more sophisticated action parsing
            bash_command = self._action_to_bash(action)
            lines.append(f"  {bash_command}")
        
        lines.extend([
            f'  log_info "Completed step {step_num}: {step.title}"',
            "}",
            "",
            f"execute_step_{step_num}",
            ""
        ])
        
        return lines
    
    def _action_to_bash(self, action: str) -> str:
        """Convert workflow action to bash command (simplified)"""
        action = action.strip()
        
        # Simple mappings for common actions
        if action.lower().startswith('clone'):
            return f'log_info "Cloning repository..."  # TODO: Implement {action}'
        elif action.lower().startswith('checkout'):
            return f'log_info "Checking out branch..."  # TODO: Implement {action}'  
        elif action.lower().startswith('verify'):
            return f'log_info "Verifying..."  # TODO: Implement {action}'
        elif action.lower().startswith('generate'):
            return f'log_info "Generating..."  # TODO: Implement {action}'
        elif action.lower().startswith('create'):
            return f'log_info "Creating..."  # TODO: Implement {action}'
        elif action.lower().startswith('trigger'):
            return f'log_info "Triggering..."  # TODO: Implement {action}'
        elif action.lower().startswith('wait'):
            return f'log_info "Waiting..."  # TODO: Implement {action}'
        else:
            return f'log_info "Executing: {action}"  # TODO: Implement specific action'
    
    def _generate_config_file(self, workflow: Workflow, skill_dir: Path):
        """Generate skill configuration file"""
        config = {
            "name": workflow.name,
            "description": workflow.description.strip(),
            "version": "1.0.0",
            "generated_by": "dark-factory-engine",
            "inputs": [
                {
                    "name": inp.name,
                    "required": inp.required,
                    "default": inp.default,
                    "description": inp.description
                }
                for inp in workflow.inputs
            ],
            "outputs": [
                {
                    "name": out.name,
                    "description": out.description
                }
                for out in workflow.outputs
            ],
            "guardrails": [
                {
                    "type": guard.type,
                    "description": guard.description
                }
                for guard in workflow.guardrails
            ]
        }
        
        config_file = skill_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _generate_readme(self, workflow: Workflow, skill_dir: Path):
        """Generate README for the skill"""
        readme_content = f"""# {workflow.name} Skill

## Description
{workflow.description.strip()}

## Generated Skill
This skill was automatically generated from a workflow template by the Dark Factory Engine.

## Usage

```bash
./skill.sh \\
"""
        
        for inp in workflow.inputs:
            req_marker = " # required" if inp.required else ""
            default_marker = f" # default: {inp.default}" if inp.default else ""
            readme_content += f"  --{inp.name} <value>{req_marker}{default_marker} \\\n"
        
        readme_content = readme_content.rstrip(" \\\n") + "\n```\n"
        
        if workflow.inputs:
            readme_content += "\n## Inputs\n\n"
            for inp in workflow.inputs:
                req_str = "**Required**" if inp.required else "Optional"
                default_str = f" (default: `{inp.default}`)" if inp.default else ""
                readme_content += f"- `{inp.name}` ({req_str}){default_str}: {inp.description}\n"
        
        if workflow.outputs:
            readme_content += "\n## Outputs\n\n"
            for out in workflow.outputs:
                readme_content += f"- `{out.name}`: {out.description}\n"
        
        if workflow.steps:
            readme_content += "\n## Execution Steps\n\n"
            for i, step in enumerate(workflow.steps, 1):
                readme_content += f"{i}. **{step.title}**\n"
                if step.description:
                    readme_content += f"   {step.description.strip()}\n"
                readme_content += "\n"
        
        readme_file = skill_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
    
    def _generate_executor_script(self, workflow: Workflow, skill_dir: Path):
        """Generate helper functions script"""
        functions_content = '''#!/bin/bash
# Helper functions for workflow execution

log_info() {
    echo "$(date -Iseconds) [INFO] $*"
}

log_error() {
    echo "$(date -Iseconds) [ERROR] $*" >&2
}

log_debug() {
    echo "$(date -Iseconds) [DEBUG] $*" >&2
}

# Store output value
set_output() {
    local key="$1"
    local value="$2"
    OUTPUTS[$key]="$value"
    
    # Also store in JSON file
    local outputs_file="$SCRIPT_DIR/outputs.json"
    if [[ ! -f "$outputs_file" ]]; then
        echo "{}" > "$outputs_file"
    fi
    
    # Update JSON file (requires jq)
    if command -v jq &> /dev/null; then
        jq --arg key "$key" --arg value "$value" '.[$key] = $value' "$outputs_file" > "${outputs_file}.tmp"
        mv "${outputs_file}.tmp" "$outputs_file"
    else
        log_debug "jq not available, outputs stored in memory only"
    fi
}

# Get input value
get_input() {
    local key="$1"
    echo "${INPUTS[$key]:-}"
}
'''
        
        functions_file = skill_dir / "functions.sh"
        with open(functions_file, 'w') as f:
            f.write(functions_content)
        
        os.chmod(functions_file, 0o755)


def main():
    """Test the generator"""
    import sys
    from .parser import WorkflowParser
    
    if len(sys.argv) != 3:
        print("Usage: python generator.py <workflow.md> <output_dir>")
        sys.exit(1)
    
    workflow_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    try:
        # Parse workflow
        parser = WorkflowParser()
        workflow = parser.parse_file(workflow_file)
        
        # Generate skill
        generator = SkillGenerator()
        skill_dir = generator.generate_skill(workflow, output_dir)
        
        print(f"Generated skill at: {skill_dir}")
        print("Files created:")
        for file_path in Path(skill_dir).rglob("*"):
            if file_path.is_file():
                print(f"  - {file_path.name}")
                
    except Exception as e:
        print(f"Error generating skill: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()