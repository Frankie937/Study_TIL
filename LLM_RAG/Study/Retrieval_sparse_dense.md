FAISS를 사용하여 벡터 DB를 로컬 파일로 구현하고 LangGraph로 Retrieval 노드를 구성할 때, 기본 설정으로 노드를 짜면 **의미 기반(Dense) 검색**으로 동작합니다.

FAISS 자체는 기본적으로 고성능의 밀집 벡터(Dense Vector) 유사도 검색(L2 거리, 내적, 코사인 유사도 등)에 특화되어 있는 라이브러리이기 때문입니다.

따라서 LangGraph의 Retrieval 노드에서 하이브리드 검색(Sparse + Dense)을 구현하려면, FAISS 단독 사용만으로는 부족하며 **두 가지 검색 결과를 결합하는 로직**을 추가해야 합니다.

---

### LangGraph에서 하이브리드 검색을 구현하는 방법

하이브리드 검색을 구성하려면 Retrieval 노드 내부에서 키워드 기반 검색과 FAISS 의미 기반 검색을 각각 수행한 뒤, 결과를 합쳐주는(Rerank 또는 Fusion) 과정이 필요합니다.

1. **검색기(Retriever) 구성:**
* **Sparse Retriever:** 키워드 매칭을 위해 BM25Retriever 등을 구성합니다. (파이썬의 `rank_bm25` 패키지나 LangChain의 `BM25Retriever` 활용)
* **Dense Retriever:** FAISS 벡터 스토어를 로드하여 `.as_retriever()`를 생성합니다.


2. **앙상블 (Ensemble):**
* LangChain의 `EnsembleRetriever`를 사용하면 BM25와 FAISS(Dense) retriever를 손쉽게 묶을 수 있습니다.
* 가중치(weight)를 조절하여 키워드 검색과 의미 검색의 비중을 조정할 수 있습니다. (예: BM25 0.3, FAISS 0.7)


3. **LangGraph Retrieval 노드 적용:**
* 노드 함수 내부에서 이 `EnsembleRetriever`를 호출하여 문서를 가져오도록 구현합니다.



---

### 구현 예시 코드 (개념)

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores import FAISS

# 1. FAISS 로드 (Dense)
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. BM25 로드 (Sparse - 원본 문서 텍스트 기반)
# docs는 FAISS를 만들 때 사용했던 전체 Document 리스트
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 3

# 3. 하이브리드 앙상블 Retriever 생성 (예: 키워드 30%, 의미 70%)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.3, 0.7]
)

# 4. LangGraph Retrieval 노드에서 활용
def retrieve_node(state):
    query = state["question"]
    retrieved_docs = ensemble_retriever.invoke(query)
    return {"documents": retrieved_docs}

```
