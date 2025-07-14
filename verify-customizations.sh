#!/bin/bash
# Verification script to check that darbot customizations are preserved

echo "🔍 Checking darbot-chia customizations..."

# Check for fork restrictions in workflows
echo "📋 Checking GitHub Actions workflow restrictions..."
fork_restricted_workflows=$(grep -l "github.repository == 'Chia-Network/chia-blockchain'" .github/workflows/*.yml | wc -l)
if [ "$fork_restricted_workflows" -ge 16 ]; then
    echo "✅ Fork restrictions present in $fork_restricted_workflows workflows (comprehensive audit completed)"
else
    echo "❌ Insufficient fork restrictions - expected 16+, found: $fork_restricted_workflows"
fi

# Check for security fix
echo "🔒 Checking security fix for clear-text logging..."
if grep -q "passphrase mismatch detected" chia/_tests/core/util/test_file_keyring_synchronization.py; then
    echo "✅ Security fix for clear-text logging is present"
else
    echo "❌ Security fix for clear-text logging is missing"
fi

# Check for standard GitHub actions usage
echo "🛠️  Checking for standard GitHub actions..."
standard_actions=$(grep -c "actions/setup-python@v4" .github/workflows/test.yml)
if [ "$standard_actions" -ge 2 ]; then
    echo "✅ Using standard GitHub actions (found: $standard_actions instances)"
else
    echo "❌ Missing standard GitHub actions usage"
fi

# Check for upstream remote
echo "🔗 Checking upstream remote..."
if git remote | grep -q "upstream"; then
    echo "✅ Upstream remote is configured"
    git remote get-url upstream
else
    echo "❌ Upstream remote not configured"
    echo "   Run: git remote add upstream https://github.com/Chia-Network/chia-blockchain.git"
fi

# Check for sync guide
echo "📚 Checking for sync guide..."
if [ -f "FORK_SYNC_GUIDE.md" ]; then
    echo "✅ Fork sync guide is present"
else
    echo "❌ Fork sync guide is missing"
fi

echo ""
echo "🎯 Summary:"
echo "   This script verifies that key darbot customizations are preserved."
echo "   Run this after each upstream sync to ensure nothing was lost."
echo ""