(** 세미나를 준비하며 정리한 Jev Model 내용) 

# Jev 모델 정리 : 문장 대신 '판단'을 반환하는 System One Model

> **TL;DR**
> - Jev는 2026년 9월 TypeSafe AI가 공개한 모델로, 문장을 생성하지 않고 **코드가 바로 쓸 수 있는 "판단 + 확률"** 을 반환합니다.
> - GPT·Claude가 "말을 잘하는 AI(System 2)"라면, Jev는 **"작은 판단을 빠르고 싸게 내리는 AI(System 1)"** 입니다.
> - 에이전트 안의 수많은 작은 판단(라우팅, 필터링, 검증)을 LLM 대신 Jev에게 맡기고, **흐름은 코드가, 어려운 추론만 LLM이** 담당하는 구조가 핵심입니다.
> - Multi-Agent의 Supervisor 라우팅, Subagent 결과 검증, RAG의 Reranker 단계에 **대체 또는 추가**로 붙이기 좋습니다.

---

## 목차

1. Jev란 무엇인가?
2. Jev는 어떻게 동작하는가?
3. 기존 기술과의 비교
4. 실제 시스템 적용 : 역할 분리
5. Multi-Agent · Subagent 구조에서의 활용
6. Reranker · RAG 파이프라인에서의 활용
7. 적합한 Task와 도입 시 고려사항
8. 마치며

---

## 1. Jev란 무엇인가?

### 1.1 개요

- **공개** : 2026년 9월 15일, TypeSafe AI
- **만든 사람** : OpenAI 연구원 출신 디오고 알메이다(Diogo Almeida, TypeSafe 공동창업자·CEO)
- **한 줄 정의** : *"Unstructured state in, typed probabilistic decisions out"*
  → 정리되지 않은 입력을 받아, **정해진 형식의 확률적 판단**을 돌려주는 모델

### 1.2 등장 배경 : 작은 판단마다 LLM을 부르는 문제

웹 에이전트가 일을 하나 처리할 때도, 내부에서는 작은 판단이 끊임없이 일어납니다.

```text
지금 페이지가 원하는 페이지인가?   → LLM 호출
어떤 버튼을 눌러야 하는가?         → LLM 호출
로그인이 필요한가?                 → LLM 호출
검색 결과가 충분한가?              → LLM 호출
이 링크는 관련 있는가?             → LLM 호출
```

간단한 판단에도 매번 박사님을 부르는 셈입니다. 아무리 저렴한 LLM을 쓰더라도 판단이 쌓이면 문제가 생깁니다.

| 병목 | 내용 |
|---|---|
| **Latency (지연 누적)** | 호출마다 몇 초씩, 판단이 쌓일수록 전체 응답이 느려짐 |
| **Cost (비용 누적)** | 답변 토큰을 매번 생성 → 호출 수만큼 비용 증가 |
| **Context (맥락 비대)** | 판단 기록이 계속 쌓여 모델이 앞 내용을 놓치기 쉬움 |

그래서 **"작은 판단만 빠르고 싸게 처리하는 AI"** 가 필요해졌고, 그 답으로 나온 것이 Jev입니다.

### 1.3 System One Model

TypeSafe는 Jev를 **System One Model**이라는 새로운 카테고리의 첫 모델로 소개합니다. 노벨경제학상 수상자 대니얼 카너먼이 대중화한 사고 체계 구분에서 가져온 이름입니다.

| 구분 | System 1 | System 2 |
|---|---|---|
| 특징 | 빠르고 직관적인 판단 | 느리고 숙고하는 추론 |
| 예시 | "저 사람 지금 화났네" | 복잡한 계산, 여행 계획 세우기 |
| 대응 모델 | **Jev** – 작고 명확한 판단을 빠르고 저렴하게 | **Reasoning LLM** (GPT·Claude·Gemini) – 복잡한 추론·글 작성 |
| 한마디로 | 판단을 빠르게 내리는 AI | 말을 잘하는 AI |

### 1.4 이름의 의미 : 제번스의 역설(Jevons Paradox)

Jev라는 이름은 19세기 영국 경제학자 **윌리엄 스탠리 제번스**에서 따왔습니다. 제번스의 역설은 "효율이 좋아져 자원 비용이 낮아지면, 새로운 사용처가 늘어 오히려 전체 소비가 증가할 수 있다"는 개념입니다.

```text
AI 판단 비용 ↓  →  AI를 쓸 수 있는 영역 ↑  →  전체 AI 판단 사용량 ↑
```

