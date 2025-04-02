### NRMS벡터란? 
- NRMS (Neural News Recommendation Model with Multi-Head Self-Attention) 벡터는 주로 뉴스 추천 시스템에서 활용되는 딥러닝 기반의 표현 벡터다.
- NRMS 모델은 사용자의 뉴스 소비 패턴을 학습하여 개별 뉴스 기사와 사용자의 관심사를 벡터 형태로 변환하고, 이를 기반으로 추천을 수행할 수 있다. 


### NRMS벡터의 장점 
- Self-Attention을 활용하여 뉴스 기사의 중요한 부분을 강조
- 사용자의 동적인 관심사를 반영하여 더 개인화된 추천 가능
- 빠른 계산 속도로 대규모 데이터에도 적용 가능


### NRMS 벡터를 활용한 실전 예제
- Microsoft의 NRMS 모델 구현( https://github.com/recommenders-team/recommenders)
- MIND Dataset을 활용한 뉴스 추천 실험
