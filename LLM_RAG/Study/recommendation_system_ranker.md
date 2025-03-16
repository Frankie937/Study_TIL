### 추천 시스템에서 랭커의 역할
추천 시스템은 보통 두 단계로 이루어져 있다. 

1) Retrieval (초기 후보군 선정)
  - 수천~수백만 개의 문서/상품 중에서 대략적인 후보군(Top-K)을 뽑음
  - 이 과정은 주로 협업 필터링(Collaborative Filtering), 콘텐츠 기반 필터링(Content-Based Filtering), 혹은 ANN(Approximate Nearest Neighbor) 검색 을 활용함.
2) Ranking (정확한 순위 매기기, 랭커)
  - Retrieval 단계에서 선택된 후보군(예: Top 100)에서 가장 적합한 문서를 정밀하게 평가하여 순위를 매김
  - 여기서 머신러닝 모델이 사용되며, 사용자의 행동 데이터, 콘텐츠 특성, 메타데이터 등 다양한 피처를 고려함.

### 문서나 상품의 순위를 매기는 방식
랭커는 보통 기계 학습 기반 모델을 사용해서 각 문서나 상품의 "적합도 점수" 를 예측한 후, 점수가 높은 순으로 정렬해. 대표적인 알고리즘은 다음과 같아.

1. 선형 회귀 (Linear Regression)
간단한 방법으로, 여러 피처를 가중합하여 점수를 계산하는 방식.
하지만 실제 추천에서는 비선형 관계를 잘 반영하지 못해서 잘 쓰이지 않음.
2. 랜덤 포레스트 (Random Forest)
여러 개의 의사결정 트리를 앙상블하여 예측하는 방식.
비선형 관계를 잘 잡아낼 수 있지만, 추천 성능이 최적화되지는 않음.
🔹 3. XGBoost / LightGBM (Gradient Boosting Machines)
가장 널리 쓰이는 랭킹 모델 중 하나.
여러 피처를 학습하여 가중치를 최적화하고, 최적의 추천 순서를 결정함.
4. 신경망 기반 모델 (Neural Network)
딥러닝을 활용한 DNN(Deep Neural Network) 모델.
특히 YouTube, TikTok, Amazon 같은 플랫폼에서 많이 활용 됨.
딥러닝 모델은 사용자의 클릭, 시청 시간, 좋아요, 장바구니 추가 등의 데이터를 학습하여 추천 품질을 극대화함.

### "Feature로 추가한다"는 의미
랭커가 문서를 정렬할 때 사용하는 다양한 입력 변수(피처, Feature) 가 있어. 예를 들어:

1. 콘텐츠 관련 피처
  - 문서의 카테고리 (예: 패션, 전자기기, 스포츠)
  - 문서의 길이 (예: 500자, 1000자 등)
  - 이미지 포함 여부
2. 사용자 관련 피처
  - 사용자의 연령대 (예: 20대, 30대, 40대)
  - 사용자의 성별 (예: 남성, 여성)
  - 사용자의 검색 이력
3. 행동 관련 피처
  - 해당 문서의 클릭 수
  - 좋아요 수
  - 이전에 비슷한 문서를 본 사용자들의 평균 체류 시간
위 피처들을 모델에 입력하면, 모델이 "이 사용자는 어떤 문서를 더 좋아할 확률이 높을까?" 를 예측하는 점수를 산출한다. 

### 예제 코드 (LightGBM을 사용한 추천 랭커)
아래는 사용자의 연령과 성별을 피처로 추가하여 추천 랭킹을 학습하는 코드 예제이다.

``` python
복사
편집
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import ndcg_score

# 예제 데이터 생성 (사용자 ID, 문서 ID, 연령대, 성별, 클릭 여부)
data = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'document_id': [101, 102, 103, 101, 104, 102, 103, 104],
    'age_group': [20, 30, 40, 30, 20, 40, 30, 20],  # 연령대 피처
    'gender': [0, 1, 1, 0, 1, 0, 1, 0],  # 성별 피처 (0=여성, 1=남성)
    'click': [1, 0, 1, 1, 0, 1, 0, 1]  # 클릭 여부 (타겟 값)
})

# 입력(X)과 타겟(y) 분리
X = data[['age_group', 'gender']]
y = data['click']

# 데이터 분할 (훈련 80%, 테스트 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM 데이터셋 생성
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

# 모델 설정
params = {
    'objective': 'binary',  # 이진 분류 (클릭 예측)
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'learning_rate': 0.1,
    'num_leaves': 31
}

# 모델 학습
model = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=100, early_stopping_rounds=10)

# 예측
y_pred = model.predict(X_test)

# NDCG 평가 (랭킹 품질 측정)
ndcg = ndcg_score([y_test], [y_pred])
print(f"NDCG Score: {ndcg:.4f}")
```
(코드설명) 
- 데이터셋 생성: 사용자 연령과 성별을 피처로 포함
- LightGBM 모델 학습: 클릭 확률을 예측하도록 모델 학습
- NDCG(Normalized Discounted Cumulative Gain) 점수 계산: 추천 랭킹의 품질 평가

### 요약 
- 랭커(Ranker)는 추천 후보군을 정렬하는 역할
- LightGBM, XGBoost, DNN 등 다양한 모델이 사용됨
- 사용자 연령, 성별 같은 정보(Feature)를 모델에 추가하여 더 개인화된 추천 가능