TypeSafe의 가설도 같습니다. AI 판단 비용이 충분히 싸지면, "이런 데까지 AI를?" 하던 작은 판단까지 AI에게 맡기게 된다는 것입니다. 즉 **AI 판단을 소프트웨어의 기본 부품**으로 만들겠다는 목표입니다.

---

## 2. Jev는 어떻게 동작하는가?

### 2.1 문장 대신 판단

고객이 *"중복 결제된 것 같은데, 하나는 빨리 환불해 주세요."* 라고 문의했다고 해 보겠습니다.

**생성형 LLM의 출력 (사람이 읽는 설명문)**

```text
이 고객은 중복 결제 문제를 겪고 있으며 환불을 요청하고 있습니다.
긴급성이 비교적 높은 문의로 판단됩니다.
```

**Jev의 출력 (코드가 바로 쓰는 데이터)**

```text
department  = billing   (Choice, 0.82)
frustration = 1.4       (Score, 0~2)
is_urgent   = 0.95      (Noul)
```

### 2.2 입력 구조 : State · Questions · Criteria

```text
State (판단 대상) + Questions (판단 질문) + Criteria (판단 기준)
        → Jev →  Typed Decision + Probability
```

| 요소 | 의미 | 비유 |
|---|---|---|
| **State** | 무엇을 보고 판단할지. 고객 문장, 사용자 query + 검색 문서, 이전 context 등. 텍스트 또는 JSON 객체 | 시험 지문 |
| **Questions** | 무엇을 판단할지. 개발자가 Jev에게 던지는 판단 질문 (`instructions`) | 시험 문제 |
| **Criteria** | 어디까지를 Yes/어느 선택지로 볼지 정하는 경계 | 채점 기준 |

> **헷갈리기 쉬운 점** : "사용자 질문(query)"과 "판단 질문(questions)"은 다릅니다. 사용자 query는 매번 바뀌는 입력이라 **State 안에 들어가는 데이터**이고, 판단 질문은 개발자가 고정해 두는 **질문**입니다.

### 2.3 3가지 판단 질문 타입 (Primitive)

| 타입 | 묻는 것 | 출력 | 예시 |
|---|---|---|---|
| **Choice** | 어느 것인가? | 선택지 하나 + 선택지별 확률 + confidence | 고객 문의 → billing / technical / sales |
| **Score** | 어느 정도인가? | 사용자가 정한 단계 사이의 위치값 | 불만 수준 0(calm) ~ 2(angry) → 1.4 |
| **Noul** | 참인가? (= Boolean) | Yes일 확률 0~1 | "긴급한 요청인가?" → 0.95 |

Noul은 1에 가까우면 강한 Yes, 0에 가까우면 강한 No, 0.5 근처면 불확실하다는 뜻입니다.

모든 출력은 **개발자가 미리 정의한 답변 공간(Answer Space) 안에서만** 나옵니다. 선택지에 없는 답을 지어내지 않습니다.

### 2.4 예시 코드 (공식 Quick start)

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()  # TYPESAFE_API_KEY 환경변수 사용, 기본 모델: jev-latest

ticket = "Hi, I've been trying to connect my Stripe account for 3 days and the integration keeps failing. I'm losing sales. Please help ASAP."

response = client.system_one(
    state=ticket,                                   # 판단 대상
    questions={                                     # 판단 질문들
        "department": Choice(
            instructions="Which team should handle this",
            criteria={                              # 판단 기준 (선택지)
                "billing": "Payment or subscription issues",
                "technical": "Bugs or integration problems",
                "sales": "Pricing or account questions",
            },
        ),
        "frustration": Score(
            instructions="How frustrated the customer appears",
            criteria=[
                "Calm, just stating facts",
                "Frustrated but civil",
                "Very angry, strong language",
            ],
        ),
        "is_urgent": Noul(
            instructions="The message conveys urgency or time-sensitivity",
        ),
    },
)

print(response.answers["department"].choice)  # "technical"
print(response.answers["frustration"].score)  # 1.0
print(response.answers["is_urgent"].noul)     # 1.0
```

응답 예시에는 판단값과 함께 `confidence`, `probabilities`가 들어 있습니다.

```json
"department": {
  "type": "choice",
  "choice": "technical",
  "confidence": 0.78,
  "probabilities": { "technical": 0.85, "sales": 0.0, "billing": 0.15 }
}
```

### 2.5 핵심 사용법 ① 질문 쪼개기 (Atomic Decomposition)

"이 상품은 좋은 상품인가?"처럼 큰 질문을 한 번에 묻지 않습니다. 작게 쪼개서 각각 확률을 받고, **최종 판단은 코드가** 합니다.

```text
"이 상품은 좋은 상품인가?"  (한 번에 통째로 묻기 ✕)
   ├─ 가격이 적절한가?      → 0.88
   ├─ 리뷰 반응이 좋은가?   → 0.91
   └─ 배송 불만이 적은가?   → 0.76

