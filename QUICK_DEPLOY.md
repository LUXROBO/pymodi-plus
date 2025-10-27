# 빠른 배포 가이드 (Quick Deploy)

## 🚀 3분 안에 PyPI 배포하기

### 준비물
- [ ] PyPI 계정 (https://pypi.org)
- [ ] PyPI API Token
- [ ] 테스트 통과 확인

---

## 📝 배포 전 체크리스트

```bash
# 1. 버전 확인
cat modi_plus/about.py | grep version
# __version__ = "0.4.0"

# 2. 테스트 실행
make test
# ============================== 82 passed in 1.24s ==============================

# 3. 린트 검사
make lint
# ✓ Code style check passed
```

---

## 🎯 방법 1: 자동 스크립트 (권장)

### 실행

```bash
./scripts/deploy_to_pypi.sh
```

### 화면 안내에 따라 진행
1. 버전 확인 (y/n)
2. 테스트 자동 실행
3. 빌드 생성
4. 배포 타겟 선택:
   - `1` - TestPyPI (테스트)
   - `2` - PyPI (프로덕션)
   - `3` - 양쪽 다
5. Token 입력
6. 완료!

---

## 🎯 방법 2: Makefile (간단)

### 빌드

```bash
make clean
make dist
```

### 배포

```bash
# PyPI에 업로드
make release

# Token 입력:
# Username: __token__
# Password: pypi-AgEI...
```

---

## 🎯 방법 3: 수동 (세부 제어)

### 1. 버전 업데이트

```bash
# modi_plus/about.py
__version__ = "0.4.0"
```

### 2. HISTORY.md 업데이트

```bash
vi HISTORY.md
# v0.4.0 추가
```

### 3. 빌드

```bash
make clean
python3 -m build
```

### 4. 검증

```bash
twine check dist/*
```

### 5. TestPyPI (선택)

```bash
twine upload --repository testpypi dist/*
```

### 6. PyPI

```bash
twine upload dist/*
```

### 7. Git Tag

```bash
git tag -a v0.4.0 -m "Release v0.4.0"
git push origin v0.4.0
```

---

## 🔑 API Token 설정

### 한 번만 설정

```bash
# ~/.pypirc 파일 생성
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # 실제 token

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...  # 실제 token
EOF

chmod 600 ~/.pypirc
```

### Token 얻는 방법
1. PyPI 로그인: https://pypi.org
2. Account Settings → API tokens
3. "Add API token" 클릭
4. Token 복사

---

## ✅ 배포 완료 확인

### PyPI 페이지 확인
```
https://pypi.org/project/pymodi-plus/0.4.0/
```

### 설치 테스트
```bash
pip install --upgrade pymodi-plus
python3 -c "import modi_plus; print(modi_plus.__version__)"
# 0.4.0
```

---

## 🐛 문제 해결

### "File already exists"
→ 버전 번호를 증가시켜야 함 (같은 버전 덮어쓰기 불가)

```bash
# modi_plus/about.py
__version__ = "0.4.1"  # 증가
```

### "Invalid credentials"
→ Token이 잘못됨

```bash
# PyPI에서 새 token 생성
# .pypirc 업데이트
```

### 테스트 실패
→ 배포 전에 반드시 수정

```bash
make test
# 모든 테스트 통과 확인
```

---

## 📊 전체 프로세스 (One-liner)

### 개발 → 테스트 → 배포

```bash
# 한 번에 실행
make clean && \
make test && \
make dist && \
twine check dist/* && \
twine upload dist/* && \
git tag -a v0.4.0 -m "Release v0.4.0" && \
git push origin v0.4.0
```

---

## 📚 상세 가이드

전체 가이드: [PYPI_DEPLOYMENT_GUIDE.md](./PYPI_DEPLOYMENT_GUIDE.md)

---

## 💡 팁

### 배포 전 필수
- ✅ 모든 테스트 통과
- ✅ 버전 번호 업데이트
- ✅ HISTORY.md 업데이트
- ✅ PR 머지 완료

### TestPyPI 먼저
- 항상 TestPyPI에 먼저 배포해서 테스트
- 문제 없으면 PyPI에 배포

### 버전 규칙
- Patch (0.3.1 → 0.3.2): 버그 수정
- Minor (0.3.x → 0.4.0): 새 기능
- Major (0.x → 1.0): 호환 안되는 변경

---

## 🎉 완료 후

1. GitHub Release 생성
2. 팀원에게 공지
3. README 업데이트 (필요시)
4. 사용자 가이드 업데이트

---

**현재 버전:** 0.3.1
**다음 버전:** 0.4.0 (RGB 기능 추가)
