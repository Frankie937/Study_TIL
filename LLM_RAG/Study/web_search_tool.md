
(** Agent tool로 사용할 web search tool 

## 1. DuckDuckGo Search Tool
- **특징:** 구글이나 Bing처럼 별도의 API 등록 없이 바로 사용 가능, 오픈소스 에이전트 프레임워크에서 자주 활용.[1]
- **예시:** LangChain, CrewAI 등에서 `DuckDuckGoSearchTool` 모듈로 외부 검색 결과를 에이전트가 받아와 요약, 분석에 활용.

## 2. Google Mariner (Bard 기반)
- **특징:** 실시간 웹 검색, Google의 최신 Bard를 기반으로 검색 결과 제공. 리치 스니펫, 실험적 베타 제공.[2]
- **예시:** 실시간 트렌드 조사, 뉴스 파악 등에 활용. 공식 API는 일부 제한적이지만, Agents/플러그인 형태로 연동되는 경우 활용도 높음.

## 3. You.com
- **특징:** AI 챗봇/에이전트 기반의 웹서치, 프라이버시 모드, 산업별 맞춤화, Pro 요금제는 커스텀 에이전트/워크플로우까지 지원.[3]
- **예시:** 자연어로 “2025년 최신 AI 투자 동향 요약” 요청 시, 실시간 웹에서 핵심정보 추출 후 대화형으로 결과 제공.

## 4. Genspark AI Browser
- **특징:** AI 브라우저 내장형. Super Agent, Autopilot, Model Context Protocol 등 AI 개인비서-도구 자동화, 웹 요약, 쇼핑비교 등 반복작업 자동화.[4]
- **예시:** “트위터 피드 요약”, “논문 다운로드”, “GitHub 이슈 자동 생성”과 같은 멀티 API 워크플로우 수행.

## 5. 오픈소스 Web Agent 프레임워크 (AgentGPT, SuperAGI, Nanobrowser 등)
- **특징:** 직접 AI agent 구성, 웹서치 단계와 응답 자동화. Python, 브라우저 확장, 커스텀 워크플로우 구현 지원.[5]
- **예시:** 브라우저 플러그인 형태의 Nanobrowser로 웹페이지 내 정보 수집, 자동 클릭·추출 작업. AgentGPT에서 직접 “리서치 agent” 만들어 연속 검색·요약 가능.


## Reference (출처) 

[1] https://www.youtube.com/watch?v=FUthk7B3EuE
[2] https://virusart.tistory.com/entry/AIAgentProcess
[3] https://nogood.io/blog/generative-ai-search-tools/
[4] https://discuss.pytorch.kr/t/genspark-ai-browser-ai-agent-browser/7115
[5] https://research.aimultiple.com/open-source-web-agents/
[6] https://wikidocs.net/264624
[7] https://x2bee.tistory.com/433
[8] https://www.gpters.org/dev/post/RBbEy3H9IT6UBBE
[9] https://docs.crewai.com/ko/tools/search-research/tavilysearchtool
[10] https://teddylee777.github.io/langchain/langchain-agent/