final = 0.4×가격 + 0.4×리뷰 + 0.2×배송 = 0.87   ← 가중치·규칙은 사람이 명시
```

- 질문이 작을수록 판단이 정확해집니다.
- 점수가 낮을 때 "배송 때문이구나" 하고 이유를 설명할 수 있습니다.
- 공식 문서도 "고객이 환불을 원하고 화가 났는가?"처럼 두 조건을 섞지 말고 **질문을 따로 나누라**고 권장합니다.

### 2.6 핵심 사용법 ② 똑똑한 if문 (Semantic If-Statement)

숫자 조건은 코드로 쉽게 쓰지만, 의미 조건은 기존 코드로는 쓸 수 없었습니다. Jev는 **if-else 구문에 지능을 넣는 부품**입니다.

```python
# 기존 if문 : 숫자·규칙으로 표현 가능한 조건만
if price > 100:
    apply_discount()

# Semantic if : '의미'로 판단해야 하는 조건 (이해를 돕기 위한 의사코드)
if jev("고객이 환불을 요청하는가?") > 0.8:
    escalate_to_manager()
if jev("검색 문서가 관련 있는가?") > 0.9:
    use_as_evidence()
```

### 2.7 Playground 실험 : 확률은 '의미'를 따라 움직인다

판단 질문과 판단 기준은 고정하고, **State(고객 문장)만 바꿔** 본 결과입니다.

- 판단 질문 : *Does the customer explicitly request a refund?*
- True 기준 : 명시적으로 환불을 요청함 / False 기준 : 요청하지 않음·원치 않는다고 함

| State (고객 문장) | P(True) | 해석 |
|---|---|---|
| "Please refund the duplicate charge." | **99%** | 명백한 환불 요청 |
| "Is a refund possible?" | **23%** | 환불을 '문의'했지만 '요청'은 아님 |
| "I was charged twice." | **7%** | 결제 문제만 설명, '환불'이라는 단어조차 없음 |

"refund"라는 단어가 있느냐가 아니라, 정의한 **의미 기준**에 맞춰 판단했습니다. 단, 23%는 "환불을 원할 확률"이 아니라 **"정한 질문·기준에서 True에 준 확률"** 이라는 점에 주의해야 합니다.

### 2.8 확률을 믿을 수 있는 이유 : RLCD와 Calibration

Jev는 **RLCD(Reinforcement Learning for Calibrated Decisions)** 로 학습되었습니다.

| 학습 방식 | 보상을 주는 기준 | 결과 |
|---|---|---|
| RLHF | 사람이 더 좋아하는 답변 | 친절하고 자연스러운 답변 |
| RLVR | 검증 가능한 정답을 맞힘 | 수학·코딩 정답률 향상 |
| **RLCD** | **확률이 실제 정답률과 일치함** | "0.9"라고 하면 실제로 약 90% 맞는 모델 |

정답이 Yes인 문제에 A는 0.99, B는 0.55, C는 0.10이라고 답했다면, 단순 채점에서는 A와 B가 똑같이 1점입니다. RLCD는 이 둘을 구분하고, C처럼 **자신 있게 틀리는 것**에 큰 벌점을 줍니다. 그래서 확신이 없을 때는 확률을 낮게 말하도록 학습됩니다.

이렇게 확률이 실제 정답률에 맞춰진 성질을 **Calibration(보정)** 이라고 합니다. 공식 문서 표현으로는 *"0.2의 확률을 준 일은 실제로 약 20% 일어나야 한다"* 입니다.

> Calibration은 "0.9라고 답한 문제들을 모으면 약 90%가 맞는다"는 **통계적 성질**입니다. 개별 답 하나의 정답을 보장하지는 않습니다.

---

## 3. 기존 기술과의 비교

### 3.1 "LLM에게 JSON으로 답하라고 하면 되지 않나?"

결과는 비슷해 보일 수 있지만, 만들어진 목적이 다릅니다.

```text
LLM + JSON :  입력 → 다음 토큰 생성 반복 → 텍스트 → JSON 형식 제약 → 판단
Jev        :  State + 질문 + 기준 → 판단 모델 → 확률 분포 (정해진 답변 공간)
```

| 구분 | LLM + JSON 출력 | Jev |
|---|---|---|
| 최적화 목표 | 자연스럽고 그럴듯한 문장 | 보정된(Calibrated) 판단 |
| 출력 범위 | 자유 생성 → 형식을 제약으로 맞춤 (**JSON 깨짐** 가능) | 정의한 선택지 안에서만 반환 |
| 확률 | 요청하면 '말로' 적어줌 (**얼마나 믿어도 되나?**) | 모든 판단에 확률이 기본 포함 |
| 여러 질문 | 한 번의 생성 안에서 이어서 작성 | 같은 State를 두고 독립적으로 병렬 평가 |
| 비용·지연 | 출력 토큰 요금 + **몇 초씩 지연** | 출력 토큰 생성 없음 |

### 3.2 속도와 비용

TypeSafe 자체 실험 결과(특정 워크플로 기준)입니다.

| 지표 | 수치 |
|---|---|
| 속도 | 기존 LLM 대비 **193.6배** 빠름 |
| 비용 | 기존 LLM 대비 **444.6배** 저렴 |
| 가격 (Jev 1.13, 2026.09.21 기준) | 입력 토큰 100만 개당 **$0.042**, **출력 토큰 무료** |
| 스펙 | Context 최대 64k 토큰, 텍스트 입력만 지원 |

빠르고 싼 이유는 구조에 있습니다. LLM은 답변을 토큰 단위로 하나씩 생성하므로 생성량만큼 시간과 비용이 듭니다. 반면 Jev는 출력 문장을 생성하지 않고, 한 요청 안의 여러 질문을 병렬로 처리합니다.

> 193.6배·444.6배는 **TypeSafe 자체 측정치**이므로 독립적인 검증이 더 필요합니다.

### 3.3 아키텍처는 공개되었나?

공개되지 않았습니다. TypeSafe는 Jev가 **"새로운 아키텍처 + 병렬 샘플러 + RLCD"** 로 구성된 새 스택이라고만 밝혔습니다. 트랜스포머 기반 여부, 베이스 모델, 파라미터 수, 가중치는 모두 비공개이며, 자체 호스팅 없이 API로만 제공됩니다.

확실한 차이는 **출력 방식**입니다. GPT·Claude는 토큰을 하나씩 이어 생성(autoregressive)하지만, Jev는 모든 판단과 확률을 한 번에 병렬로 산출합니다.

---

## 4. 실제 시스템 적용 : 역할 분리

### 4.1 계층형 구조

```text
[기존] 모든 것을 LLM 에이전트에게
  LLM: 생각 → Tool 호출 → 결과 확인 → LLM: 다음 판단 → Tool 호출 → ...

