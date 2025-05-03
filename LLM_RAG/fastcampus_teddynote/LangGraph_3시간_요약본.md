
(영상 : https://www.youtube.com/watch?v=W_uwR_yx4-c) 
(유튜브 테디노트 - 영상제목 : #LangGraph 개념 완전 정복 몰아보기(3시간))

✅ 소스코드 링크: 
https://github.com/teddylee777/langchain-kr/tree/main/17-LangGraph/02-Structures
✅ 타임라인
  - 00:00 LangGraph 개요
  - 21:29 LangGraph 세부 기능(State, Node, Edge, Conditional Edge, Compile)
  - 46:56 LangGraph 로 자유롭게 그래프 로직 구성(흐름 엔지니어링)
  - 1:10:30 Naive RAG(전통적인 방식의 RAG) 를 LangGraph 로 구현
  - 1:31:43 답변의 할루시네이션 관련성 평가 모듈 추가
  - 1:43:28 웹 검색 노드 추가
  - 1:51:37 쿼리 재작성 모듈 추가
  - 2:00:55  [프로젝트] Agentic RAG - 에이전트를 활용한 RAG
  - 2:24:50  [프로젝트] Adaptive RAG


(아직 수정 중... 강의 들으면서 메모한 내용들) 

---

### LangGraph 개요

기존 langchain의 rag방식은 한 번에 잘해야 하는 부담
But, LangGraph는 노드의 흐름을 구성, 순환 가능 
즉, 다이나믹한 플로우 엔지니어링을 통해서 파이프라인을 좀 더 정교하게 만들 수 있음! 
LangGraph는 langchain의 dependency는 많이 줄어듦
모듈러 rag의 장점 - 모듈로 짜서 하나씩 조립하듯이 짜는 게 어렵지 않음

문서 검색 
검색 쿼리
쿼리 리라이트
분기 노드
검색 노드
등등 ... 흐름을 잘 짜줘야 함

노드들을 만드는 방법, 엣지들을 만드는 방법, 분기엣지를 만드는 방법 중요 

--- 

### LangGraph 세부 기능(State, Node, Edge, Conditional Edge, Compile)

* 구성요소 
  - state 상태관리 : 메세지 전달자 역할
  - node 노드 : python 함수 def
  - edge 엣지 : 노드 간 연결
  - graph workflow compile 시, checkpointer 굉장히 중요 - 수정 & 리플레이 가능

* state
  - 노드와 노드간에 정보를 전달할 때 state 객체에 담아 전달(graph 노드와 노드 간 공유하는 상태를 정의)
  - typedict : 파이썬의 dict에 '타입힌팅'을 추가한 개념 (쉽게 dictionary로 생각해도 됨)

* add_messages - reducer개념
  - messages를 주로 쌓을 때 사용
  - append 개념이 아닌라, 반환값에 리스트를 주기만 하면 자동으로 기존 리스트에 추가하는 개념(langgraph에서 쉽게 사용하기 위해 만든 개념)

** 랭그래프 문법은 굉장히 쉬움!, 어려운 건 핵심 로직에 들어가는 '좋은 품질의 노드'를 만드는 게 중요하고 어려울 수 있음!!
** 좋은 노드를 만드는 것-> python 함수의 좋은 품질의 노드를 구성하는 게 중요해짐!!

* RunnableConfig
  - recursion_limit - 순환로직 제한
  - thread_id -- configurable
	-  thread_id 별로 대화 내용을 따로 저장

** 처음부터 끝까지 모두 state를 입력받고 반환, 마지막 저장된 상태값들이 출력되는 것!!

---

### Naive RAG(전통적인 방식의 RAG) 를 LangGraph 로 구현

(1번 파일 : 기본 그래프 생성하는 과정)

* 기본 랭그래프 structure 구성 요소 
  - state정의
  - 노드정의
  - 그래프정의
  - 컴파일
  - 시각화

* set_entry_point : 시작점을 지정해주는 
* visualize_graph(app) : 랭그래프 구조 시각화 
* condidtional edge에서 사용하는 함수 - callable  - 호출가능한 함수

* 멀티 llm ?
	- llm을 하나만 쓰는 게 아니라 여러 개 쓰겠다는 것
  

* 테디노트님이 만든 format_docs 함수
  - 불필요한 토크낭비할 필요 없기에 필요한 컨텐츠 내용, 메타정보 중에서도 source(파일명), page(페이지정보) 정보만 따로 추출하도록 XML 형식 태깅을 걸어줘서 구분자까지 넣어서 포맷팅
  - 여러 개의 문자 리스트들을 하나의 문자열로 만들어주는


* 테디노트님이 만든 invoke_graph/stream_graph 함수
  - invoke_graph(app, inputs, config) -- 개발단계 확인 (노드의 반환값을 모두 확인하려면 invoke가 좋음)
  - stream_graph(app, inputs, config) -- 실제 서비스 할 때 확인


---

### 답변의 할루시네이션 관련성 평가 모듈 추가

- 검색된 문서에 대한 관련성 체크 추가 (groundedness check)
	-> conditional edge 사용 

* Groundnesschecker의 target 인자값
  - 질문과 검색한 문서의 관련성 체크를 할 때 target 인자 값으로는, "question-retrieval"
  - 질문과 답변의 관련성 체크를 할 때 target 인자 값으로는, "question-answer"


---

### 웹 검색 노드 추가

- 쿼리 변경없이 동일한 문서가 검색되고 있기 때문에 relevance check에 따라 검색을 다시 하는 게 아니라, 웹서치해서 문서를 보강하는 내용
- TavilySearch 사용 


--- 

### 쿼리 재작성 모듈 추가

Query Rewrite 모듈

** 기존에 question은 str로 받아서 overwrite하게 사용했는데, 원본을 왜 살려두는 걸까?
	- ui적인 면에서 유저가 실제 입력한 질문을 보여주는 건 그대로 해주는 게 좋기에
	- add_mesage reducer로 구현

---

### [프로젝트] Agentic RAG - 에이전트를 활용한 RAG

(6번 파일)
agentic rag
agent를 활용한 rag

* agent의 역할부분
	- "thought" 판단을 통해 tool을 사용해야 할 지, 안할 지 결정하는 게 있음
	- 무조건 적인 정해진 플로우에 매번 비효율적으로 행동하는 게 아닌게 큰 차이!!!

* create_retriever_tool 함수의 document_prompt 인자
	- 검색할 문서의 내용 뿐만 아니라 원하는 메타데이터를 효과적으로 반영해주기 위함
	- 원하는 메타데이터의 key값을 metadata 태그 안에 중괄호 활용하여 넣어주기
```python
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.prompts import PromptTemplate

# PDF 문서를 기반으로 검색 도구 생성
retriever_tool = create_retriever_tool(
    pdf_retriever,
    "pdf_retriever",
    "Search and return information about SPRI AI Brief PDF file. It contains useful information on recent AI trends. The document is published on Dec 2023.",
    document_prompt=PromptTemplate.from_template(
        "<document><context>{page_content}</context><metadata><source>{source}</source><page>{page}</page></metadata></document>"
    ),
)
``` 
