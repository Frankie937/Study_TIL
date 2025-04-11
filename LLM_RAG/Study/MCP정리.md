(** MCP관련 설명 - 테디노트 유튜브 영상 : https://youtu.be/VKIl0TIDKQg?si=idnD4wuXPS8Jf1kQ )

(** MCP관려 블로그 - https://chatgpt.com/c/67e3a8cf-f1c8-8011-b295-3a74596682d2 ) 


(정리중)

* MCP 배경 
  - 2024년 11월 26일 출시
  - 2025년 2월 19일 Cursor AI에서 MCP 프로토콜 intergration 이후 인기 급상승 


* MCP(Model Context Protocol) 란?
  MCP(Model Context Protocol)는 AI 모델이 외부 데이터 소스와 도구에 연결되어 실시간으로 정보를 주고받을 수 있도록 설계된 프로토콜이다. 이는 AI 모델이 단순히 텍스트를 생성하는 것을 넘어, 필요한 정보를 실시간으로 가져오고 다른 소프트웨어나 데이터 시스템과 협업할 수 있도록 만들어 줍니다


* MCP 관련 테디디노트님의 유스케이스 
  - langcahin rag (local) 
  - Dify - External Knowledge
  - Dify workflow
  - Python Function : 커스텀한 로직들 구현해놓고 호출 할 수 있도록 


* MCP servers 
  - cursor ai settings > MCP > test해볼 수 있음 
  - Claude 데스크탑, Cursor AI에 연결이 가능
    -> 앞으로 Cursor AI뿐만 아니라 다른 IDE, 다른 LLM 서비스에서도 integration이 가능할 것으로 봄(안하면 독점이 되어버리니)


* Vibe Coder
  - Cursor AI를 사용해서 수많은 자료들을 프롬프트 입력만으로 코드를 작성하도록 


* Lagnchain이나 LangGraph 코드는굉장히 빨리 바뀌어서 Rag시스템을 사용해야만 하는데, 현재 GPT나 Claude 에 물어봐도 제대로 된 최신 코드가 아닌 outdated된 코드를 주는 경우가 많음


* smithery 
  - 현재 넘버원 MCP 서버
  - tool market place라고 보면 됨


### MCP의 핵심 구성요소 (출처: https://dytis.tistory.com/112)
![image](https://github.com/user-attachments/assets/558f3cf1-5c53-4ac9-a6b8-bad8495b626d)

-> MCP는 클라이언트-서버 아키텍처를 기반으로 하며, AI 모델과 외부 데이터 소스 간의 원활한 통신을 가능하게 하는 구조로 설계 되었음 
-> MCP는 다음 3가지 핵심 구성 요소로 이루어져 있음 

* 호스트(Host)
  - AI 애플리케이션의 컨테이너이자 조정자 역할
  - 여러 클라이언트 인스턴스를 관리
  - 클라이언트 연결 권한과 생명주기를 제어
  - 보안 정책과 등의 요구사항을 시행
  - AI/LLM 활용 및 샘플링을 조정
  - 클라이언트 간 컨텍스트 집계를 관리
  - ex) Claude App, IDEs, AI 도구들

*  MCP 클라이언트(MCP Clients)
  - 호스트에 의해 생성되며 서버와의 독립적인 연결을 유지함
  - 서버당 하나의 상태 유지 세션을 설정
  - 프로토콜 형상 및 기능 교환을 처리
  - 양방향으로 프로토콜 메시지를 라우팅함
  - 구독 및 알림을 관리
  - 서버 간 보안 경계를 유지함

* MCP 서버(MCP Servers)
  - 특화된 컨텍스트와 기능을 제공
  - MCP 기본 요소를 통해 리소스, 도구 및 프롬프트를 노출함
  - 독립적으로 작동하며 집중된 책임을 가짐
  - 클라이언트는 인터페이스를 통해 샘플링을 요청함
  - 보안 제약을 준수해야 합
  - 로컬 프로세스 또는 원격 서비스일 수 있음


### MCP의 작동방식 
1) 연결 설정 (Connection Establishment)
 
2) 컨텍스트 교환 (Context Exchange)

3) 도구 호출 (Tool Invocation)

4) 결과 처리 (Result Processing)
   

### Client의 역할 
-Client의 역할은 호스트와 MCP서버 간에 소통이 되도록 통역사라고 생각하면 좋음 

### MCP관련 커뮤니티 긍정/부정적 반응
- 긍정적 반응 
  - 표준화 - 플랫폼 간 호환성 증대, 플러그인 파편화 해소 
  - 생산성 향상
  - 오픈소스 구현 늘어나 신뢰도 상승 

- 부정적 반응
  - 복잡성 증가 (기존 플러그인 방식보다 러닝커브가 있음)
  - 기존 기술 활용 아쉬움: "결국 HTTP API 래핑 아니냐", "OpenAPI나 gRPC 같은 기존 표준을 활용했다면 더 좋았을 것" 이라는 의견도 나옵니다. 
- 권한 및 보안 문제: OAuth가 추가되었지만, 여전히 세분화된 권한 관리 모델 부재에 대한 우려가 있습니다. "엔터프라이즈급 보안 요구사항 충족에는 미흡하다", *"민감한 작업(결제 등)에 쓰기엔 불안하다"*는 지적입니다.
전반적으로 커뮤니티는 MCP의 가능성에 기대를 걸면서도, 실제 적용 과정에서의 어려움과 개선 필요성에 대해 솔직한 의견을 나누며 프로토콜의 발전을 지켜보는 분위기입니다.




### 최근 MCP 업데이트 (2025.03.26) 
1. 보안 강화: OAuth 2.1 인증 도입 
2. 원격 연결성 향상: HTTP 스트리밍 지원
3. 개발 편의성 증대: SDK 및 도구 개선 
** BUT 아직 해결해야 할 문제들이 있음 : 세분화된 권한 관리, 복잡성 완화 등 

### MCP 로드맵
- MCP Roadmap : https://modelcontextprotocol.io/development/roadmap
(MCP 로드맵에는 OAuth 기반 원격 지원 강화, 서비스 디스커버리, 상태 없는 서버리스 MCP 등의 계획들이 있음)

