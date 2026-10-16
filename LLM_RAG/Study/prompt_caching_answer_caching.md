(** 두 가지 모두 "같은 일을 다시 계산하지 않는다"는 발상이지만, 캐싱하는 대상과 위치가 다릅니다.) 

| 구분 | 프롬프트 캐싱 | 응답(답변) 캐싱 |
|---|---|---|
| 캐싱 대상 | 입력 프롬프트의 **앞부분(prefix)** 계산 결과 | LLM이 만든 **최종 답변** |
| 위치 | LLM 제공사 서버 (API 기능) | 우리 애플리케이션 (Redis, DB 등) |
| LLM 호출 | **여전히 호출함**. 앞부분만 재사용 | 캐시가 맞으면 **호출하지 않음** |
| 효과 | 입력 비용 최대 90~95% 절감, 첫 응답까지의 지연 감소 | 비용 0, 지연이 ms 단위로 줄어듦 |
| 위험 | 거의 없음. 답변은 매번 새로 생성됨 | 오래된 답변이나 남의 답변이 나갈 수 있음 |

---

## 1. 프롬프트 캐싱

### 의미
에이전트는 매 턴마다 같은 입력을 반복해서 보냅니다. 시스템 프롬프트, 도구 정의, 사내 규정 문서, 이전 대화가 매번 포함됩니다. LLM은 원래 이 입력 전체를 매번 처음부터 읽고 계산합니다. 프롬프트 캐싱은 **앞부분이 이전 요청과 바이트 단위로 같으면 그 계산 결과를 서버가 보관했다가 재사용**하는 기능입니다.

에이전트에 특히 효과가 큰 이유는 도구 호출 루프 때문입니다. 한 번의 질문에도 LLM을 5~20번 호출하고, 매번 앞부분은 같고 끝에 도구 결과만 붙습니다.

### 핵심 규칙
- **앞부분 일치 방식입니다.** 렌더링 순서는 `tools → system → messages`이고, 중간에 한 글자라도 바뀌면 그 뒤는 모두 캐시 미스가 납니다.
- 변하지 않는 내용은 앞에, 매번 바뀌는 내용(질문, 현재 시각, 요청 ID)은 뒤에 둡니다.
- 최소 길이가 있습니다. 최신 모델(Opus 5.5, Sonnet 5.5, Haiku 5.5)은 512토큰입니다. 이보다 짧으면 오류 없이 캐싱이 되지 않습니다.
- 유지 시간(TTL): 기본 5분이고, 캐시를 읽을 때마다 연장됩니다. 1시간 옵션도 있습니다.
- 비용 (Opus 5.5, 입력 $4/백만 토큰 기준)
  - 캐시 쓰기: 5분 TTL은 1.25배, 1시간 TTL은 2배
  - 캐시 읽기: $0.20/백만 토큰으로 원가의 **0.05배**
  - 5분 TTL이면 2번째 요청부터 이득입니다.

### 코드 예시 (Anthropic Python SDK)

```python
import anthropic

client = anthropic.Anthropic()

# 고정 영역: 매 요청마다 바이트 단위로 동일해야 함
# 주의: 여기에 datetime.now(), 사용자명, 요청 ID 등을 넣으면 캐시가 매번 깨짐
SYSTEM_PROMPT = open("prompts/purchase_agent_system.md", encoding="utf-8").read()
POLICY_DOC = open("docs/구매규정_v3.md", encoding="utf-8").read()  # 수천 토큰짜리 문서

# 도구 목록도 순서를 고정 (dict 순회나 set으로 만들면 순서가 바뀔 수 있음)
TOOLS = [
    {
        "name": "search_po",
        "description": "Oracle EBS에서 구매오더(PO)를 조회한다",
        "input_schema": {
            "type": "object",
            "properties": {"po_number": {"type": "string"}},
            "required": ["po_number"],
        },
    },
]


def ask_agent(messages: list[dict]) -> anthropic.types.Message:
    return client.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        tools=TOOLS,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT},
            {
                "type": "text",
                "text": POLICY_DOC,
                # 명시적 브레이크포인트: tools + system 전체를 캐싱
                "cache_control": {"type": "ephemeral"},  # 5분 TTL
            },
        ],
        # 자동 캐싱: 점점 길어지는 대화 꼬리 부분을 매 턴 자동으로 캐싱
        cache_control={"type": "ephemeral"},
        messages=messages,
    )


# 에이전트 루프: 매 턴 앞부분은 같고 뒤에만 내용이 추가됨
messages = [{"role": "user", "content": "PO-2026-1234 납기 지연 사유 알려줘"}]
resp = ask_agent(messages)

# 캐시 효과 확인 (실제로 캐시가 동작하는지 판단할 수 있는 유일한 근거)
u = resp.usage
print("캐시 쓰기:", u.cache_creation_input_tokens)  # 첫 요청에서 발생 (1.25배 과금)
print("캐시 읽기:", u.cache_read_input_tokens)      # 두 번째 요청부터 발생 (0.05배 과금)
print("일반 입력:", u.input_tokens)                 # 캐시되지 않은 나머지
```

