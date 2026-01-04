(영상: http://youtube.com/watch?v=Ipa6JNbFq4g) 

## 랭체인(LangChain)과 랭그래프(LangGraph) V1 업데이트 이후의 핵심 기능과 에이전트 개발 전략

### 1. AI 어플리케이션 아키텍처의 중요성
- 단순히 고성능 LLM(국가대표 AI, Sovereign AI)을 보유하는 것만으로는 충분하지 않습니다. 
- 엔진 vs 자동차: LLM 모델은 '엔진'에 불과하며, 이를 활용해 실제 가치를 만드는 '자동차(어플리케이션)'를 만드는 기술이 중요합니다.
- 아키텍처 논의 필요성: 모델 성능에만 집중하기보다, 실제 서비스 적용을 위한 어플리케이션 아키텍처에 대한 고민과 커뮤니티 내의 논의가 활발해져야 합니다.

### 2. LangSmith 신규 기능 업데이트
에이전트의 모니터링과 디버깅을 담당하는 LangSmith의 주요 업데이트 기능입니다.

* LangSmith Insights
  - 기능: 프로덕션 환경에서 쌓이는 방대한 로그 데이터를 계층적으로 자동 분류해주는 기능입니다.
  - 필요성: 챗봇 하나에 '사내 문서 검색', '이메일 자동화' 등 여러 기능이 섞여 있을 때, 로그가 혼재되어 분석이 어렵습니다.
  - 동작 방식: 자연어 설정을 통해 분류 기준을 정하면, LLM이 자동으로 트레이스(Trace)를 카테고리화합니다. 이를 통해 특정 기능(예: 검색 실패율)에 대한 정밀한 데이터 분석이 가능해집니다.

* Multi-turn Evaluation
   - 단발성 질문이 아닌, 여러 번 오가는 대화(Multi-turn)에 대한 품질 평가 기능이 강화되었습니다.
   - 복잡한 대화형 에이전트의 성능을 체계적으로 측정할 수 있습니다.

* LangSmith Agent Builder
   - 개요: 자연어 프롬프트만으로 에이전트를 생성할 수 있는 도구입니다.
   - 차별점: n8n, Dify 같은 '워크플로우 빌더'와는 다릅니다. 워크플로우 빌더는 복잡한 로직 설계에 진입장벽이 있지만, Agent Builder는 비개발자도 "웹 검색 에이전트 만들어줘" 같은 자연어 입력만으로 툴 선택과 시스템 프롬프트를 자동 구성합니다.
   - 커버리지: 코드로 구현하는 범위를 100이라 할 때, 약 70~80% 수준의 일반적인 에이전트 작업을 빠르게 구축하는 데 적합합니다.

### 3. LangGraph V1 및 에이전트 설계 전략
LangGraph V1 업데이트를 통해 에이전트 구축이 더 직관적이고 구조적으로 변했습니다.
### 구조적 개선 및 신기능
* create_agent : 복잡한 그래프 정의 없이도 직관적으로 에이전트를 구축할 수 있는 API가 도입되었습니다.
  <img width="1032" height="552" alt="image" src="https://github.com/user-attachments/assets/86fe2b07-37d8-41ce-b355-d2896942a709" />
  - response_format 기능
      <img width="1071" height="564" alt="image" src="https://github.com/user-attachments/assets/10207246-0061-4045-b071-a26b78d0fa10" />

* 미들웨어(Middleware) 패턴: 인증, 로깅, 에러 처리 등 공통적으로 필요한 기능을 비즈니스 로직과 분리하여 깔끔한 아키텍처를 설계할 수 있습니다.
  <img width="1498" height="776" alt="image" src="https://github.com/user-attachments/assets/78b512cd-118d-4f17-8d32-c93dcce9f654" />
  - 예를 들어, 모델에 적용하기 전에 요약하는 로직을 넣을 때
      <img width="1504" height="628" alt="image" src="https://github.com/user-attachments/assets/c149c8af-117d-43cc-b503-a26522fc7859" />
  - 알짜 배기 미들웨어를 built-in 해서 이미 만들어놨음(그냥 쓰면 됨)
       <img width="1180" height="793" alt="image" src="https://github.com/user-attachments/assets/daaeef85-4fce-41ba-88a1-dc14e59f05a1" />
  - custom해서 만드는 것고 가능 - AgentMiddleware 상속받아서 하거나 데코레이터 형식으로 가능
       - <img width="1479" height="788" alt="image" src="https://github.com/user-attachments/assets/185601a3-2ff8-4258-8c80-92633730fbf9" />
       - <img width="1498" height="793" alt="image" src="https://github.com/user-attachments/assets/309cfffa-54c9-4ffd-906e-71fac63bc030" />


* DeepAgents 설계 전략 (심화)
복잡한 태스크를 처리하기 위한 고급 설계 패턴입니다.
   - Context Offloading: 대화가 길어질 때 메모리를 효율적으로 관리하여 토큰 비용과 컨텍스트 윈도우 한계를 극복합니다.
   - Context Isolation: 여러 에이전트가 협업할 때 서로의 맥락이 섞이지 않도록 독립성을 확보합니다.
   - Subagent & Delegation: 대규모 작업을 여러 하위 에이전트(Subagent)에게 위임하고 협력하게 하는 멀티 에이전트 시스템 구축 전략입니다.

### 4. Recap
이번 업데이트는 단순히 기능 추가를 넘어, 개발자가 복잡한 에이전트 시스템을 더 쉽게 구축(Builder), 관리(Insights), 그리고 확장(DeepAgents 패턴)할 수 있도록 돕는 "어플리케이션 아키텍처의 고도화"에 초점을 맞추고 있습니다.
