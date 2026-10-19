LangGraph 기반의 챗봇에서 3중 환각 가드(Triple Hallucination Guard)를 설계할 때는, 단순히 하나의 프롬프트로 답변을 검사하는 것을 넘어 **LLM의 역할을 분산하고 결정론적(Deterministic) 필터를 조합**하는 구조가 효과적입니다.

실무에서 주로 사용하는 3중 가드(입력-검색-출력 단계별 검증)의 설계 방식은 다음과 같습니다.

---

### 1단계: 입력 및 검색 단계 (Input & Retrieval Guard)

* **목적**: 엉뚱한 질문을 사전에 차단하고, 답변 생성에 쓸 만한 유효한 문서(Context)가 실제로 검색되었는지 강제 검증합니다.
* **설계 방식 (LangGraph Node)**:
* **무관한 질문 필터링 (Query Guard)**: 사용자의 질문이 사내 문서와 관련이 없는 경우(예: 일상 대화, 정치 등) LLM 또는 분류기를 통해 즉시 턴을 종료(Fallback)시킵니다.
* **검색 임계치 폴백 (Retrieval Threshold Fallback)**: FAISS 등에서 벡터 검색을 수행한 뒤, **유사도 점수(Score)나 BM25 키워드 매칭 결과가 임계치(Threshold) 미만**이면 "관련 문서를 찾지 못했습니다"라는 정형화된 폴백 문구를 반환합니다. (LLM이 아예 모르는 내용을 지어낼 기회를 원천 차단)



### 2단계: 생성 및 근거 강제 단계 (Generation & Source Enforcement Guard)

* **목적**: LLM이 답변을 생성할 때 오직 검색된 사내 문서(Context)만을 근거로 삼도록 제약하고, 출처(Citation) 표기를 강제합니다.
* **설계 방식 (Prompt & Model Configuration)**:
* **System Prompt 제약**: *"제공된 Context에 명시된 내용만 사용하여 답변하시오. Context에 없는 내용은 '정보 없음'이라고 답변하고 임의로 추측하거나 지어내지 마시오. 모든 문장 끝에 출처 문서명을 명시하시오."* 라는 엄격한 룰을 프롬프트에 고정합니다.
* **Structured Output (Pydantic 연동)**: LLM이 자유 서술형태로 대답하는 대신, `답변 내용(Answer)`과 `사용한 근거 문서 목록(Sources)`을 JSON 형태로 강제 출력하도록 설계하여 근거 누락을 방지합니다.



### 3단계: 출력 사후 검증 단계 (Self-Correction / Output Evaluation Guard)

* **목적**: LLM이 생성한 답변에 실제로 환각(Hallucination)이 포함되었는지 최종적으로 교차 검증(Cross-check)합니다.
* **설계 방식 (LangGraph Conditional Edge)**:
* **Self-RAG / NLI(Natural Language Inference) 검증 노드**: 답변이 생성된 후, 이를 별도의 가벼운 평가 모델(또는 동일 LLM의 빠른 체인)에 통과시킵니다.
* *"생성된 답변의 각 주장이 제공된 Context 내에서 온전히 유도될 수 있는가?"*를 판단하게 합니다.


* **라우팅(Conditional Edge)**:
* **Pass**: 검증을 통과하면 사용자에게 답변을 출력합니다.
* **Fail (환각 감지)**: 환각 판정이 나면 그래프를 다시 생성 노드로 돌리거나(재시도), 미리 정의된 안전 폴백 답변("제공된 문서의 내용만으로는 정확한 답변을 드리기 어렵습니다")으로 전환합니다.





---

### 💡 LangGraph 구현 구조 예시 (Conceptual Flow)

```text
[사용자 입력] 
     │
     ▼
(1) [질문/검색 유효성 검증 Node] ──(임계치 미달 / 무관한 질문)──> [폴백 답변 출력]
     │ (통과)
     ▼
(2) [FAISS 문서 검색 Node]
     │
     ▼
(3) [LLM 답변 생성 Node (근거 및 출처 강제)]
     │
     ▼
(4) [환각 검증(Self-Correction) Node] ──(환각 감지)──> [재시도 또는 폴백]
     │ (안전함)
     ▼
[최종 답변 출력]

```

이처럼 LangGraph의 **상태(State) 관리**와 **조건부 엣지(Conditional Edge)** 기능을 활용하면, 환각이 감지되었을 때 흐름을 제어(Loop back 또는 Fallback)하는 파이프라인을 안정적으로 구축할 수 있습니다.

