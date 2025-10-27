# PyPI 배포 가이드 (pymodi-plus)

## 📋 목차
1. [사전 준비](#사전-준비)
2. [버전 업데이트](#버전-업데이트)
3. [빌드 및 테스트](#빌드-및-테스트)
4. [PyPI 배포](#pypi-배포)
5. [설치 확인](#설치-확인)
6. [문제 해결](#문제-해결)

---

## 🔧 사전 준비

### 1. PyPI 계정 생성

**PyPI (Production):**
- URL: https://pypi.org/account/register/
- 계정 생성 및 이메일 인증

**TestPyPI (테스트용):**
- URL: https://test.pypi.org/account/register/
- 테스트 배포용 계정

### 2. API Token 생성

#### PyPI Token 생성
1. PyPI 로그인: https://pypi.org
2. Account Settings → API tokens
3. "Add API token" 클릭
4. Token name: `pymodi-plus-upload`
5. Scope: `Entire account` 또는 `Project: pymodi-plus`
6. Token 복사 (한 번만 표시됨!)

#### TestPyPI Token 생성
1. TestPyPI 로그인: https://test.pypi.org
2. 동일한 절차로 token 생성

### 3. .pypirc 설정 (선택사항)

홈 디렉토리에 `.pypirc` 파일 생성:

```bash
# ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # 실제 token 입력

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...  # 실제 token 입력
```

**권한 설정:**
```bash
chmod 600 ~/.pypirc
```

### 4. 필요한 도구 설치

```bash
# 빌드 도구
pip install --upgrade build

# 업로드 도구
pip install --upgrade twine

# 또는 Makefile 사용
make install-dev
```

---

## 📝 버전 업데이트

### 1. 버전 번호 결정

**Semantic Versioning (MAJOR.MINOR.PATCH):**
- **MAJOR**: 호환되지 않는 API 변경 (예: 1.x → 2.x)
- **MINOR**: 하위 호환 기능 추가 (예: 0.3.x → 0.4.x)
- **PATCH**: 하위 호환 버그 수정 (예: 0.3.1 → 0.3.2)

**현재 버전:** `0.3.1`

**RGB 기능 추가 권장 버전:**
- `0.4.0` (새로운 기능 추가) ← **권장**
- `0.3.2` (버그 수정만 있다면)
- `1.0.0` (안정화 릴리스)

### 2. about.py 수정

```bash
# modi_plus/about.py 파일 수정
vi modi_plus/about.py
```

**변경 내용:**
```python
__title__ = "pymodi-plus"
__version__ = "0.4.0"  # ← 버전 업데이트
__author__ = "LUXROBO"
__email__ = "module.dev@luxrobo.com"
__description__ = "Python API for controlling modular electronics, MODI+."
__url__ = "https://github.com/LUXROBO/pymodi-plus"
__license__ = "MIT"
__summary__ = "Python API for controlling modular electronics, MODI+."
```

### 3. HISTORY.md 업데이트

```bash
# HISTORY.md 파일 수정
vi HISTORY.md
```

**추가 내용:**
```markdown
# Release History

## v0.4.0 (2025-10-27)

### New Features
- **Env Module RGB Support**: Added RGB color sensor support for Env module v2.x+
  - New properties: `red`, `green`, `blue`, `rgb`
  - Version-based automatic detection (v1.x: not supported, v2.x+: supported)
  - Multi-module support with mixed versions

### Improvements
- Improved Makefile with better test commands
- Added pytest configuration to resolve test conflicts
- Enhanced test coverage: 67 → 82 tests (all passing)
- Fixed packaging dependency issue

### Examples
- `env_rgb_example.py`: Multi-module RGB monitoring
- `env_rgb_mixed_versions.py`: Handle mixed v1.x/v2.x modules
- `env_rgb_color_detection.py`: RGB-based color detection

### Documentation
- Complete API documentation for RGB features
- Multi-module examples guide
- Comprehensive Makefile usage guide

### Bug Fixes
- Fixed pytest naming conflict with setup_module
- Fixed mock buffer size for RGB properties

## v0.3.1 (Previous release)
...
```

---

## 🔨 빌드 및 테스트

### 1. 테스트 실행

```bash
# 모든 테스트 실행
make test

# 또는 직접 실행
python3 -m pytest tests/ -v

# 예상 결과:
# ============================== 82 passed in 1.24s ==============================
```

### 2. 린트 검사

```bash
make lint

# 에러가 있다면 수정
make format  # 자동 포맷팅
```

### 3. 이전 빌드 정리

```bash
# 이전 빌드 파일 삭제
make clean

# 또는 수동으로
rm -rf build/ dist/ *.egg-info
```

### 4. 빌드 실행

```bash
# Makefile 사용 (권장)
make dist

# 또는 수동으로
python3 -m build

# 생성된 파일 확인
ls -lh dist/
# pymodi_plus-0.4.0-py3-none-any.whl
# pymodi-plus-0.4.0.tar.gz
```

### 5. 빌드 파일 검증

```bash
# twine으로 빌드 파일 검증
twine check dist/*

# 예상 결과:
# Checking dist/pymodi_plus-0.4.0-py3-none-any.whl: PASSED
# Checking dist/pymodi-plus-0.4.0.tar.gz: PASSED
```

---

## 🚀 PyPI 배포

### 단계 1: TestPyPI에 먼저 배포 (권장)

**테스트 배포로 문제 확인:**

```bash
# TestPyPI에 업로드
twine upload --repository testpypi dist/*

# Token 입력 요청 시:
# Username: __token__
# Password: pypi-AgENdGVzdC5weXBpLm9yZwI...  (TestPyPI token)
```

**TestPyPI에서 설치 테스트:**

```bash
# 새로운 가상환경에서 테스트
python3 -m venv test_env
source test_env/bin/activate

# TestPyPI에서 설치
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pymodi-plus

# 설치 확인
python3 -c "import modi_plus; print(modi_plus.__version__)"
# 출력: 0.4.0

# RGB 기능 확인
python3 -c "from modi_plus.module.input_module.env import Env; print('RGB offsets:', Env.PROPERTY_OFFSET_RED, Env.PROPERTY_OFFSET_GREEN, Env.PROPERTY_OFFSET_BLUE)"
# 출력: RGB offsets: 8 10 12

deactivate
rm -rf test_env
```

### 단계 2: 실제 PyPI에 배포

**프로덕션 배포:**

```bash
# PyPI에 업로드
twine upload dist/*

# 또는 Makefile 사용
make release

# Token 입력 요청 시:
# Username: __token__
# Password: pypi-AgEIcHlwaS5vcmcC...  (PyPI token)
```

**업로드 성공 메시지:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading pymodi_plus-0.4.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.0/50.0 kB • 00:01
Uploading pymodi-plus-0.4.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.0/45.0 kB • 00:01

View at:
https://pypi.org/project/pymodi-plus/0.4.0/
```

---

## ✅ 설치 확인

### 1. PyPI에서 설치

```bash
# 새로운 환경에서 설치
pip install --upgrade pymodi-plus

# 버전 확인
pip show pymodi-plus

# 출력:
# Name: pymodi-plus
# Version: 0.4.0
# Summary: Python API for controlling modular electronics, MODI+.
# Home-page: https://github.com/LUXROBO/pymodi-plus
# Author: LUXROBO
# Author-email: module.dev@luxrobo.com
# License: MIT
```

### 2. 기능 테스트

```python
# Python에서 테스트
import modi_plus
from modi_plus.module.input_module.env import Env

print(f"Version: {modi_plus.__version__}")
print(f"RGB Offsets: {Env.PROPERTY_OFFSET_RED}, {Env.PROPERTY_OFFSET_GREEN}, {Env.PROPERTY_OFFSET_BLUE}")

# 예상 출력:
# Version: 0.4.0
# RGB Offsets: 8, 10, 12
```

### 3. PyPI 페이지 확인

**URL:** https://pypi.org/project/pymodi-plus/

확인 사항:
- ✅ 버전 번호 (0.4.0)
- ✅ 설명 (README 내용)
- ✅ 다운로드 통계
- ✅ Dependencies

---

## 🏷️ GitHub Release 생성 (권장)

### 1. Git Tag 생성

```bash
# 현재 브랜치가 master인지 확인
git checkout master

# PR 머지 후
git pull origin master

# Tag 생성
git tag -a v0.4.0 -m "Release v0.4.0: Add Env module RGB support"

# Tag 푸시
git push origin v0.4.0
```

### 2. GitHub Release 생성

1. GitHub 저장소 방문: https://github.com/LUXROBO/pymodi-plus
2. "Releases" → "Create a new release"
3. Tag: `v0.4.0` 선택
4. Release title: `v0.4.0 - Env Module RGB Support`
5. Description:

```markdown
## 🎉 What's New

### RGB Support for Env Module
- Added RGB color sensor support for Env module v2.x+
- New properties: `red`, `green`, `blue`, `rgb`
- Automatic version detection (v1.x: not supported, v2.x+: supported)
- Multi-module support with mixed versions

### Examples
- Multi-module RGB monitoring
- Mixed version handling (v1.x + v2.x)
- RGB-based color detection

### Improvements
- Enhanced Makefile with test commands
- Comprehensive test coverage (82 tests)
- Complete documentation

## 📦 Installation

```bash
pip install --upgrade pymodi-plus==0.4.0
```

## 📚 Documentation
- [RGB Feature Guide](./ENV_RGB_FEATURE.md)
- [Examples Guide](./ENV_RGB_EXAMPLES.md)
- [Makefile Guide](./MAKEFILE_GUIDE.md)

## 🧪 Testing
All 82 tests passing ✅

## 🔗 Links
- [PyPI Package](https://pypi.org/project/pymodi-plus/0.4.0/)
- [Changelog](./HISTORY.md)
```

6. "Publish release" 클릭

---

## 🔄 빠른 배포 체크리스트

### 배포 전
- [ ] 모든 테스트 통과 (`make test`)
- [ ] 버전 번호 업데이트 (`modi_plus/about.py`)
- [ ] HISTORY.md 업데이트
- [ ] 린트 검사 통과 (`make lint`)
- [ ] PR 머지 완료

### 빌드
- [ ] 이전 빌드 정리 (`make clean`)
- [ ] 새 빌드 생성 (`make dist`)
- [ ] 빌드 파일 검증 (`twine check dist/*`)

### 테스트 배포
- [ ] TestPyPI 업로드
- [ ] TestPyPI에서 설치 테스트
- [ ] 기능 동작 확인

### 프로덕션 배포
- [ ] PyPI 업로드 (`make release`)
- [ ] PyPI에서 설치 테스트
- [ ] Git tag 생성 및 푸시
- [ ] GitHub Release 생성

### 배포 후
- [ ] PyPI 페이지 확인
- [ ] 설치 가이드 업데이트
- [ ] 팀원에게 공지

---

## ⚡ One-liner 배포 스크립트

### 전체 배포 (master 브랜치)

```bash
# 1. 테스트 → 빌드 → TestPyPI
make clean && make test && make dist && twine check dist/* && twine upload --repository testpypi dist/*

# 2. 테스트 확인 후 PyPI 배포
make release

# 3. Git tag 생성
git tag -a v0.4.0 -m "Release v0.4.0" && git push origin v0.4.0
```

### Makefile 명령어 사용

```bash
# 모든 배포 과정을 Makefile로
make clean
make test
make dist
make release  # PyPI 업로드
```

---

## 🐛 문제 해결

### 문제 1: "File already exists"

**원인:** 같은 버전이 이미 PyPI에 존재

**해결:**
```bash
# 버전 번호 증가
# modi_plus/about.py
__version__ = "0.4.1"  # 0.4.0 → 0.4.1

# 재빌드
make clean
make dist
```

**참고:** PyPI는 같은 버전을 덮어쓸 수 없습니다!

### 문제 2: "Invalid credentials"

**원인:** API token이 잘못되었거나 만료됨

**해결:**
```bash
# 1. PyPI에서 새 token 생성
# 2. .pypirc 업데이트
# 3. 또는 직접 입력
twine upload dist/* --username __token__ --password pypi-AgEI...
```

### 문제 3: "Long description failed"

**원인:** README.md 형식 오류

**해결:**
```bash
# README 검증
python3 -m readme_renderer README.md -o /dev/null

# 또는 build 검증
twine check dist/*
```

### 문제 4: 테스트 실패

**원인:** 코드 변경 후 테스트 미실행

**해결:**
```bash
# 전체 테스트
make test

# 실패한 테스트만
python3 -m pytest tests/module/input_module/test_env.py -v

# 테스트 통과 후 배포
```

---

## 📚 참고 자료

### 공식 문서
- PyPI 가이드: https://packaging.python.org/
- Twine 문서: https://twine.readthedocs.io/
- Setuptools: https://setuptools.pypa.io/

### 유용한 링크
- PyPI: https://pypi.org
- TestPyPI: https://test.pypi.org
- Semantic Versioning: https://semver.org/

### 내부 문서
- `MAKEFILE_GUIDE.md` - Makefile 사용법
- `ENV_RGB_FEATURE.md` - RGB 기능 문서
- `TESTS_README.md` - 테스트 가이드

---

## 📊 배포 체크리스트 요약

```bash
# 1. 버전 업데이트
vi modi_plus/about.py  # __version__ = "0.4.0"

# 2. 히스토리 업데이트
vi HISTORY.md  # v0.4.0 추가

# 3. 테스트
make test

# 4. 빌드
make clean && make dist

# 5. 검증
twine check dist/*

# 6. TestPyPI (선택)
twine upload --repository testpypi dist/*

# 7. PyPI 배포
make release

# 8. Git tag
git tag -a v0.4.0 -m "Release v0.4.0" && git push origin v0.4.0

# 9. GitHub Release 생성
# GitHub 웹에서 수동 생성

# 10. 확인
pip install --upgrade pymodi-plus
python3 -c "import modi_plus; print(modi_plus.__version__)"
```

---

완료! 🎉
