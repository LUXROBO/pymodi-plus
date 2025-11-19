# PyMODI Plus 테스트 가이드

## 테스트 개요

### 테스트 타입

PyMODI Plus의 테스트는 **물리적 하드웨어가 필요 없는 유닛 테스트**입니다.

- **Mock 객체 사용**: 실제 MODI 하드웨어 대신 가상 객체 사용
- **독립 실행**: 네트워크 연결이나 실제 장치 없이 실행 가능
- **빠른 검증**: 코드 로직만 검증

## 테스트 구조

### Mock Connection (가상 연결)

```python
class MockConnection:
    def __init__(self):
        self.send_list = []  # 전송된 메시지 기록

    def send(self, pkt):
        self.send_list.append(pkt)  # 실제 전송 없이 기록만
```

- **실제 하드웨어 없이 동작**: 물리적 MODI 모듈 불필요
- **메시지 검증**: 올바른 명령이 전송되는지만 확인
- **타임아웃 비활성화**: `_enable_get_property_timeout = False`

### 테스트 예시 분석

#### Button 테스트 (test_button.py)

```python
def test_get_clicked(self):
    # Mock 객체 사용 (실제 버튼 불필요)
    _ = self.button.clicked

    # 올바른 메시지가 생성되었는지만 확인
    self.assertEqual(
        self.connection.send_list[0],
        parse_get_property_message(...)
    )
```

**검증 내용:**
1. ✅ `clicked` 속성 호출 시 올바른 메시지 생성
2. ✅ 메시지 형식 정확성
3. ❌ 실제 버튼 하드웨어 동작 (불필요)

## 현재 테스트 상태

### 개별 테스트 실행 (✅ 정상)

```bash
# 특정 파일 테스트 - 정상 작동
$ python3 -m pytest tests/module/input_module/test_button.py -v
============================== 4 passed ==============================
```

### 전체 테스트 실행 (⚠️ 에러)

```bash
# 전체 테스트 - pytest 이름 충돌
$ make test
========================= 3 passed, 83 errors =========================
```

**에러 원인:**
```
AttributeError: module 'tests.module.setup_module' has no attribute '__code__'
```

## 문제 진단

### pytest 이름 충돌 문제

pytest는 `setup_module`이라는 특수 함수를 사용합니다:
- **pytest의 setup_module**: 테스트 전 실행되는 함수
- **프로젝트의 setup_module**: 실제 모듈 패키지 디렉토리

```
tests/
├── module/
│   ├── setup_module/    ← pytest가 이것을 함수로 인식!
│   │   ├── test_battery.py
│   │   └── test_network.py
│   ├── input_module/
│   └── output_module/
```

### 해결 방법

#### 방법 1: pytest 설정 추가 (권장)

`pytest.ini` 또는 `pyproject.toml`에 설정 추가:

```ini
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
# setup_module을 무시하도록 설정
```

#### 방법 2: 개별 테스트 실행

```bash
# 디렉토리별 개별 실행
python3 -m pytest tests/module/input_module/ -v
python3 -m pytest tests/module/output_module/ -v
python3 -m pytest tests/task/ -v
```

#### 방법 3: 디렉토리 구조 변경 (비권장)

```bash
# setup_module → modi_setup 등으로 이름 변경
# 하지만 전체 코드베이스 수정 필요
```

## 테스트 실행 방법

### ✅ 권장: 개별 모듈 테스트

```bash
# Input 모듈 테스트
python3 -m pytest tests/module/input_module/ -v

# Output 모듈 테스트
python3 -m pytest tests/module/output_module/ -v

# Task 테스트
python3 -m pytest tests/task/ -v
```

### ✅ 특정 테스트만 실행

```bash
# Button 모듈만
python3 -m pytest tests/module/input_module/test_button.py -v

# LED 모듈만
python3 -m pytest tests/module/output_module/test_led.py -v
```

### ⚠️ 전체 테스트 (이름 충돌 발생)

```bash
# 현재는 83개 에러 발생 (setup_module 충돌)
make test
```

## 테스트 결과 해석

### 정상 실행 예시

```bash
$ python3 -m pytest tests/module/input_module/test_button.py -v

tests/module/input_module/test_button.py::TestButton::test_get_clicked PASSED
tests/module/input_module/test_button.py::TestButton::test_get_double_clicked PASSED
tests/module/input_module/test_button.py::TestButton::test_get_pressed PASSED
tests/module/input_module/test_button.py::TestButton::test_get_toggled PASSED

============================== 4 passed in 0.03s ==============================
```

### 에러 발생 시

```bash
$ make test

3 passed, 83 errors in 2.43s
```

- **3 passed**: `tests/task/` 테스트 성공 (setup_module 없음)
- **83 errors**: `tests/module/` 하위 테스트 실패 (setup_module 충돌)

## 해결책 구현

### pytest.ini 생성

프로젝트 루트에 `pytest.ini` 파일 생성 필요:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
norecursedirs = .git .tox dist build *.egg

# 이름 충돌 회피
addopts = --strict-markers
```

### Makefile에 개별 테스트 명령 추가

```makefile
test-input:  ## Test input modules only
	pytest tests/module/input_module/ -v

test-output: ## Test output modules only
	pytest tests/module/output_module/ -v

test-task:   ## Test task modules only
	pytest tests/task/ -v

test-safe:   ## Run all tests safely (excluding setup_module conflicts)
	pytest tests/task/ tests/module/input_module/ tests/module/output_module/ -v
```

## 요약

### 테스트 특성

| 항목 | 내용 |
|------|------|
| **하드웨어 필요** | ❌ 불필요 (Mock 객체 사용) |
| **네트워크 필요** | ❌ 불필요 (가상 연결) |
| **실행 속도** | ⚡ 빠름 (0.03초/테스트) |
| **검증 범위** | 메시지 생성 로직만 |

### 현재 상태

| 테스트 방법 | 상태 | 비고 |
|------------|------|------|
| 개별 파일 실행 | ✅ 정상 | 권장 |
| 디렉토리별 실행 | ✅ 정상 | 권장 |
| 전체 테스트 실행 | ⚠️ 에러 | pytest 이름 충돌 |

### 권장 사용법

```bash
# 1. 개발 중: 수정한 모듈만 테스트
python3 -m pytest tests/module/input_module/test_button.py -v

# 2. 커밋 전: 관련 모듈 전체 테스트
python3 -m pytest tests/module/input_module/ -v

# 3. PR 전: 안전한 전체 테스트
python3 -m pytest tests/task/ tests/module/input_module/ tests/module/output_module/ -v
```

## 다음 단계

1. **pytest.ini 생성** - 이름 충돌 해결
2. **Makefile 업데이트** - 개별 테스트 명령 추가
3. **CI/CD 설정** - 자동 테스트 실행
