* (주주총회 진행날짜 : 20261003)


# Jev모델 & Herder 

## Jev 튜토리얼 
* https://github.com/teddylee777/fastcampus-jev

## Herder 
* 백그라운드에서 진행되는 점이 굉장히 큰 장점
* Cluade/ Codex 서로 세션 창을 볼 수 있게 해서 여러 agent에게 위임시키기 좋음 

---

## 1. 유용한 도구 및 시스템

* **[Aside 브라우저](https://aside.com/)**
* 웹 애플리케이션 생성 후 테스트 진행에 유용함.
* 영상 재생 버튼 등 반복 작업을 자동화하도록 지시 가능.
* Discord 연동 지원 (`Computer ↔ Aside ↔ Discord` 구조)으로 외부/모바일 환경에서도 작업 지시 가능.


* **GitHub Label 시스템**
* AI 코딩 및 작업 흐름 관리에 유용한 시스템 (추후 학습 필요).


* **Open Wiki**
* LangChain에서 제작한 Wiki 관리 솔루션 (추후 학습 필요).



---

## 2. 주요 논의 및 Q&A

### Q1. 바이브 코딩(Vibe Coding) 도입을 통한 개인 및 조직 생산성 향상
* 구독 비용 대비 생산성 향상 효과에 대한 검토 및 실무 적용 방안 논의 필요.

### Q2. LLM Agent 성능 평가 및 Failure Attribution 
* **문제의식:** Agent 실패 시 원인이 모델의 Reasoning, Prompt, Tool Schema/Description, Planner/Orchestration 중 어디에 있는지 파악하기 어려움.
* **해결 방안:**
* **Traceability 프레임워크 활용:** LangSmith, Langfuse 등의 Observability 툴 도입.
* **평가 프로세스:** 실행 데이터 DB 적재 $\rightarrow$ 평가 항목 설계 $\rightarrow$ 핵심 지표 수립 및 정량 평가.

### Q3. AI Agent 기반 개발 환경에서의 코드 리뷰 병목 해결
* **문제의식:** 여러 Agent에게 작업을 위임하면서 인간의 검토/검증 및 이해 과정이 주요 병목(Bottleneck)으로 작용.
* **최근 실무 트렌드:**
* 코드 리뷰 자체도 AI Agent에게 위임하는 추세.
* 인간은 Policy(정책) 및 최종 승인 단계만 담당.
* Grok 등 AI Tool에 PR(Pull Request) 링크를 전달하여 전수 조사 수행.

* **참고 자료:**
* [Dioxus 개발자 유튜브 영상](https://www.youtube.com/watch?v=b3I_zBYF3e0)
* [Laurie Voss (npm 창업자) - "코드 리뷰의 종말"](https://youtu.be/-TeOEuplMrQ?si=JHe9PKlQydZC2Dr6)


---

## 3. 추후 조사 예정 리스트 (To-Do)

* [ ] **Ollama + Nimble** 조합 분석
* [ ] **Dot, Muse** 도구 조사
* [ ] **GitHub Label 시스템** 활용법 학습
* [ ] **[tedylee777 GitHub](https://github.com/teddylee777/fastcampus-jev)** - Jev 튜토리얼 RAG 관련 업데이트 내용 확인
