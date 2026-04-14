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

---
