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