**자주 하는 실수:** 시스템 프롬프트에 `f"오늘은 {datetime.now()}"`를 넣거나, `json.dumps()`를 `sort_keys` 없이 쓰거나, 요청마다 도구 목록을 바꾸는 경우입니다. 그러면 `cache_read_input_tokens`가 계속 0으로 나옵니다. 날짜가 필요하면 시스템 프롬프트가 아니라 사용자 메시지 쪽에 넣으세요.

---

## 2. 자주 묻는 질문의 답변 캐싱

### 의미
"연차 신청 방법", "법인카드 한도 조회 절차"처럼 **많은 사용자가 거의 같은 질문을 반복**하는 경우가 있습니다. 이때 처음 생성한 답변을 저장해 두었다가 LLM을 호출하지 않고 바로 돌려주는 방식입니다. 두 가지 방식이 있습니다.

1. **정확 일치 캐시:** 질문을 정규화(공백, 대소문자, 문장부호 정리)한 뒤 해시값을 키로 씁니다. 단순하고 안전하지만 적중률이 낮습니다.
2. **의미 기반 캐시:** 질문을 임베딩(문장의 의미를 숫자 벡터로 바꾼 것)으로 변환하고, 유사도가 0.93 이상처럼 충분히 높으면 같은 질문으로 봅니다. 적중률은 높지만, 비슷해 보여도 다른 질문을 잘못 매칭할 위험이 있습니다.

### 반드시 지켜야 할 것
- **사용자나 권한에 따라 답이 달라지는 질문은 캐싱하지 않습니다.** 예: "내 PO 현황", "우리 팀 예산". 캐싱하면 다른 사람의 데이터가 노출됩니다.
- 캐시 키에 **법인, 언어, 프롬프트 버전, 원천 문서 버전**을 포함합니다. 규정 문서가 바뀌면 옛 답변이 자동으로 무효화됩니다.
- TTL을 설정합니다. 변동이 잦은 정보는 짧게, 규정 FAQ는 길게 둡니다.
- 도구를 호출한 답변(실시간 조회 결과)은 캐싱하지 않습니다.

### 코드 예시

