( 링크: https://aifactory.space/task/8841/overview)

![image](https://github.com/user-attachments/assets/8e636776-a708-4aaf-ac8e-1dc547f90ca1)


## 에이전틱 AI - 랭체인코리아 밋업 2025Q1 - 2025/03/04

### LangGraph를 활용한 에이전틱AI 시스템 구축 | 멀티에이전트 협업 네트워크 시스템 중심으로 ( 이경록 | 브레인크루 )

(강의 링크 : https://www.youtube.com/watch?v=edsshVochqM)
(자료 링크: https://drive.google.com/file/d/1MDAbmH2cDG-X4MBVvLFRbbfCjDUP1yNE/view)
(랭그래프 핸즈온 코드 링크 : [LangGraph-HandsOn](https://github.com/teddylee777/LangGraph-HandsOn)) 

- 왜 modular rag로 가려고 하는가?
    - 기존 RAG는 단방향의 구조는
        - 한 번에 다 잘해야 하는 부담이 많음
        - 이전 단계로 되돌아가기 어려움
    
- LangGraph
    - 워크플로우 특화 프레임워크
    - 장점 : 보다 유연한 흐름을 만들 수 있음
        - cycle & branching (루프 & 조건문 구현)
        - persistance
        - low level control
    - 노드를 독립적으로 개발 가능
    - 협업시 장점 - 모듈 단위의 분산 개발 가능
        - base template 정의
        - 도메인 전문가 : 노드의 개발에 집중
        - 흐름(flow) 엔지니어 : 작성된 노드로 흐름을 구성
    - 워크플로우 일부 단계의 실험에 용이 (모둘 교체 쉬움 → 테스트 용이)
        - 노드를 선택하여 plug-in 방식으로 쉽게 교체
            - ex) deepseek 모델같이 새로 나올 때 쉽게 테스트 가능
    - 분기처리 (coditional edge로 가능)
        - 룰베이스 기반도 가능
        - llm판단 기능도 가능
        - 실전에서는 라우팅(coditional edge로 가능) 기능 무조건 필요하기에 langgraph가 굉장히 유용…!
        - llm이 라우팅을 선택하게끔 만드는데, 2가지 방식
            - #1 agentic 키워드 방식
                - 도구들을 먼저 정의
                - agent 한테 질문을 받으면 적절한 도구를 선택하도록
                - 선택을 안하는 옵션도 있음
                - 도구에 대한 정의 description을 잘 적어주는 게 중요
            - #2 fuction calling 방식
                - agent 키워드 방식과 비슷해보이나 구조화된 흐름에서 더 적합 
                - 아무것도 선택하지 않는 옵션을 넣어줘야 함
                - 도구에 대한 정의도 중요하지만, 프롬프트에 더 적극적으로 적어주고, 정성을 들여야 함 
                 → 좀 더 structured 한 구조에서 더 적합                
    - 병렬처리 (Fan out /Fan in)
        - 지연시간 줄일 수 있음
        - 순차적인 구조가 아니면 병렬처리로 구조를 설계가능
    - 메모리
        - 단기 메모리 기능 지원 short-term memory : checkpointer
            - thread_id로 context 관리
            - 멀티턴 기능 가능
            - time travel 기능
                - 채크포인터
                   ->  체크포인터를 활용하여 특정 시점으로 되돌리기 기능
        - 장기 메모리 기능 지원 long-term memory
            - 사용자의 personal information을 활용
            - thread_id를 바꿔도 다시 기록을 살려줌
        - Human-in-the-loop 기능
        - langchain의 에코시스템과 상호작용 용이
            - langchain
            - langsmith -추적기능
            - langgraph cloud - 배포
            - langgraph studio -개발 tool
    
- 멀티 에이전트 협업 네트워크
    - 복잡한 업무를 분산 처리하는 시스템
    - langgraph swarm
    - supervisior pattern
        - supervisor - user 상호작용
        - supervisor가 적합한 agent에게 작업
        - agent는 작업완료 후 supervisor에게 작업완료
          
- 멀티에이전트 패턴 여러가지가 있다.
  ![image](https://github.com/user-attachments/assets/3f073454-9bea-4f25-a996-2f71f87dc59d)
  - 그 중에 제일 유명한 패턴 "Supervisor Pattern"
      ![image](https://github.com/user-attachments/assets/64364999-dc65-4328-8d10-bdec0f373d20)
  - Plan and Excute 패턴
      ![image](https://github.com/user-attachments/assets/460f3932-f6c3-42c8-a5dd-0c6e65d41484)
  - Hierarchical 패턴 (계층적 에이전트 팀)
      ![image](https://github.com/user-attachments/assets/c68750c6-1f46-4a75-a59e-129691d5b8b5)
  - Storm Research 패턴 
    - open ai 딥리서치와 비슷한 패턴
      ![image](https://github.com/user-attachments/assets/8dd65817-f9b3-46fe-b736-9030b8cdabf9)




### 어시웍스를 활용한 에이전틱AI 시스템 구축 | 생성형AI에서 에이전틱AI까지 ( 김태영 | AIFactory )
** 어시웍스를 무료로 지금 사용 가능 (횟수 제한) 

** 테디노트 유튜브 참고 - 유튜브 라이브 

- AssiWorks 업무정의
    - 업무 흐름을 작은 단위로 쪼개서 최대한 자동화할 수 있도록 업무를 정의하는 단계
    - 2021년 처음 생성
    - 스마트팜 IoT 챗봇  - 유성구청
        - 온프레미스에 대한 수요가 굉장히 높을 것이다 라고 생각
- 디지털새싹 - 케이브레인
    - 초등학생들도 만들 수 있음
    - 코딩기반이 아니라 GUI방식으로 만들어야 겠다고 생각 - 그래서 어시웍스를 만들게 됨
- 어시웍스의 플로우 - 정형화된 플로우
- 모든 사원들은 모든 도구들을 사용하면 안됨 (접근권한이 있는 도구들이 있기에)
    - 도구들에 대해 권한관리도 할 수 있는 기능을 만들어야 함
- GeoWERT 서비스 시연
    - 답변이 잘 나오면 그 답변을 바로 예시로 사용도 가능
    - 프롬프트를 잘 작성하는 게 중요
    - 
- 순차적호출/ 체인드 호출 방식 2가지 있음
- Iot 기기랑 api로 연결해서 스크린 올려줘 시연 - 신기 ㅎㅎ
- 개인비서 - 메모리 기억
- 팀빌딩 - 멀티에이전트 구성 방식 다양함
    - 라우팅 방식
    - 자율 task 방식
    - 대화형 방식
    - 계층적 방식
    - 경쟁토론 방식

### PydanticAI를 활용한 에이전틱AI 시스템 구축 ( 허정준 | Engineer )
- PydanticAI 소개
    - 2024년 말 공개된 에이전트 프레임워크
    - Pydantic
        - 자동형변환 가능 등 유용한 기능이 많음
    - AI와 무슨 연관 ?
        - 기존 정해진 입려/출력 → (llm 서비스) 다양한 입력/출력 (결과를 코드에 통합하기 어려움)
    - LLM의 출력을 활용하는 유형
        - 사람 - LLM의 출력을 그대로 사용 -llm/rag 중심
        - LLM - LLM의 출력을 그대로 사용 -llm/rag 중심
        - 코드 - 특정 스키마 조건을 만족해야 함 - agent 중심
    - 코드활용 유형의 특징
        - 기존 코드는 많은 분기처리의 집합
    - LLM의 판단이 활용되는 방법
        - 구조화된 출력 (structured output)
        - 도구호출 (tool calling)
- PydanticAI 사용법
    - 간단한 사용법 - agent 정의
    - LLM활용 추상화
        - 멀티에이전트
            - 에이전트 사이의 순서관리 (handoff)
            - 에이전트 오케스트레이션 (autogen 등)
    - 의존성 주입 기능
        - 실행 시점에 필요한 객체, 값등을 전달
    - 멀티 에이전트 ?
        - 도구호출 방식의 멀티 에이전트
            
            ```python
            @main_agent.tool_plain으로 노드 위의 데코레이터 사용
            ```
            
        - 애플리케이션 코드에서 에이전트 실행
            - 애플리케이션 내부 특정 조건에서만 에이전트를 실행하도록 만듦
        - 그래프를 사용한 복잡한 흐름 관리
- Pydantic-Graph와 LangGraph
    - langgraph와 비슷한 기능, 구현하고자 하는 방향성이 비슷
    - 아직 기능이 langgraph보다는 적음 (2025년 1월 15일 공개됨)
        - interrupt(human-in-the-roop), command, memory 기능이 아직 되지는 않음
- QnA
    - 더 안정성이 높다고 할 수는 없으나, 라이브러리의 품질 자체는 높다고 봄
    - PydanticAI 관심을 가진 이유는 pydantic과 AI가 붙었다는 관점에서 지금의 흐름에 맞다고 생각해서  관심이 가서 지켜보고 있음
    - 역할에 맞는 라이브러리르 사용하고 싶어서 pydantic ai 를 사용
    - llama index는 rag 에 좀더 집중적 langchain보다

### 에이전틱 AI가 가져올 검색의 미래 ( 백승윤 | Engineer )
발표 타겟 

- 챗봇을 개발하신 분들
- 에이전틱AI로 실제 가치를 창출하고 싶으신 분들

현재 목적

→ AI와 대화를 통해 상품을 구매하는 오프라인 매장의 경험을 온라인에서도 구현할 수 있게끔 

유저의 개인화된 취향을 알려주면서 해당 추천의 이유에 대해서도 잘 추천해줄 수 있어야 함 

Main Problem - 4 sub-task

- user preference
- recommendation
- explanation
- item information search

추천된 상품리스트를 가지고 친절하게 설명해줘야 함 

쿼리 rewriting 기법 

test-to-sql : keywordsearch 방식 문제

ex) 베이지색 말고 → 베이지색 키워드롤 찾기에 베이지색이 계속 추천이 됨

→ 해결방법: 긍/부정어를 반영, llm rerank 방식 도입 

모든 문제를 llm으로 해결하려고 하지 않아도 됨!!! 

유저에게 채팅위젯으로 입력받는 방식으로도 해결하는 방법을 생각해야 함 

ex) 상품추천을 받고 싶은지/ 상품정보 설명을 듣고 싶은지 등등..

사용자 레벨 수준을 고려

챗봇 경험의 긍정적인 경험들이 쌓이는 게 중요 

QnA

- 저작권문제?
    - 현재 사용 data는 b2b 데이터라 생각 못했음
- bert기반의 분류의 한계를 느꼈는데, 위젯으로 풀었을 때도 한계가 있을거라 생각. 어떻게 해결하는 지?
    - sub task detection 을 다시 해보고싶다는 생각
    - 요즘 모델 성능이 좋아짐 (few shot보다도 zero shot으로도 성능 좋다고함)
- 베이지색 바지 추천해줘 → 카테고리는 바지, 색깔을 베이지로 뽑았을 텐데, 유저에게 좀 더 유저 프리퍼런스를 뽑아내는 방식을 하기 위해 유저에게 가격대는 어느 정도 일지 등등 2-3개 좀 더 추출할 수 있도록 물어봄
- 유저취향이 3개 미만이면 좀 더 물어볼 수 있도록 / 그 이상은 추천을 하도록 하는 등의 룰베이스 기반으로 개발
- 일단 먼저 상품을 보여주되, 좀 더 유저 프리퍼런스를 뽑아볼 수 있도록
### OpenAI Swarm를 활용한 에이전틱AI 시스템 구축 ( 서호건 | 한국원자력연구원 박사 )

### 에이전틱 서치 시스템 구축 | 높아진 Autonomy Level을 중심으로 ( 허훈 | Engineer )
- 코드링크
    
    https://colab.research.google.com/drive/1dPSdEIbcvkbFZWc6lZvbzb8dZeM-edHm#scrollTo=4af524afef6ffda2
    
- 수단으로서 AI > 해결 주체로서의 AI
- fuction calling > chain > router > agent
- perception / thinking/ action
- 새로운 유의미적 가치를 창출하는 개척차로서 인간의 역할이 중요해짐
- 통솔력/공감력/중재력/ 통합력 등의 능력이 점점 중요해질 것으로 봄
- 핸드오프 (핸드오버랑 다른 의미)
    - 한 에이전트에서 다른 에이전트에게 제어권을 전달하여 적절한 전문가가 작업을 수행할 수 있도록 보장
- 루틴: 다단계 작업에서 일관성과 정확성을 유지하기위해 agent가 절차적으로 ~~


