![image](https://github.com/user-attachments/assets/ea0572e2-4774-4193-bc59-71921b59eb30)## Langchain Interrupt Recap 
1) 일정
2025년 5월 31일 (토) 저녁 9시 (약 1시간~1시간 30분)

2) 주제
- LangChain 첫 글로벌 컨퍼런스 후기와 비하인드 스토리
- 실리콘밸리 개발 문화 (feat. 바이브 코딩에 대한 의견)
- 비즈니스적인 수익 창출을 위한 AI 시대 고민
- 그 외 주요 인사이트 정리 및 공유



### Ambient Agent 
![image](https://github.com/user-attachments/assets/b985880b-f2e2-4fcb-8e5e-f03513aae5e3)


![image](https://github.com/user-attachments/assets/27e2f798-fc57-40d7-ba01-088744c3d103)


* Agent inbox 
![image](https://github.com/user-attachments/assets/cf104c09-6153-4f46-a91e-e89605c0589e)
![image](https://github.com/user-attachments/assets/a7e6f5ee-6c99-4a13-ba98-33fcc536f66f)
* Agent inbox 요약 
![image](https://github.com/user-attachments/assets/7531fc45-a38c-4262-83f6-fd4f0b8f2fd1)



### Key note

![image](https://github.com/user-attachments/assets/fe6354bd-ae4d-4da6-8329-e257bdbf7336)

* Agent를 만들 때 필요한 재료 
![image](https://github.com/user-attachments/assets/fee87579-4b9a-4c5d-a10a-48c854703b6c)
-> 이 4가지를 다 할 수 있는 사람이 Agent Engineer

* langchain이 바라본 agnet 의 미래
![image](https://github.com/user-attachments/assets/1757fc41-4755-498a-9ef6-8883778ccfec)
다양한 llm 모델들을 적재적소에 맞게 잘 사용해야 함
llm 모델들을 쉽게 잘 쓸 수 있도록 하겠다고 함

* langchain 이 openai sdk 다운로드보다 많음 
![image](https://github.com/user-attachments/assets/e594f644-714a-4460-a5c3-cedbed1ade9c)

* 신뢰할 수 있는 에이전트는 올바른 컨텍스트에서 시작 
![image](https://github.com/user-attachments/assets/a9f36c9c-2e66-4dc4-9239-245a821f803c)
* 올바른 컨텍스트 관리를 위한 Context Engineering - langGraph를 개발하게 된 이유


* ![image](https://github.com/user-attachments/assets/14709178-34bc-4a45-b2f1-9350473a234d)

* 툴 사용 추적

* ![image](https://github.com/user-attachments/assets/96b3cb64-b2cf-47f6-ba5d-ea82b69b7e47)


![image](https://github.com/user-attachments/assets/44f28dc0-9748-4db3-b557-f46cc9c6677b)

* 모두가 agent builder 가 될 수 있다. Everyone will be an agent builder 
![image](https://github.com/user-attachments/assets/57582992-ef2d-4f74-952c-a7b112c070a4)

-> 이제 앞으로는 비개발자을 위한 도구들도 만들 것이다-- citizen developer! 
(ex- dify, n8n) 

* open agent platform 
![image](https://github.com/user-attachments/assets/8c91100b-1733-436c-8633-355975a56cc5)

* open agent platform  - demo 
![image](https://github.com/user-attachments/assets/c28a8c89-ab74-4a20-934a-0e25a56a0336)

* lang connect
![image](https://github.com/user-attachments/assets/cf07c968-4406-41ed-95ab-46def9e5c90f)

* Arcade dev
![image](https://github.com/user-attachments/assets/e04eed86-ee52-436e-9b71-34e5ded1b8f8)

* langchain의 방향성 - 누구나 에이전트 빌더가 될 수 있게 
![image](https://github.com/user-attachments/assets/e0f53f05-6de6-4084-a111-965657601239)
개발도 쉽게 : ReAct agent / supervisor agent
누구나 쉽게 배포 - LangGraph Studio lv2


 ### 실리콘 밸리 인사이트! 
 * 많은 기업이 이미 AI를 적용하고 있다 : 우버, Cisco, BlackRock, Nu Bank
 ![image](https://github.com/user-attachments/assets/aba92891-d226-4790-a102-10dec337f925)

* Nu bank - 고객이 2억명 (설립연도 2013) 
* ![image](https://github.com/user-attachments/assets/ae4d5051-f72a-45fd-9a87-315eb6d006f6)

* Evaluation에 대한 고민 
우리 서비스에 맞는 평가 방식은 이렇습니다. 라고 소개하는 게 인상깊었음 !
평가 방식에 대한 고민이 각 기업마다 있었음. 그게 굉장히 인상깊었음
우리 프로덕트에 맞는 평가방식을 고민하는 게 중요
고개만족 지표를 어떤 걸로 하는게 적합할 지에 대한 고민 필요
즉, 표준화된, 정해진 평가방식이 정답은 아님
![image](https://github.com/user-attachments/assets/ac258ca8-6a0a-409b-97a2-97f061fec483)


* 우리가 무슨 문제를 풀려고하는가?
고객이 진짜 불편한 게 무엇인가
Agent로 풀어줄 수 있는 문제는 무엇인가
실제 검색시스템을 만들고자 한다면, 실제 현업이 업무를 할 때 어떤 업무에서 검색을 많이 사용하는지
그런 부분을 먼저 찾아서, 문제정의를 하고 특화된 agent 서비스를 만드는 게 중요하다
![image](https://github.com/user-attachments/assets/a741fc4b-ee25-4f8a-8f86-5f8d8f48ac72)

* 비즈니스 인사이트 
![image](https://github.com/user-attachments/assets/9f82b738-1869-4600-bf2d-9810ba08b2b1)

- 마차 vs 자동차 비유 : 마차만 있는 시절에 더 빠른 말만 찾으려고 함, 즉 자동차를 만드는 생각을 못함. 자동차가 없는 시절에 자동차를 만들기 위한 시도들과 도전이 있었기에 자동차가 나온 것

* 추천 책 :말콤 글래드웰의 아웃라이어
