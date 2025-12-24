# MODI+ RGB 센서 보정 시스템

MODI+ Env 센서의 VEML6040 RGB 센서를 위한 머신러닝 기반 색상 보정 시스템입니다.

## 📁 프로젝트 구조

```
examples/test/
├── 📂 models/                          # 학습된 모델과 결과
│   ├── rgb_models.pkl                  # 기본 모델
│   ├── rgb_models_enhanced.pkl         # 개선 모델 ⭐
│   ├── rgb_model_coefficients.json     # JSON 계수
│   ├── feature_importance.json         # 특징 중요도
│   ├── model_performance.png           # 성능 그래프
│   └── residual_analysis.png           # 잔차 분석
├── 📂 data/                            # 학습 데이터
│   ├── MODI RGB 센서 Sample 100 측정_Ethan.csv
│   └── MODI RGB 센서 Sample 100 측정_Ethan.xlsx
├── 📂 c_implementation/                # C 코드 구현
│   ├── rgb_color_sensor.h              # 헤더 파일
│   ├── rgb_color_sensor.c              # 구현 파일
│   └── rgb_model_coefficients.h        # 모델 계수
├── 📂 colab/                           # Google Colab 노트북
│   └── train_rgb_model_enhanced_colab2.ipynb  # 교육용 노트북
├── 📂 docs/                            # 문서 및 스펙
│   └── VEML6040.pdf                    # 센서 데이터시트
├── train_rgb_model.py                  # 기본 모델 학습
├── train_rgb_model_enhanced.py         # 개선 모델 학습 ⭐
├── test_rgb_model_realtime.py          # 실시간 테스트
└── README.md                           # 이 문서
```

---

## 🚀 빠른 시작

### 1단계: 모델 학습

#### Option A: 기본 모델 (빠르고 간단)
```bash
cd examples/test
python train_rgb_model.py
```

**특징:**
- 입력: 4개 피처 (RAW_R, RAW_G, RAW_B, RAW_W)
- 학습 시간: ~5초
- 정확도: 좋음 (MAE ~18-21)
- C 구현: 쉬움

#### Option B: 개선 모델 ⭐ 추천
```bash
cd examples/test
python train_rgb_model_enhanced.py
```

**특징:**
- 입력: 16개 피처 (원본 + Lux 정규화 + White 비율 + Cross-channel)
- 학습 시간: ~5초
- 정확도: 우수 (MAE ~10-16, **38% 개선!**)
- C 구현: 중간 복잡도

**성능 비교:**

| 채널 | 기본 모델 MAE | 개선 모델 MAE | 개선율 |
|------|---------------|---------------|--------|
| R | 20.76 | **10.10** | **51% ⬇️** |
| G | 21.39 | **10.85** | **49% ⬇️** |
| B | 18.11 | 16.29 | 10% ⬇️ |
| **평균** | 20.09 | **12.41** | **38% ⬇️** |

### 2단계: 실시간 테스트

```bash
# 기본 모델 테스트
python test_rgb_model_realtime.py

# 개선 모델 테스트 (추천!)
python test_rgb_model_realtime.py --enhanced
```

**전제 조건:**
- MODI+ Env 모듈 연결
- RGB 지원 펌웨어 v2.x 이상

**출력 예시:**
```
M#1: RAW=(1325,921,364,2096) | RGB255=(227,122,0) | RGB100=(89,48,0) | W=116 B=139
```

**컨트롤 키:**
- `1` - 디스플레이 모드 전환 (Compact ↔ Detailed)
- `s` - 통계 표시
- `r` - 통계 리셋
- `q` - 종료

---

## 🎓 Google Colab에서 학습하기

교육용 Jupyter Notebook을 제공합니다. 단계별로 실행하며 학습할 수 있습니다.

### 사용 방법

