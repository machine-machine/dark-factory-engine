#!/bin/bash
# Dark Factory Engine Demo
# Demonstrates workflow compilation and execution

set -e

echo "🌟 Dark Factory Engine Demo"
echo "=================================="
echo

# Compile both workflow templates
echo "📄 Compiling workflow templates..."
echo

echo "1. Deploy Service workflow:"
./bin/compile workflow-templates/deploy-service.md
echo

echo "2. Run Tests workflow:"  
./bin/compile workflow-templates/run-tests.md
echo

# Show generated skills
echo "✅ Generated Skills:"
echo "   - output/deploy-service-skill/"
echo "   - output/run-tests-skill/"
echo

# Demo execution
echo "🚀 Demo Execution:"
echo

echo "Running Deploy Service workflow..."
cd output/deploy-service-skill
./skill.sh \
  --service_name "demo-api" \
  --git_repo "https://github.com/company/demo-api" \
  --branch "main" \
  --environment "staging"
cd ../..
echo

echo "Running Tests workflow..."
cd output/run-tests-skill  
./skill.sh \
  --project_path "/workspace/demo-project" \
  --test_type "unit" \
  --coverage_threshold "75"
cd ../..
echo

echo "✨ Demo Complete!"
echo
echo "🔧 Next Steps:"
echo "   1. Add Coolify integration for automatic deployment"
echo "   2. Implement meta-agent monitoring"
echo "   3. Add more workflow templates"
echo "   4. Build web UI for workflow management"
echo

echo "📊 Factory Status:"
echo "   - Workflows: 2"
echo "   - Generated Skills: 2"
echo "   - Successful Executions: 2"