[제안] 역할을 나눈 계층형 구조
  Input → Workflow(코드)
            ├─ Deterministic Code : 정해진 규칙·계산·흐름 제어     (항상)
            ├─ Jev × N            : 분류·필터링·경로 선택, 대량·병렬 (자주)
            └─ Reasoning LLM      : 복잡한 추론·최종 답변 작성       (가끔)
```

회사로 치면 매뉴얼 업무는 시스템이, 빠른 분류는 실무자가, 어려운 판단만 임원이 하는 구조입니다.

### 4.2 Jev 확률을 쓰는 2가지 방식

**① 확률 구간별 라우팅 (Confidence-aware Routing)**

```text
p > 0.90         → 자동 처리 (근거로 바로 채택)
0.60 < p ≤ 0.90  → 추가 검증 (강한 LLM 또는 사람에게)
p ≤ 0.60         → 제외·보류
```

공식 문서는 오탐(잘못된 Yes)의 비용이 크면 0.8~0.9, 놓침(잘못된 No)의 비용이 크면 0.3~0.5를 임계값으로 쓰고, 중간 구간은 검토자에게 보내라고 안내합니다.

**② 여러 판단을 규칙으로 결합**

```python
if (relevance > 0.9
    and support > 0.8
    and credibility > 0.8
    and contradiction < 0.2):
    evidence.append(doc)
```

> **원칙** : Jev의 결과는 '최종 결론'이 아니라 '확률 신호'입니다. 질문별 확률은 독립적으로 평가되므로 "뒷받침"과 "충돌"이 동시에 높게 나올 수도 있습니다. 모순 해결과 최종 승인은 **코드와 규칙 엔진이 명시적으로** 관리해야 합니다.

### 4.3 예시 : 웹 검색 에이전트

```text
웹 검색 (후보 50건)
   → Jev : 문서마다 4개 기준 병렬 판단
        relevance 0.96 / support 0.81 / credibility 0.88 / contradiction 0.12
   → 코드 필터 (조건 통과 5건)
   → Reasoning LLM : 최종 답변 작성
