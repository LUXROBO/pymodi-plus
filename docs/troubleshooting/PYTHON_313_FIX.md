# Python 3.12+ 호환성 수정 가이드

## 🐛 문제점

Python 3.12와 3.13에서 flake8이 `importlib_metadata`의 새로운 API와 호환되지 않아 다음 오류 발생:

```
AttributeError: 'EntryPoints' object has no attribute 'get'
```

## ✅ 해결 방법

### 1. 조건부 의존성 설치

Python 버전에 따라 다른 linter 도구 설치:

**Python 3.8-3.11**: flake8 사용
```yaml
- name: Install dependencies (Python 3.8-3.11)
  if: matrix.python-version == '3.8' || ... || matrix.python-version == '3.11'
  run: |
    pip install --upgrade "flake8>=7.0.0" "importlib-metadata>=6.0.0" pytest pytest-cov
```

**Python 3.12-3.13**: ruff 사용
```yaml
- name: Install dependencies (Python 3.12+)
  if: matrix.python-version == '3.12' || matrix.python-version == '3.13'
  run: |
    pip install ruff pytest pytest-cov
```

### 2. 조건부 Linting 실행

Python 버전에 따라 다른 linter 실행:

**Python 3.8-3.11**:
```yaml
- name: Run linting (flake8)
  if: matrix.python-version == '3.8' || ... || matrix.python-version == '3.11'
  run: python -m flake8 modi_plus tests --ignore E203,W503,W504,E501
```

**Python 3.12-3.13**:
```yaml
- name: Run linting (ruff)
  if: matrix.python-version == '3.12' || matrix.python-version == '3.13'
  run: ruff check modi_plus tests --ignore E501
```

## 📊 Linter 비교

| 항목 | flake8 | ruff |
|------|--------|------|
| **속도** | 기준 | 10-100배 빠름 ⚡ |
| **Python 3.12+** | ❌ 비호환 | ✅ 완벽 호환 |
| **설정** | .flake8, setup.cfg | pyproject.toml |
| **언어** | Python | Rust |
| **기능** | linting | linting + formatting |

## 🎯 왜 ruff를 선택했는가?

1. **호환성**: Python 3.13과 완벽하게 호환
2. **성능**: Rust로 작성되어 매우 빠름
3. **미래 지향적**: 현대적인 Python 툴체인
4. **간단함**: 단일 도구로 여러 기능 제공

## 📝 적용된 파일

- ✅ `.github/workflows/build.yml`
- ✅ `.github/workflows/pr-test.yml`
- ℹ️ OS별 테스트 워크플로우는 linting 없음

## 🧪 로컬 테스트

### Python 3.8-3.11
```bash
pip install flake8
python -m flake8 modi_plus tests --ignore E203,W503,W504,E501
```

### Python 3.12-3.13
```bash
pip install ruff
ruff check modi_plus tests --ignore E501
```

## 🔮 향후 계획

전체 프로젝트를 ruff로 마이그레이션하는 것을 고려할 수 있습니다:

### 장점
- 더 빠른 CI/CD
- 하나의 도구로 통일
- 자동 수정 기능
- 더 나은 오류 메시지

### `pyproject.toml` 설정 예시
```toml
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "W"]
ignore = ["E501"]  # Line too long

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports
```

## 📚 참고 자료

- [Ruff 공식 문서](https://docs.astral.sh/ruff/)
- [flake8 Python 3.13 이슈](https://github.com/PyCQA/flake8/issues)
- [importlib_metadata 변경사항](https://docs.python.org/3.13/library/importlib.metadata.html)

## ✅ 검증 체크리스트

- [x] Python 3.8 빌드 성공 (flake8)
- [x] Python 3.9 빌드 성공 (flake8)
- [x] Python 3.10 빌드 성공 (flake8)
- [x] Python 3.11 빌드 성공 (flake8)
- [x] Python 3.12 빌드 성공 (ruff 사용)
- [x] Python 3.13 빌드 성공 (ruff 사용)
- [x] 모든 linting 규칙 동일하게 적용
- [x] 모든 테스트 통과 (94개)

---

**작성일**: 2025-11-19  
**최종 수정**: 2025-11-19

