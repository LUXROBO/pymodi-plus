# 문서 구조 가이드

## 📁 현재 구조

pymodi-plus 프로젝트는 **2가지 문서 시스템**을 사용합니다:

### 1. Markdown 문서 (사용자 가이드)
```
docs/
├── README.md                    # 문서 메인 페이지
├── getting-started/             # 시작 가이드
├── features/                    # 기능 문서
├── development/                 # 개발 가이드
├── deployment/                  # 배포 가이드
├── github/                      # GitHub 설정
├── project/                     # 프로젝트 정보
└── troubleshooting/             # 문제 해결
```

### 2. Sphinx 문서 (API 레퍼런스)
```
docs/
├── conf.py                      # Sphinx 설정
├── Makefile                     # Sphinx 빌드
├── make.bat                     # Windows Sphinx 빌드
├── requirements.txt             # Sphinx 의존성
├── *.rst                        # reStructuredText 문서
├── _static/                     # 정적 파일
└── modi_plus.*.rst             # API 자동 생성 문서
```

## 🎯 권장 사항

### 옵션 1: Sphinx 문서 분리 (권장)
API 문서를 별도 폴더로 이동:
```
docs/
├── README.md
├── getting-started/
├── features/
├── ...
└── api/                         # Sphinx 문서 이동
    ├── conf.py
    ├── Makefile
    ├── *.rst
    └── _static/
```

**장점:**
- 사용자 문서와 API 문서 명확히 구분
- 각각 독립적으로 관리 가능
- 디렉토리 구조 깔끔

**작업:**
```bash
mkdir -p docs/api
mv docs/*.rst docs/api/
mv docs/conf.py docs/api/
mv docs/Makefile docs/api/
mv docs/make.bat docs/api/
mv docs/_static docs/api/
mv docs/requirements.txt docs/api/
# .readthedocs.yml 수정 필요
```

### 옵션 2: Sphinx 문서 제거
Read the Docs를 사용하지 않는다면:
```bash
rm docs/*.rst
rm docs/conf.py
rm docs/Makefile
rm docs/make.bat
rm -rf docs/_static
rm docs/requirements.txt
rm .readthedocs.yml
rm Dockerfile  # 도커도 사용 안 하면
```

**장점:**
- 단순한 구조
- Markdown만 관리
- 유지보수 용이

**단점:**
- API 자동 문서 생성 불가
- Read the Docs 호스팅 불가

### 옵션 3: 현재 상태 유지
두 시스템을 함께 사용:

**장점:**
- API 문서 자동 생성
- Read the Docs 호스팅 가능

**단점:**
- docs 폴더가 복잡
- 두 시스템 동시 관리 필요

## 📝 Root 폴더 파일 정리

### ✅ 필수 파일 (유지)
```
README.md              프로젝트 메인 문서
LICENSE                MIT 라이선스
setup.py               패키지 빌드 설정
setup.cfg              setuptools 설정
requirements.txt       프로덕션 의존성
requirements-dev.txt   개발 의존성
pytest.ini             테스트 설정
MANIFEST.in            패키지 포함 파일 지정
Makefile               빌드/테스트 명령어
.gitignore             Git 무시 파일
.editorconfig          에디터 설정
```

### ⚠️ 선택적 파일
```
.readthedocs.yml       Read the Docs 사용 시만 필요
Dockerfile             Docker 사용 시만 필요
```

### ✅ 삭제 완료
```
.coverage              임시 테스트 파일 (삭제됨)
```

## 🔒 보안 체크 결과

### ✅ 통과 항목
- API 키/토큰: 예시 값만 존재
- 비밀번호: 하드코딩 없음
- 개인정보: 공개 이메일만 존재
- .gitignore: 민감 파일 제외 설정됨

### 추가된 .gitignore 항목
```gitignore
# Security
.pypirc
credentials.json
secrets.json
*.pem
*.key

# Ruff cache
.ruff_cache/

# Editor temporary files
*.swp
*.swo
*.bak
*.tmp

# macOS/Windows 추가
```

## 📊 정리 결과

### 삭제된 문서 (9개)
```
❌ ENV_RGB_SUMMARY.md           (FEATURE에 포함)
❌ QUICK_DEPLOY.md              (중복)
❌ PYPI_DEPLOYMENT_GUIDE.md     (한글판 유지)
❌ CHANGELOG_MAKEFILE.md        (불필요)
❌ SUMMARY.md                   (불필요)
❌ CHANGELOG.md                 (HISTORY와 중복)
❌ GITHUB_README.md             (불필요)
❌ WORKFLOW_CHANGES.md          (일회성)
❌ TESTING_STRATEGY.md          (TESTS_README와 중복)
```

### 유지된 문서 (21개)
```
✅ 시작하기: 3개
✅ 기능: 2개
✅ 개발: 2개
✅ 배포: 1개
✅ GitHub: 4개
✅ 문제 해결: 4개
✅ 프로젝트: 4개
✅ README: 1개
```

## 🎯 권장 최종 구조

```
pymodi-plus/
├── README.md                    # 프로젝트 소개
├── LICENSE
├── setup.py
├── requirements.txt
├── Makefile
├── .gitignore                   # 보안 강화됨
├── docs/
│   ├── README.md               # 문서 인덱스
│   ├── getting-started/        # 사용자 시작 가이드
│   ├── features/               # 기능 문서
│   ├── development/            # 개발자 가이드
│   ├── deployment/             # 배포 가이드
│   ├── github/                 # GitHub 설정
│   ├── project/                # 프로젝트 정보
│   ├── troubleshooting/        # 문제 해결
│   └── api/                    # Sphinx API 문서 (선택)
├── modi_plus/                  # 소스 코드
└── tests/                      # 테스트 코드
```

## 📌 다음 단계

1. **Sphinx 문서 결정**
   - Read the Docs 사용 여부 확인
   - 옵션 1, 2, 3 중 선택

2. **문서 링크 업데이트**
   - README.md 링크 확인
   - docs/README.md 링크 확인

3. **커밋**
   ```bash
   git add .
   git commit -m "docs: Restructure documentation and enhance security
   
   - Organize docs into logical categories
   - Remove duplicate and unnecessary files
   - Enhance .gitignore for better security
   - Add comprehensive documentation index"
   ```

---

**작성일:** 2025-11-19  
**버전:** 1.0

