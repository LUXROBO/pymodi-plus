# Env Module RGB Examples Guide

## 📝 Overview

이 가이드는 여러 개의 Env 모듈이 연결되었을 때, 버전별로 RGB 기능을 테스트하는 예제들을 설명합니다.

## 📁 예제 파일들

### 1. env_rgb_example.py - 멀티 모듈 기본 예제

**기능:**
- 연결된 **모든 Env 모듈** 자동 검색
- 각 모듈의 버전 확인 및 RGB 지원 여부 테스트
- RGB 지원 모듈들의 실시간 RGB 값 표시

**사용 시나리오:**
```
연결된 모듈:
- Env Module #1: v1.5.0 (RGB 미지원)
- Env Module #2: v2.0.0 (RGB 지원)

결과:
- Module #1: 기본 센서만 표시 (온도, 습도 등)
- Module #2: RGB 실시간 모니터링
```

**실행:**
```bash
python3 examples/basic_usage_examples/env_rgb_example.py
```

**출력 예시:**
```
============================================================
Env Module RGB Example - Multi-Module Support
============================================================

Found 2 Env module(s)

============================================================
Env Module #1 (ID: 0x1234)
============================================================
App Version: 1.5.0
✗ RGB properties are NOT supported in this version
Please upgrade firmware to version 2.x or above

Available properties:
  - Temperature: 25°C
  - Humidity: 60%
  - Illuminance: 350 lux
  - Volume: 45 dB

============================================================
Env Module #2 (ID: 0x5678)
============================================================
App Version: 2.0.0
✓ RGB properties are supported!

============================================================
Reading RGB values from 1 module(s)
Press Ctrl+C to stop
============================================================

Module #2: RGB=(128,  64, 255)
```

---

### 2. env_rgb_mixed_versions.py - 혼합 버전 예제

**기능:**
- v1.x와 v2.x 모듈이 섞여있을 때 처리
- 버전별로 그룹화하여 표시
- 각 그룹에 적합한 센서 값 표시

**특징:**
- RGB 모듈: RGB + 온도
- Legacy 모듈: 온도 + 습도 + 조도

**실행:**
```bash
python3 examples/basic_usage_examples/env_rgb_mixed_versions.py
```

**출력 예시:**
```
======================================================================
Connected Env Modules Summary (3 total)
======================================================================

✓ RGB-capable modules (v2.x+): 2
  Module #1: ID=0x1000, Version=2.0.0
  Module #3: ID=0x3000, Version=2.1.0

✗ Legacy modules (v1.x): 1
  Module #2: ID=0x2000, Version=1.5.0

======================================================================
Multi-Version Env Modules Monitor
======================================================================
RGB Modules:
  #1: RGB=(255,100, 50) Temp=25°C
  #3: RGB=( 50,200,100) Temp=24°C

Legacy Modules:
  #2: Temp=26°C Humidity=55% Lux=400
```

---

### 3. env_rgb_color_detection.py - 색상 감지 예제

**기능:**
- RGB 센서를 이용한 색상 감지
- 여러 모듈 동시 모니터링
- 색상별 이름 표시 (RED, GREEN, BLUE, YELLOW 등)
- ASCII 바 차트로 RGB 값 시각화

**감지 가능한 색상:**
- RED (빨강)
- GREEN (녹색)
- BLUE (파랑)
- YELLOW (노랑)
- PURPLE (보라)
- WHITE (흰색)
- MIXED/GRAY (혼합/회색)

**실행:**
```bash
python3 examples/basic_usage_examples/env_rgb_color_detection.py
```

**출력 예시:**
```
======================================================================
RGB Color Detection Monitor
======================================================================

Module #1 (0x1000): RGB=(200,  50,  30) -> RED
  R: ████████████████████
  G: █████
  B: ███

Module #2 (0x3000): RGB=( 40, 180,  60) -> GREEN
  R: ████
  G: ██████████████████
  B: ██████
```

---

## 🎯 사용 시나리오별 추천

### Scenario 1: 모듈 1개만 테스트
```bash
python3 examples/basic_usage_examples/env_rgb_example.py
```
→ 가장 단순한 예제, 기본 사용법 학습

### Scenario 2: 여러 모듈, 같은 버전
```bash
python3 examples/basic_usage_examples/env_rgb_color_detection.py
```
→ 여러 센서로 동시 색상 감지

### Scenario 3: 여러 모듈, 다른 버전 (v1.x + v2.x)
```bash
python3 examples/basic_usage_examples/env_rgb_mixed_versions.py
```
→ 버전별 적절한 센서 사용

