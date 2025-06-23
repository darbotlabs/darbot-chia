# Fork Sync Guide for darbot-chia

This document explains how to properly sync with the upstream Chia blockchain repository while preserving custom darbot changes.

## Important: What Happened Previously

During a previous sync attempt, custom darbot work was lost because the sync process overwrote the fork's history with the upstream repository's history. This included:

- GitHub Actions workflow modifications for fork compatibility
- Security fixes for clear-text logging
- Build system adaptations
- Dependency management changes

## Proper Sync Process

### 1. Set up upstream remote (one-time setup)

```bash
git remote add upstream https://github.com/Chia-Network/chia-blockchain.git
git remote -v  # Should show both origin (darbot-chia) and upstream (chia-blockchain)
```

### 2. Fetch latest changes from upstream

```bash
git fetch upstream
git fetch upstream --tags
```

### 3. Create a sync branch

```bash
git checkout main
git checkout -b sync-upstream-$(date +%Y%m%d)
```

### 4. Merge upstream changes

```bash
# Merge the latest upstream main into your sync branch
git merge upstream/main
```

### 5. Resolve conflicts carefully

If there are conflicts, resolve them carefully to preserve darbot customizations:

- **Keep** workflow modifications that make builds work in forks
- **Keep** security fixes and darbot-specific changes
- **Accept** new upstream features and bug fixes
- **Update** version numbers and dependencies as needed

### 6. Test the merged changes

```bash
# Test that the code still works
python -m py_compile chia/_tests/core/util/test_file_keyring_synchronization.py

# Check that GitHub Actions workflows have the fork restrictions
grep -n "github.repository == 'Chia-Network/chia-blockchain'" .github/workflows/build-*.yml
```

### 7. Merge back to main

```bash
git checkout main
git merge sync-upstream-$(date +%Y%m%d)
git push origin main
```

## Key Customizations to Preserve

### 1. GitHub Actions Workflow Restrictions

The following workflows should only run in the official Chia-Network repository:
- `build-linux-installer-deb.yml`
- `build-linux-installer-rpm.yml`
- `build-macos-installers.yml`
- `build-windows-installer.yml`

These include the condition: `if: github.repository == 'Chia-Network/chia-blockchain'`

### 2. Use of Standard GitHub Actions

Instead of proprietary Chia-Network actions, use standard GitHub actions:
- `actions/setup-python@v4` instead of `Chia-Network/actions/setup-python@main`
- Custom environment setup instead of `Chia-Network/actions/setjobenv@main`

### 3. Security Fixes

- Clear-text logging fixes in test files
- Any other security improvements

### 4. Build System Compatibility

- OS version adjustments for better compatibility
- Python path fixes for test execution

## What NOT to Do

1. **Never force push** over the main branch with upstream changes
2. **Never delete** the fork's git history
3. **Never ignore** merge conflicts - resolve them carefully
4. **Never use** `git reset --hard upstream/main` on the main branch

## Recovery from Lost Work

If work is lost again:

1. Check if the work exists in other branches: `git branch -a`
2. Look for commits with your changes: `git log --oneline --all --grep="your search term"`
3. Use `git diff` to compare branches and identify lost changes
4. Cherry-pick or manually restore the important changes

## Automation Considerations

Consider setting up:
1. Regular backup branches before major syncs
2. Automated checks for required customizations
3. CI tests that verify fork-specific functionality

## Contact

If you need help with syncing or lose work again, refer to this guide and the repository's issue tracker.