1. [Google Colab](https://colab.research.google.com/) 접속
2. `colab/train_rgb_model_enhanced_colab2.ipynb` 업로드
3. 셀을 순서대로 실행

### 노트북 구성

1-3: 환경 설정  
4: CSV 데이터 업로드  
5-7: 데이터 전처리 (7단계로 세분화) + 중간 시각화  
8-9: 모델 학습 (R, G, B 채널별)  
10-15: 성능 분석 및 결과 저장  

**특징:**
- 📊 각 전처리 단계마다 결과 확인
- 📈 중간 과정 시각화 (Lux 분포, White 비율, Cross-channel)
- 📝 상세한 교육용 설명
- 💾 모델 자동 다운로드

---

## 🔬 VEML6040 센서 특성 기반 개선

### 센서 스펙
- **해상도**: 16-bit (0-65535) per channel
- **채널**: R, G, B, W (White)
- **Peak Wavelength**: R=650nm, G=550nm, B=450nm
- **Sensitivity**: 0.007865 lux/step

### 개선 기법

#### 1. Lux 정규화
```python
lux = RAW_W * 0.007865
R_norm = RAW_R / (lux + 1)
```
**효과**: 조명 밝기에 무관한 색상 정보

#### 2. White 채널 비율
```python
R_W_ratio = RAW_R / RAW_W
```
**효과**: 조명 종류 변화에 강인

#### 3. Cross-channel 특징
```python
total = RAW_R + RAW_G + RAW_B
DOM_R = RAW_R / total  # 색상 지배도
```
**효과**: 스펙트럼 중첩 영역 정보 활용

---

## 💻 C 코드 통합

### 기본 사용법

```c
#include "rgb_color_sensor.h"

int main(void) {
    struct RGB_color_data_t rgb;
    RGB_color_type_t color;
    
    // 센서 값 읽기
    uint16_t r_raw = 1325;
    uint16_t g_raw = 921;
    uint16_t b_raw = 364;
    uint16_t w_raw = 2096;
    
    // RGB 색상 계산
    color = calculate_RGB_color_v2(r_raw, g_raw, b_raw, w_raw, &rgb);
    
    // 결과 사용
    printf("RGB_100: R=%u G=%u B=%u\n", rgb.red, rgb.green, rgb.blue);
    printf("Color: %s\n", rgb_color_to_string(color));
}
```

### 출력 데이터 구조

```c
struct RGB_color_data_t {
    uint8_t red;      // 0-100% RED
    uint8_t green;    // 0-100% GREEN
    uint8_t blue;     // 0-100% BLUE
    uint8_t white;    // 0-100% WHITE 성분
    uint8_t black;    // 0-100% BLACK 성분
    uint8_t color;    // 분류된 색상
};
```

### 색상 분류

지원되는 색상:
- **기본**: Red, Green, Blue, Yellow, Cyan, Magenta
- **무채색**: Black, DarkGray, Gray, LightGray, White
- **변형**: DarkRed, LightRed, DarkGreen, LightGreen, DarkBlue, LightBlue
- **기타**: Unknown (분류 불가)

### 모델 계수 업데이트

1. Python에서 모델 학습:
   ```bash
   python train_rgb_model.py
   ```

2. 생성된 `c_implementation/rgb_model_coefficients.h` 확인

3. C 코드에 통합:
   ```c
   #include "rgb_model_coefficients.h"
   float r = predict_r(raw_r, raw_g, raw_b, raw_w);
   ```

---

## 📊 출력 데이터 설명

### 12개 값 출력

1. **RAW (4개)**: 센서 원시값 (0-65535)
2. **RGB_255 (3개)**: 보정된 RGB (0-255)
3. **RGB_100 (3개)**: 0-100 스케일 RGB
4. **Color (1개)**: 분류된 색상 이름
5. **White (1개)**: White 성분 (0-255)
6. **Black (1개)**: Black 성분 (0-255)

### Black/White 계산

**Color Theory 방식:**
```python
White = min(R, G, B)    # 공통 밝기
Black = 255 - max(R, G, B)  # 어두움 정도
```

**해석:**
- White = 0 → 순수 색상 (채도 높음)
- White > 0 → 흰색 섞임 (채도 낮음)
- Black = 0 → 밝은 색상
- Black > 0 → 어두운 색상

### 색상 분류 예시

| RGB | Color | White | Black | 설명 |
|-----|-------|-------|-------|------|
| (255, 0, 0) | Red | 0 | 0 | 순수 빨강 |
| (255, 200, 200) | LightRed | 200 | 0 | 분홍 (흰색 섞임) |
| (80, 0, 0) | DarkRed | 0 | 175 | 어두운 빨강 |
| (227, 122, 0) | Yellow | 0 | 28 | 노랑 |
| (128, 128, 128) | Gray | 128 | 127 | 회색 |

---

## 🔧 고급 기능

### 통계 표시 (키 's')

```
--- Statistics ---
Samples: 157
Average RGB: R=183.2 G=98.4 B=45.1
Std Dev: R=42.3 G=31.8 B=28.9
Min/Max R: 120/255 G: 45/180 B: 0/120
Color Distribution:
  Red: 45% (71 samples)
  Yellow: 30% (47 samples)
  Orange: 15% (24 samples)
  White: 10% (15 samples)
```

### 모델 비교

```bash
# 두 모델로 동시 테스트하여 비교
python test_rgb_model_realtime.py
python test_rgb_model_realtime.py --enhanced

# 예측 차이 확인
```

---

## 📈 성능 지표

### 평가 메트릭

- **MAE (Mean Absolute Error)**: 평균 절대 오차, 낮을수록 좋음
- **RMSE (Root Mean Squared Error)**: 큰 오차에 민감
- **R² Score**: 모델 설명력, 1에 가까울수록 좋음 (0.8+ 우수)

### 기대 성능

**기본 모델:**
- MAE: ~20
- R²: ~0.87-0.89

**개선 모델:**
- MAE: ~12 (38% 개선)
- R²: ~0.91-0.95

---

## 🛠️ 문제 해결

### 모델 파일 없음
```
✗ Error: Model file not found
```
**해결**: 먼저 학습 스크립트 실행
```bash
python train_rgb_model.py
```

### RGB 지원 안 됨
```
✗ RGB properties are NOT supported
```
**해결**: Env 모듈 펌웨어를 v2.x 이상으로 업그레이드

### 높은 예측 오차
- 더 많은 학습 데이터 수집 (다양한 색상/조명)
- 개선 모델 사용 (`train_rgb_model_enhanced.py`)
- 센서 각도 및 거리 최적화

### Unknown 색상이 자주 나옴
- 조명을 밝게 함
- 센서를 물체에 더 가까이 위치
- RGB 값이 모두 30 미만이거나 비슷한 경우 발생

---

## 📝 체크리스트

### 학습 단계
- [ ] 학습 데이터 준비 (CSV)
- [ ] 기본 모델 학습 (`train_rgb_model.py`)
- [ ] 개선 모델 학습 (`train_rgb_model_enhanced.py`)
- [ ] 성능 비교 및 모델 선택

### 테스트 단계
- [ ] Python 실시간 테스트
- [ ] 다양한 색상/조명에서 검증
- [ ] 통계 수집 및 분석

### 배포 단계
- [ ] C 코드로 포팅
- [ ] 임베디드 시스템에 통합
- [ ] 최종 검증

---

## 🔗 참고 자료

### 내부 문서
- `docs/VEML6040.pdf` - VEML6040 센서 데이터시트
- `c_implementation/` - C 구현 예제
- `models/` - 학습된 모델 및 결과

### 관련 파일
- `../../docs/features/ENV_RGB_FEATURE.md` - 특징 엔지니어링 설명
- `../../docs/features/ENV_RGB_EXAMPLES.md` - 사용 예제

---

## 📞 도움말

문제가 발생하면:
1. 이 README의 문제 해결 섹션 확인
2. GitHub Issues에 질문
3. 예제 코드 참조

---

**Made with ❤️ for MODI+**
