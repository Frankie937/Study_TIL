### NRMS벡터란? 
- NRMS (Neural News Recommendation Model with Multi-Head Self-Attention) 벡터는 주로 뉴스 추천 시스템에서 활용되는 딥러닝 기반의 표현 벡터이다. 
- NRMS 모델은 사용자의 뉴스 소비 패턴을 학습하여 개별 뉴스 기사와 사용자의 관심사를 벡터 형태로 변환하고, 이를 기반으로 추천을 수행할 수 있음 
- NRMS 벡터는 뉴스 문서와 사용자의 관심을 표현하는 벡터로, NRMS 모델에서 다음과 같은 과정으로 생성된다.
    * 뉴스 인코딩 (News Encoder)
      - 개별 뉴스 기사는 Word Embedding (예: Glove, FastText)과 CNN 또는 Multi-Head Self-Attention을 사용하여 벡터로 변환됨.
      - 이 과정에서 중요한 단어들이 강조되어 뉴스의 중요한 의미를 담은 벡터가 생성됨.
    * 사용자 인코딩 (User Encoder)
      - 사용자가 읽은 여러 뉴스 기사 벡터를 하나의 벡터로 합쳐 사용자의 관심사를 나타냄.
      - Self-Attention을 사용하여 사용자 관심사를 동적으로 조정하여 최종 사용자 벡터를 생성.
    * 추천 점수 계산 (Matching & Ranking)
      - 뉴스 벡터와 사용자 벡터 간 내적(dot product) 또는 유사도 연산을 통해 추천 점수를 계산.
      - 추천 점수가 높은 뉴스가 사용자에게 추천됨

### 추천 시스템에서 NRMS 벡터 활용 방법
NRMS 벡터는 다음과 같은 방식으로 추천 시스템에 적용될 수 있다.

1) 뉴스 추천
뉴스 기사 데이터를 임베딩하여 벡터화한 후, 사용자의 관심사 벡터와 비교하여 개인화된 뉴스 추천을 수행.

2) 콘텐츠 기반 추천 (Content-Based Filtering)
뉴스뿐만 아니라 영화, 블로그, 논문 추천에도 적용 가능. 
사용자가 이전에 소비한 콘텐츠와 유사한 항목을 추천하는 방식으로 활용.

3) 협업 필터링 (Collaborative Filtering)과 결합
NRMS 벡터를 Latent Factor 모델과 결합하여 추천 품질을 향상.
예를 들어, Hybrid Recommendation System에서 콘텐츠 기반 벡터(NRMS)와 사용자-아이템 행렬을 함께 활용할 수 있음.


### NRMS벡터의 장점 
- Self-Attention을 활용하여 뉴스 기사의 중요한 부분을 강조
- 사용자의 동적인 관심사를 반영하여 더 개인화된 추천 가능
- 빠른 계산 속도로 대규모 데이터에도 적용 가능


### NRMS 벡터를 활용한 실전 예제
- Microsoft의 NRMS 모델 구현( https://github.com/recommenders-team/recommenders)
- MIND Dataset을 활용한 뉴스 추천 실험 (https://msnews.github.io/)
  
