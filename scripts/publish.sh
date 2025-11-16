#!/bin/bash
# Publish script for Python package

set -e

echo "🔧 Python Package Publisher"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: pyproject.toml not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Clean old builds
echo -e "${YELLOW}🧹 Cleaning old builds...${NC}"
rm -rf dist/ build/ *.egg-info src/*.egg-info

# Build package
echo -e "${YELLOW}🏗️  Building package...${NC}"
python -m build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful${NC}"
echo ""

# Check distribution
echo -e "${YELLOW}🔍 Checking distribution...${NC}"
python -m twine check dist/*

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Distribution check failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Distribution check passed${NC}"
echo ""

# Ask which repository to upload to
echo "📦 Where do you want to upload?"
echo "1) TestPyPI (test.pypi.org) - for testing"
echo "2) PyPI (pypi.org) - production"
echo "3) Both (TestPyPI first, then PyPI)"
echo "4) Skip upload (just build)"
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}🧪 Uploading to TestPyPI...${NC}"
        echo "Enter your TestPyPI credentials:"
        echo "Username: __token__"
        echo "Password: [Your TestPyPI API token]"
        echo ""
        python -m twine upload --repository testpypi dist/*
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Upload to TestPyPI successful!${NC}"
            echo ""
            echo "📥 Install with:"
            echo "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sandbox-executor"
        else
            echo -e "${RED}❌ Upload failed${NC}"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo -e "${YELLOW}🚀 Uploading to PyPI...${NC}"
        echo "Enter your PyPI credentials:"
        echo "Username: __token__"
        echo "Password: [Your PyPI API token]"
        echo ""
        python -m twine upload dist/*
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✅ Upload to PyPI successful!${NC}"
            echo ""
            echo "📥 Install with:"
            echo "pip install sandbox-executor"
        else
            echo -e "${RED}❌ Upload failed${NC}"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo -e "${YELLOW}🧪 Uploading to TestPyPI first...${NC}"
        python -m twine upload --repository testpypi dist/*
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ TestPyPI upload successful${NC}"
            echo ""
            read -p "Continue with PyPI upload? (y/N) " -n 1 -r
            echo
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${YELLOW}🚀 Uploading to PyPI...${NC}"
                python -m twine upload dist/*
                
                if [ $? -eq 0 ]; then
                    echo -e "${GREEN}✅ PyPI upload successful!${NC}"
                else
                    echo -e "${RED}❌ PyPI upload failed${NC}"
                    exit 1
                fi
            fi
        else
            echo -e "${RED}❌ TestPyPI upload failed${NC}"
            exit 1
        fi
        ;;
    
    4)
        echo -e "${GREEN}✅ Build complete. Skipping upload.${NC}"
        echo "Distribution files are in: dist/"
        ;;
    
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Done!${NC}"
