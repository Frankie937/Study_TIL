## ColBERT (Contextualized Late Interaction over BERT) 모델이란?
ColBERT는 Facebook AI에서 개발한 효율적인 문서 검색 및 정보 검색(IR, Information Retrieval) 모델이다. 기존의 BERT 기반 검색 모델들은 연산량이 많아 실시간 검색에서 속도가 느리다는 단점이 있었다.
ColBERT는 "Late Interaction" (지연된 상호작용) 방식을 사용하여 빠른 검색과 높은 정확도를 동시에 달성한 모델이다.

### ColBERT의 핵심 개념: Late Interaction
ColBERT의 가장 큰 특징은 "Late Interaction" 구조다. 일반적인 BERT 기반 검색 모델과 비교해보자.

1) 기존 Dense 모델 (BERT-based Cross-Encoder)
  - 문장 쌍을 입력받아 하나의 벡터(임베딩) 로 변환
  - 문서 쌍을 직접 비교해야 하므로, 계산량이 많아 검색 속도가 느림
2) ColBERT (Late Interaction 방식)
  - 쿼리(Query)와 문서(Document)를 별도로 다수의 벡터(임베딩) 로 변환 (토큰 단위)
  - 사전에 문서의 토큰 임베딩을 계산해 저장해둠 (오프라인 계산 가능!)
  - 검색할 때는 쿼리의 임베딩과 문서 임베딩을 비교하여 빠르게 검색 수행

### ColBERT의 아키텍처 및 알고리즘
ColBERT의 모델 아키텍처는 크게 세 단계로 나뉜다.

1) 오프라인 임베딩 생성 (Pre-computed Document Encoding)
  - 문서(D) 내 각 토큰을 BERT를 통해 임베딩 벡터로 변환
  - 이 벡터들을 인덱싱하여 저장 (오프라인에서 계산 가능)

2) 실시간 검색 (Efficient Online Query Processing)
  - 쿼리(Q)의 각 토큰을 BERT를 통해 임베딩 변환
  - 저장된 문서 토큰 임베딩과 비교하여 가장 관련성 높은 문서를 찾음
    
3) Late Interaction 방식으로 유사도 계산
  - ColBERT는 문서와 쿼리를 비교할 때, **"최대 유사도 연산 (MaxSim)"**을 사용
  - 즉, 문서의 각 토큰과 쿼리의 각 토큰 간 코사인 유사도를 계산한 후, 쿼리 토큰별 가장 높은 유사도를 선택하여 최종 점수를 계산

### ColBERT의 장점: 왜 빠르게 서빙이 가능할까?
ColBERT가 빠르게 서빙할 수 있는 이유는 "Late Interaction" 구조 덕분에 문서 임베딩을 오프라인에서 미리 계산할 수 있기 때문이다.
이를 좀 더 자세히 설명하면 다음과 같다.

1. 문서 임베딩을 사전에 계산하여 저장 (Pre-computed Document Embeddings)
  - ColBERT는 문서의 모든 단어(토큰) 임베딩을 BERT를 통해 미리 계산하여 저장한다.
  - 기존의 BERT 기반 모델들은 검색할 때마다 문서를 BERT에 통과시켜야 하지만, ColBERT는 오프라인에서 미리 계산하므로 검색 시 연산량을 줄일 수 있다.
2. 실시간 검색 시에는 쿼리만 임베딩 변환 (Query Encoding at Runtime)
  - 검색할 때는 쿼리의 토큰만 BERT로 임베딩 변환하면 된다.
  - 문서의 임베딩을 다시 계산할 필요가 없으므로, 검색 속도가 빠름.
3. Late Interaction을 이용한 효율적인 비교
  - 쿼리의 각 토큰과 문서의 각 토큰 간의 유사도를 계산할 때,
  - MaxSim 연산을 사용하여 불필요한 연산을 줄인다.
  - 기존 Cross-Encoder 방식은 문장 전체를 비교하는 반면,
  - ColBERT는 각 토큰 단위로 독립적인 비교를 수행하여 병렬 처리 가능.
4. 효율적인 인덱싱과 검색 (FAISS와 결합 가능)
  - ColBERT는 문서의 임베딩을 인덱싱하여 저장할 수 있으며, FAISS(Facebook AI Similarity Search) 같은 고속 검색 라이브러리와 결합 가능.
  - 즉, ColBERT의 벡터들을 최근접 이웃 검색(ANN, Approximate Nearest Neighbor) 방식으로 검색하여 속도를 더욱 향상시킬 수 있음.

### ColBERT의 장점과 단점 비교
![image](https://github.com/user-attachments/assets/7b9c8fc3-f89d-4346-a472-c18a091a932d)

### ColBERT 활용 사례
1. 웹 검색 엔진
대량의 문서를 저장하고 빠르게 검색해야 하는 검색 엔진에서 ColBERT 활용
예: 구글, Bing 등의 웹 검색 기술

2. 전자상거래 검색 최적화
제품 검색 시 키워드 매칭이 아니라 의미 기반 검색을 수행
예: 아마존, 쿠팡 등의 쇼핑몰 검색 최적화

3. 대규모 문서 검색
법률 문서, 논문 검색, 뉴스 검색 등에서 활용 가능
예: Google Scholar, LexisNexis 같은 법률/학술 검색 엔진

### 결롱
  - ColBERT는 "Late Interaction" 구조를 통해 기존 BERT 기반 검색 모델의 속도 문제를 해결하고, 빠르고 정확한 검색을 가능하게 한 모델이다.
  - 특히, 문서의 임베딩을 미리 계산해 저장할 수 있기 때문에 실시간 검색 속도를 획기적으로 향상시킬 수 있다.
  - 검색 엔진, 전자상거래, 문서 검색 등에서 활용되며, FAISS 같은 고속 검색 라이브러리와 결합하면 더 강력한 성능을 발휘할 수 있다.


