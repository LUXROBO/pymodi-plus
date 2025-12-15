# PyPI 배포 완전 가이드 (pymodi-plus)

## 📋 목차
1. [빠른 시작](#빠른-시작)
2. [자동 배포 (GitHub Actions)](#자동-배포-github-actions)
3. [수동 배포 (로컬)](#수동-배포-로컬)
4. [PyPI 계정 설정](#pypi-계정-설정)
5. [문제 해결](#문제-해결)

---

## 🚀 빠른 시작

### 현재 상황
- ✅ 버전: `0.3.1` → `0.4.0`
- ✅ RGB 기능 추가 완료
- ✅ 94개 테스트 모두 통과
- ✅ GitHub Actions 설정 완료

### 3가지 배포 옵션

| 방법 | 난이도 | 시간 | 추천 |
|------|--------|------|------|
| **자동 배포 (GitHub Actions)** | 쉬움 | 5분 | ⭐⭐⭐ |
| **수동 배포 (Makefile)** | 보통 | 10분 | ⭐⭐ |
| **수동 배포 (직접)** | 어려움 | 20분 | ⭐ |

---

## 🤖 자동 배포 (GitHub Actions)

**가장 권장하는 방법입니다!** Git tag만 푸시하면 자동으로 PyPI에 배포됩니다.

### 필수 조건

1. **GitHub Secrets 설정 (한 번만 필요)**

```
GitHub Repository → Settings → Secrets and variables → Actions
```

**추가할 Secrets:**
- `PYPI_USERNAME`: `__token__`
- `PYPI_PASSWORD`: `pypi-AgEI...` (PyPI API token)

### 배포 단계

#### **1단계: 버전 커밋**

```bash
# 현재 디렉토리에서
git add modi_plus/about.py HISTORY.md
git commit -m "chore: Bump version to 0.4.0"
git push origin feature/env-rgb-support
```

#### **2단계: PR 머지**

```bash
# GitHub에서 PR 생성 및 머지
# feature/env-rgb-support → develop → master
```

**또는 로컬에서 직접 머지:**
```bash
# develop 브랜치로 머지
git checkout develop
git merge feature/env-rgb-support
git push origin develop

# master 브랜치로 머지 (릴리스 준비 완료 시)
git checkout master
git merge develop
git push origin master
```

#### **3단계: Git Tag 생성 및 푸시 (자동 배포 트리거)**

```bash
# master 브랜치에서
git checkout master
git pull origin master

# Tag 생성
git tag -a v0.4.0 -m "Release v0.4.0: Add Env module RGB support

Features:
- RGB color sensor support (red, green, blue, white, black)
- Color classification (color_class: 0-5)
- Brightness measurement (0-100%)
- Version-based automatic detection (v2.x+)
- 31 new tests added (94 tests total)

Improvements:
- Python 3.8-3.13 support
- GitHub Actions enhancements
- Platform-specific compatibility fixes"

# Tag 푸시 (이 명령어가 자동 배포를 시작합니다!)
git push origin v0.4.0
```

#### **4단계: GitHub Actions 확인**

```
GitHub Repository → Actions → "PyPi Deploy" workflow
```

**자동으로 실행되는 작업:**
1. ✅ 코드 체크아웃
2. ✅ Python 3.8 설치
3. ✅ 의존성 설치
4. ✅ 빌드 생성 (`sdist`, `bdist_wheel`)
5. ✅ PyPI 업로드

**성공 시:** ✅ 녹색 체크마크  
**실패 시:** ❌ 빨간 X (로그 확인)

#### **5단계: 설치 확인**

```bash
# 새로운 환경에서 테스트
python3 -m venv test_env
source test_env/bin/activate

# PyPI에서 설치
pip install --upgrade pymodi-plus

# 버전 확인
python3 -c "import modi_plus; print(modi_plus.__version__)"
# 출력: 0.4.0

# RGB 기능 확인
python3 -c "from modi_plus.module.input_module.env import Env; print('RGB support added!')"

deactivate
rm -rf test_env
```

#### **6단계: GitHub Release 생성 (선택 사항)**

```
GitHub Repository → Releases → "Create a new release"
```

**내용:**
- Tag: `v0.4.0`
- Title: `v0.4.0 - Env Module RGB Support`
- Description: (HISTORY.md 내용 복사)

---

## 🛠️ 수동 배포 (로컬)

GitHub Actions를 사용할 수 없는 경우 로컬에서 수동으로 배포할 수 있습니다.

### 방법 A: Makefile 사용 (권장)

```bash
# 1. 테스트
make test

# 2. 린트 검사
make lint

# 3. 이전 빌드 정리
make clean

# 4. 새 빌드 생성
make dist

# 5. 빌드 검증
twine check dist/*

# 6. PyPI 배포
make release
# Username: __token__
# Password: pypi-AgEI... (PyPI API token 입력)
```

### 방법 B: 직접 명령어 사용

```bash
# 1. 필요한 도구 설치
pip install --upgrade build twine

# 2. 테스트
python3 -m pytest tests/ -v

# 3. 이전 빌드 정리
rm -rf build/ dist/ *.egg-info

# 4. 빌드 생성
python3 -m build

# 5. 빌드 검증
twine check dist/*

# 6. PyPI 업로드
twine upload dist/*
# Username: __token__
# Password: pypi-AgEI... (PyPI API token 입력)
```

---

## 🔑 PyPI 계정 설정

### 1. PyPI 계정 생성

**프로덕션 (실제 배포):**
- URL: https://pypi.org/account/register/
- 이메일 인증 필요

**테스트 (연습용):**
- URL: https://test.pypi.org/account/register/
- 테스트 배포 전용

### 2. API Token 생성

#### PyPI Token 생성 (프로덕션)

1. https://pypi.org 로그인
2. `Account Settings` → `API tokens`
3. `Add API token` 클릭
4. Token name: `pymodi-plus-deploy`
5. Scope:
   - `Entire account` (모든 프로젝트)
   - 또는 `Project: pymodi-plus` (특정 프로젝트만)
6. `Add token` 클릭
7. **Token 복사** (한 번만 표시됩니다!)
   ```
   pypi-AgEIcHlwaS5vcmcC...
   ```

#### TestPyPI Token 생성 (테스트)

1. https://test.pypi.org 로그인
2. 동일한 절차로 token 생성

### 3. GitHub Secrets 설정

```
GitHub Repository → Settings → Secrets and variables → Actions
```

**New repository secret 추가:**

**프로덕션:**
- Name: `PYPI_USERNAME`
- Value: `__token__`

- Name: `PYPI_PASSWORD`
- Value: `pypi-AgEIcHlwaS5vcmcC...` (복사한 token)

**테스트 (선택 사항):**
- Name: `TEST_PYPI_USERNAME`
- Value: `__token__`

- Name: `TEST_PYPI_PASSWORD`
- Value: `pypi-AgENdGVzdC5weXBpLm9yZwI...` (TestPyPI token)

### 4. 로컬 .pypirc 설정 (선택 사항)

수동 배포 시 매번 token을 입력하지 않으려면:

```bash
# ~/.pypirc 파일 생성
nano ~/.pypirc
```

**내용:**
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...
```

**권한 설정:**
```bash
chmod 600 ~/.pypirc
```

---

## 🧪 TestPyPI에서 먼저 테스트 (권장)

실제 PyPI에 배포하기 전에 TestPyPI에서 먼저 테스트하는 것이 좋습니다.

### TestPyPI 배포

```bash
# 빌드 생성
make clean && make dist

# TestPyPI에 업로드
twine upload --repository testpypi dist/*

# 또는 URL 직접 지정
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### TestPyPI에서 설치 테스트

```bash
# 테스트 환경 생성
python3 -m venv test_env
source test_env/bin/activate

# TestPyPI에서 설치
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            pymodi-plus

# 버전 확인
python3 -c "import modi_plus; print(modi_plus.__version__)"
# 출력: 0.4.0

# 테스트
python3 -c "
from modi_plus.module.input_module.env import Env
print('RGB Offsets:', Env.PROPERTY_OFFSET_RED, Env.PROPERTY_OFFSET_GREEN, Env.PROPERTY_OFFSET_BLUE)
print('✅ TestPyPI installation successful!')
"

deactivate
rm -rf test_env
```

---

## ✅ 배포 체크리스트

### 배포 전
- [ ] 모든 테스트 통과 확인 (`make test`)
- [ ] Linter 통과 확인 (`make lint`)
- [ ] 버전 번호 업데이트 (`modi_plus/about.py`)
- [ ] HISTORY.md 업데이트
- [ ] README.md 업데이트 (필요시)
- [ ] 코드 리뷰 완료
- [ ] PR 머지 완료

### 배포 중
- [ ] Git tag 생성 및 푸시
- [ ] GitHub Actions 성공 확인
- [ ] 또는 수동 배포 완료

### 배포 후
- [ ] PyPI 페이지 확인 (https://pypi.org/project/pymodi-plus/)
- [ ] 설치 테스트 (`pip install --upgrade pymodi-plus`)
- [ ] 버전 확인 (`modi_plus.__version__`)
- [ ] 기능 테스트 (RGB 프로퍼티 확인)
- [ ] GitHub Release 생성
- [ ] 문서 업데이트
- [ ] 팀원/사용자에게 공지

---

## 🐛 문제 해결

### 문제 1: "File already exists"

**증상:**
```
HTTPError: 400 Client Error: File already exists
```

**원인:** 같은 버전이 이미 PyPI에 존재

**해결:**
```bash
# 버전 번호 증가
# modi_plus/about.py
__version__ = "0.4.1"  # 0.4.0 → 0.4.1

# 재빌드
make clean && make dist && make release
```

⚠️ **중요:** PyPI는 같은 버전을 절대 덮어쓸 수 없습니다!

### 문제 2: "Invalid credentials"

**증상:**
```
HTTPError: 403 Client Error: Invalid or non-existent authentication information
```

**원인:** API token이 잘못되었거나 만료됨

**해결:**
1. PyPI에서 새 token 생성
2. GitHub Secrets 업데이트 (자동 배포)
3. 또는 .pypirc 업데이트 (수동 배포)
4. 또는 직접 입력:
   ```bash
   twine upload dist/* --username __token__ --password pypi-AgEI...
   ```

### 문제 3: "Long description failed"

**증상:**
```
The description failed to render for 'text/markdown'
```

**원인:** README.md 마크다운 형식 오류

**해결:**
```bash
# README 검증
pip install readme-renderer
python3 -m readme_renderer README.md -o /dev/null

# 빌드 검증
twine check dist/*
```

### 문제 4: GitHub Actions 실패

**증상:** Actions에서 배포 실패

**원인:**
- Secrets가 설정되지 않음
- Token이 만료됨
- 빌드 오류

**해결:**
1. Actions 로그 확인
2. Secrets 재설정
3. 로컬에서 빌드 테스트:
   ```bash
   make clean && make dist
   twine check dist/*
   ```

### 문제 5: 테스트 실패

**증상:**
```
FAILED tests/module/input_module/test_env.py
```

**해결:**
```bash
# 전체 테스트
make test

# 특정 테스트만
python3 -m pytest tests/module/input_module/test_env.py -v

# 테스트 통과 확인 후 재배포
```

### 문제 6: Tag가 이미 존재

**증상:**
```
fatal: tag 'v0.4.0' already exists
```

**해결:**
```bash
# Tag 삭제 (로컬)
git tag -d v0.4.0

# Tag 삭제 (원격)
git push origin :refs/tags/v0.4.0

# 새로 Tag 생성
git tag -a v0.4.0 -m "Release v0.4.0"
git push origin v0.4.0
```

---

## 📊 배포 후 확인 사항

### 1. PyPI 페이지 확인

**URL:** https://pypi.org/project/pymodi-plus/

**확인 항목:**
- ✅ 버전 번호: `0.4.0`
- ✅ 설명: README 내용이 제대로 표시됨
- ✅ 의존성: requirements.txt 내용
- ✅ 다운로드 파일:
  - `pymodi_plus-0.4.0-py3-none-any.whl`
  - `pymodi-plus-0.4.0.tar.gz`
- ✅ 메타데이터: 작성자, 라이선스 등

### 2. 설치 테스트

```bash
# 새 환경에서
pip install --upgrade pymodi-plus==0.4.0

# 버전 확인
pip show pymodi-plus

# 출력:
# Name: pymodi-plus
# Version: 0.4.0
# Summary: Python API for controlling modular electronics, MODI+.
# Home-page: https://github.com/LUXROBO/pymodi-plus
# Author: LUXROBO
# License: MIT
```

### 3. 기능 테스트

```python
# test_installation.py
import modi_plus
from modi_plus.module.input_module.env import Env

print(f"✅ Version: {modi_plus.__version__}")
print(f"✅ RGB Property Offsets: {Env.PROPERTY_OFFSET_RED}, {Env.PROPERTY_OFFSET_GREEN}, {Env.PROPERTY_OFFSET_BLUE}")
print(f"✅ New Properties: white={Env.PROPERTY_OFFSET_WHITE}, black={Env.PROPERTY_OFFSET_BLACK}")
print(f"✅ Color Class Offset: {Env.PROPERTY_OFFSET_COLOR_CLASS}")
print(f"✅ Brightness Offset: {Env.PROPERTY_OFFSET_BRIGHTNESS}")
print("✅ All new RGB features available!")
```

### 4. 다운로드 통계 확인

**PyPI Stats:** https://pepy.tech/project/pymodi-plus

---

## 📚 참고 자료

### 공식 문서
- PyPI Packaging: https://packaging.python.org/
- Twine: https://twine.readthedocs.io/
- Semantic Versioning: https://semver.org/

### 프로젝트 문서
- `PYPI_DEPLOYMENT_GUIDE.md` - 영문 배포 가이드
- `MAKEFILE_GUIDE.md` - Makefile 사용법
- `ENV_RGB_FEATURE.md` - RGB 기능 문서
- `.github/workflows/deploy.yml` - 자동 배포 워크플로우

### 유용한 링크
- PyPI: https://pypi.org
- TestPyPI: https://test.pypi.org
- GitHub Actions Docs: https://docs.github.com/actions

---

## 🎉 배포 완료!

축하합니다! pymodi-plus 0.4.0이 성공적으로 배포되었습니다.

**다음 단계:**
1. 사용자에게 업데이트 공지
2. 문서 사이트 업데이트 (있는 경우)
3. Release Notes 공유
4. 피드백 수집

**설치 방법 (사용자용):**
```bash
pip install --upgrade pymodi-plus
```

**새 기능 사용 예:**
```python
import modi_plus

# MODI+ 연결
bundle = modi_plus.MODIPlus()

# Env 모듈 (v2.x+) RGB 사용
env = bundle.envs[0]
print(f"Red: {env.red}%")
print(f"Green: {env.green}%")
print(f"Blue: {env.blue}%")
print(f"RGB: {env.rgb}")
```

---

**작성일:** 2025-11-19  
**버전:** 0.4.0  
**작성자:** pymodi-plus Team

