[랭체인노트](https://wikidocs.net/book/14314) 
- CH17 LangGraph 03. Use Cases 09. SQL 데이터베이스와 상호작용하는 에이전트 부문 공부하다가 이해안되는 부분 정리 


```python
# 질문과 사용 가능한 테이블을 기반으로 관련 테이블을 선택하는 모델 노드 추가
model_get_schema = ChatOpenAI(model=MODEL_NAME, temperature=0).bind_tools(
    [get_schema_tool]
)
workflow.add_node(
    "model_get_schema",
    lambda state: {
        "messages": [model_get_schema.invoke(state["messages"])],
    },
)
```

* 위의 코드에서 왜 lambda를 쓸까?
  - lambda는 “이름 없는 간단한 함수”를 만들 때 쓰는 파이썬 문법
  - 즉, lambda state: ...는 state라는 입력값을 받아서, 그걸 활용해 무언가 결과값을 딕셔너리 형태로 반환하는 함수를 “한 줄로” 정의한 것
  - 여기서는 이 함수(람다)를 workflow의 노드로 넘겨주기 위해 사용한 것

* 코드가 작동하는 프로세스 설명
  - 워크플로우에서 이 노드가 실행될 때 state라는 데이터를 넘겨받음.(이 데이터는 이전 단계까지의 모든 정보, 또는 입력 메시지들을 담고 있을 수 있음.)
  - 그 state에서 state["messages"]를 꺼내서, model_get_schema.invoke(state["messages"]) 실행 → 반환값을 리스트 안에 넣음
  - 최종적으로 {"messages": [위의 결과물]} 형태의 dict을 반환!
    -> 즉, ‘model_get_schema’라는 노드는 state(상태, 정보)를 받아서, 그 안에 들어있는 ‘messages’라는 값을 꺼내 모델에 넣고, 모델의 응답을 받아 다시 ‘messages’라는 키의 리스트 값으로 담아서 반환하는 역할
* 왜 lambda를 사용하는 건가?
  - 함수를 직접 정의해도 되지만, 간단할 땐 굳이 따로 def로 만들지 않고 한 줄로 익명 함수(lambda)를 쓰면 코드가 더 짧고 직관적
  - 아래 함수처럼 정의해도 되긴 함
  - ```python
    def process_state(state):
    return {
        "messages": [model_get_schema.invoke(state["messages"])]
    }
    workflow.add_node("model_get_schema", process_state)
    ```
    