```

| 효과 | 내용 |
|---|---|
| 비용 | LLM이 읽는 문서 50건 → 5건으로 감소 |
| 속도 | 문서별 판단을 병렬로 빠르게 처리 |
| 품질 | 관련 없는 문서가 답변에 섞이지 않음, 컨텍스트 관리 |

*(문서 건수·확률값은 이해를 돕기 위한 예시)*

---

## 5. Multi-Agent · Subagent 구조에서의 활용

Multi-Agent 구조에서는 에이전트끼리 일을 주고받을 때마다 **"누구에게 넘길까?", "이 결과로 충분한가?", "다음 단계로 가도 되나?"** 같은 판단이 반복됩니다. 이 판단은 대부분 Supervisor LLM이나 각 Subagent의 LLM이 **글을 생성하며** 내리고 있습니다. Jev는 이 중 **"정해진 선택지 안에서 고르는 판단"** 을 떼어내 맡기기 좋습니다.

### 5.1 활용 지점 한눈에 보기

| 활용 지점 | 기존 방식 | Jev 활용 | 대체 / 추가 |
|---|---|---|---|
| **Supervisor 라우팅** | Supervisor LLM이 다음 Subagent를 텍스트로 선택 | `Choice`로 Subagent 선택 + confidence 게이트 | 대체 (애매할 때만 LLM Supervisor로 fallback) |
| **Tool·Skill 선택** | 에이전트 LLM이 도구 설명을 읽고 선택 | `Choice`로 후보 순위 → 상위 후보 `Noul`로 재확인 | 대체 또는 추가 (사전 필터) |
| **Subagent 결과 검증** | 결과 전체를 메인 에이전트 컨텍스트에 전달 | `Noul`로 "작업 완료?", "근거 포함?" 판정 후 통과분만 전달 | 추가 (게이트) |
| **루프 종료 판단** | LLM이 매 턴 "더 찾아야 하나?" 판단 | `Noul`로 "정보가 충분한가?" 판정 | 대체 |
| **입출력 가드레일** | 별도 LLM 모더레이션 호출 | `Noul` + `Score` 한 요청으로 위험 유형·심각도 판정 | 대체 또는 추가 |

### 5.2 Supervisor 라우팅을 Jev로 대체하기

Supervisor 패턴에서 Supervisor LLM의 역할 중 상당 부분은 **"이 요청을 어느 Subagent에게 보낼지"** 고르는 분류 작업입니다. 이 부분을 Jev `Choice`로 바꾸고, **confidence가 낮을 때만** 기존 LLM Supervisor에게 넘깁니다.

```python
from typesafe_sdk import Choice, Score, TypeSafeClient

client = TypeSafeClient(model="jev-1.13.0")  # 운영에서는 버전 고정 권장

ROUTER_QUESTIONS = {
    "next_agent": Choice(
        instructions="Which specialist agent should handle the user's latest request?",
        criteria={
            "order_agent":    "Order status, delivery, or shipment tracking",
            "product_agent":  "Questions about product details, ingredients, or recommendations",
            "refund_agent":   "Refunds, cancellations, or duplicate charges",
            "research_agent": "Requires searching external or internal documents",
            "other":          "None of the above",   # 선택지에는 '기타'를 꼭 포함
        },
    ),
    "complexity": Score(
        instructions="How complex is it to resolve this request?",
        criteria=["Simple lookup", "Needs some reasoning", "Complex, multi-step"],
    ),
}

def route(user_msg: str, history_summary: str) -> str:
    res = client.system_one(
        state={"latest_request": user_msg, "conversation_summary": history_summary},
        questions=ROUTER_QUESTIONS,
    )
    agent = res.answers["next_agent"]
    complexity = res.answers["complexity"]

    # 확신이 낮거나, '기타'이거나, 복잡도가 높으면 → 기존 LLM Supervisor에게 위임
    if agent.confidence < 0.6 or agent.choice == "other" or complexity.score > 1.5:
        return "llm_supervisor"
    return agent.choice
