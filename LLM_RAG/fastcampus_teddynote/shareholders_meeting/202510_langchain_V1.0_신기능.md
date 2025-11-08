
### 2025년 10월 주주총회 (20251030)
* 주제: LangChain V1.0 출시 기념 신기능 살펴보기
  - LangChain V1.0 의 달라진 기능
  - LangChain V1.0 새로운 한글 문서를 소개
  - MCP 도구의 활용 방법을 통해 코드 마이그레이션에 대한 부담을 덜어낼 수 있음
  - Q&A 진행
  - 주요링크
     - 확 바뀐 LangChain Document 페이지: https://docs.langchain.com/
     - 한국어 번역 페이지: https://kr.langchain-docs.com/
     - 튜토리얼 소스코드(V1): https://github.com/teddynote-lab/langgraph-v1-tutorial
     - LangChain Agent Builder-신청: https://docs.langchain.com/langsmith/agent-builder


* langchain v1의 핵심 - Middleware (ex- 모델 호출 전에 prompt selection 동적처리, tool 호출 전에  인증 및 보안(PII탐지기능 등) 등)  
  - middleware를 세부적으로 컨트롤 가능 > 코드의 간결함 증가
  - middleware를 플러그인 형식으로 넣었다 뺐다 관리측면에서 굉장히 용이
  - structured output - create_agent 함수 내부 response_format 옵션 생김 
  <img width="831" height="560" alt="image" src="https://github.com/user-attachments/assets/014f03b9-e7ef-4469-b3ff-36e27bb9dfd7" />
  - context engineering
     - model context: model call에 들어가는 것 (지시사항, 메세지기록, tool, 응답형식 등)
     - tool context: tool이 엑세스하고 생성할 수 있는 것 (state, store, runtime context에 대한 읽기/쓰기)
     - life-cycle context: model과 tool call 사이에 발생하는 것 (요약, guardrail, 로깅 등)
   
* langchain 신기능 LangSmith -  Agent Builder 출시 - No code Agnet building platfrom!
   - 참고링크 1: https://blog.langchain.com/langsmith-agent-builder/
   - 참고링크 2: https://digitalbourgeois.tistory.com/2240

* runtime.context 기능 - 굉장히 유용

* response formtat 기능 (응답형식)

* create_react_agent > create_agent 함수로 변경

* Middleware 기능
  - Human in the Loop Middleware : 승인 필요여부에 따라 tool을 컨트롤 할 수 있는 기능이 생김 (너무 좋음!!! -이전에는 이런 자잘한 기능 때문에 하나 하나 노드로 다 구현해줘야 했었는데...)
     - 세부적으로 중간에 interrupt를 할 tool을 쉽게 정할 수 있음!!!
  - wrap_model_call 데코레이터 : 모델 호출 직전에 wrap_model_call이 일어나면서 모델을 동적으로 변경처리 가능 (일반모델/추론모델 사용해야 하는 상황에 따라 동적으로 모델 변경하여 처리 가능 - model selection이 가능 ex- 긴 메세지 기준에 따라 일반/추론모델 변경, 구독여부에 따라 일반/추론모델 변경 등)
  - wrap_tool_call 데코레이터 : tool 호출 직전에 wrap_tool_call이 일어나면서 tool관련 오류 처리 등 가능
  - dynamic prompt (동적 시스템 프롬프트) 기능
    
* context engineering
  - 입력을 세부조정하는 모든 것들을 말하는 거라 생각 (이미 우리가 하고 있던 것임, 좀 더 마케팅 용어로 나온 개념일 뿐)
  - 장기메모리 기능 사용 - 유저마다 권한차이 기능 등... 

* langgraph middleware (참고로 middleware는 한 번에 여러 개 추가 가능) 
  - SummarizationMiddleware : 멀티턴 대화 구현 중 대화가 계속 길어지면 토큰비용 잡아먹기 때문에 예를 들어 max_token 4000이 넘어가면 요약하게 끔 구현
  - ModelCallLimitMiddleware : 모델 호출 제한 기능 (과도한 비용 방지)
