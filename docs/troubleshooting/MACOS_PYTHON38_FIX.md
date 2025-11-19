# macOS Python 3.8 호환성 문제 해결

## 🐛 문제점

macOS에서 Python 3.8 실행 시 pyobjc-core 설치 오류 발생:

```
PyObjC: Need at least Python 3.9
```

## 🔍 원인 분석

### 의존성 체인
```
bleak (BLE 라이브러리)
  └─ pyobjc-core (macOS only)
      └─ Python 3.9+ 필수
```

### 세부 원인
1. **bleak 0.13.0**: macOS에서 BLE 통신을 위해 pyobjc-core 필요
2. **pyobjc-core 최신 버전**: Python 3.9+ 이상 요구
3. **Python 3.8**: pyobjc-core 최신 버전과 비호환

## ✅ 해결 방법

macOS workflow에서 Python 3.8 제외:

```yaml
# unit_test_macos.yml
matrix:
  # Python 3.8 excluded: pyobjc-core requires Python 3.9+
  python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']
```

## 📊 플랫폼별 Python 지원

| Python | Ubuntu | macOS | Windows | 이유 |
|--------|--------|-------|---------|------|
| 3.8    | ✅ | ❌ | ✅ | macOS: pyobjc-core 비호환 |
| 3.9    | ✅ | ✅ | ✅ | 모든 플랫폼 지원 |
| 3.10   | ✅ | ✅ | ✅ | 모든 플랫폼 지원 |
| 3.11   | ✅ | ✅ | ✅ | 모든 플랫폼 지원 |
| 3.12   | ✅ | ✅ | ✅ | 모든 플랫폼 지원 |
| 3.13   | ✅ | ✅ | ✅ | 모든 플랫폼 지원 |

## 🎯 영향

### Python 3.8 지원 범위
- ✅ **Ubuntu**: 완전 지원
- ❌ **macOS**: 지원 안 함 (pyobjc-core 이슈)
- ✅ **Windows**: 완전 지원
- ✅ **build.yml**: 지원 (Ubuntu 기반)
- ✅ **pr-test.yml**: 지원 (Ubuntu 기반)

### 실제 사용자 영향
**최소**: 대부분의 사용자는 Python 3.9+ 사용
- Python 3.8 출시: 2019년 10월
- Python 3.9 출시: 2020년 10월
- Python 3.8 EOL: 2024년 10월 (이미 종료)

## 🔄 대안 (선택 사항)

### 옵션 1: pyobjc-core 버전 고정
```yaml
# Python 3.8에서만 오래된 버전 설치
pip install "pyobjc-core<9.0"  # Python 3.8 호환 버전
```
→ 복잡성 증가, 관리 어려움

### 옵션 2: Python 3.8 제외 (현재 방법) ✅
```yaml
python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']
```
→ 간단하고 명확, Python 3.8 이미 EOL

### 옵션 3: bleak 버전 다운그레이드
```yaml
pip install "bleak<0.13.0"
```
→ 기능 제한, 권장하지 않음

## 🧪 검증

### Ubuntu (Python 3.8 지원)
```bash
python3.8 -m pytest tests/ -v
# ✅ 통과
```

### macOS (Python 3.9+ 지원)
```bash
python3.9 -m pytest tests/ -v
# ✅ 통과
```

### Windows (Python 3.8 지원)
```bash
python -m pytest tests/task/ tests/module/input_module/ tests/module/output_module/ -v
# ✅ 통과 (94개 테스트)
```

## 📝 개발자 노트

### macOS에서 Python 3.8 사용 시
로컬 개발에서도 동일한 문제 발생 가능:
```bash
# 해결 방법 1: Python 3.9+ 사용 (권장)
brew install python@3.9

# 해결 방법 2: pyobjc-core 오래된 버전 설치
pip install "pyobjc-core<9.0"
```

### BLE 기능 개발 시
macOS에서 BLE 테스트하려면 Python 3.9+ 필수:
```bash
# pyenv로 여러 버전 관리
pyenv install 3.9.18
pyenv local 3.9.18
```

## ✅ 최종 테스트 매트릭스

```
Ubuntu:
  ✅ Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

macOS:
  ✅ Python 3.9, 3.10, 3.11, 3.12, 3.13
  ❌ Python 3.8 (제외됨)

Windows:
  ✅ Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
```

## 📚 참고 자료

- [pyobjc-core 요구사항](https://pypi.org/project/pyobjc-core/)
- [Python 3.8 EOL 공지](https://peps.python.org/pep-0569/)
- [bleak 라이브러리](https://github.com/hbldh/bleak)

---

**작성일**: 2025-11-19  
**최종 수정**: 2025-11-19  
**상태**: Python 3.8 EOL로 인해 영구적 해결

