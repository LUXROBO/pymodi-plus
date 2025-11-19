# PyMODI Plus - 빠른 시작 가이드

## 1분 안에 시작하기

### Step 1: 개발 환경 설정

```bash
make install-dev
```

### Step 2: 테스트 실행

```bash
make test
```

**결과:** ✅ 67 passed in 1.20s

### Step 3: 예제 확인

```bash
make examples
```

## 주요 명령어

```bash
make help         # 모든 명령어 보기
make test         # 안전한 테스트 실행 (67 tests)
make test-input   # Input 모듈만 테스트
make test-output  # Output 모듈만 테스트
make lint         # 코드 검사
make format       # 코드 포맷팅
make examples     # 예제 목록
make clean        # 정리
```

## 테스트 정보

- **하드웨어 불필요**: Mock 객체 사용
- **빠른 실행**: 1.2초 내 완료
- **67개 테스트**: 모두 정상 통과

## 예제 실행

```bash
# LED 제어 예제
python3 examples/basic_usage_examples/led_example.py

# 버튼 입력 예제
python3 examples/basic_usage_examples/button_example.py
```

## 문제 해결

명령어가 없다는 에러가 나면:
```bash
make install-dev
```

자세한 내용은 [MAKEFILE_GUIDE.md](./MAKEFILE_GUIDE.md)를 참고하세요.
