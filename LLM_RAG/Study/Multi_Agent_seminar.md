(회사에서 준비한 내부 세미나 자료) 

* 기술의 변천이라는게 그 기존 기술의 한계와 새로운 니즈가 생기면 그걸 개선하고 혁신하기 위해서 새로운 기술들이 만들어지는 것 

### LLM의 주요 굵직한 트렌드 살펴보기 
- 2022년말 ~ 2023년: Open AI가 ChatGPT 출시 > 이때 한창 '프롬프트 엔지니어링' 기법 관심 급증/ LLM을 활용하여 사전학습된 지식으로 답변을 생성하는 간단한 챗봇서비스 구축 사례 많아짐
But, 각 개인 및 회사만의 고유한 문서/지식Database 등에 대한 답변을 받고 싶어하는 니즈가 생겨나면서 RAG가 주목받기 시작! 
- 2023말~2024 : RAG - 각 회사만의 문서를 기반으로 하는 챗봇 서비스 급증 (여전히 나만의 개인화된 지식을 접목하고 싶으면 지금도 여전히 필요한 기술임 !)
(사실 RAG는 2020년 말에 논문에서 처음 소개된 기법이기는 하지만, 제대로 주목받고 기업에서 활용하기 시작했던 건 작년!)
But, 지식기반을 통해 답변을 하는 게 좋지만, 외부 도구와의 연계가 필요함을 느끼기 시작 > LLM이 여러 도구를 직접 주체적으로 판단하고 선택해서 action까지 해주었으면 좋겠다는 니즈를 바탕으로 생겨난 개념, Agent! 
- 2024말~2025 : Agent (RAG로 지식기반을 통해 답변을 하는 게 좋지만, 외부 도구와의 연계가 필요함을 느끼기 시작해서 나오기 시작) 
- 2025중~ : Multi-Agent, MCP, A2A ... 등 새로운 기술들이 끝없이 생겨나고 있음


### 멀티에이전트 배경 
멀티에이전트라는 개념이 왜 생겼는 지는 싱글에이전트에 대해 먼저 간략하게 봐야 함

* single agent 특징 
  - "단일 프로세스"로 작동
  - 한 명의 작업자가 처음부터 끝까지 작업을 처리
  - 하나의 에이전트에 모든 툴을 바인딩
  - 한계점: 너무 많은 tool > LLM도 tool을 결정하고 판단하는 데 헷갈려 하고(성능저하), 지연시간도 길어짐, 복잡한 프로세스에는 어려울 수 있음  

* multi-agent 특징
  - 여러 개의 Agent를 구성하고, 하나의 에이전트가 사용하는 도구를 제한
  - 각 에이전트의 역할을 특화(system prompt를 narrow down 한다고 함)
  - 서로 다른 역할과 전문성을 가진 여러 독립적인 에이전트가 협업하여 복잡한 작업을 수행(supervisor 패턴이 가장 효율적이라고 함)
  - 비용은 많이 드는 게 단점이긴 하지만, 작업의 질이 높아짐 -> 확장성/ 모듈화/ 강건성 측면에서 single agent 보다 좋음! 

### 멀티에이전트 - Supervisor 패턴 

* multi-agent 중 가장 효율적인 패턴 : Supervisor 패턴
  -  Supervisor는 다양한 전문 에이전트를 한 데 모아, 하나의 팀(team)으로 운영하는 감독관 역할
  -  Supervisor 에이전트는 팀의 진행 상황을 관찰하고, 각 단계별로 적절한 에이전트를 호출하거나 작업을 종료하는 등의 로직을 수행

* multi-agent 단점
  - 추론 조정 (Coordinating Reasoning): 에이전트들이 효과적으로 추론하고 실행하게 하려면 정교한 조정 메커니즘이 필요함 (-> 시스템과 상황에 맞는 정교한 아키텍처 설계 및 고민 필요)
  - 문맥 관리 (Managing Context): 에이전트 간의 모든 정보, 작업 및 대화를 추적하는 것이 복잡해질 수 있음
  - 시간 및 비용 (Time and Cost): 다중 에이전트 상호 작용은 계산 비용이 많이 들고 시간이 소요될 수 있음 (-> 어떤 최적화 방법이 있을지 고민 필요)
  - 복잡성 (Complexity): 마이크로 서비스 아키텍처와 유사하게, 각 에이전트 자체는 단순할 수 있지만 시스템 전체는 더 복잡해지는 경향이 있음


### multi-agent - supervisor 패턴 사례 코드 (참고: https://wikidocs.net/270690)

