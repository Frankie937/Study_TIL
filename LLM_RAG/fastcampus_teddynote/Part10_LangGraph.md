### Ch1. LangGraph 개요

### Ch2. LangGraph 핵심 기능

08-09- 중간 단계의 상태 수동 업데이트 

- tool messages id 중요
- reducer 기능이 있기 때문에 id가 다르면 추가해주지만, id가 같으면 교체시켜줌

(add_message reducer 기능 )

(** 참고: query 부분이 지금 웹 검색에 넣을 검색 내용인데 구글링 문법으로 검색어 + [ site: 사이트주소 ] 로 검색하면 그 웹 사이트 한 정해서 검색해줌! )

![image](https://github.com/user-attachments/assets/81a7ebce-06a5-4f35-afa6-cb5daf3fe7d8)

-> 이 기능의 요지는, 검색할 query를 llm이 만드는데 그 query가 대부분 맘에 안들 때가 있다. 그때 interrupt해서 직접 검색 query를  수정할 수 있는 프로세스를 만들 수 있음

10. **지난 스냅샷의 결과 수정 및 Replay**

프로세스가 다 끝난 상태에서 다시 되짚어보니 어떤 부분이 맘에 안들었었네 하고 수정하고 다시 한 번 리플레이를 하는 기능 

11 . 사람의 의견을 묻는 노드 추가

→ 그래프가 항상 멈추는 **"human" 노드** 를 생성하는 것입니다. 이 노드는 LLM이 "human" 도구를 호출할 때만 실행됩니다. 편의를 위해, 그래프 상태에 "ask_human" 플래그를 포함시켜 LLM이 이 도구를 호출하면 플래그를 전환하도록 할 것

12. RemoveMessages 로 메시지 기록 삭제
`RemoveMessage` reducer 기능으로 동일한 id에 밀어넣으면 삭제하는 기능 

13. ToolNode 활용법(2개 이상의 도구 사용)
도구는 우리 로컬PC에서 호출이 일어나는 것이다 
llm같은 경우 gpt 모델을 쓰게 되면 opne ai사의 서버에 요청해서 호출이 일어나는 API 호출방식이지만, 도구는 LLM에게 이러이러한 도구들이 준비되어 있다고 LLM에게 정보를 쥐어주면 사용자의 입력이 들어왔을 때 LLM이 어떤 도구를 사용했으면 좋겠다고 알려만 주고 그 특정 도구를 우리PC에서 호출이 일어나는 것 !! 
 (**이러한 로직으로  흐름이 이어기는데, LangGraph 안에서 도구를 하나의 노드로 인식하게 하기 위해 `ToolNode`라는 것으로 감싸서 패키징 처리를  하는 것)

14.  병렬 노드의 처리(fan-out, fan-in) 및 우선순위 설정
동시다발적으로 여러 프로세스를 한 방에 처리할 수 있도록 만들어주는 기능 (이전까지는 조건부 노드로 구성했었음) 
** superstep(여러 노드들이 처리되는 전체 프로세스 스텝) 내에서 노드를 실행하는데, 이는 병렬 분기가 동시에 실행되더라도 전체 superstep이 트랜잭션 방식(모았다가 한번에 처리)으로 처리됨을 의미함. 따라서 이러한 분기 중 하나라도 예외가 발생하면 상태에 대한 업데이트가 전혀 적용되지 않음 (전체 superstep이 오류처리됨)
**신뢰도(가중치 개념)를 두어서 병렬 step 노드의 순서를 변경할 수 도 있음 

15.  대화 기록의 요약을 노드로 추가
대화가 길어질 땐 요약노드를 추가하여 토큰비용을 아낄 수 있음 

16. 그래프에 서브 그래프(SubGraph) 를 추가하는 방법
스키마를 공유하게 되면 subgraph 노드로서 그냥 추가하면 되지만, 상태공유를 하지 않는 경우에(스키마가 다를 경우) 별도로 변한하는 노드를 만들어서 invoke를 통해서 상태 변환하는 로직을 추가해주고 수행을 해야  함 
 
17. 2개 이상의 SubGraph 추가 및 상태 변환(State Transformation)

18.  LangGraph 출력 스트리밍(토큰 단위 스트리밍, tag 필터링)

**- steam_mode = “values”일 때** 
    
    `chunk.items()`
    
    - `key`: State 의 key 값
    - `value`: State 의 key 에 대한하는 value

    **-  steam_mode = “updates”일 때** 

`chunk.items()`

- `key`: 노드(Node) 의 이름
- `value`: 해당 노드(Node) 단계에서의 출력 값(dictionary). 즉, 여러 개의 key-value 쌍을 가진 dictionary 입니다.

**- steam_mode = “messages”일 때 (**토큰단위의 출력 원할 떼!!!)**
`messages` 모드는 각 단계에 대한 메시지를 스트리밍합니다.

`chunk` 는 두 개의 요소를 가진 tuple 입니다.

- `chunk_msg`: 실시간 출력 메시지
- `metadata`: 노드 정보

### Ch3. LangGraph 구조 설계

01. LangGraph로 자유롭게 그래프 로직 구성(흐름 엔지니어링) 

- LangGraph의 그래프 정의
    - State 정의
    - 노드 정의
    - 그래프 정의
    - 그래프 컴파일
    - 그래프 시각화
```python
# state 정의
class GraphState(TypeDict):
	context : Annotated[List[Document], operator.add]
	answer : Annotated[List[Documnet], operator.add]
	question : Annotated[str, "user question"]
	sql_query : Annotated[str, "sql query"]
	binary_score : Annotated[str, "binary score yes or no"]

# 노드 정의 

def retrieve(state : GraphState) -> GraphState : 
	documents = "검색된 문서" 
	return GraphState(contexts = documents)



# 그래프 정의 
workflow = StateGrpah(GraphState)

workflow.add_node("retireve", retrieve)
...
workflow.add_edge("retrieve", "GPT 요청")
...
workflow.set_entry_point("retrieve") # 시작점 설정

momory = MemeorySaver() # 기록을 위한 메모리 저장소 설정 

# 그래프 컴파일 
app = workflow.compile(checkpointer = memeory)  


# 그래프 시작화 
from langchain_teddynote.graphs import visualize_graph

visaulize_graph(app)
```
→ Graph의 장점은 여러 흐름을 손쉽게 추가하고 빼고, 수정하는 등 흐름을 제어하고 테스트하기에 너무나도 편리함

→ 이번 강의의 코드파일에는 내부가 복잡하면 큰 그림을 못 볼 수 있기 때문에 sudo코드 처럼 큰 뼈대를 볼 수 있도록 안의 함수의 내용들은 네이밍 말고는 비어져있음 

→ sudo 코드를 통해서 그래프를 다양하게 설계해보는 연습을 해보는 게 좋음 (큰 뼈대로 다양하게 흐름을 잡아보는 연습을 하기에 좋음)