```

- 대부분의 **평범한 요청은 Jev 한 번**으로 바로 Subagent에 배정됩니다.
- **애매한 요청만** 기존 LLM Supervisor가 처리하므로 비용과 지연이 줄어듭니다.
- 공식 문서의 **Intent routing** 패턴도 같은 구조입니다. 의도를 분류한 뒤 결정론적 코드, 전문 LLM, 사람 중 적합한 곳으로 보내고, 분류 confidence가 0.5 미만이면 사람에게 넘깁니다.

### 5.3 Tool · Skill 선택

도구나 스킬이 많아질수록 에이전트가 **엉뚱한 도구를 부르거나 불필요하게 부르는** 문제가 커집니다. 공식 Cookbook 두 가지가 참고가 됩니다.

- **Skill suggestion**
  - 182개 스킬 전체를 `Choice`로 순위 매깁니다.
  - 상위 3개는 상세 설명과 함께 `Noul`("이 스킬이 실제로 이 작업을 하는가?")로 다시 확인합니다.
  - 488개 요청 테스트에서 **잘못 로드한 비율이 16.8% → 7.3%**, **불필요하게 로드한 비율이 9.8% → 4.0%** 로 줄었습니다.
- **Function calling**
  - 도구 이름은 `Choice`로 고릅니다.
  - 인자는 정해진 목록(Literal) 안에서만 고르게 해서 **"문장 → 함수명 + 인자"** 로 변환합니다.
  - 이때 confidence는 전체 판단 중 **가장 확신이 낮은 판단 기준**으로 보고됩니다.

즉 Jev를 **"도구 라우터"** 로 앞단에 두면, 메인 LLM의 프롬프트에 모든 도구 설명을 넣지 않아도 됩니다. 필요한 도구만 골라 넣을 수 있어 **컨텍스트 절약**에도 도움이 됩니다.

### 5.4 Subagent 결과 검증 게이트 (Context Engineering)

Deep Agent류 구조에서 Subagent를 쓰는 이유 중 하나는 **컨텍스트 격리**입니다. Subagent가 따로 작업하고 결과만 메인 에이전트에게 돌려주는 방식이죠. 여기서 Jev를 **Subagent → 메인 에이전트 사이의 게이트**로 둘 수 있습니다.

```text
Subagent 결과
   → Jev (Noul × 3)
        task_completed        : 요청한 작업을 끝냈는가?
        has_supporting_source : 근거(출처)를 포함하는가?
        off_topic             : 요청과 무관한 내용이 섞였는가?
   → 코드 규칙
        통과 → 메인 에이전트 컨텍스트에 추가
        미흡 → Subagent 재시도 (이유 태그와 함께)
        애매 → 메인 LLM이 직접 확인
```

- 메인 에이전트가 **검증되지 않은 긴 결과를 매번 읽지 않아도** 됩니다.
- 재시도 여부를 LLM이 아니라 **확률 + 규칙**으로 정하므로 동작이 예측 가능해집니다.

*(설계 아이디어로, 공식 Cookbook이 아닌 적용 예시입니다.)*

### 5.5 한 번의 호출로 여러 판단 받기 (Speculative fan-out)

Jev는 한 요청의 질문들을 **병렬로** 평가하므로, 질문을 늘려도 응답 시간이 거의 늘지 않습니다. 공식 문서의 **Speculative fan-out** 패턴은 이 특성을 활용합니다.

- 지금 당장 필요하지 않을 수도 있는 질문까지 미리 한 번에 묻습니다.
  - 예 : 카테고리, 버그 심각도, 재현 단계 유무, 환불 요청 여부, 불만 수준
- 코드가 필요한 값만 골라 씁니다.

Multi-Agent에서는 **라우팅과 사전 정보 추출을 한 번에** 끝내고, 선택된 Subagent에게 추출한 값을 함께 넘기는 식으로 쓸 수 있습니다.

### 5.6 대체하지 말아야 할 부분

| Jev로 대체하기 좋은 것 | LLM에 남겨둬야 할 것 |
|---|---|
| 정해진 선택지 중 고르기 (라우팅, 도구 선택) | 작업 계획 수립 (Planning, To-do 작성) |
| 참/거짓 확인 (완료 여부, 근거 포함 여부, 종료 조건) | 선택지를 미리 정할 수 없는 열린 판단 |
| 정도 매기기 (복잡도, 긴급도, 심각도) | 보고서·답변·코드 생성, 요약 |

---

## 6. Reranker · RAG 파이프라인에서의 활용

### 6.1 Reranker와 Jev의 차이

| 구분 | Cross-encoder Reranker | LLM Reranker | Jev |
|---|---|---|---|
| 판단 기준 | 질문–문서 **의미 유사도** (고정) | 프롬프트로 설명한 기준 | **자연어로 정의한 판단 질문 + 기준** |
| 출력 | 관련도 점수 1개 | 생성된 텍스트(순위·점수) → 파싱 | 기준별 **보정된 확률** |
| 확장성 | 새 기준을 쓰려면 재학습 필요 | 유연하지만 느리고 비쌈 | 유연하고 빠름 |
| 한계 | "비슷하지만 답은 없는 문서"를 못 거름 | 출력 토큰 비용, 형식 깨짐 | 후보마다 호출 → 후보 수만큼 비용 |

Reranker가 **"얼마나 비슷한가"** 를 본다면, Jev는 **"우리가 정한 기준을 만족하는가"** 를 봅니다.

### 6.2 활용 방식 ① Reranker 대체 : Noul 확률로 재정렬

공식 **Re-ranking Cookbook**은 `Noul` 확률을 그대로 정렬 점수로 씁니다.

```python
question = Noul(
    instructions="Is this candidate the cited precedent?",
    criteria=NoulCriteria(
        true="Candidate states the specific rule",
        false="Candidate is only on a similar topic",   # '비슷한 주제'와 '정답'을 명시적으로 구분
    ),
)
# 후보마다 호출 → answers[...].noul (0~1) 기준으로 정렬
```

법률 판례 데이터셋(CLERC)에서 BM25로 쿼리당 30개 후보를 뽑은 뒤 Jev로 재정렬한 결과입니다.

| 지표 | BM25만 | BM25 + Jev 재정렬 |
|---|---|---|
| 1위 적중 | 5% | **18%** |
| Top 5 적중 | 15% | **35%** |
| Top 10 적중 | 38% | **62%** |

비용은 1,200회 호출(153만 입력 토큰)에 **약 $0.0645**였습니다.

> 이 비교는 **BM25 단독 대비** 결과이며, Cross-encoder Reranker와 직접 비교한 수치는 아닙니다.

포인트는 `criteria.false`에 **"비슷한 주제일 뿐인 문서"** 를 명시해, 유사도 기반 Reranker가 놓치는 경계를 판단 기준으로 직접 정의했다는 점입니다.

### 6.3 활용 방식 ② Reranker 뒤에 추가 : 검증 게이트

기존 Retriever/Reranker는 그대로 두고, 그 뒤에 Jev를 **분류 게이트**로 붙이는 방식입니다. 공식 **Classifying RAG passages Cookbook**의 구조입니다.

```text
임베딩 검색 (코사인 유사도 상위 12개)
   → Jev : 패시지마다 Noul 4개
        is_relevant               : 질문 주제를 다루는가?
        contains_answer_evidence  : 직접 답할 근거가 있는가?
        contradicts_query_premise : 질문의 전제와 충돌하는가?
        contains_prompt_injection : 모델을 조종하려는 문장이 있는가?
   → 코드 라우팅 (위에서부터 먼저 걸리는 규칙 적용)
        1) injection > 0.70      → 제외
        2) contradiction > 0.70  → '충돌 근거' 블록으로 분리
        3) relevance < 0.45      → 제외
        4) evidence > 0.55       → 포함
        5) 그 외                 → 제외
   → LLM : '답변 근거'와 '전제와 충돌하는 근거'를 구분해서 답변 생성
