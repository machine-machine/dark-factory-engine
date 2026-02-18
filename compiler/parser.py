#!/usr/bin/env python3
"""
Dark Factory Workflow Parser
Parses Markdown workflow definitions into structured data
"""

import re
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class WorkflowInput:
    name: str
    required: bool
    default: Optional[str] = None
    description: str = ""


@dataclass
class WorkflowStep:
    title: str
    description: str
    actions: List[str] = field(default_factory=list)


@dataclass 
class WorkflowOutput:
    name: str
    description: str


@dataclass
class WorkflowGuardrail:
    type: str  # timeout, approval, rate_limit, etc.
    value: str
    description: str


@dataclass
class Workflow:
    name: str
    description: str
    inputs: List[WorkflowInput] = field(default_factory=list)
    steps: List[WorkflowStep] = field(default_factory=list)
    outputs: List[WorkflowOutput] = field(default_factory=list)
    guardrails: List[WorkflowGuardrail] = field(default_factory=list)
    error_handling: List[str] = field(default_factory=list)


class WorkflowParser:
    """Parses Markdown workflow definitions"""
    
    def __init__(self):
        self.current_section = None
        self.current_step = None
        
    def parse_file(self, filepath: str) -> Workflow:
        """Parse a workflow markdown file"""
        with open(filepath, 'r') as f:
            content = f.read()
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Workflow:
        """Parse workflow content from markdown text"""
        lines = content.split('\n')
        workflow = Workflow(name="", description="")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Main title (# Workflow: Name)
            if line.startswith('# Workflow:'):
                workflow.name = line.replace('# Workflow:', '').strip()
                
            # Section headers (## Section)
            elif line.startswith('## '):
                self.current_section = line.replace('## ', '').lower()
                self.current_step = None
                
            # Step headers (### N. Step Name)
            elif line.startswith('### ') and self.current_section == 'steps':
                step_title = re.sub(r'^### \d+\.\s*', '', line)
                self.current_step = WorkflowStep(title=step_title, description="")
                workflow.steps.append(self.current_step)
                
            # Content based on current section
            else:
                self._parse_line_by_section(line, workflow)
                
        return workflow
    
    def _parse_line_by_section(self, line: str, workflow: Workflow):
        """Parse line content based on current section"""
        
        if self.current_section == 'description':
            if line and not line.startswith('#'):
                workflow.description += line + ' '
                
        elif self.current_section == 'inputs':
            if line.startswith('- `'):
                input_match = re.match(r'- `([^`]+)`\s*(\([^)]+\))?\s*:\s*(.*)', line)
                if input_match:
                    name = input_match.group(1)
                    required_str = input_match.group(2) or ""
                    description = input_match.group(3) or ""
                    
                    required = 'required' in required_str.lower()
                    default = None
                    
                    # Extract default value
                    default_match = re.search(r'default:\s*([^)]+)', description)
                    if default_match:
                        default = default_match.group(1).strip()
                        
                    workflow.inputs.append(WorkflowInput(
                        name=name,
                        required=required, 
                        default=default,
                        description=description
                    ))
                    
        elif self.current_section == 'steps' and self.current_step:
            if line.startswith('- '):
                self.current_step.actions.append(line[2:])
            elif line and not line.startswith('#'):
                if self.current_step.description:
                    self.current_step.description += ' '
                self.current_step.description += line
                
        elif self.current_section == 'outputs':
            if line.startswith('- `'):
                output_match = re.match(r'- `([^`]+)`:\s*(.*)', line)
                if output_match:
                    workflow.outputs.append(WorkflowOutput(
                        name=output_match.group(1),
                        description=output_match.group(2)
                    ))
                    
        elif self.current_section == 'guardrails':
            if line.startswith('- **'):
                guardrail_match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
                if guardrail_match:
                    guardrail_type = guardrail_match.group(1).lower()
                    description = guardrail_match.group(2)
                    workflow.guardrails.append(WorkflowGuardrail(
                        type=guardrail_type,
                        value="",  # Extract from description if needed
                        description=description
                    ))
                    
        elif self.current_section == 'error handling':
            if line.startswith('- **'):
                workflow.error_handling.append(line[2:])


def main():
    """Test the parser"""
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py <workflow.md>")
        sys.exit(1)
        
    parser = WorkflowParser()
    try:
        workflow = parser.parse_file(sys.argv[1])
        
        print(f"Workflow: {workflow.name}")
        print(f"Description: {workflow.description.strip()}")
        print(f"\nInputs ({len(workflow.inputs)}):")
        for inp in workflow.inputs:
            req = "required" if inp.required else "optional"
            default = f" (default: {inp.default})" if inp.default else ""
            print(f"  - {inp.name} ({req}){default}: {inp.description}")
            
        print(f"\nSteps ({len(workflow.steps)}):")
        for i, step in enumerate(workflow.steps, 1):
            print(f"  {i}. {step.title}")
            if step.description:
                print(f"     {step.description.strip()}")
            for action in step.actions:
                print(f"     - {action}")
                
        print(f"\nOutputs ({len(workflow.outputs)}):")
        for output in workflow.outputs:
            print(f"  - {output.name}: {output.description}")
            
        print(f"\nGuardrails ({len(workflow.guardrails)}):")
        for guardrail in workflow.guardrails:
            print(f"  - {guardrail.type}: {guardrail.description}")
            
    except Exception as e:
        print(f"Error parsing workflow: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()