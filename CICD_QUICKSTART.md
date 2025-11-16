# 🚀 Quick Start Guide - GitHub Actions CI/CD

## ✅ What's Set Up

4 automated workflows have been created:

1. **Tests** - Run tests automatically
2. **Build** - Build package 
3. **Publish** - Publish to PyPI on release
4. **Docker** - Build Docker image

## 🎯 Steps to Complete

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflows"
git push origin main
```

→ **Tests and Build will run automatically!**

### 2. Setup PyPI Tokens (For Auto-publish)

#### Create PyPI Token:
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `github-actions`
4. Scope: "Entire account"
5. Copy token (format: `pypi-AgEI...`)

#### Create TestPyPI Token (Optional):
1. Go to https://test.pypi.org/manage/account/token/
2. Follow the same steps

#### Add Secrets to GitHub:
1. Go to repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add 2 secrets:
   - Name: `PYPI_API_TOKEN`, Value: `pypi-AgEI...`
   - Name: `TEST_PYPI_API_TOKEN`, Value: `pypi-AgEN...`

### 3. Create Release to Auto-Publish

```bash
# 1. Update version in pyproject.toml
# version = "0.1.1"

# 2. Commit & Push
git add pyproject.toml
git commit -m "Bump version to 0.1.1"
git push

# 3. Create release on GitHub
# Method 1: Via GitHub UI
# - Go to Releases → Draft a new release
# - Tag: v0.1.1
# - Title: Release 0.1.1
# - Click "Publish release"

# Method 2: Via CLI (if you have gh CLI)
gh release create v0.1.1 --title "Release 0.1.1" --notes "First release"
```

→ **Package will be automatically published to PyPI!**

## 📊 View Results

### View CI/CD Runs:
```bash
# On GitHub
# Go to repository → Actions tab

# Or use CLI
gh run list
gh run watch  # View realtime
```

### Badges in README:

Already added badges to README.md:
- ✅ Tests status
- ✅ Build status  
- ✅ PyPI version
- ✅ Python version
- ✅ License

## 🧪 Test Workflows Locally

### Test Python Code:
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
flake8 src/

# Format check
black --check src/ tests/
```

### Test Build:
```bash
python -m build
python -m twine check dist/*
```

### Test Docker:
```bash
docker build -t python-sandbox:test .
docker run -p 8000:8000 python-sandbox:test
```

## 🎬 Workflow Details

### When Pushing Code:
1. **Tests workflow** runs:
   - ✅ Test on Python 3.8-3.12
   - ✅ Test on Linux/Windows/macOS
   - ✅ Lint & format check
   - ✅ Coverage report

2. **Build workflow** runs:
   - ✅ Build package
   - ✅ Test installation

3. **Docker workflow** runs (if pushed to main):
   - ✅ Build Docker image
   - ✅ Push to GitHub Container Registry

### When Creating Release:
1. **Publish workflow** runs:
   - ✅ Build package
   - ✅ Publish to TestPyPI
   - ✅ Publish to PyPI

## 🔧 Troubleshooting

### Tests Fail?
```bash
# Check logs on GitHub Actions tab
# Or
gh run view <run-id> --log

# Test locally first
pytest -v
```

### Publish Fail?
```bash
# Check:
# 1. Are secrets added?
# 2. Is token still valid?
# 3. Is version incremented?
```

### Docker Build Fail?
```bash
# Test locally
docker build -t python-sandbox:test .

# Check logs
docker logs <container-id>
```

## 📝 Useful Commands

```bash
# View all workflow runs
gh run list

# Watch current run
gh run watch

# View specific run
gh run view <run-id>

# Rerun failed workflow
gh run rerun <run-id>

# Create release
gh release create v0.1.1 --generate-notes

# List releases
gh release list
```

## 🎯 Next Steps

1. ✅ Push code to GitHub
2. ✅ Check Actions tab
3. ✅ Add PyPI tokens if you want auto-publish
4. ✅ Create first release
5. ✅ Monitor build status via badges

## 📚 Detailed Documentation

- `.github/ACTIONS_SETUP.md` - Complete setup guide
- `.github/workflows/` - Workflow files
- Docs: https://docs.github.com/actions

---

**🎉 Done! CI/CD is ready!**
