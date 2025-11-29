
* 코드 : https://github.com/teddynote-lab/deep-agents-from-scratch

* context window 폭발 - vanishing gradient와 유사한 문제
* 단점 : latency가 많이 일어남(도구호출이 많이 일어나므로) / 도구호출에 대한 정확도가 굉장히 높아야 함

* 도구호출 : doc string 중요
 
* State Injection (상태 주입) - LLM에게 전달되지 않음 (시스템 구조적으로 넘김) 

* context-offloading
* context-isolation
  - sub agent에게 위임/격리
 
* 기존 멀티에이전트 방식에서 달라진 점? sub agent가 노드의 구조였다면, -> sub agent가 도구호출의 기능 & 위임/격리
* but 중복 문제 발생 - sub agent의 답변을 그대로 바로 답변하게 하거나 / 요약해주는 방식 등등 ....
* think tool
* langchain docs - deep agent 읽어보기 - middle ware쪽도 반드시!
  - https://docs.langchain.com/oss/javascript/deepagents/overview

* Middleware - To-do-list
* filesystem
  - offsest
  - limit

* ls - lists all files
* 




* 컨텍스트 오프로딩
  - 컨텍스트를 파일, 혹은 가상 메모리에 offloading
  - step_1: 작업 수행 시 해당 작업에 필요할 것으로 추정되는 컨텍스트를 load
  - step_2: agent 판단
  	step_2-a. 작업 수행에 필요한 정보가 충족되었을 경우 작업 수행
  	step_2-b. 불충분한 경우 추가 컨텍스트 loading
      - >2-b에 의해 2를 반복하면서 토큰의 소모는 지속적으로 발생하는 거고, 오프로딩이 해소해주는 부분은 context window limit과 alignment 로 이해

- deep agent는 기존의 ai 에이전트 시스템에 context engineering에 대한 고려를 langgraph를 통해 풀어낸 것




* (참고)컨택스트 매니지먼트 관련 강의 추천 - manus CTO
https://youtu.be/6_BcCthVvb8?si=fxW1iOtvsULlK6Ey
