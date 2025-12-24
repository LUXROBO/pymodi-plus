# 빠른 참조 가이드

## 🎯 목적별 파일 찾기

### 모델 학습하고 싶을 때
```bash
# 기본 모델
python train_rgb_model.py

# 개선 모델 (추천)
python train_rgb_model_enhanced.py

# Google Colab (교육용)
colab/train_rgb_model_enhanced_colab2.ipynb
```

### 실시간 테스트하고 싶을 때
```bash
# 기본 모델
python test_rgb_model_realtime.py

# 개선 모델 (추천)
python test_rgb_model_realtime.py --enhanced
```

### C 코드로 구현하고 싶을 때
```
📁 c_implementation/
   ├── rgb_color_sensor.h       ← 헤더 파일
   ├── rgb_color_sensor.c       ← 구현 파일
   └── rgb_model_coefficients.h ← 모델 계수
```

### 학습 데이터 확인하고 싶을 때
```
📁 data/
   ├── MODI RGB 센서 Sample 100 측정_Ethan.csv  ← CSV 형식
   └── MODI RGB 센서 Sample 100 측정_Ethan.xlsx ← Excel 형식
```

### Google Colab으로 학습하고 싶을 때
```
📁 colab/
   └── train_rgb_model_enhanced_colab2.ipynb ← 교육용 노트북
```

### 센서 스펙 확인하고 싶을 때
```
📁 docs/
   └── VEML6040.pdf ← 센서 데이터시트
```

### 학습 결과 확인하고 싶을 때
```
📁 models/
   ├── rgb_models.pkl              ← 기본 모델
   ├── rgb_models_enhanced.pkl     ← 개선 모델
   ├── feature_importance.json     ← 특징 중요도
   ├── model_performance.png       ← 성능 그래프
   └── residual_analysis.png       ← 잔차 분석
```

---

## 🚀 워크플로우

### 처음 시작하는 경우

1. **README.md** 읽기
2. **data/** 폴더의 CSV 확인
3. **train_rgb_model_enhanced.py** 실행
4. **test_rgb_model_realtime.py** 실행
5. 만족하면 **c_implementation/** 참조

### 모델 성능 개선하고 싶은 경우

1. **data/** 폴더에 새 학습 데이터 추가
2. **train_rgb_model_enhanced.py** 재실행
3. **models/feature_importance.json** 확인
4. 중요한 특징 선별
5. **test_rgb_model_realtime.py --enhanced** 검증

### C 코드에 통합하는 경우

1. **c_implementation/rgb_color_sensor.h** include
2. **c_implementation/rgb_color_sensor.c** 참조
3. **models/rgb_model_coefficients.h** 계수 확인
4. 임베디드 시스템에 통합

---

## 📞 문제 발생 시

1. **README.md** 의 "문제 해결" 섹션 확인
2. **FOLDER_CLEANUP_SUMMARY.md** 폴더 구조 재확인
3. GitHub Issues에 질문

---

## 🎓 학습용으로 사용하는 경우

**Google Colab 추천:**
- `colab/train_rgb_model_enhanced_colab2.ipynb` 업로드
- 단계별 실행하며 학습
- 중간 과정 시각화 확인

**Python 스크립트:**
- `train_rgb_model_enhanced.py` 코드 읽기
- 각 함수의 역할 이해
- `models/` 폴더의 결과 분석

---

## ✨ 팁

- 🔄 모델 재학습: `train_rgb_model_enhanced.py`
- 📊 성능 확인: `models/model_performance.png`
- 🎨 색상 테스트: `test_rgb_model_realtime.py --enhanced`
- 💻 C 구현: `c_implementation/` 폴더 참조
- 📖 상세 설명: `README.md`
- 📄 센서 스펙: `docs/VEML6040.pdf`

