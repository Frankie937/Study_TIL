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


---
(다시 정리) 

LangGraph Langchain이 정답은 아니지만, LLM 어플리케이션을 쉽게 만들 수 있는 프레임워크로서 좋다. 

### LangChain 에코시스템 
LangChain(기본 기능함수 등) / LangGraph(흐름 구성) / LangSmith (모니터링/추적/배포)

### V1.0 버전 업데이트 주요 변화 - LangSmith 주요 4가지 (-추적 부분에서 많이 개선됨) 
(요번에 v1.0으로 업데이트 되면서 여러 불편함들이 많이 개선되었다.) 

1) LangSmith Insights : 챗봇시스템을 오픈하게 되면, 굉장히 많은 대화가 쌓이게 됨. 
직장인 A씨는 사내 문서를 검색하고 싶고 B씨는 이메일 자동화 에이전트 
분류를 위해 카테고리를 도와주는 기능 (토큰 비용 및 시간은 소요됨 -> 자동화 하면 지속적으롭 분류함) 

2) Multi-turn Evaluation
대부분 멀티턴 챗봇을 만들게 되는데, 멀티턴 대화를 평가하는 게 쉽지는 않은데 이 기능을 사용하게 되면 쉽게 평가 결과를 받아보 수 있음 

3) LangSmith Agent Builder
- 배경지식을 알아 볼 필요가 있음 : 작년 n8n, dify, Open AI Agent Builder 등 노코드 툴이 트렌드였음.
- 그러나, 해당 툴들은 workflow tool이다. (workflow builder이다. 사실 비개발자들이 그 툴을 사용하기에 진입장벽이 있다
- 그래서, 자연어로 에이전트를 구축할 수 있도록 만든 것이 LangSmith Agent Builder이다. 
- 코드로 구현하는 걸 100% 라고 하면, n8n이나 dify와 같음 노코드 툴로 75-90%정도 , Agent Builder는 70-85%정도 커버가 가능한 수준이라고 볼 수 있다고 생각.
(작업할 상황과 설계에 따라 굳이 모든 걸 LangGraph로 구현할 필요가 없음) 
- 바이브 LangGraph 느낌 (구글 Opal 비슷) 

4) Polly - LangSmith Trace에 추가된 기능 
- Trace에 대한 오류 요약, 분석, 해결책을 제시 해줌 (system prompt도 개선해 줌 / 도구호출전략 개선 등등)

### V1.0 버전 업데이트 주요 변화 - LangGraph 
1) Create Agent 
- create_react_agent > create_agent 
(react agent 구조를 차용/ 주요 파라미터 - 좀 더 직관적으로 바뀜)

- 해당 create_agent 함수가 받는 파라미터 변화
	 - system_prompt
	 - tools
	 - middleware (굉장히 유용한 기능 - built-in 미들웨어도 있고, custom하게 미들웨어를 만들 수 도 있음)  
	 - response_format (정형화된 포맷으로 답변을 지정 할 수 있도록 파라미터로 아예 내재화된 옵션으로 변화 - 자동화 연계 시 굉장히 유용한 기능) 
	 - state_shcemam
	 - context_schema 


2) Middleware
(베이스 리액트 구조를 살펴보면)
- 만약에 예를 들어, 검색 도구를 호출 했는데 구글 검색결과 지저분한 것들이 모두 context에 다 들어가면 금방 context가 차서 폭발하거나, 할루네이션을 뱉어버리거나 등등 문제가 있음...
- 그래서 그러한 문제를 해결하기 위해 텍스트 전처리 등의 기능에 대한 코드를 덕지 덕지 앞 뒤로 추가하거나 뜯어봐야 했었는데, 대신 미들웨어의 기능을 활용 
- life cycle 개념 : before agent(에를 둘어, agent가 구동되기 전에 처리해야 할 로직을 여기에 그 로직을 middleware로 넣어주면 됨) / before model/ after model / after agent 등 
    - (예시) 할루시네이션 체커 로직을 최종 답변에 넣기 전에 넣고 싶다 하면 after agent에 middleware를 넣어주면 됨 
    - (예시) 쿼리라우팅 로직 - before agent 에 해당 middleware를 넣어주면 됨 
	- (예시) 메세지 큐에 너무 많은 context가 차있을 수 있기에 after model에 모델의 답변 요약 로직을 middleware로 넣어주면 됨 
	- (예시) tool calling이 일어날 때 해당 내용을 전처리하겠다는 로직이 들어가면 비용도 훨씬 줄어들을 것임 (wrap tool call) 