```python
import hashlib
import json
import re
import time

import numpy as np
from sentence_transformers import SentenceTransformer  # 로컬 임베딩 모델 (사내 GPU 활용 가능)

embedder = SentenceTransformer("BAAI/bge-m3")  # 한국어 지원 임베딩 모델

PROMPT_VERSION = "faq-v3"
DOC_VERSION = "구매규정_2026-09"       # 규정이 개정되면 값만 바꾸면 기존 캐시가 자동 무효화
SIM_THRESHOLD = 0.93                   # 운영 로그로 튜닝 필요 (너무 낮으면 오답 위험)
TTL_SEC = 60 * 60 * 24                 # 24시간


def normalize(q: str) -> str:
    """정확 일치용 정규화: 공백, 문장부호, 대소문자 차이 제거"""
    q = q.strip().lower()
    q = re.sub(r"[?!.。,~]+", "", q)
    return re.sub(r"\s+", " ", q)


def scope_key(company: str, lang: str) -> str:
    """답변이 달라질 수 있는 맥락을 키에 포함"""
    return f"{company}|{lang}|{PROMPT_VERSION}|{DOC_VERSION}"


class AnswerCache:
    """운영 환경에서는 Redis(정확 일치) + 벡터DB(의미 기반)로 교체"""

    def __init__(self):
        self.exact: dict[str, tuple[str, float]] = {}            # key -> (답변, 저장시각)
        self.semantic: list[tuple[str, np.ndarray, str, float]] = []  # (scope, 벡터, 답변, 저장시각)

    def get(self, question: str, scope: str) -> str | None:
        now = time.time()

        # 1단계: 정확 일치 (가장 빠르고 안전)
        k = hashlib.sha256(f"{scope}|{normalize(question)}".encode()).hexdigest()
        hit = self.exact.get(k)
        if hit and now - hit[1] < TTL_SEC:
            return hit[0]

        # 2단계: 의미 유사도 (같은 scope 안에서만 검색)
        qv = embedder.encode(question, normalize_embeddings=True)
        best, best_sim = None, 0.0
        for s, v, ans, ts in self.semantic:
            if s != scope or now - ts >= TTL_SEC:
                continue
            sim = float(np.dot(qv, v))  # 정규화된 벡터이므로 내적 = 코사인 유사도
            if sim > best_sim:
                best, best_sim = ans, sim
        return best if best_sim >= SIM_THRESHOLD else None

    def put(self, question: str, scope: str, answer: str):
        now = time.time()
        k = hashlib.sha256(f"{scope}|{normalize(question)}".encode()).hexdigest()
        self.exact[k] = (answer, now)
        qv = embedder.encode(question, normalize_embeddings=True)
        self.semantic.append((scope, qv, answer, now))


cache = AnswerCache()


def answer(question: str, company: str, lang: str = "ko", personal: bool = False) -> str:
    scope = scope_key(company, lang)

    # 개인화 질문은 캐시를 아예 거치지 않음 (데이터 노출 방지)
    if not personal:
        cached = cache.get(question, scope)
        if cached:
            return cached  # LLM 호출 없이 반환 (비용 0, 지연 수 ms)

    # 캐시 미스: LLM 호출 (이때도 1번의 프롬프트 캐싱은 그대로 적용됨)
    resp = ask_agent([{"role": "user", "content": question}])
    text = "".join(b.text for b in resp.content if b.type == "text")

    # 도구를 쓰지 않은 순수 지식/규정 답변만 저장
    used_tool = any(b.type == "tool_use" for b in resp.content)
    if not personal and not used_tool and resp.stop_reason == "end_turn":
        cache.put(question, scope, text)
    return text
```

---

## 3. 실무에서 함께 쓰는 구조

```
사용자 질문
  ├─ 개인화/실시간 질문인가? ──예──▶ LLM 호출 (프롬프트 캐싱 적용)
  └─ 아니오
       ├─ 답변 캐시 적중 ──▶ 즉시 반환 (LLM 호출 없음)
       └─ 미스 ──▶ LLM 호출 (프롬프트 캐싱 적용) ──▶ 답변 캐시에 저장
```

- **프롬프트 캐싱은 부작용이 거의 없으므로 기본으로 켜는 것을 권장합니다.** 효과는 `usage.cache_read_input_tokens`로 반드시 모니터링하세요.
- **답변 캐싱은 적용 범위를 FAQ성 질문으로 좁혀서 시작하는 것을 권장합니다.** 처음에는 정확 일치만 운영하고, 로그로 적중률과 오답률을 확인한 뒤 의미 기반 캐시와 유사도 임계값을 조정하는 순서가 안전합니다.

이 코드를 실행해 보지는 않았습니다. 지금 작업 중인 프로젝트에 붙여 보고 싶으시면 어떤 에이전트(n8n, Dify, 자체 Python 코드)인지 알려주세요. 그 구조에 맞춰 적용 방법을 정리해 드리겠습니다.
