### ANN(Approximate Nearest Neighbors) 이란? 
대량의 벡터 데이터에서 특정 벡터와 가장 가까운 벡터를 빠르게 찾는 기법

### FAISS(Facebook AI Similarity Search) 라이브러리를 활용하여 ANN(Approximate Nearest Neighbor) 기반의 유사 문서 검색 서비스를 구현하는 예제 코드
(** 오픈 데이터셋인 quora question pairs 활용 > 문장 임베딩을 생성한 후, 유사한 질문을 검색하는 예제) 
(SentenceTransformers 모델을 사용하여 문장을 벡터로 변환 > FAISS를 활용해 빠르게 유사한 질문을 검색하는 프로세스) 
```python 

### 데이터로드 및 전처리 
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1. 데이터셋 로드 (Quora Question Pairs 데이터셋 사용)
url = "https://raw.githubusercontent.com/zhiyzuo/Quora-Question-Pairs/master/data/quora_duplicate_questions.tsv"
df = pd.read_csv(url, sep="\t")

# 2. 데이터 정리 (중복 제거 후, 질문 리스트 만들기)
df = df.dropna(subset=["question1", "question2"])  # 결측값 제거
questions = pd.concat([df["question1"], df["question2"]]).unique()  # 중복 제거

# 3. 일부 샘플만 사용 (속도 최적화를 위해 10,000개만 사용)
questions = questions[:10000]

print(f"총 {len(questions)}개의 질문이 로드되었습니다.")


### 임베딩 벡터 생성 
# 1. Sentence-BERT 모델 로드
model = SentenceTransformer("all-MiniLM-L6-v2")  # 가벼운 모델

# 2. 질문들을 벡터로 변환
question_embeddings = model.encode(questions, convert_to_numpy=True)

# 3. 벡터 차원 확인
print(f"임베딩 벡터 차원: {question_embeddings.shape}")  # (10000, 384)


### FAISS를 활용한 ANN 인덱스 구축
# 1. FAISS Index 생성 (L2 거리 기반)
embedding_dim = question_embeddings.shape[1]  # 384 차원
index = faiss.IndexFlatL2(embedding_dim)

# 2. 벡터 데이터 추가 (질문 벡터 저장)
index.add(question_embeddings)

# 3. 인덱스에 저장된 벡터 개수 확인
print(f"FAISS에 저장된 벡터 개수: {index.ntotal}")


### 유사 질문 검색 함수 구현
def search_similar_questions(query, top_k=5):
    """입력된 질문과 가장 유사한 질문들을 검색"""
    
    # 1. 입력 문장을 벡터로 변환
    query_vector = model.encode([query], convert_to_numpy=True)
    
    # 2. FAISS를 활용하여 ANN 검색
    distances, indices = index.search(query_vector, top_k)
    
    # 3. 검색 결과 출력
    print(f"\n '{query}' 와 가장 유사한 질문들:")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. {questions[idx]} (거리: {distances[0][i]:.4f})")

# 테스트 실행
search_similar_questions("How to learn machine learning?")

``` 
### distances, indices = index.search(query_vector, top_k) 코드에서 index.search() 내부동작 원리
- 벡터로 변환된 유저 쿼리, query_vector를 FAISS Index에서 top_k개의 가장 가까운 벡터를 검색
- 검색된 문서들의 인덱스(indices)와 거리(distances) 반환
- 즉, 주어진 쿼리 벡터와 가장 유사한 벡터를 찾는 과정이 여기서 실행돼.
- 여기서 사용하는 index.search()의 동작 방식은 FAISS Index 타입에 따라 다르다.


### FAISS index 생성 이유? 
FAISS(Facebook AI Similarity Search)는 대량의 벡터 데이터에서 빠르게 유사한 벡터를 찾기 위한 라이브러리이다. 
문장을 벡터로 변환했으니, 유사한 문장을 빠르게 검색할 수 있어야 하는데 이때, FAISS Index를 생성해서 효율적으로 벡터를 저장하고 검색할 수 있도록 하는 것 
