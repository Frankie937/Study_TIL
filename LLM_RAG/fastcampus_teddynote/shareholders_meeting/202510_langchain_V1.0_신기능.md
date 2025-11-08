
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
   
* langchain 신기능 Agent Builder 출시 - No code Agnet building platfrom!
   - 참고링크 1: https://blog.langchain.com/langsmith-agent-builder/
   - 참고링크 2: https://digitalbourgeois.tistory.com/2240
