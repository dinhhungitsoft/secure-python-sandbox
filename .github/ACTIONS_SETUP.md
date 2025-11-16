# GitHub Actions Setup Guide

## Overview

This repository includes 4 GitHub Actions workflows:

1. **Tests** (`tests.yml`) - Run on every push/PR
2. **Build** (`build.yml`) - Build package on every push
3. **Publish** (`publish.yml`) - Publish to PyPI on release
4. **Docker** (`docker.yml`) - Build and push Docker image

## Setup Instructions

### 1. Enable GitHub Actions

GitHub Actions are enabled by default. Check:
- Go to repository → Settings → Actions → General
- Ensure "Allow all actions and reusable workflows" is selected

### 2. Add Secrets for PyPI Publishing

#### For TestPyPI (Optional - for testing):

1. Generate token at https://test.pypi.org/manage/account/token/
2. Go to repository → Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `TEST_PYPI_API_TOKEN`
5. Value: Paste your TestPyPI token
6. Click "Add secret"

#### For PyPI (Production):

1. Generate token at https://pypi.org/manage/account/token/
2. Go to repository → Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

### 3. Configure Environments (Recommended)

For better security with PyPI publishing:

1. Go to repository → Settings → Environments
2. Click "New environment"
3. Name: `testpypi`
4. Add protection rules if desired
5. Repeat for environment: `pypi`

### 4. Enable Docker Registry (Optional)

For Docker image publishing to GitHub Container Registry:

1. Go to repository → Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click "Save"

## Workflows Explained

### 1. Tests Workflow (`tests.yml`)

**Triggers**: Push to main/develop, Pull Requests

**What it does**:
- ✅ Runs tests on Python 3.8-3.12
- ✅ Tests on Linux, Windows, macOS
- ✅ Lints with flake8
- ✅ Format check with black
- ✅ Type check with mypy
- ✅ Runs pytest with coverage
- ✅ Uploads coverage to Codecov
- ✅ Integration tests
- ✅ Docker build test

**Badge**: Add to README.md:
```markdown
[![Tests](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/tests.yml/badge.svg)](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/tests.yml)
```

### 2. Build Workflow (`build.yml`)

**Triggers**: Push to main/develop, Pull Requests

**What it does**:
- ✅ Builds Python package
- ✅ Validates distribution
- ✅ Tests installation on multiple OS
- ✅ Uploads artifacts

**Badge**:
```markdown
[![Build](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/build.yml/badge.svg)](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/build.yml)
```

### 3. Publish Workflow (`publish.yml`)

**Triggers**: When you create a GitHub Release

**What it does**:
1. ✅ Builds package
2. ✅ Publishes to TestPyPI first
3. ✅ If successful, publishes to PyPI

**How to trigger**:
```bash
# 1. Update version in pyproject.toml
# version = "0.1.1"

# 2. Commit and push
git add pyproject.toml
git commit -m "Bump version to 0.1.1"
git push

# 3. Create release on GitHub
# Go to: Releases → Draft a new release
# Tag: v0.1.1
# Title: Release 0.1.1
# Click "Publish release"

# Or via CLI:
gh release create v0.1.1 --title "Release 0.1.1" --notes "Bug fixes and improvements"
```

**Badge**:
```markdown
[![PyPI](https://img.shields.io/pypi/v/sandbox-executor.svg)](https://pypi.org/project/sandbox-executor/)
```

### 4. Docker Workflow (`docker.yml`)

**Triggers**: Push to main, Tags (v*), Pull Requests

**What it does**:
- ✅ Builds Docker image
- ✅ Pushes to GitHub Container Registry
- ✅ Tests the image
- ✅ Tags with version, SHA, branch

**Pull image**:
```bash
docker pull ghcr.io/dinhhungitsoft/secure-python-sandbox:main
```

**Badge**:
```markdown
[![Docker](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/docker.yml/badge.svg)](https://github.com/dinhhungitsoft/secure-python-sandbox/actions/workflows/docker.yml)
```

## Test Locally Before Pushing

### Test the build:
```bash
python -m build
python -m twine check dist/*
```

### Test the code:
```bash
pip install -e ".[dev]"
pytest
flake8 src/
black --check src/ tests/
```

### Test Docker:
```bash
docker build -t python-sandbox:test .
docker run -p 8000:8000 python-sandbox:test
```

## Monitoring

### View Workflow Runs:
- Go to repository → Actions tab
- Click on any workflow to see runs
- Click on a run to see logs

### Get Email Notifications:
- Go to GitHub → Settings → Notifications
- Check "Actions" under Email notifications

## Troubleshooting

### Tests fail but work locally?
- Check Python version compatibility
- Check if all dependencies are in `pyproject.toml`
- Look at the logs in Actions tab

### Publishing fails?
- Verify secrets are set correctly
- Check token permissions on PyPI
- Ensure version in `pyproject.toml` is incremented

### Docker build fails?
- Check Dockerfile syntax
- Ensure all files exist
- Test locally first

## Cost

- ✅ GitHub Actions is FREE for public repositories
- ✅ 2,000 minutes/month for private repositories (free tier)

## Advanced Configuration

### Skip CI for commits:
```bash
git commit -m "docs: update readme [skip ci]"
```

### Run only specific workflows:
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'tests/**'
```

### Matrix testing (already configured):
```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    os: [ubuntu-latest, windows-latest, macos-latest]
```

## Quick Reference

```bash
# Create a release (triggers publish)
gh release create v0.1.1

# View workflow runs
gh run list

# Watch a workflow
gh run watch

# View logs
gh run view <run-id> --log
```

## Next Steps

1. ✅ Push workflows to GitHub
2. ✅ Add secrets (PYPI_API_TOKEN, TEST_PYPI_API_TOKEN)
3. ✅ Test by creating a PR
4. ✅ Add badges to README.md
5. ✅ Create first release to test publishing
