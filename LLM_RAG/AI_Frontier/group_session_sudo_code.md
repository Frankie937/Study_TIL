### Step 1. LLM 기반 구조 분석 (MVP) 
-> 가장 기초적인 단계로, 기획안 텍스트를 LLM에게 입력하여 기본적인 '후킹(Hooking)' 요소와 '구조'를 평가받습니다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. 분석가 LLM 설정
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 2. 스크립트 입력 (가상 데이터)
script_draft = """
안녕하세요. 오늘 리뷰할 제품은 AI 핀입니다. 
스펙은 퀄컴 프로세서를 썼고, 무게는 50g입니다. 
레이저 잉크 디스플레이 기술이 들어갔는데요. 
이게 사실 화면이 손바닥에 나오는데 잘 안 보일 때가 많습니다.
가격은 699달러인데... 한번 자세히 알아보겠습니다.
"""

# 3. 분석 프롬프트
prompt = ChatPromptTemplate.from_template("""
당신은 100만 유튜버의 메인 PD입니다. 아래 대본의 초반 30초(Hook)를 평가하세요.
단, 다음 기준으로 점수(10점 만점)와 이유를 JSON으로 출력하세요.
1. 호기심 유발 (Curiosity)
2. 문제 제기 (Conflict)
3. 이탈 위험도 (Drop-off Risk)

대본: {script}
""")

chain = prompt | llm
result = chain.invoke({"script": script_draft})
print(result.content)
```


* 실행 결과 예시
```json
{
  "scores": {
    "Curiosity": 3,
    "Conflict": 4,
    "Drop_off_Risk": 8
  },
  "feedback": "초반에 '스펙(프로세서, 무게)' 나열이 너무 빠릅니다. 시청자는 기술명보다 '이게 왜 망했는지' 혹은 '얼마나 신기한지'를 먼저 보고 싶어 합니다. '잘 안 보일 때가 많습니다'라는 부정적 경험을 맨 앞으로 꺼내서 충격을 주는 것이 좋습니다."
}
```
-> 해석: 스펙 나열식 구성이라 이탈 위험이 8점으로 높게 나왔습니다. 구조 변경이 필요함을 즉시 알 수 있습니다.

### Step 2. RAG 기반 유사 성과 데이터 비교
-> 내 과거 영상이나 경쟁사의 영상 중, 현재 기획안과 **'의미론적(Semantic)'**으로 가장 유사한 영상의 성과를 찾아옵니다.

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1. 가상의 과거 데이터 (Knowledge Base)
# 실제로는 Youtube Data API로 수집한 DB가 들어갑니다.
past_videos = [
    {"title": "갤럭시 S24 울트라, 3주 사용기 - 스펙 설명 위주", "views": "1.2만", "retention": "30%"},
    {"title": "비전 프로, 이거 사지 마세요 (치명적 단점)", "views": "85만", "retention": "65%"},
    {"title": "AI 핀, 제가 직접 써봤습니다. (레이저 기술 분석)", "views": "5천", "retention": "20%"}
]

# 2. 임베딩 및 벡터 DB 저장 (Metadata 포함)
embeddings = OpenAIEmbeddings()
texts = [v["title"] for v in past_videos]
metadatas = past_videos
vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

# 3. 현재 기획안과 유사한 과거 사례 검색
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
matched_docs = retriever.invoke("AI 핀 스펙 프로세서 무게 레이저 잉크")

for doc in matched_docs:
    print(f"유사 레퍼런스 발견: {doc.page_content}")
    print(f"당시 성과: {doc.metadata}")
```

* 실행 결과 예시
```text
유사 레퍼런스 발견: AI 핀, 제가 직접 써봤습니다. (레이저 기술 분석)
당시 성과: {'views': '5천', 'retention': '20%'}
```
-> 해석: 현재 기획안(스펙 위주)대로 가면 과거 '5천 뷰' 영상과 유사한 패턴임이 확인되었습니다. '비전 프로(사지 마세요)' 영상처럼 부정적/자극적 앵글로 수정해야 함을 데이터로 암시합니다.​

### Step 3. LangGraph 기반 멀티 페르소나 시뮬레이션 (핵심)
이 부분이 데시(Dhesy)의 핵심 경쟁력이 될 것입니다. 성향이 다른 가상 시청자들을 LangGraph로 연결하여 실제 댓글창처럼 논쟁하게 만들고 최종 점수를 도출합니다.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# 1. 상태(State) 정의
class SimulationState(TypedDict):
    script: str
    comments: List[str]  # 에이전트들의 반응 누적
    final_decision: str

# 2. 페르소나 에이전트 노드 정의
def tech_expert_agent(state: SimulationState):
    # IT 전문가 페르소나: 기술적 깊이를 중시함
    response = "IT전문가: 프로세서랑 무게 정보는 좋은데, 레이저 잉크의 원리에 대한 깊이가 부족해요. 그냥 스펙만 읊는 느낌?"
    state['comments'].append(response)
    return state

def mass_audience_agent(state: SimulationState):
    # 대중(일반인) 페르소나: 재미와 실용성을 중시함, 어렵으면 이탈
    response = "일반시청자: 퀄컴이 뭔지 모르겠고... 699달러나 하는데 화면이 안 보인다고요? 그게 제일 중요한 거 아닌가? 앞부분 너무 지루해요."
    state['comments'].append(response)
    return state

def aggregator_node(state: SimulationState):
    # 종합 분석가: 의견을 종합하여 결론 도출
    comments = "\n".join(state['comments'])
    decision = f"종합 결론: 전문가에게는 얕고, 일반인에게는 지루함. \n핵심 피드백: '화면이 안 보인다'는 단점을 오프닝 5초 안에 보여주고 시작할 것."
    state['final_decision'] = decision
    return state

# 3. 그래프 구성 (Workflow)
workflow = StateGraph(SimulationState)

workflow.add_node("Tech_Expert", tech_expert_agent)
workflow.add_node("General_Public", mass_audience_agent)
workflow.add_node("Aggregator", aggregator_node)

# 병렬 실행 (동시에 시청) 후 종합
workflow.set_entry_point("Tech_Expert")
workflow.add_edge("Tech_Expert", "General_Public") # 실제로는 병렬 처리가 좋으나 예시는 순차 연결
workflow.add_edge("General_Public", "Aggregator")
workflow.add_edge("Aggregator", END)

app = workflow.compile()

# 4. 시뮬레이션 실행
initial_state = {"script": script_draft, "comments": [], "final_decision": ""}
result = app.invoke(initial_state)

print(result['final_decision'])
```

* 실행 결과 예시
```text
종합 결론: 전문가에게는 얕고, 일반인에게는 지루함. 
핵심 피드백: '화면이 안 보인다'는 단점을 오프닝 5초 안에 보여주고 시작할 것.
예상 시청 지속률: 초반 15% 구간에서 급락 예상.
```
-> 해석: 여러 명의 가상 시청자가 콘텐츠를 미리 보고 피드백을 남겼습니다. 이를 통해 창작자는 **"아, 이대로 올리면 둘 다 놓치겠구나"**를 깨닫고 편집 방향을 수정할 수 있습니다.​

