### langchain 및 langgraph 차이 
(https://birdgang82.medium.com/langchain-%EA%B3%BC-langgraph-%EC%B0%A8%EC%9D%B4%EC%A0%90-%EA%B5%AC%EC%A1%B0-%EB%B6%84%EC%84%9D-%EA%B7%B8%EB%A6%AC%EA%B3%A0-mcp-%EC%97%B0%EA%B2%B0-82cad8d390a1)
* LangChain에서는 각 도구를 Tool로 등록 하고, LLM 이 질문을 보고 어떤 도구를 쓸지 결정 합니다. 
(복잡한 대화/상태/분기/루프 한계 )
(하지만, 여러 도구의 결과를 조합하거나 순차적으로 도구1 → 도구2 → 답변을 만들려면 LLM이 “체인”을 스스로 추론해야 하므로 복잡한 분기/반복/상태관리는 어려습니다.)
* LangGraph는 내부적으로 “상태”를 추적하며 LLM이 여러 도구를 순차적으로 호출하고, 각 도구의 결과를 종합해서 답변을 만들 수 있습니다. 복잡한 분기/반복/상태관리가 자연스럽게 지원합니다. 


