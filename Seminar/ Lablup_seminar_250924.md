<img width="818" height="465" alt="image" src="https://github.com/user-attachments/assets/7a461646-71e3-49f1-8945-25bf8090d712" />
( https://event-us.kr/lablup/event/111442)
* 20250924 래블업 세미나 - 래블업은 ‘Make AI Composable’를 주제로 5회 컨퍼런스를 개최
* 장소 :서울 서초구 강남대로 27 양재 aT센터 3층 세계로룸


### 효율적인 Agentic 아키텍처 구성을 위한 개발 Tip (이경록님- 테디노트)
<img width="329" height="80" alt="image" src="https://github.com/user-attachments/assets/8879b0e9-15c3-4b0f-b57e-1cc691a880f4" />


- MCP 툴 + 지식데이터베이스 관리하는게 중요
    -> 유용한 mcp 를 만들려면 유용한 기획이 필요
- ReAct: thought + Action + Observation
- Agent의 강점? 재시도를 한다는 점 / recursion test를 한다는 것
- 싱글에이전트 한계: 도구의 개수 너무 많으면 지연시간, 성능 저하 (prompt도 하나 밖에 들어갈 수 없음)
- supervisor 패턴이 유지보수관점에서 좋음 (에이전트 단위의 모듈화) 
- agent의 기술적 기능
   - Recursion
   - Routing (질문의 요청 수준에 따라 모델을 다르게 사용하게끔 하는 것도 중요 ex- 점심메뉴 추천해줘 같은 질문은 논문 분석 요청과 같은 수준의 모델을 사용할 필요가 없음! 라우팅은 필수!)
     - agentic한 라우팅 (확장성 면에서 function calling 보다 용이함)
     - function calling 라우팅 (룰베이스 기반- 성능은 안전정 그러나 확장성이 어려움)
       
- 워크플로우 흐름관리
- 메모리 (단기/장기메모리)
  - 단기메모리 ex) 멀티턴 - thread id로 관리
  - 장기메모리 (요즘의 화두) --MemoryStroe (langchain에서 제공) -> 사용성을 획기적으로 개선시켜줌
    - ex) email assistant 개발: 이메일 초안 작성 스타일 > 교정 > 가이드를 장기적으로 기억해서 프롬프트를 하지 않아도 다음부터 교정이 됨 (나의 스타일대로)
    - 장기기억하라는 '트리거 워드'같은 게 있음 (Trigger word)
      
- Human in The Loop (HITL)
  - 해당 내용 굉장히 중요!
  - RAG, 멀티 에이전트 시스템 등 반드시 들어가야 하는 HITL 기법 (유저에게 한 번 더 허락을 받는 - 유저 입장에서 안심하고 사용 가능)
    
- MCP
  - 독립적인 knowledge database
  - sequential한 방식이 관리에 더 용이
  - 계층적 호출 구조
  
- 문서변경사항 반영 어려움
- context window 초과
- 검색성능 저하
- 문서의 1/5 정도의 내용을 압축해서 갖고올 수 있도록(관련있는 url페치/ 문서리스트 조회 등등)

- 평가
  - 답변 평가
  - 라우터에 대한 평가 (잘 분기했는지)
  - 도구호출에 대한 평가(도구호출 잘 했는지)
  - 툴에 대한 지연시간이나 얼마나 많이 사용되고 있는지 그런 부분도 분석해서 최적화하는 방법이 중요!!

- 소버린 AI 아쉬운 점?
  - 어플리케이션에 대한 고민 /엔지니어링에 대한 고민-> 이런 부분이 외국에 비해 많이 부족하다고 생각함



<img width="481" height="804" alt="image" src="https://github.com/user-attachments/assets/806743f2-92ad-4433-8624-fbb3c72e6966" />
