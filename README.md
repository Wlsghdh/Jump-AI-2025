# Jump AI 2025: 제3회 AI 신약개발 경진대회 🧬

## 대회 개요

### 배경
AI 신약개발 생태계 활성화와 AI 신약 개발 젊은 연구원들의 의욕 고취 및 인재 유입을 위해 개최된 경진대회입니다.

### 주제
**MAP3K5 (ASK1) IC50 활성값 예측 모델 개발**

### 과제 설명
- PubChem, ChEMBL, CAS 등에서 수집한 실험 기반 화합물 정보를 활용
- 127종 화합물의 구조 정보(SMILES)를 입력값으로 사용
- 해당 화합물들의 ASK1에 대한 IC50 값을 예측

### 주최/주관/운영
- **주최/주관**: 한국제약바이오협회
- **후원**: 보건복지부, 유한양행, CAS
- **운영**: 데이콘

---

## 솔루션 개요

본 프로젝트는 **분자 정보학(Cheminformatics)과 앙상블 머신러닝**을 결합한 IC50 예측 모델입니다.

### 🔬 핵심 접근법

#### 1. 분자 특성 추출 (Feature Engineering)
- **분자 기술자**: RDKit을 활용하여 29개의 화학적 특성 계산
  - 분자량, LogP, TPSA, 회전 가능한 결합 수
  - Lipinski의 5 법칙 위반 개수
  - 방향족/지방족 고리 정보 등
- **Morgan Fingerprint**: 1024-bit 구조적 fingerprint → PCA로 100차원 압축

#### 2. 다중 스케일링 전략
```python
scalers = {
    'standard': StandardScaler(),      # 표준 정규화
    'robust': RobustScaler(),          # 이상치에 강한 정규화  
    'quantile': QuantileTransformer()  # 정규분포 변환
}
```

#### 3. 앙상블 모델 구성
- **LightGBM**: 그래디언트 부스팅 (메인 모델)
- **XGBoost**: 그래디언트 부스팅
- **Random Forest**: 배깅 기반 트리 앙상블
- **Extra Trees**: 극도 랜덤화 트리
- **MLP**: 다층 퍼셉트론 신경망

#### 4. 하이퍼파라미터 최적화
- **Optuna**를 활용한 베이지안 최적화
- 5-Fold Cross Validation으로 모델 성능 평가
- 각 모델별 30회 시행으로 최적 파라미터 탐색

#### 5. 고급 앙상블 기법
```python
# 1단계: 가중 평균 최적화
optimal_weights = minimize(ensemble_objective)

# 2단계: Quantile Matching
matched_predictions = quantile_match(predictions, base_pred)

# 3단계: 메타 앙상블
final_pred = 0.6 × weighted_ensemble + 0.4 × quantile_matched_ensemble
```

---

## 📁 프로젝트 구조

```
Jump_AI_2025/
├── Jump_AI (2).ipynb          # 메인 모델링 노트북
├── data/
│   ├── chembl_processed_rescaled.csv  # 훈련 데이터
│   └── test.csv                       # 테스트 데이터
└── submissions/
    ├── submit_conservative_enhanced.csv
    ├── submit_conservative_weighted_only.csv
    ├── submit_conservative_quantile_matched.csv
    └── submit_conservative_final_meta.csv
```

---

## 🚀 실행 방법

### 필요한 라이브러리
```bash
pip install pandas numpy scikit-learn
pip install lightgbm xgboost catboost
pip install optuna rdkit-pypi
pip install scipy
```

### 실행
```bash
jupyter notebook "Jump_AI (2).ipynb"
```

---

## 🧪 모델 성능

### 검증 데이터 성능
- **LightGBM**: RMSE=0.8587, R²=0.3449
- **XGBoost**: RMSE=0.8653, R²=0.3348  
- **Random Forest**: RMSE=0.8954, R²=0.2877

### 최적 가중치
- **LightGBM**: 72.5%
- **XGBoost**: 27.5%

---

## 🔍 주요 특징

1. **QSAR 모델링**: 분자 구조-활성 관계 예측
2. **견고한 앙상블**: 5개 서로 다른 알고리즘 조합으로 과적합 방지
3. **분포 정렬**: Quantile matching으로 모델 간 예측 분포 차이 보정  
4. **다단계 최적화**: Optuna + 가중치 최적화 + 메타 앙상블
5. **물리적 제약**: IC50 값을 생물학적으로 합리적인 범위로 클리핑

---

## 📊 데이터 전처리

### IC50 → pIC50 변환
```python
# 로그 스케일 변환으로 넓은 범위의 IC50 값 정규화
df_train["pIC50"] = 9 - np.log10(df_train["IC50"])
```

### 후처리
```python
# pIC50 → IC50 역변환 및 클리핑
ic50_pred = 10 ** (9 - final_pred)
ic50_pred = np.clip(ic50_pred, 0.1, 100000)  # nM 단위
```

---

## 🎯 결과

다양한 앙상블 전략으로 여러 submission 파일 생성:
- `weighted_only`: 단순 가중 평균
- `quantile_matched`: 분포 정렬 앙상블  
- `final_meta`: 메타 앙상블 (최종 제출)

---

**신약 개발의 미래를 AI와 함께! 🚀**