# PyMODI Plus - Makefile 사용 가이드

이 문서는 PyMODI Plus 프로젝트의 Makefile 사용법을 안내합니다.

## 빠른 시작

### 1. 개발 환경 설정

```bash
# 모든 의존성 설치 (패키지 + 개발 도구)
make install-dev
```

이 명령은 다음을 자동으로 설치합니다:
- 프로젝트 필수 패키지 (requirements.txt)
- 개발 도구: pytest, flake8, black, coverage 등

### 2. 사용 가능한 명령어 확인

```bash
# 도움말 보기
make help
```

## 주요 명령어

### 설치 (Setup)

| 명령어 | 설명 |
|--------|------|
| `make install` | 패키지 의존성만 설치 |
| `make install-dev` | 패키지 + 개발 도구 전체 설치 (권장) |
| `make install-editable` | editable 모드로 패키지 설치 |
| `make reinstall` | 패키지 재설치 (의존성 문제 해결) |

### 테스트 (Testing)

| 명령어 | 설명 |
|--------|------|
| `make test` | pytest로 테스트 실행 |
| `make test-verbose` | 상세 출력과 함께 테스트 실행 |
| `make coverage` | 코드 커버리지 리포트 생성 |

**예시:**
```bash
# 기본 테스트 실행
make test

# 더 자세한 정보와 함께 실행
make test-verbose

# 커버리지 확인 (htmlcov/index.html 생성)
make coverage
```

### 코드 품질 (Code Quality)

| 명령어 | 설명 |
|--------|------|
| `make lint` | flake8로 코드 스타일 검사 |
| `make format` | black으로 코드 자동 포맷팅 |

**예시:**
```bash
# 코드 스타일 검사
make lint

# 코드 자동 포맷팅
make format
```

### 예제 (Examples)

| 명령어 | 설명 |
|--------|------|
| `make examples` | 사용 가능한 모든 예제 파일 목록 보기 |

**예시:**
```bash
# 예제 목록 확인
make examples

# 특정 예제 실행
python examples/basic_usage_examples/led_example.py
```

### 정리 (Cleanup)

| 명령어 | 설명 |
|--------|------|
| `make clean` | 모든 빌드/테스트 아티팩트 제거 |
| `make clean-build` | 빌드 아티팩트만 제거 |
| `make clean-pyc` | Python 캐시 파일만 제거 |
| `make clean-test` | 테스트 결과 파일만 제거 |

### 빌드 & 배포 (Build & Release)

| 명령어 | 설명 |
|--------|------|
| `make dist` | 배포용 패키지 빌드 |
| `make docs` | Sphinx 문서 생성 |
| `make release` | PyPI에 패키지 업로드 |

## 일반적인 워크플로우

### 새로운 기능 개발

```bash
# 1. 개발 환경 설정
make install-dev

# 2. 코드 작성
# ... 코드 수정 ...

# 3. 코드 포맷팅
make format

# 4. 코드 스타일 검사
make lint

# 5. 테스트 실행
make test

# 6. 커버리지 확인 (선택사항)
make coverage
```

### 테스트 실행 전 체크리스트

```bash
# 개발 도구가 설치되어 있는지 확인
make install-dev

# 테스트 실행
make test
```

만약 "command not found" 에러가 발생하면:
```bash
# 개발 의존성을 다시 설치
make install-dev
```

### 배포 준비

```bash
# 1. 모든 테스트 통과 확인
make test

# 2. 코드 스타일 검사
make lint

# 3. 이전 빌드 정리
make clean

# 4. 배포 패키지 빌드
make dist
```

## 문제 해결

### pytest를 찾을 수 없다는 에러

```bash
Error: pytest is not installed. Run 'make install-dev' first.
```

**해결방법:**
```bash
make install-dev
```

### flake8 또는 black을 찾을 수 없다는 에러

**해결방법:**
```bash
make install-dev
```

### 테스트 실패 시

1. 상세 출력으로 다시 실행:
   ```bash
   make test-verbose
   ```

2. 특정 테스트만 실행:
   ```bash
   python3 -m pytest tests/module/input_module/test_button.py -v
   ```

### 의존성 충돌

패키지 버전 충돌이 발생하면:
```bash
# 방법 1: 패키지 재설치
make reinstall

# 방법 2: 개발 도구 재설치
make install-dev

# 방법 3: 가상환경 사용 (권장)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
make install-dev
```

**주의:** `packaging` 패키지 관련 경고가 나타날 수 있지만, requirements.txt가 `packaging>=21.3`으로 업데이트되어 안전합니다.

## 예제 실행하기

### 기본 사용 예제

```bash
# 예제 목록 확인
make examples

# LED 예제 실행
python3 examples/basic_usage_examples/led_example.py

# 버튼 예제 실행
python3 examples/basic_usage_examples/button_example.py
```

### 중급 예제

```bash
# 다중 모듈 예제
python3 examples/intermediate_usage_examples/multi_module_example.py
```

## 팁

1. **자주 사용하는 명령어**
   ```bash
   make test          # 빠른 테스트
   make lint          # 코드 검사
   make format        # 코드 정리
   ```

2. **개발 시작 시**
   ```bash
   make install-dev   # 한 번만 실행
   ```

3. **코드 커밋 전**
   ```bash
   make format && make lint && make test
   ```

4. **여러 명령어 연속 실행**
   ```bash
   # 코드 포맷팅 → 검사 → 테스트를 한 번에
   make format && make lint && make test
   ```

## 추가 정보

- 모든 명령어는 `make help`로 확인 가능
- 명령어는 현재 디렉토리 체크와 의존성 검사를 자동으로 수행
- 색상 출력으로 성공/실패를 쉽게 구분