```python

from dotenv import load_dotenv
import operator
from typing import Sequence, Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel
import functools
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_teddynote.models import get_model_name, LLMs
from langchain_teddynote.tools.tavily import TavilySearch
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_teddynote.graphs import visualize_graph
from langchain_core.runnables import RunnableConfig
from langchain_teddynote.messages import random_uuid, invoke_graph
import matplotlib.pyplot as plt

# API 키 정보 로드
load_dotenv()

# 모델명 로드 
MODEL_NAME = get_model_name(LLMs.GPT4)
print(MODEL_NAME)



############################## 1) 상태 정의 ##############################
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]  # 메시지
    next: str  # 다음으로 라우팅할 에이전트



############################## 2) 도구 생성 ##############################

# 최대 5개의 검색 결과를 반환하는 Tavily 검색 도구 초기화
tavily_tool = TavilySearch(max_results=5)
# 로컬에서 코드를 실행하는 Python REPL 도구 초기화 (안전하지 않을 수 있음)
python_repl_tool = PythonREPLTool()



############################## 3) Utility 생성 ##############################

# 지정한 agent와 name을 사용하여 agent 노드를 생성
def agent_node(state, agent, name):
    # agent 호출
    agent_response = agent.invoke(state)
    # agent의 마지막 메시지를 HumanMessage로 변환하여 반환
    return {
        "messages": [
            HumanMessage(content=agent_response["messages"][-1].content, name=name)
        ]
    }
# functools.partial의 역할은 기존 함수의 일부 인자 또는 키워드 인자를 미리 고정하여 새 함수를 생성하는 데 사용됨. 즉, 자주 사용하는 함수 호출 패턴을 간소화할 수 있도록 도와줌



############################## 4) supervisor Agent 생성 ##############################

# 멤버 Agent 목록 정의
members = ["Researcher", "Coder"]

# 다음 작업자 선택 옵션 목록 정의
options_for_next = ["FINISH"] + members

# 작업자 선택 응답 모델 정의: 다음 작업자를 선택하거나 작업 완료를 나타냄
class RouteResponse(BaseModel):
    next: Literal[*options_for_next]

# 시스템 프롬프트 정의: 작업자 간의 대화를 관리하는 감독자 역할
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)

# ChatPromptTemplate 생성
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next? "
            "Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options_for_next), members=", ".join(members))

# LLM 초기화
llm = ChatOpenAI(model=MODEL_NAME, temperature=0)

# Supervisor Agent 생성
def supervisor_agent(state):
    # 프롬프트와 LLM을 결합하여 체인 구성
    supervisor_chain = prompt | llm.with_structured_output(RouteResponse)
    # Agent 호출
    return supervisor_chain.invoke(state)



############################## 5) speacilaist Agent 2개 생성  ##############################

# Research Agent 생성
research_agent = create_react_agent(llm, tools=[tavily_tool])
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")


# Coder Agent 생성
coder_agent = create_react_agent(
    llm,
    tools=[python_repl_tool],
    # state_modifier=code_system_prompt, # 해당 인자 없어짐- 주석처리 
)
coder_node = functools.partial(agent_node, agent=coder_agent, name="Coder")



############################## 6) Graph 구성 ##############################

# 그래프 생성
workflow = StateGraph(AgentState)

# 그래프에 노드 추가
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", coder_node)
workflow.add_node("Supervisor", supervisor_agent)

# 멤버 노드 > Supervisor 노드로 엣지 추가
for member in members:
    workflow.add_edge(member, "Supervisor")

# 조건부 엣지 추가 (
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END


def get_next(state):
    return state["next"]


# Supervisor 노드에서 조건부 엣지 추가
workflow.add_conditional_edges("Supervisor", get_next, conditional_map)

# 시작점
workflow.add_edge(START, "Supervisor")

# 그래프 컴파일
graph = workflow.compile(checkpointer=MemorySaver())



############################## 7) 실행 ##############################

# config 설정(재귀 최대 횟수, thread_id)
config = RunnableConfig(recursion_limit=10, configurable={"thread_id": random_uuid()})

# 질문 입력
inputs = {
    "messages": [
        HumanMessage(
            content="2015 ~ 2024년까지의 대한민국의 1인당 GDP 추이를 그래프로 시각화 해주세요."
        )
    ],
}

# 그래프 실행
invoke_graph(graph, inputs, config)


```


### repo 
- https://www.philschmid.de/single-vs-multi-agents#the-universal-truths-of-building-agents
- https://brunch.co.kr/@miminy91/2
- https://wikidocs.net/270690
