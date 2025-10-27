#!/bin/bash
# PyPI 배포 자동화 스크립트

set -e  # 에러 발생 시 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수 정의
print_step() {
    echo -e "\n${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 루트 디렉토리로 이동
cd "$(dirname "$0")/.."

# 배너 출력
echo "======================================================"
echo "  PyMODI Plus - PyPI Deployment Script"
echo "======================================================"

# 1. 버전 확인
print_step "Checking version..."
VERSION=$(python3 -c "exec(open('modi_plus/about.py').read()); print(__version__)")
echo "Current version: ${GREEN}${VERSION}${NC}"

read -p "Is this version correct? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Please update version in modi_plus/about.py"
    exit 1
fi
print_success "Version confirmed"

# 2. 브랜치 확인
print_step "Checking git branch..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: ${BRANCH}"

if [ "$BRANCH" != "master" ]; then
    print_warning "Not on master branch!"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
print_success "Branch check passed"

# 3. Git 상태 확인
print_step "Checking git status..."
if [[ -n $(git status -s) ]]; then
    print_error "Uncommitted changes detected!"
    git status -s
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
print_success "Git status clean"

# 4. 테스트 실행
print_step "Running tests..."
if make test; then
    print_success "All tests passed"
else
    print_error "Tests failed!"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 5. 린트 검사
print_step "Running lint..."
if make lint 2>/dev/null; then
    print_success "Lint check passed"
else
    print_warning "Lint check failed (continuing...)"
fi

# 6. 이전 빌드 정리
print_step "Cleaning previous builds..."
make clean
print_success "Build directory cleaned"

# 7. 빌드 생성
print_step "Building distribution packages..."
if make dist; then
    print_success "Build completed"
else
    print_error "Build failed!"
    exit 1
fi

# 8. 빌드 검증
print_step "Validating build..."
if twine check dist/*; then
    print_success "Build validation passed"
else
    print_error "Build validation failed!"
    exit 1
fi

# 9. 빌드 파일 목록
print_step "Build artifacts:"
ls -lh dist/

# 배포 타겟 선택
echo ""
echo "Select deployment target:"
echo "  1) TestPyPI (test.pypi.org) - Recommended for testing"
echo "  2) PyPI (pypi.org) - Production"
echo "  3) Both (TestPyPI first, then PyPI)"
echo "  4) Skip upload"
read -p "Choice (1-4): " -n 1 -r DEPLOY_TARGET
echo

case $DEPLOY_TARGET in
    1)
        # TestPyPI 배포
        print_step "Uploading to TestPyPI..."
        if twine upload --repository testpypi dist/*; then
            print_success "Upload to TestPyPI successful!"
            echo ""
            echo "Test installation:"
            echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pymodi-plus==${VERSION}"
            echo ""
            echo "View at: https://test.pypi.org/project/pymodi-plus/${VERSION}/"
        else
            print_error "Upload to TestPyPI failed!"
            exit 1
        fi
        ;;
    2)
        # PyPI 배포
        print_warning "You are about to upload to PRODUCTION PyPI!"
        read -p "Are you sure? (yes/no): " -r
        echo
        if [ "$REPLY" != "yes" ]; then
            print_error "Upload cancelled"
            exit 1
        fi

        print_step "Uploading to PyPI..."
        if twine upload dist/*; then
            print_success "Upload to PyPI successful!"
            echo ""
            echo "Installation:"
            echo "  pip install --upgrade pymodi-plus==${VERSION}"
            echo ""
            echo "View at: https://pypi.org/project/pymodi-plus/${VERSION}/"

            # Git tag 제안
            echo ""
            read -p "Create git tag v${VERSION}? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git tag -a "v${VERSION}" -m "Release v${VERSION}"
                git push origin "v${VERSION}"
                print_success "Git tag created and pushed"
            fi
        else
            print_error "Upload to PyPI failed!"
            exit 1
        fi
        ;;
    3)
        # 양쪽 배포
        print_step "Uploading to TestPyPI..."
        if twine upload --repository testpypi dist/*; then
            print_success "Upload to TestPyPI successful!"
        else
            print_error "Upload to TestPyPI failed!"
            exit 1
        fi

        echo ""
        print_warning "TestPyPI upload successful. Continue to PyPI?"
        read -p "Upload to production PyPI? (yes/no): " -r
        echo
        if [ "$REPLY" != "yes" ]; then
            print_error "PyPI upload cancelled"
            exit 0
        fi

        print_step "Uploading to PyPI..."
        if twine upload dist/*; then
            print_success "Upload to PyPI successful!"
            echo ""
            echo "View at:"
            echo "  TestPyPI: https://test.pypi.org/project/pymodi-plus/${VERSION}/"
            echo "  PyPI:     https://pypi.org/project/pymodi-plus/${VERSION}/"

            # Git tag 제안
            echo ""
            read -p "Create git tag v${VERSION}? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git tag -a "v${VERSION}" -m "Release v${VERSION}"
                git push origin "v${VERSION}"
                print_success "Git tag created and pushed"
            fi
        else
            print_error "Upload to PyPI failed!"
            exit 1
        fi
        ;;
    4)
        print_warning "Upload skipped"
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# 완료
echo ""
echo "======================================================"
print_success "Deployment completed successfully!"
echo "======================================================"