-> 이렇게 life cycle 안에 편하게 풀어낼 수 있음
- built-in Middleware가 langchain 도큐먼트에 있음 (https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- custom middleware으로 직접 구현하는 것도 가능 (AgentMiddleware 상속받아서 하거나 데코레이터 형식으로넣고 함수 로직으로 구현하면 됨) 
- 미들웨어를 잘 사용하면, 적절하게 세부 로직을 조작할 수 있고, 비용도 절감 가능 하는 등 굉장히 유용한 기능이다!!! 


3) Runtime context  
- context engineering 이 도와주기 위해서 나온 기능 
- 에이전트가 잘 안되는 이유 : llm 역량이 충분하지 않음 / 올바른 컨텍스트가 전달되지 않아서 (그래서 context engineering이 화두가 되었고 그것이 중요해짐!) 
- transient context / persistant context 
- invoke 하는 시점에 context shcema를 참조할 수 있다.
- 나중에 user_name을 확인해서 해당 context를 tool 호출할 때 넘길 수 있음 (기존에 도구를 호출하는 주체/ 호출 대상(tool)이 있는데 이럴 경우, tool 호출을 주고받을 때 context를 서로 받지 않았었음 )
- 예를 들어, llm이 파라미터를 지정해서 넘기는 프로세스가 있는데, 도구호출이 유저가 원하는 방향으로 호출이 일어나지 않을 수 있는데 그런 부분을 보완하는 것 > 그래서, 할루시네이션도 줄이고 토큰 비용도 줄일 수 있음 
- 그래서, tool 호출할 때, 주입해야 할 정보가 있을 경우 runtime context를 활용하면 좋음!! 


4) Deep agent 아키텍처 
- claude code, manus, antigravity등 agent harness 아키텍처 그걸 묘사해서 만든게 deep agent ! (이런 아키텍처를 활용해서 상황에 맞게 아키텍처를 잘 설계하는 게 중요!) 
- Agent 아키텍처관련 된 부분이기에 deep agent 를 뜯어보면 아키텍처 관점에서 나만의 agent 아키텍처를 정립해나가는 데에 있어서 굉장히 많은 공부가 됨 
- 멀티 에이전트가 나온배경울 생각해보면, 단일 에이전트가 복잡한 작업을 모두 처리하기 어렵고, 단순 구조라, 짧은 맥락/단기 작업에는 충분하지만 다단계 연구, 대규모 코드베이스 작업, 장기 맥락 유지가 필요한 시나리오에서는 쉽게 망가지는 한계 
- 장기 맥락을 유지하면서 복잡한 시스템이 가능할 지에 대해서 고민했던 게 1차적으로 멀티 에이전트 시스템이 나온 것 
- 그러나, 실질적인 좋은 결과로 이어지지는 않음 (적용되지 않은 부분 : 긴 계획 수립, 중간 산적물 축적 등 그런 게 되지 않음) 
- 그래서, 단순히 에이전트 10개 있다고 해서 성능이 곱하기 10배가 되는 게 아니라는 것!! 
- 그래서, claude code, manus 를 뜯어봐서 인사이트가 있었고 그걸 종합해서 오픈소스로 만든 게 deep agent이다. 
- deep agent의 핵심 구성요소로는 다음과 같다. 
- 4-1) TO-do 플래닝(사전계획 플래닝) : 어떻게 일처리를 했으면 좋겠는 지 우선순위를 정하기 위한 것 (규칙: to-do list를 생성하고 to-do 파일로 적게(write) 함, 그리고 그걸 읽어서 처리할 때마다 그 파일을 읽어서 체크하는 방식으로 동작하게 끔)  
- 4-2) 컨텍스트를 file-system 으로 관리 (공간 안의 메모리 잡아 먹는 걸 줄이고, 토큰비용 줄어들고, 효율적으로 관리 가능, 에이전트를 껐다 켜도 파일형태로 남아있기에 관리도 편함)
	 - context off loading system : llm이 파일 목록들을 살펴보고, 참조 context 파일을 읽어올 때 off loading 방식으로 파일을 읽어옴 
	      - 즉, main agent 에게 주어지는 맥락을 파일 형태로 관리하고, 파일 목록을 조회해서 관련성 있는 파일을 off loading 하는 방식으로 가져온다는 의미 
	      - **context off loading 방식이란? offset을 지정하고 참조 하는 파일 안에 필요한 정보가 있는 지 offset으로 지정한 라인까지 읽고 없으면 다음 블록으로 넘어가는 방식 
		  (오래동안 long running할 수 있는 에이전트를 만들어야 하기 때문에 그 파일을 전부 읽는게 아니라 해당 파일에 offset으로 지정한 만큼 읽으면서 필요한 정보만 갖고 올 수 있도록) 
- 4-3) sub-agent : 멀티 에이전트 패턴 지향 (for context isolation / delegation) 
	 - context isolation : 왜 필요한가? long running 하는 에이전트를 만들기 위해서는 main agent에게 context가 일목요연하게 필요한 정보만 있는 게 좋음 
	 - context delegation : sub agent에게 위임시켜서 main agent에게 compact한 정보만 넘길 수 있도록 하기 위함
	      - 복잡한 작업을 에이전트가 오랫동안 지속할 수 있으려면, sub agent를 만들어서 할 일들을 각각 위임하고 그 정보들 중에서 핵심 정보만 받아오기에 context가 금방 차지 않을 수 있어서 장기적으로 지속할 수 있는 것!
- 4-4) 장기 메모리 


### 주요 deep agent 사례 코드 확인 가능 
https://github.com/teddynote-lab/deep-agents-from-scratch


* agent 아키텍처에 대해서 의견을 서로 나누는 게 중요하다고 생각 
agent를 벤치마킹할 수 있는 리더보드
agent를 오픈소스로 올리는 환경 기반이 되어야 하는 

* langchain - langsmith 아카데미 잘 정리 되어 있다고 함 

* 추상화가 많이 되어서 langchain, langgraph가 정답은 아니지만, 스타트를 하기에 굉장히 좋은 프레임워크라고 생각함 

