# Testing Strategy - pymodi-plus

## 📋 테스트 전략 개요

### 테스트 레벨

```
Level 1: Unit Tests (자동) ✅
  └─ tests/ 디렉토리의 모든 테스트
  └─ Mock 객체 사용, 하드웨어 불필요
  └─ make test로 실행

Level 2: Syntax/Lint Check (자동) ✅
  └─ 모든 Python 파일 문법 검증
  └─ examples/ 포함
  └─ make lint로 실행

Level 3: Example Syntax Check (자동) 🆕
  └─ example 파일들의 문법만 검증
  └─ 실행은 하지 않음 (하드웨어 필요)
  └─ make test-examples-syntax로 실행

Level 4: Example Manual Test (수동) ⚠️
  └─ 실제 하드웨어 연결 후 수동 실행
  └─ 배포 전 필수 체크리스트
```

---

## 🎯 현재 상태

### make test (Level 1)
```bash
$ make test
# Unit tests만 실행
# 82 tests, 하드웨어 불필요
# Mock 객체 사용
```

**포함:**
- ✅ modi_plus 모듈 테스트
- ✅ RGB 기능 테스트
- ✅ 버전별 동작 테스트

**미포함:**
- ❌ Example 파일 실행 (하드웨어 필요)
- ❌ 실제 하드웨어 통신

---

## 🆕 개선안

### 1. Example 문법 검증 추가

Example 파일이 문법적으로 올바른지만 검증 (실행은 안 함):

```bash
# 새로운 명령어
make test-examples-syntax
```

### 2. 통합 테스트 명령어

```bash
# 모든 자동 테스트 실행
make test-all
  ├─ make test (unit tests)
  ├─ make lint (code style)
  └─ make test-examples-syntax (example syntax)
```

### 3. 배포 전 체크리스트

```bash
# CI/CD에서 실행 가능한 자동 테스트
make ci-test
  ├─ make test
  ├─ make lint
  └─ make test-examples-syntax

# 수동으로 해야 하는 것
- 실제 하드웨어로 example 실행
- RGB 센서 동작 확인
- 멀티 모듈 테스트
```

---

## 📊 테스트 비교

| 테스트 타입 | 자동화 | 하드웨어 | 실행 시간 | 명령어 |
|------------|--------|---------|----------|--------|
| **Unit Tests** | ✅ | ❌ 불필요 | 1.2초 | `make test` |
| **Lint Check** | ✅ | ❌ 불필요 | 2초 | `make lint` |
| **Example Syntax** | ✅ | ❌ 불필요 | 1초 | `make test-examples-syntax` |
| **Example 실행** | ❌ | ✅ 필요 | 수동 | 직접 실행 |

---

## 🔧 구현

### Makefile에 추가할 명령어

```makefile
##@ Testing

test-examples-syntax: ## Check example files syntax without execution
	$(call check_command,python3)
	@echo "$(BLUE)Checking example files syntax...$(NC)"
	@for file in examples/basic_usage_examples/*.py examples/creation_examples/*.py examples/intermediate_usage_examples/*.py 2>/dev/null; do \
		if [ -f "$$file" ]; then \
			echo "  Checking $$file..."; \
			$(PYTHON) -m py_compile "$$file" || exit 1; \
		fi \
	done
	@echo "$(GREEN)✓ All example files have valid syntax$(NC)"

test-all: test lint test-examples-syntax ## Run all automated tests
	@echo "$(GREEN)✓ All automated tests passed$(NC)"

ci-test: test-all ## Run all CI/CD tests (same as test-all)
	@echo "$(GREEN)✓ CI tests completed$(NC)"
```

---

## 📝 Example 테스트 가이드

### 자동 테스트 (CI/CD에서 실행)

```bash
# 1. Unit tests
make test

# 2. Lint check
make lint

# 3. Example syntax check
make test-examples-syntax

# 또는 한 번에
make test-all
```

### 수동 테스트 (배포 전 필수)

#### 1. 기본 Example 테스트

```bash
# Env 모듈 연결 후
python3 examples/basic_usage_examples/env_example.py
```

