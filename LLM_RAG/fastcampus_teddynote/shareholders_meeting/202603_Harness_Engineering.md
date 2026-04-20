## Harness Engineering 

### 고정된 지식 

* CLAUDE.MD
    - 기본적으로 read
    - 프로젝트 단위로 관리하는 걸추천

* rules
    - 조건부 로딩
    - 기본적으로 read
    - 기능별 규칙 (필요할 때 쓰도록)

* MEMORY
    - 클로드가 자동으로 수정
    - 기본적으로 read/write

---
**추가 팁) ADR(Architecture Decision Records) 변경사항들을 적는 파일을 거기에 넣고, 새롭게 Skill을 만들어서 ADR폴더를 읽고 claude.md/rules.md/memory.md 싱크를 맞추도록 하기
--> 이러한 부분들이 하네스 엔지니어링이다 

---

* custom agent - front meta 정보 항시 로드가 됨  

* claude.md에서 참조할 파일들도 항시 로드가 됨 

* auto memory (root 메모리는 200줄 제한) 
--> /memory 해서 auto memory on 을 켜줘야 함 
(** auto memory로 업데이트 하는 건 memory 이다 claude.md가 아님) 

* advanced memory를 알려면 sub-agent memory에 대해서 알아야 함 
sub-agent 정의 파일(front meta)에 memory 필드가 있음 (기본값으로 사용 안함으로 되어있음) 
sub-agent 사용할 때 memory 기능이 작동됨 
sub-agent 는 컨텍스트 따로 관리할 수 있는데 해당 sub agent가 memory도 따로 관리할 수 있게 됨 -->> 굉장히 좋음!!!! 
(메모리 설정 기능 확인!!)

* /context : 컨텍스트 확인 가능 

---
** 컨텍스트 꽉채워서 1million 사용하면 안됨 !!! 
(why? 26만 토큰정도 컨텍스트 정확도 93% 가 100만 토큰의 컨텍스트가 꽉  채워지면 정확도가  76%로 떨어짐) 


---
### LL(Lesson Learned) - agent builder 300만줄을 클로드코드와 코딩하면서 배우고 얻게된 것들 
- oh-my-opencode
- oh-my-claudecode 
- oh-my-openagent 

** 위의 훌륭한 하네스 엔지니어링 코드를 가져다 쓰는 것은 좋지만, 유명항 시장에서 파는 기성복을 입고 만족하는 정도이다. 여기서 올라갈 수 있는 한계가 있을 수 있다.  
** 내 작업에 최적화 되어있는건 아니기 때문에 기존의 훌륭한 하네스를 바탕으로 내 작업에 맞게 깎아 내는 게 필요하고 중요하다 

**  shft+tab으로 planning mode 굉장히 필요!! 


### 가변적 지식 관련된 부분 
- 가변하는 지식 부분에 사전에 깎고 깎아서 확정된 의사결정만 넣어주어야 함 (context rot이 일어나면 안됨) 
- 플래닝을 할 때 플래닝하더 대화도 가변하는 지식에 포함이 됨! 
- 그렇기 때문에 .claude/plan 폴더 아래 plan용 md 파일을 만들고 거기에 쓰고 clear로 컨텍스트 비우기 

---
** plan.md -> review -> ~~ 
-> (리뷰 하는 로직 꼭 넣어주기!!! -- Agent team 구성해서 )
-> 테디님은 처음에 plan을 촘촘하게 짜지 않는다고 함. 이후 리뷰에서 인프라/ 백엔드/ 프론트엔드 등 관점에서 구체화시킨다고 함. 그래서 구체화된 결과물을 llm에게 넣어주면 결과과 훨씬 더 좋다고 하심 (plan을 오히려 초안처럼 느슨하게 짠다고 하심)
-> 리뷰 단계에서 적극 개입하여 자신의 생각과 일치하도록 만드는 것이 중요 
-> AskUserQuestion 도구를 활용해서 질문 10개 물어봐달라고 설정할 수 도 있음 

---

* Planning 단계에서 철저하게 검증하기
    - Brainstorming skill(superpowers)
    - interview skill을 만들어 두자(나에게 최소 10개 이상의 질문을 하도록 하자  -- AskUserQuestion 도구 사용!!)
    - 이 단계에서 알고 있는 개발 용어와 지식을 총 망라하여 기획/설계를 탄탄하게
    - 검증 Plan에서도 느슨하게 잡지 말고, 최소 85%이상의 coverage를 가져가도록 (그냥 TDD기반으로 테스트코드 짜달라고하면 쉬운 테스트 코드로 만들어서 통과하게끔 하는 경향이 큼. 구체적인 수치와 함께 해당 수치의 coverage 이상을 하도록 검증하게 만드는게 중요)
    - 일반 자연어로 지시하는 것보다 개발/아키텍처 지식을 주입하는 관점이 훨씬 좋음 (software/framework를 공부한 사람이 유리할 수 밖에 없음) 


* Sub-Agent로 분리하면 좋은 점 2가지
    - Main Agent의 Context Window 분리 및 절약
    - 병렬처리 가능(단, 의존성 없는 작업의 경우! 의존성이 있으면 순차적으로 처리해야 함)  

* Skill로 만들어야 하는 것?
    - Claude Code 자체로는 할 수 없는 새로운 기능
    - ex) 카카오톡 메세지 발송/ Gmail 읽어서 요약하는 기능/ HWP문서를 다루는 기능 등
* Agent로 만들어야 하는 것?
    - 독립적인 역할을 가지고 수행하는 일
    - 독립적인 Sub-Agent는 각각의 skill과 도구를 활용할 수 있음(기능 분리) 
* Command
    - 내가 쓸 수 있는 agent들과 skill들을 어떤 순서대로 쓸 것인지 정의해서 묶음으로 묶어준 것 (세부 workflow 느낌이 듦)
    - 한 번만 쓰려면 프롬프트에 그냥 명시하고 말겠으나, 여러 번 그런 순서대로 쓰겠다고 하면 command로 정의해서 만들어주는 게 좋음
    - sub-agent는 다른 sub-agent를 spwan할 수 없기 때문에 command로 오케스트레이션 해줘야 함 (claude code가 재귀호출 방지로 못하게 막아놓음)
    - context window 오염 방지
    - sub-agent는 plan모드가 없음
 
* Hooks

  
* 

### 참고 
* Harness engineering 참고 github 
    - https://github.com/modu-ai/moai-adk
    - https://github.com/Yeachan-Heo/oh-my-claudecode
    - https://ohmyopenagent.com/ko
* 학습용 추천 도큐먼드 
    - https://ohmyopenagent.com/ko/docs
