### 사용자 개인화 키워드 선호도 모델링"
: 선호도를 다이나믹하게 조정해가며 가중치 기반 추천 시스템을 만드는 방식


### 핵심 아이디어 
1. 사용자-키워드 테이블 유지
  - 각 사용자마다 키워드에 대한 선호도를 가중치(weight) 형태로 관리.
2. 행동 기반 선호도 조정
  - 부스트 (Boost): 특정 키워드를 클릭, 구매, 자주 조회하면 선호도 증가.
  - 패널티 (Penalty): 오랫동안 소비하지 않거나, 관심이 줄어든 경우 선호도 감소.
3. Decay (감쇠)
  - 시간이 지남에 따라 선호도 자연스러운 감소 적용 (예: 시간 기반 exponential decay).
4. 활용처: 추천, 콘텐츠 정렬, 마케팅 타겟팅 등.


### 선호도 수식 예시
```python 
preference_score = base_score + alpha * positive_actions - beta * negative_signals - gamma * time_decay
```
- base_score: 초기 가중치 (default = 0)
- positive_actions: 클릭, 구매 등 긍정 행동 수
- negative_signals: 무관심, 클릭 없음 등
- time_decay: 경과 시간에 따른 감소
- alpha, beta, gamma: 하이퍼파라미터 (튜닝 가능)

### 예제코드
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 예시: 사용자 행동 로그 데이터
data = [
    {'user_id': 1, 'keyword': 'laptop', 'action': 'click', 'timestamp': '2025-04-10'},
    {'user_id': 1, 'keyword': 'laptop', 'action': 'purchase', 'timestamp': '2025-04-11'},
    {'user_id': 1, 'keyword': 'book', 'action': 'view', 'timestamp': '2025-04-05'},
    {'user_id': 1, 'keyword': 'camera', 'action': 'ignore', 'timestamp': '2025-03-30'},
]

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 가중치 설정
action_weights = {
    'click': 2.0,
    'purchase': 5.0,
    'view': 1.0,
    'ignore': -3.0
}

# 현재 시간 기준 decay
def time_decay(days_passed, gamma=0.05):
    return np.exp(-gamma * days_passed)

# 사용자 키워드 선호도 계산
def compute_user_keyword_score(df, action_weights):
    now = datetime.now()
    keyword_scores = {}

    for _, row in df.iterrows():
        key = (row['user_id'], row['keyword'])
        days_ago = (now - row['timestamp']).days
        decay = time_decay(days_ago)

        score_delta = action_weights.get(row['action'], 0) * decay

        if key in keyword_scores:
            keyword_scores[key] += score_delta
        else:
            keyword_scores[key] = score_delta

    return pd.DataFrame([
        {'user_id': k[0], 'keyword': k[1], 'score': round(v, 2)}
        for k, v in keyword_scores.items()
    ])

# 실행
user_keyword_scores = compute_user_keyword_score(df, action_weights)
print(user_keyword_scores)

```
