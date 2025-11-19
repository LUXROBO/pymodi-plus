# pymodi-plus 문서

MODI+ 모듈형 전자제품 제어를 위한 Python API 완전 가이드

## 📚 문서 구조

### 🚀 [시작하기](./getting-started/)
- [빠른 시작 가이드](./getting-started/QUICKSTART.md) - 빠르게 시작하기
- [기여 가이드](./getting-started/CONTRIBUTING.md) - 프로젝트 기여 방법
- [행동 강령](./getting-started/CODE_OF_CONDUCT.md) - 커뮤니티 가이드라인

### ✨ [기능](./features/)
- [Env 모듈 RGB 지원](./features/ENV_RGB_FEATURE.md) - RGB 센서 상세 문서
- [RGB 예제](./features/ENV_RGB_EXAMPLES.md) - RGB 기능 코드 예제

### 🛠️ [개발](./development/)
- [Makefile 가이드](./development/MAKEFILE_GUIDE.md) - Makefile 사용법
- [테스트 가이드](./development/TESTS_README.md) - 테스트 실행 및 작성 방법

### 📦 [배포](./deployment/)
- [배포 가이드 (한글)](./deployment/DEPLOY_GUIDE_KOREAN.md) - PyPI 배포 완전 가이드

### 🔧 [GitHub & CI/CD](./github/)
- [Branch Protection 가이드](./github/BRANCH_PROTECTION_GUIDE.md) - 브랜치 보호 설정
- [Pull Request 템플릿](./github/PULL_REQUEST_TEMPLATE.md) - PR 템플릿
- [Issue 템플릿](./github/issue-templates/) - 버그 리포트, 기능 요청 등

### 🐛 [문제 해결](./troubleshooting/)
- [Python 3.12+ 호환성](./troubleshooting/PYTHON_313_FIX.md) - flake8/ruff 마이그레이션
- [Coverage 이슈](./troubleshooting/COVERAGE_FIX.md) - pytest-cov 호환성
- [macOS Python 3.8](./troubleshooting/MACOS_PYTHON38_FIX.md) - pyobjc-core 문제
- [Windows BLE 이슈](./troubleshooting/WINDOWS_BLE_FIX.md) - bleak-winrt 호환성

### 📋 [프로젝트 정보](./project/)
- [릴리스 히스토리](./project/HISTORY.md) - 버전 히스토리 및 변경사항
- [보안 정책](./project/SECURITY.md) - 보안 가이드라인
- [보안 감사](./project/SECURITY_AUDIT.md) - 보안 체크 리포트
- [기여자](./project/AUTHORS.md) - 기여자 및 메인테이너

## 🔗 빠른 링크

- [메인 README](../README.md) - 프로젝트 개요
- [PyPI 패키지](https://pypi.org/project/pymodi-plus/)
- [GitHub 저장소](https://github.com/LUXROBO/pymodi-plus)

## 🆘 도움말

1. [문제 해결](./troubleshooting/) 섹션 확인
2. [테스트 가이드](./development/TESTS_README.md) 검토
3. [기여 가이드](./getting-started/CONTRIBUTING.md) 읽기
4. [템플릿](./github/issue-templates/)을 사용하여 이슈 생성

## 🎯 자주 사용하는 작업

### 설치
```bash
pip install pymodi-plus
```

### 테스트 실행
```bash
make test
```

### PyPI 배포
[배포 가이드](./deployment/DEPLOY_GUIDE_KOREAN.md) 참조

## 📊 문서 통계

- **총 문서:** 21개
- **카테고리:** 7개
- **예제 코드:** 20+ 개
- **문제 해결 가이드:** 4개

---

**버전:** 0.4.0  
**최종 업데이트:** 2025-11-19  
**관리:** LUXROBO