### Scenario 4: RGB 기능만 테스트
```bash
python3 examples/basic_usage_examples/env_rgb_color_detection.py
```
→ v2.x 모듈만 필요, RGB 센서 집중 테스트

---

## 💡 코드 패턴

### 패턴 1: 모든 Env 모듈 검색

```python
import modi_plus

bundle = modi_plus.MODIPlus()

# 모든 Env 모듈 가져오기
all_envs = bundle.envs
print(f"Found {len(all_envs)} Env module(s)")

for i, env in enumerate(all_envs):
    print(f"Module #{i+1}: Version {env.app_version}")
```

### 패턴 2: RGB 지원 모듈만 필터링

```python
# RGB 지원 모듈만 선택
rgb_modules = []
for i, env in enumerate(bundle.envs):
    if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
        rgb_modules.append((i, env))

print(f"RGB-capable: {len(rgb_modules)}/{len(bundle.envs)}")
```

### 패턴 3: 버전별 그룹화

```python
v1_modules = []  # RGB 미지원
v2_modules = []  # RGB 지원

for i, env in enumerate(bundle.envs):
    if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
        v2_modules.append((i, env))
    else:
        v1_modules.append((i, env))
```

### 패턴 4: 여러 모듈 동시 읽기

```python
import time

while True:
    for idx, env in rgb_modules:
        r, g, b = env.rgb
        print(f"Module #{idx+1}: RGB=({r}, {g}, {b})", end="  ")
    print("\r", end="", flush=True)
    time.sleep(0.1)
```

---

## 🔧 문제 해결

### 문제 1: "No Env modules found"

**원인:**
- 모듈이 연결되지 않음
- 연결 지연

**해결:**
```python
import time

bundle = modi_plus.MODIPlus()
time.sleep(2)  # 연결 대기

if len(bundle.envs) == 0:
    print("Waiting for modules...")
    time.sleep(3)
```

### 문제 2: 특정 모듈만 감지됨

**원인:**
- 모듈 초기화 시간 차이

**해결:**
```python
# 재스캔
bundle = modi_plus.MODIPlus()
time.sleep(3)  # 충분한 대기 시간

print(f"Found {len(bundle.envs)} modules")
```

### 문제 3: RGB 값이 항상 0

**원인:**
- 센서가 어두운 곳에 있음
- 센서가 가려져 있음

**해결:**
- 밝은 곳에서 테스트
- 컬러 카드를 센서 앞에 배치

---

## 📊 예제 비교표

| 예제 | 멀티 모듈 | 버전 혼합 | 색상 감지 | 난이도 |
|------|-----------|----------|----------|--------|
| env_rgb_example.py | ✅ | ✅ | ❌ | ⭐ 쉬움 |
| env_rgb_mixed_versions.py | ✅ | ✅ | ❌ | ⭐⭐ 보통 |
| env_rgb_color_detection.py | ✅ | ❌ | ✅ | ⭐⭐⭐ 고급 |

---

## 🚀 다음 단계

### 1. 커스텀 색상 감지

```python
def detect_custom_color(r, g, b):
    # 내 제품의 특정 색상 감지
    if 100 <= r <= 150 and g < 50 and b < 50:
        return "MY_PRODUCT_RED"
    # ...
```

### 2. 데이터 로깅

```python
import csv
import time

with open('rgb_log.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Module', 'R', 'G', 'B'])

    while True:
        for idx, env in rgb_modules:
            r, g, b = env.rgb
            writer.writerow([time.time(), idx, r, g, b])
```

### 3. 색상 기반 제어

```python
# 빨간색 감지 시 LED 켜기
led = bundle.leds[0]

r, g, b = env.rgb
if r > 200 and g < 100 and b < 100:
    led.rgb = 255, 0, 0  # 빨간색
else:
    led.rgb = 0, 0, 0    # 끄기
```

---

## 📚 참고 자료

- **API 문서**: ENV_RGB_FEATURE.md
- **구현 요약**: ENV_RGB_SUMMARY.md
- **테스트 코드**: tests/module/input_module/test_env.py

---

## ✅ 체크리스트

예제 실행 전 확인사항:

- [ ] Env 모듈 연결 확인
- [ ] 모듈 버전 확인 (v1.x 또는 v2.x)
- [ ] 여러 모듈 테스트 시 모두 연결 확인
- [ ] RGB 테스트 시 v2.x 모듈 필요
- [ ] 색상 감지 시 조명 확인

실행 후 확인사항:

- [ ] 모든 모듈이 감지되었는가?
- [ ] RGB 값이 정상적으로 표시되는가?
- [ ] 버전별로 올바르게 동작하는가?
- [ ] 에러 메시지가 없는가?
