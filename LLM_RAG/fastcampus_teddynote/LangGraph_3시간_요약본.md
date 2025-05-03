(영상 : https://www.youtube.com/watch?v=W_uwR_yx4-c) 

(아직 수정 중... 강의들으면서 메모한 내용들) 

################# langgraph 3시간 요약 #################

기존 langchain의 rag방식은 한 번에 잘해야 하는 부담
But, LangGraph는 노드의 흐름을 구성, 순환 가능 
즉, 다이나믹한 플로우 엔지니어링을 통해서 파이프라인을 좀 더 정교하게 만들 수 있음! 
LangGraph는 langchain의 dependency는 많이 줄어듦

문서 검색 
검색 쿼리
쿼리 리라이트
분기 노드
검색 노드
등등 ... 흐름을 잘 짜줘야 함

노드들을 만드는 방법, 엣지들을 만드는 방법, 분기엣지를 만드는 방법 중요 

* 구성요소 
  - state 상태관리 : 메세지 전달자 역할
  - node 노드 : python 함수 def
  - edge 엣지 : 노드 간 연결
  - graph workflow compile 시, checkpointer 굉장히 중요 - 수정 & 리플레이 가능

* state
  - 노드와 노드간에 정보를 전달할 때 state 객체에 담아 전달
  - typedict : 파이썬의 dict에 '타입힌팅'을 추가한 개념 (쉽게 dictionary로 생각해도 됨)

* add_messages - reducer개념
  - messages를 주로 쌓을 때 사용
  - append 개념이 아닌라, 반환값에 리스트를 주기만 하면 자동으로 기존 리스트에 추가하는 개념(langgraph에서 쉽게 사용하기 위해 만든 개념)

** 랭그래프 문법은 굉장히 쉬움!, 어려운 건 핵심 로직에 들어가는 '좋은 품질의 노드'를 만드는 게 중요하고 어려울 수 있음!!
** 좋은 노드를 만드는 것-> python 함수의 좋은 품질의 노드를 구성하는 게 중요해짐!!

* RunnableConfig
  - recursion_limit - 순환로직 제한
  - thread_id -- configurable
	-> thread_id 별로 대화 내용을 따로 저장

** 처음부터 끝까지 모두 state를 입력받고 반환, 마지막 저장된 상태값들이 출력되는 것!!

---

< 랭그래프 structure 구조 실행 코드 강의 >

1번 기본 그래프 생성하는 과정

state정의
class GraphState(TypedDict):
context: Annotated[List[Document], operator.add]
노드정의

def retrieve_documnet(state: GraphState) -> GraphState:
retreived_docs
그래프정의
컴파일
시각화

2~5번

6번 agent

7번 adaptive rag

from to

set_entry_point
visualize_graph(app)
context
question
answer
relevance_check
langgraph.graph StateGraph
langgraph
conventional RAG
workflow.add_conditional
langgraph 장점
gpt relevance_check
retrieve
add_coditional_edges

callable - 호출가능한 함수

멀티 llm ?
-> llm을 하나만 쓰는 게 아니라 여러 개 쓰겠다는 것

함수의 구현체는 없음

## 이후 문제는 더 쉽게 풀 수 있습니다.

naive rag를 랭그래프로 구현

2~5번 파일 코드 -- 쭉 이어지는 내용이 이어짐

기본 pdf 기반 retrieval chain 생성

state 정의
graph 노드와 노드 간 공유하는 상태를 정의

하나의 문자열 형태로 가공해서 넣어주겠다는 것

add_message - reducer 함수

naive rag

format_docs(docs: Any -> GraphState
불필요한 토크낭비할 필요 없음
필요한 메타데이터만

page 정보
소스정보 (파일명, 페이지정보)
포맷팅 10개의 문자를 하나로 만들어주는

def llm_answer(state : GraphState) -> GraphStaet:
latest_questioin = state["question"]
context= state["context"]
response = pdf_chain.invoke({
"question" : latest_question,
"
"chat_history" : messages_to_history(stae["messages"]

```
	}
)

```

XML 형식 태깅을 걸어줘서 구분자까지 넣어서 포맷팅

retrieve
generate

response = pdf
chat_history
add_message

messages_to_history

pdf_chain
question
context
chat_history

Edges
workflow = StateGraph(GraphState)
config
recursion_limit
stream_graph
invoke_graph

반환되는 값을 보면
llm_answer
answer
invoke
stream
debuging
노드의 반환값을 모두 확인하려면 invoke가 좋음

invoke_graph(app, inputs, config) -- 개발단계 확인
stream_graph(app, inputs, config) -- 실제 서비스 할 때 확인

inovke_graph

---

< 관련성 체크 >

-검색된 문서에 대한 관련성 체크 추가
groundedness check
conditional edge

Groundnesschecker - target = "question-retrieval"
def relevance_checker

relevant llm answer
not relevant retrieve
recursion_error

relevance_check
retrieve

query_rewrite

---

< 웹검색 모듈 추가 >

쿼리 변경없이 동일한 문서가 검색되고 있기 때문에
relevance check에 따라 웹서치해서 문서를 보강하는 내용으로
TavilySearch

노드로 패키징
def web_search(state: GraphState) -> GraphState:
retrieve > relevance_check > websearch

---

< 쿼리재작성 모듈 추가 >

Query Rewrite 모듈
모듈러 rag의 장점 - 모듈로 짜서 하나씩 조립하듯이 짜는 게 어렵지 않음

기존에 question은 str로 받아서 overwrite하게 사용했는데,
원본을 왜 살려두는 걸까?
ui적인 면에서 유저가 실제 입력한 질문을 보여주는 건 그대로 해주는 게 좋기에
add_mesage reducer로 구현

---

< Agentic 프로젝트 >

6번 파일
agentic rag

agent를 활용한 rag

agent의 역할부분
-> "thought" 판단을 통해 tool을 사용해야 할 지, 안할 지 결정하는 게 있음
-> 무조건 적인 정해진 플로우에 매번 비효율적으로 행동하는 게 아닌게 큰 차이!!!
->
