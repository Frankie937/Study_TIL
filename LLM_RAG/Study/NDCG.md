NDCG(Normalized Discounted Cumulative Gain) 

### 랭킹 모델에서 NDCG(정규화된 순위 평가 지표)의 개념과 계산 방식
추천 시스템에서 NDCG (Normalized Discounted Cumulative Gain) 는 추천된 아이템들의 순위 품질을 평가하는 랭킹 성능 지표이다. 

### NDCG의 핵심 개념
NDCG는 사용자가 실제로 관심을 가졌던 문서(혹은 상품)가 추천 결과에서 얼마나 높은 순위에 배치되었는지를 측정한다. 
- 높은 순위(Top)에 있는 추천이 더 중요한 가치를 가짐.
- 클릭, 구매, 좋아요 같은 사용자 피드백을 기반으로 추천 품질을 평가함.

### NDCG 계산 공식
NDCG는 두 가지 단계로 계산된다. 

(1) DCG (Discounted Cumulative Gain)
추천된 문서(상품) 리스트에서 가중합 점수(DCG)를 계산한다. 
![image](https://github.com/user-attachments/assets/60cc274d-cd28-4448-8693-b8c8ad89e02c)

(2) IDCG (Ideal DCG) & NDCG
DCG는 추천 품질을 측정할 수 있지만, 절대적인 값이라 비교가 어렵기 때문에 정규화된 값(NDCG)을 사용한다. 
![image](https://github.com/user-attachments/assets/6a3a5304-23cf-4afc-a800-133c3b107842)

### NDCG 예제 코드 
```python
import numpy as np

# 실제 관련도 (예: 클릭, 구매 여부)
relevance = [3, 2, 3, 0, 1, 2]  # 실제 유저 피드백

# DCG 계산 함수
def dcg(scores):
    return np.sum([
        rel / np.log2(idx + 2) for idx, rel in enumerate(scores)
    ])

# IDCG 계산 (이상적인 정렬)
ideal_relevance = sorted(relevance, reverse=True)
idcg = dcg(ideal_relevance)

# NDCG 계산
ndcg = dcg(relevance) / idcg
print(f"NDCG Score: {ndcg:.4f}")
```
- 높은 관련도의 문서가 더 상위에 위치할수록 점수가 높아짐.
- 로그 함수 때문에 순위가 낮아질수록 점수 기여도가 감소함.