#### 2. RGB Example 테스트 (v2.x 모듈 필요)

```bash
# Env v2.x 모듈 연결 후
python3 examples/basic_usage_examples/env_rgb_example.py
```

**체크리스트:**
- [ ] 모듈 자동 검색 동작
- [ ] 버전 정보 정확히 표시
- [ ] RGB 값 정상 출력
- [ ] v1.x 모듈 에러 메시지 확인

#### 3. 멀티 모듈 테스트

```bash
# 2개 이상 Env 모듈 연결 (v1.x + v2.x 혼합)
python3 examples/basic_usage_examples/env_rgb_mixed_versions.py
```

**체크리스트:**
- [ ] 모든 모듈 검색됨
- [ ] 버전별 그룹화 정확
- [ ] 각 모듈 개별 동작
- [ ] 에러 없이 실행

#### 4. 색상 감지 테스트

```bash
# Env v2.x 모듈 연결 후
python3 examples/basic_usage_examples/env_rgb_color_detection.py
```

**체크리스트:**
- [ ] RGB 값 실시간 업데이트
- [ ] 색상 이름 정확히 감지
- [ ] 여러 모듈 동시 동작

---

## ✅ 배포 전 체크리스트

### 자동 테스트 (필수)

```bash
# 모두 통과해야 배포 가능
make test-all

# 개별 실행
make test              # ✅ 82 passed
make lint              # ✅ No errors
make test-examples-syntax  # ✅ All valid
```

### 수동 테스트 (권장)

**하드웨어 테스트:**
- [ ] `env_example.py` - 기본 동작 확인
- [ ] `env_rgb_example.py` - RGB 기능 확인 (v2.x)
- [ ] `env_rgb_mixed_versions.py` - 멀티 모듈 확인
- [ ] `env_rgb_color_detection.py` - 색상 감지 확인

**버전별 테스트:**
- [ ] v1.x 모듈: RGB 접근 시 에러 확인
- [ ] v2.x 모듈: RGB 정상 동작 확인
- [ ] 혼합: 각각 적절히 동작 확인

---

## 🚀 CI/CD 통합

### GitHub Actions 예시

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: make install-dev

      - name: Run all automated tests
        run: make test-all
```

---

## 🎯 테스트 전략 요약

### 개발 중
```bash
make test          # 빠른 unit test
```

### PR 전
```bash
make test-all      # 모든 자동 테스트
```

### 배포 전
```bash
# 1. 자동 테스트
make test-all

# 2. 수동 테스트
python3 examples/basic_usage_examples/env_rgb_example.py
python3 examples/basic_usage_examples/env_rgb_mixed_versions.py
python3 examples/basic_usage_examples/env_rgb_color_detection.py
```

---

## 🔍 왜 Example을 자동 실행하지 않나?

### 이유

1. **하드웨어 의존성**
   - 실제 MODI 모듈 필요
   - CI/CD 환경에 하드웨어 없음

2. **무한 루프**
   - 대부분 `while True:` 루프
   - 자동 종료 안됨

3. **사용자 입력**
   - `Press Enter...`, `Ctrl+C to stop`
   - 자동화 불가능

### 해결책

✅ **문법 검증만**: `make test-examples-syntax`
- Import 오류 감지
- 문법 오류 감지
- 실행은 안 함

✅ **수동 테스트**: 배포 전 체크리스트
- 실제 하드웨어로 검증
- 기능 동작 확인

---

## 📚 참고

- **Unit Tests**: `tests/` 디렉토리
- **Examples**: `examples/` 디렉토리
- **Test Guide**: `TESTS_README.md`
- **Makefile Guide**: `MAKEFILE_GUIDE.md`

---

## 결론

| 질문 | 답변 |
|------|------|
| **make test에 example 포함?** | ❌ 아니오 (하드웨어 필요) |
| **Example 검증 방법?** | ✅ 문법만 검증 가능 |
| **배포 전 Example 테스트?** | ✅ 수동으로 실행 필수 |
| **자동 테스트로 충분?** | ⚠️ 아니오, 수동 테스트도 필요 |
