### Agentic Workflow 통합 아키텍처
이 워크플로우는 '분석(Analyzer) → 검색(Retriever) → 시뮬레이션(Simulator) → 전략 수립(Strategist)' 순으로 흐르는 데이터 파이프라인입니다.

- Analyzer Agent (Step 1): 입력된 기획안을 분석하여 '검색 키워드'와 '초기 평가'를 생성.
- Retriever Tool (Step 2): 생성된 키워드로 과거 유사 영상(성공/실패) 데이터를 조회.
- Simulation Agent (Step 3): 조회된 과거 데이터를 참고하여, 가상 페르소나들이 현재 기획안을 평가.
- Strategist Agent: 모든 정보를 종합하여 최종 수정 제안


```python

import operator
from typing import Annotated, List, TypedDict, Union
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# --- 1. 통합 상태(State) 정의 ---
# 워크플로우 전체에서 공유되는 메모리 공간입니다.
class WorkflowState(TypedDict):
    input_script: str                # 사용자가 입력한 기획안/스크립트
    analysis_result: dict            # Step 1 결과: 구조 분석 및 키워드
    retrieved_docs: List[str]        # Step 2 결과: 유사 성공/실패 사례
    simulation_feedback: List[str]   # Step 3 결과: 가상 시청자 반응
    final_report: str                # 최종 결과: 수정 제안 리포트

# --- 2. 각 단계별 노드(Node) 구현 ---

# [Node 1] Analyzer Agent (Step 1)
def analyze_script(state: WorkflowState):
    print("--- [Step 1] 스크립트 구조 분석 중 ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    당신은 콘텐츠 분석가입니다. 아래 기획안을 분석하여 다음 두 가지를 도출하세요.
    1. 핵심 키워드 3개 (예: #빠른템포, #IT리뷰, #비판적)
    2. 초반 30초의 예상 몰입도 점수 (10점 만점)
    
    기획안: {script}
    
    결과는 JSON 형식으로 출력하세요.
    """)
    
    # 실제로는 JSON 파싱 로직이 필요하지만 간소화함
    result = prompt | llm
    analysis = result.invoke({"script": state["input_script"]})
    
    # 가상의 분석 결과 생성 (실제로는 LLM 응답 파싱)
    analyzed_data = {
        "keywords": "IT리뷰 실패경험담 고가장비",
        "score": 7
    }
    return {"analysis_result": analyzed_data}

# [Node 2] Retriever Tool (Step 2: Multimodal RAG)
def retrieve_references(state: WorkflowState):
    print("--- [Step 2] 유사 레퍼런스 검색 중 (RAG) ---")
    keywords = state["analysis_result"]["keywords"]
    
    # 가상의 Vector DB (실제로는 Multimodal Embedding 된 DB 연결)
    # 여기서는 텍스트로 예시를 들지만, 실제로는 영상의 정보를 바탕으로 한한 벡터로 검색됨
    fake_db = [
        "성공사례: '비싼 쓰레기'라고 솔직하게 깐 리뷰 (조회수 100만, 컷전환 빠름)",
        "실패사례: 스펙만 나열하다 끝난 리뷰 (조회수 2천, 컷전환 느림)",
        "성공사례: 분해해서 내부를 보여주는 하드코어 리뷰 (조회수 50만)"
    ]
    
    # 키워드와 매칭되는 문서 검색 (간소화된 로직)
    matched_docs = [doc for doc in fake_db if "리뷰" in doc][:2]
    
    return {"retrieved_docs": matched_docs}

# [Node 3] Simulation Agent (Step 3: Multi-Persona)
def run_simulation(state: WorkflowState):
    print("--- [Step 3] 가상 시청자 시뮬레이션 중 ---")
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # 이전 단계의 정보(RAG 결과)를 컨텍스트로 활용
    context = "\n".join(state["retrieved_docs"])
    script = state["input_script"]
    
    # 페르소나 정의 (동적 생성 가능)
    personas = [
        "깐깐한 30대 IT 덕후: 기술적 깊이와 비판적 시각 중시",
        "자극을 원한 10대 시청자: 재미없으면 3초 만에 이탈"
    ]
    
    feedbacks = []
    for persona in personas:
        msg = f"""
        당신은 [{persona}]입니다. 
        과거 유사 사례 참고: {context}
        
        위 사례를 볼 때, 현재 아래 기획안을 보면 어떤 반응을 보일까요?
        솔직한 댓글을 남겨주세요.
        
        기획안: {script}
        """
        response = llm.invoke(msg)
        feedbacks.append(f"[{persona}]: {response.content}")
        
    return {"simulation_feedback": feedbacks}

# [Node 4] Strategist Agent (Final Output)
def generate_strategy(state: WorkflowState):
    print("--- [Final] 최종 전략 수립 중 ---")
    llm = ChatOpenAI(model="gpt-4o")
    
    feedbacks = "\n".join(state["simulation_feedback"])
    analysis = state["analysis_result"]
    
    final_prompt = f"""
    당신은 총괄 프로듀서입니다.
    
    [분석 결과]: 점수 {analysis['score']}점
    [시뮬레이션 반응]:
    {feedbacks}
    
    위 내용을 종합하여, 제작자에게 구체적인 수정 제안 3가지를 작성해주세요.
    특히 이탈을 막기 위한 '오프닝 수정'에 집중하세요.
    """
    
    response = llm.invoke(final_prompt)
    return {"final_report": response.content}

# --- 3. LangGraph 워크플로우 구성 ---

workflow = StateGraph(WorkflowState)

# 노드 추가
workflow.add_node("analyzer", analyze_script)
workflow.add_node("retriever", retrieve_references)
workflow.add_node("simulator", run_simulation)
workflow.add_node("strategist", generate_strategy)

# 엣지 연결 (순차적 흐름)
workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", "retriever")
workflow.add_edge("retriever", "simulator")
workflow.add_edge("simulator", "strategist")
workflow.add_edge("strategist", END)

# 컴파일
app = workflow.compile()

# --- 4. 실행 예시 ---
if __name__ == "__main__":
    input_data = {
        "input_script": "안녕하세요, 오늘은 AI 핀을 가져왔습니다. 스펙은 퀄컴 칩셋이고..."
    }
    
    final_state = app.invoke(input_data)
    
    print("\n========== [최종 리포트] ==========\n")
    print(final_state["final_report"])


```