```

- 평균적으로 검색된 패시지의 **2/3 이상이 제외**되었습니다.
- 유사도 **1위였던 프롬프트 인젝션 문서**(유사도 0.584)가 인젝션 확률 **0.99**로 걸러졌습니다. 유사도만으로는 절대 거를 수 없는 문서입니다.
- 사용자 질문이 **잘못된 전제**를 담고 있을 때, 전제와 충돌하는 문서를 별도로 넘겨 LLM이 "그 전제는 틀렸다"고 답할 수 있게 합니다.

### 6.4 어떤 방식을 고를까?

| 상황 | 추천 |
|---|---|
| 후보가 적고(수십 건) 기준이 도메인 특화 | **대체** : Jev Noul로 재정렬 |
| 후보가 많음(수백~수천 건) | **추가** : Retriever/Reranker로 먼저 줄이고 → Jev로 조건 검증 |
| 보안·신뢰성이 중요 (외부 웹 문서, 사용자 업로드) | **추가** : 인젝션·신뢰성·충돌 여부 게이트 필수 |
| 순위보다 "쓸지 말지"가 중요 | **추가** : 확률 임계값으로 포함/제외 라우팅 |

> **주의** : Jev는 후보마다 호출하므로 **비용이 후보 수에 비례**합니다. 서로 다른 질문의 확률끼리는 직접 비교하지 말고, 같은 질문의 확률끼리만 정렬에 쓰는 것이 안전합니다.

---

## 7. 적합한 Task와 도입 시 고려사항

### 7.1 적합한 Task / 적합하지 않은 Task

| 적합 (판단) | 부적합 (생성) |
|---|---|
| 고객 문의·내부 문서 **유형 분류** (Choice) | 긴 보고서 작성 |
| RAG **근거 문서 필터링** (Noul) | 코드 생성 |
| 에이전트 **경로 선택·라우팅** (Choice) | 복잡한 수학 추론 |
| 긴급도·불만도·심각도 **판단** (Score) | 문서 전체 요약 |
| 입출력 **가드레일** (Noul + Score) | 자연스러운 장문 설명 |

공식 가이드도 *"이 메시지가 긴급한가?"* 처럼 빠르고 좁은 판단에는 바로 쓰고, *"분석해서 최선의 조치를 정하라"* 같은 복합 질문은 **작게 분해**해서 쓰라고 권장합니다.

### 7.2 도입 시 반드시 고려할 3가지

1. **안전장치 (Fallback / Escalation)**
   확률이 애매하거나(예: 50~60%) 낮을 때 LLM이나 사람에게 넘기는 우회 로직을 설계합니다.
2. **우리 데이터로 신뢰성 검증**
   Jev도 범용 데이터로 학습된 모델입니다. 실제 업무 데이터로 먼저 평가해서, 확률 구간별 실제 정답률이 맞는지 확인해야 합니다. 예를 들어 0.9라고 한 건들이 실제로 약 90% 맞는지 봅니다.
3. **판단 질문·기준 설계 (Atomic Design)**
   문구 하나로 결과가 달라집니다. 작고 명확한 질문, 명시적인 판단 기준을 쓰고, **Choice 선택지에는 '기타(other)'를 꼭 포함**합니다.

### 7.3 알아둘 한계

- **"Zero Hallucination"의 의미** : 선택지 밖의 답을 지어내지 않는다는 뜻이지, 판단이 틀리지 않는다는 뜻은 아닙니다. 타입은 맞지만 내용이 틀린 판단(예: 정답이 부산인데 서울 0.91)은 가능합니다.
- **공개 초기 모델** : 2026년 9월 공개된 모델이라, 실제 업무 데이터에서의 독립 검증이 아직 부족합니다.
- **비공개 사항** : RLCD로 학습했다는 것 외에 아키텍처와 학습 레시피는 공개되지 않았습니다.
- **입력 제약** : 텍스트 입력만 지원하며, context는 최대 64k 토큰입니다.

> **Jev 기반 시스템의 품질** = 모델 성능 + 좋은 분류 체계 + 질문 분해 + 적절한 임계값 + 우회 로직 + 명시적인 코드

---

## 8. 마치며

지금까지의 AI 시스템은 **하나의 큰 LLM이 생각하고, 판단하고, 글까지 쓰는** 방향으로 발전해 왔습니다.

```text
[기존]  Input → Reason · Generate → Text
[Jev]   State → Semantic Judgment → Typed Probability → Code · Rules → Action
```

Jev의 의미는 "GPT 경쟁 모델이 하나 더 나왔다"가 아닙니다. **"생성(Generation)과 판단(Decision)을 꼭 같은 모델이 모두 해야 하는가?"** 라는 AI 시스템 설계 차원의 질문을 던진다는 점이 중요합니다.

특히 Multi-Agent와 RAG처럼 **판단이 반복되는 구조**일수록 효과가 큽니다. Supervisor 라우팅, Subagent 결과 검증, Reranker 뒤의 근거 게이트처럼 작은 판단을 Jev에게 넘기면 속도, 비용, 컨텍스트를 함께 줄일 수 있습니다. 다만 아직 초기 모델인 만큼, 작은 과제로 **우리 데이터에서 먼저 검증**하고 확장하는 접근을 권장합니다.

---

## References

- [TypeSafe AI – Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [TypeSafe Docs – Quick start](https://docs.typesafe.ai/introduction/quickstart)
- [TypeSafe Docs – Noul](https://docs.typesafe.ai/primitives/noul)
- [TypeSafe Docs – AI primer (RLCD)](https://docs.typesafe.ai/introduction/machine-learning-primer)
- [TypeSafe Docs – Intent routing](https://docs.typesafe.ai/patterns/intent-routing)
- [TypeSafe Docs – Confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing)
- [TypeSafe Docs – Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out)
- [TypeSafe Cookbook – Re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe)
- [TypeSafe Cookbook – Classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages)
- [TypeSafe Cookbook – Skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion)
- [TypeSafe Cookbook – Function calling](https://docs.typesafe.ai/cookbooks/function_calling)
- [TypeSafe Cookbook – Guardrails for LLMs](https://docs.typesafe.ai/cookbooks/llm_guardrails)
- [velog – Jev가 뭐길래 : 생성형 AI와 무엇이 다를까?](https://velog.io/@sobit/Jev)
- [YouTube – Jev 소개 영상](https://www.youtube.com/watch?v=lx3YkhzM_04)
- [Jev Playground](https://jevplayground.com/)
- [Turing Post – What Is Jev AI? Inside TypeSafe's RLCD Model](https://www.turingpost.com/p/what-is-jev-rlcd)
