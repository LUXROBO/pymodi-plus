# Branch Protection Rules 설정 가이드

이 문서는 `master`와 `develop` 브랜치에 PR을 머지하기 전에 필수 테스트가 통과해야 하도록 GitHub Branch Protection Rules를 설정하는 방법을 설명합니다.

## 📋 개요

PR이 `master` 또는 `develop` 브랜치에 머지되기 전에 다음 조건들이 만족되어야 합니다:
- ✅ 모든 테스트 통과 (Python 3.8 ~ 3.13)
- ✅ 코드 스타일 검사 통과 (flake8)
- ✅ unittest 및 pytest 테스트 통과

## 🔧 설정 방법

### 1. GitHub 저장소 설정으로 이동

1. GitHub 저장소 페이지로 이동
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Branches** 클릭

### 2. Branch Protection Rule 추가

#### Master 브랜치 보호 설정

1. **Add rule** 버튼 클릭
2. **Branch name pattern**에 `master` 입력
3. 다음 옵션들을 활성화:

```
☑️ Require a pull request before merging
   ☑️ Require approvals (최소 1명 추천)
   ☑️ Dismiss stale pull request approvals when new commits are pushed

☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date before merging
   
   필수 Status Checks (검색하여 추가):
   - ✅ All Tests Must Pass to Merge (pr-test.yml의 merge-check job)
   - Build and Test (build.yml) - 모든 Python 버전
   - Test Python 3.8 (pr-test.yml)
   - Test Python 3.9 (pr-test.yml)
   - Test Python 3.10 (pr-test.yml)
   - Test Python 3.11 (pr-test.yml)
   - Test Python 3.12 (pr-test.yml)
   - Test Python 3.13 (pr-test.yml)

☑️ Require conversation resolution before merging

☑️ Do not allow bypassing the above settings
```

4. **Create** 버튼 클릭

#### Develop 브랜치 보호 설정

위의 Master 브랜치 설정과 동일하게 반복하되, Branch name pattern에 `develop`을 입력합니다.

### 3. Status Checks 설정 확인

Branch Protection Rule을 처음 설정할 때는 status checks 목록이 비어있을 수 있습니다. 
다음 단계를 따르세요:

1. 먼저 PR을 하나 생성합니다
2. GitHub Actions가 실행되어 status checks가 나타날 때까지 기다립니다
3. Branch Protection Rule 설정으로 돌아가서 status checks를 추가합니다

## 📊 설정된 GitHub Actions Workflows

현재 저장소에는 다음 workflows가 설정되어 있습니다:

### 1. **PR Test - Required for Merge** (`pr-test.yml`)
- **트리거**: PR → master, develop
- **목적**: PR 머지 전 필수 테스트
- **Python 버전**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **실행 항목**:
  - Linting (flake8)
  - 전체 테스트 실행 (`make test` 동등)
  - 테스트 커버리지 확인 (Python 3.11만)
  - 최종 merge-check job (모든 테스트 통과 확인)

### 2. **Build Status** (`build.yml`)
- **트리거**: 모든 push, PR → master, develop
- **목적**: 빌드 및 테스트 확인
- **Python 버전**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **실행 항목**:
  - Linting (flake8)
  - unittest 실행
  - pytest 실행

### 3. **Unit Test - OS별** (`unit_test_*.yml`)
- **ubuntu**: Ubuntu 최신 버전
- **macos**: macOS 최신 버전  
- **windows**: Windows 최신 버전
- **Python 버전**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **실행 항목**:
  - unittest 실행
  - pytest 실행

## ✅ 권장 필수 Status Checks

최소한 다음 status checks를 필수로 설정하는 것을 권장합니다:

1. **✅ All Tests Must Pass to Merge** (가장 중요)
   - 이것만 설정해도 모든 Python 버전의 테스트를 보장합니다
   
2. **Build and Test** (선택사항)
   - 추가적인 보안을 위해 설정

## 🔍 테스트 실패 시 동작

테스트가 실패하면:
1. ❌ PR에 실패 표시가 나타납니다
2. ❌ "Merge pull request" 버튼이 비활성화됩니다
3. 📝 개발자는 코드를 수정하고 다시 push해야 합니다
4. 🔄 새로운 commit이 push되면 테스트가 자동으로 다시 실행됩니다

## 📝 테스트 우회 (권장하지 않음)

관리자 권한이 있는 경우, 긴급 상황에서만 "Override" 옵션을 사용할 수 있습니다.
하지만 이는 코드 품질을 해칠 수 있으므로 권장하지 않습니다.

## 🐛 문제 해결

### Status Checks가 보이지 않는 경우
- 최소 한 번의 PR을 생성하여 GitHub Actions가 실행되도록 합니다
- Actions 탭에서 workflow가 정상적으로 실행되는지 확인합니다

### 테스트가 로컬에서는 통과하지만 GitHub Actions에서 실패하는 경우
- Python 버전 차이 확인
- 의존성 버전 확인 (`requirements.txt`)
- 로컬에서 `make test` 실행하여 확인

### Actions 권한 오류
- Settings → Actions → General에서 "Read and write permissions" 확인

## 📚 관련 문서

- [GitHub Branch Protection Rules 공식 문서](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Actions 공식 문서](https://docs.github.com/en/actions)
- 프로젝트 Makefile 참조: `make help`

## 💡 추가 권장사항

1. **Code Review**: 코드 리뷰를 필수로 설정 (Require approvals)
2. **Linear History**: "Require linear history" 활성화로 깔끔한 git history 유지
3. **Delete Head Branches**: PR 머지 후 브랜치 자동 삭제 활성화
4. **Automatic Deletion**: 머지된 브랜치 자동 삭제 설정

---

**문의사항**: 문제가 발생하면 프로젝트 관리자에게 문의하세요.

