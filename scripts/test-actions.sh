#!/bin/bash

# Quick test script for GitHub Actions using act
# This script demonstrates common testing scenarios

set -e  # Exit on any error

echo "🚀 GitHub Actions Local Testing with act"
echo "======================================="

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ act is not installed. Please install it first:"
    echo "   brew install act  # macOS"
    echo "   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux"
    exit 1
fi

echo "✅ act is installed"

# Function to run with error handling
run_test() {
    local description="$1"
    local command="$2"
    
    echo ""
    echo "🔍 Testing: $description"
    echo "Command: $command"
    echo "---"
    
    if eval "$command"; then
        echo "✅ $description: PASSED"
    else
        echo "❌ $description: FAILED"
        return 1
    fi
}

# Test 1: List available workflows
run_test "List available workflows" \
    "act push --list"

# Test 2: Test banking-api changes (dry run first)
echo ""
echo "🔍 Testing: Banking API changes (dry run)"
echo "Command: act push -j test-banking-api --eventpath .github/act-events/banking-api-change.json --dry-run"
echo "---"
act push -j test-banking-api --eventpath .github/act-events/banking-api-change.json --dry-run

# Test 3: Test basics changes (dry run)
echo ""
echo "🔍 Testing: Basics module changes (dry run)"
echo "Command: act push -j test-basics --eventpath .github/act-events/basics-change.json --dry-run"
echo "---"
act push -j test-basics --eventpath .github/act-events/basics-change.json --dry-run

# Test 4: Security scan (dry run)
echo ""
echo "🔍 Testing: Security scan (dry run)"
echo "Command: act push -j security-scan --dry-run"
echo "---"
act push -j security-scan --dry-run

echo ""
echo "🎉 All dry-run tests completed!"
echo ""
echo "To run actual tests (not just dry-run), use:"
echo "  make test-banking-api  # Test banking API"
echo "  make test-basics       # Test basics module"
echo "  make test-security     # Test security scan"
echo "  make test-ci           # Test full CI pipeline"
echo ""
echo "For interactive debugging:"
echo "  act push -W .github/workflows/ci.yml --step --verbose"
echo ""
echo "Happy testing! 🚀"
