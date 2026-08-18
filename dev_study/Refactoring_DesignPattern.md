# 리팩토링과 디자인 패턴 — 주니어 개발자를 위한 실전 가이드 (Python)

> 이 문서의 목표: "이름만 아는" 상태에서 "월요일 아침 내 코드에 적용할 수 있는" 상태로.
> 모든 예제는 실제 업무 상황(주문·재고·배송·정산·시스템 연동)을 소재로 합니다.

---

## 0. 두 개념의 관계부터

| | 리팩토링(Refactoring) | 디자인 패턴(Design Pattern) |
|---|---|---|
| 무엇 | 겉으로 보이는 **동작은 그대로 두고 내부 구조만** 개선하는 작업 | 반복되는 설계 문제에 대한 **검증된 해결책의 이름표** |
| 비유 | 창고 정리 (물건은 그대로, 배치만 바꿈) | 창고 정리의 정석 레이아웃 도면 |
| 언제 | 코드를 만질 때마다, 조금씩 | 같은 문제가 3번째 반복될 때 |

**핵심은 이 둘의 관계입니다.**

> 디자인 패턴은 처음부터 그려놓고 시작하는 설계도가 아니라,
> **냄새나는 코드를 리팩토링하다 보면 도착하게 되는 목적지**입니다.

주니어가 가장 많이 하는 실수가 "패턴을 써보고 싶어서 패턴부터 적용"하는 것입니다.
순서는 항상 이렇습니다.

```
동작하는 코드 작성 → 냄새를 감지 → 작게 리팩토링 → (반복되면) 패턴으로 정착
```

---

# 1부. 리팩토링

## 1.1 정의: 동작은 불변, 구조는 개선

리팩토링의 정의에서 가장 중요한 단어는 **"동작을 바꾸지 않는다"** 입니다.

```
✅ 리팩토링   : 함수를 3개로 쪼갰다. 입력/출력은 동일하다.
❌ 리팩토링 X : 함수를 3개로 쪼개면서 김에 할인 로직 버그도 고쳤다.
```

두 번째가 왜 문제일까요? 테스트가 깨졌을 때 **구조 변경 때문인지 기능 변경 때문인지 알 수 없기** 때문입니다.
그래서 이런 원칙이 있습니다.

> **두 개의 모자 (Two Hats)**
> "기능 추가" 모자와 "리팩토링" 모자를 동시에 쓰지 않는다. 번갈아 쓴다.
> 커밋도 분리한다. `refactor:` 커밋과 `feat:` 커밋은 따로.

## 1.2 왜 하는가

가장 설득력 있는 이유는 이겁니다.

> 코드는 **쓰는 시간보다 읽는 시간이 10배** 깁니다.
> 리팩토링은 미래의 나(그리고 인수인계 받을 동료)의 읽는 시간을 줄이는 투자입니다.

부수 효과로 얻는 것들:

- 버그가 숨을 곳이 줄어든다 (함수가 짧으면 버그가 눈에 띈다)
- 기능 추가 속도가 빨라진다
- 테스트를 붙일 수 있는 모양이 된다

## 1.3 언제 하는가

| 타이밍 | 설명 |
|---|---|
| **3의 법칙** | 같은 코드를 처음 쓸 땐 그냥 쓴다. 두 번째는 참는다. **세 번째에 리팩토링한다.** |
| **준비를 위한 리팩토링** | 기능 추가가 어렵다면, 먼저 **추가하기 쉬운 구조로 바꾼 뒤** 추가한다. 가장 효율이 좋은 타이밍. |
| **이해를 위한 리팩토링** | 남의 코드를 읽다 이해한 내용을 변수명·함수명으로 코드에 새겨둔다. |
| **보이스카우트 규칙** | 캠핑장을 떠날 땐 올 때보다 깨끗하게. 파일 하나 만질 때 그 주변만 조금 정리한다. |

**하지 말아야 할 때도 있습니다.**

- 어차피 곧 통째로 버릴 코드
- 테스트가 하나도 없고, 만들 수도 없는 레거시 (→ 먼저 특성화 테스트부터)
- 마감 3시간 전 (리팩토링은 리스크가 0이 아님)

## 1.4 안전벨트: 테스트

**테스트 없는 리팩토링은 리팩토링이 아니라 도박입니다.**

```python
# 리팩토링 전에 최소한 이 정도는 만들어 둡니다.
def test_배송비_계산_기본():
    assert calculate_shipping_fee(order_amount=25000, is_cold=True) == 3000

def test_배송비_계산_무료배송_기준():
    assert calculate_shipping_fee(order_amount=50000, is_cold=True) == 0
```

리팩토링 사이클은 이렇게 돕니다.

```
테스트 통과 확인 → 아주 작은 변경 1개 → 테스트 실행 → 통과 → 커밋 → (반복)
```

한 번에 30분어치를 바꾸고 테스트를 돌리면, 깨졌을 때 어디서 깨졌는지 찾느라 하루를 씁니다.
**작게, 자주.**

---

## 1.5 코드 냄새 6종과 처방

"코드 냄새(Code Smell)"는 **버그는 아니지만 구조에 문제가 있다는 신호**입니다.

### 냄새 1. 긴 함수 (Long Method) → 함수 추출

가장 흔하고, 가장 효과가 큰 리팩토링입니다.

**Before — 주문 처리 함수 하나가 모든 걸 다 함**

```python
def process_order(order):
    # 1. 검증
    if not order["items"]:
        raise ValueError("주문 상품이 없습니다")
    if order["amount"] <= 0:
        raise ValueError("주문 금액이 올바르지 않습니다")

    # 2. 배송비 계산
    fee = 0
    if order["amount"] < 50000:
        fee = 3000
        if order["is_cold"]:
            fee += 1500
        if order["region"] in ("제주", "울릉도"):
            fee += 3000

    # 3. 적립금 계산
    point = int(order["amount"] * 0.01)
    if order["grade"] == "VIP":
        point = int(order["amount"] * 0.03)

    # 4. 저장
    total = order["amount"] + fee
    db.save({"order_id": order["id"], "total": total, "point": point})
    return total
```

무엇이 문제일까요? **"배송비 계산 로직만 테스트하고 싶은데 방법이 없습니다."**
DB까지 붙여야 테스트가 됩니다. 그리고 함수 이름 `process_order`는 이 함수가 뭘 하는지 아무것도 알려주지 않습니다.

**After — 의미 단위로 추출**

```python
JEJU_ISLANDS = ("제주", "울릉도")


def validate_order(order):
    if not order["items"]:
        raise ValueError("주문 상품이 없습니다")
    if order["amount"] <= 0:
        raise ValueError("주문 금액이 올바르지 않습니다")


def calculate_shipping_fee(amount, is_cold, region):
    if amount >= 50000:
        return 0
    fee = 3000
    if is_cold:
        fee += 1500          # 냉장/냉동 포장 비용
    if region in JEJU_ISLANDS:
        fee += 3000          # 도서산간 추가
    return fee


def calculate_point(amount, grade):
    rate = 0.03 if grade == "VIP" else 0.01
    return int(amount * rate)


def process_order(order):
    validate_order(order)
    fee = calculate_shipping_fee(order["amount"], order["is_cold"], order["region"])
    point = calculate_point(order["amount"], order["grade"])
    total = order["amount"] + fee
    db.save({"order_id": order["id"], "total": total, "point": point})
    return total
```

**무엇이 좋아졌나**

- `process_order`를 읽으면 **처리 순서(줄거리)가 4줄로 보입니다.** 세부사항은 필요할 때만 내려가서 봅니다.
- `calculate_shipping_fee`는 DB 없이 단독 테스트가 가능합니다.
- 제주 배송비 정책이 바뀌면 고칠 곳이 **한 군데**로 명확합니다.

> 💡 **판단 기준**: 함수에 주석으로 `# 1. 검증`, `# 2. 계산` 같은 단계 주석을 달고 있다면,
> 그 주석은 사실 **"여기를 함수로 빼세요"** 라는 신호입니다. 주석 문구가 곧 함수 이름이 됩니다.

---

### 냄새 2. 매직 넘버 / 매직 문자열 → 상수·Enum

**Before**

```python
def get_delivery_slot(order):
    if order["type"] == 1:
        return "새벽배송"
    elif order["type"] == 2:
        return "택배"
    elif order["type"] == 3:
        return "직배송"
```

`1`, `2`, `3`이 뭔지 아는 사람은 이 코드를 쓴 사람뿐입니다. 6개월 뒤엔 본인도 모릅니다.

**After — Enum 사용**

```python
from enum import Enum


class DeliveryType(Enum):
    DAWN = 1      # 새벽배송
    PARCEL = 2    # 일반 택배
    DIRECT = 3    # 직배송 (물류센터 → 매장)


SLOT_NAMES = {
    DeliveryType.DAWN: "새벽배송",
    DeliveryType.PARCEL: "택배",
    DeliveryType.DIRECT: "직배송",
}


def get_delivery_slot(delivery_type: DeliveryType) -> str:
    return SLOT_NAMES[delivery_type]
```

**얻는 것**

- `DeliveryType.DAWN`은 자기 설명적입니다.
- 오타 방지: `DeliveryType.DAWNN`은 즉시 에러, `"dawnn"` 문자열은 조용히 통과.
- IDE 자동완성이 됩니다.

---

### 냄새 3. 중첩 조건문 → 가드 절 (Guard Clause)

**Before — 화살표 모양 코드 (Arrow Anti-pattern)**

```python
def can_ship_today(order):
    if order is not None:
        if order["status"] == "PAID":
            if order["stock_ok"]:
                if datetime.now().hour < 14:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
```

들여쓰기가 오른쪽으로 계속 밀립니다. 진짜 로직은 4단계 안쪽에 숨어 있습니다.

**After — 예외 상황을 먼저 걸러내고 나간다**

```python
CUTOFF_HOUR = 14  # 당일 출고 마감 시각


def can_ship_today(order) -> bool:
    if order is None:
        return False
    if order["status"] != "PAID":
        return False
    if not order["stock_ok"]:
        return False
    return datetime.now().hour < CUTOFF_HOUR
```

**핵심 아이디어**: "안 되는 조건"을 위에서 **먼저 return으로 탈출**시키면,
아래로 내려올수록 코드는 "정상 케이스"만 남습니다. 들여쓰기가 평평해집니다.

> 💡 주니어가 자주 헷갈리는 것: `if ...: return True else: return False`는
> 그냥 `return ...` 로 쓰면 됩니다. 조건식 자체가 이미 True/False입니다.

---

### 냄새 4. 긴 파라미터 목록 → 파라미터 객체

**Before**

```python
def create_shipment(order_id, receiver_name, receiver_phone, address1,
                    address2, zipcode, is_cold, memo, requested_date):
    ...

# 호출부 — 순서 하나 틀리면 전화번호 자리에 주소가 들어갑니다
create_shipment("ORD-1", "홍길동", "010-0000-0000", "서울시 강남구",
                "101동 202호", "06000", True, "부재시 경비실", "2026-08-20")
```

**After — dataclass로 묶기**

```python
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Receiver:
    name: str
    phone: str
    address1: str
    address2: str
    zipcode: str


@dataclass(frozen=True)
class ShipmentRequest:
    order_id: str
    receiver: Receiver
    is_cold: bool
    requested_date: date
    memo: str = ""


def create_shipment(request: ShipmentRequest):
    ...


# 호출부 — 무엇이 무엇인지 명확합니다
req = ShipmentRequest(
    order_id="ORD-1",
    receiver=Receiver("홍길동", "010-0000-0000", "서울시 강남구", "101동 202호", "06000"),
    is_cold=True,
    requested_date=date(2026, 8, 20),
    memo="부재시 경비실",
)
create_shipment(req)
```

**부가 효과**: 나중에 "수령인 주소 전체를 한 줄로 합치기" 같은 로직이 필요해지면
`Receiver` 안에 메서드로 넣으면 됩니다. **데이터와 그 데이터를 다루는 로직이 한곳에 모입니다.**

```python
@dataclass(frozen=True)
class Receiver:
    ...
    def full_address(self) -> str:
        return f"({self.zipcode}) {self.address1} {self.address2}"
```

---

### 냄새 5. 반복되는 분기문 → 딕셔너리 디스패치

**Before — 채널이 추가될 때마다 이 함수를 열어야 함**

```python
def get_commission_rate(channel):
    if channel == "자사몰":
        return 0.0
    elif channel == "쿠팡":
        return 0.12
    elif channel == "네이버":
        return 0.06
    elif channel == "마켓컬리":
        return 0.15
    else:
        raise ValueError(f"알 수 없는 채널: {channel}")
```

**After — 데이터로 분리**

```python
COMMISSION_RATES = {
    "자사몰": 0.0,
    "쿠팡": 0.12,
    "네이버": 0.06,
    "마켓컬리": 0.15,
}


def get_commission_rate(channel: str) -> float:
    try:
        return COMMISSION_RATES[channel]
    except KeyError:
        raise ValueError(f"알 수 없는 채널: {channel}") from None
```

**왜 좋은가**: 채널 추가가 **로직 수정이 아니라 데이터 추가**가 됩니다.
나중에 이 표를 DB나 설정 파일로 옮기면 코드 배포 없이 수수료율을 바꿀 수 있습니다.

분기마다 하는 **일(동작)이 다르다면** 값 대신 함수를 담습니다.

```python
def parse_coupang(raw): ...
def parse_naver(raw): ...
def parse_kurly(raw): ...

PARSERS = {
    "쿠팡": parse_coupang,
    "네이버": parse_naver,
    "마켓컬리": parse_kurly,
}


def parse_order(channel: str, raw: dict):
    parser = PARSERS.get(channel)
    if parser is None:
        raise ValueError(f"파서가 없는 채널: {channel}")
    return parser(raw)
```

> 이 지점에서 이미 **Strategy 패턴 / Factory 패턴의 문턱**을 넘고 있습니다.
> 2부에서 다시 만나게 됩니다.

---

### 냄새 6. 기능 편애 (Feature Envy) → 메서드 이동

"어떤 함수가 자기 데이터보다 **남의 데이터를 더 많이 만지는**" 냄새입니다.

**Before**

```python
class Order:
    def __init__(self, items):
        self.items = items  # [{"price": 3000, "qty": 2}, ...]


def print_receipt(order):
    subtotal = sum(item["price"] * item["qty"] for item in order.items)
    vat = int(subtotal / 11)
    count = sum(item["qty"] for item in order.items)
    print(f"총 {count}개 / 합계 {subtotal}원 (부가세 {vat}원)")
```

`print_receipt`는 이름만 "출력"이지, 실제로는 `Order`의 내부를 뒤져서 계산까지 다 합니다.

**After — 계산 책임을 데이터가 있는 곳으로 이동**

```python
class Order:
    def __init__(self, items):
        self.items = items

    @property
    def subtotal(self) -> int:
        return sum(item["price"] * item["qty"] for item in self.items)

    @property
    def item_count(self) -> int:
        return sum(item["qty"] for item in self.items)

    @property
    def vat(self) -> int:
        return int(self.subtotal / 11)


def print_receipt(order: Order):
    print(f"총 {order.item_count}개 / 합계 {order.subtotal}원 (부가세 {order.vat}원)")
```

이제 `print_receipt`는 **정말로 출력만** 합니다. 그리고 합계 계산이 필요한 다른 곳(정산, 리포트)에서도
같은 `order.subtotal`을 씁니다. **중복 계산 로직이 사라집니다.**

> 💡 판단 기준: `a.b.c.d` 처럼 점(.)이 3개 이상 이어지거나,
> 남의 객체 속성을 3개 이상 꺼내 쓰고 있다면 "그 로직을 저쪽으로 옮길 때"입니다.

---

## 1.6 리팩토링 체크리스트

작업 전:
- [ ] 이 코드에 테스트가 있는가? 없으면 먼저 만든다
- [ ] 지금 기능 추가와 섞고 있지 않은가?

작업 중:
- [ ] 한 번에 한 가지만 바꾸고 있는가?
- [ ] 테스트를 5~10분 안에 다시 돌리고 있는가?

작업 후:
- [ ] 함수 이름만 읽어도 하는 일이 짐작되는가?
- [ ] 커밋 메시지를 `refactor:`로 시작할 수 있는가? (기능 변경이 섞였다면 못 씁니다)

---

# 2부. 디자인 패턴

## 2.0 시작 전 마음가짐

패턴은 **어휘(vocabulary)** 입니다.
"채널별로 파싱 방식이 다른데 런타임에 바꿔 끼워야 해서 인터페이스를 두고..."를
**"Strategy로 갔어요"** 한마디로 끝낼 수 있게 해주는 것, 그게 패턴의 1차 효용입니다.

패턴은 크게 셋으로 나뉩니다.

| 분류 | 관심사 | 이 문서에서 다루는 것 |
|---|---|---|
| **생성 (Creational)** | 객체를 **어떻게 만들까** | Factory |
| **구조 (Structural)** | 객체를 **어떻게 조립할까** | Adapter, Decorator |
| **행위 (Behavioral)** | 객체가 **어떻게 협력할까** | Strategy, Observer, Template Method |
| (+ 실무 필수) | 계층 분리 | Repository |

---

## 2.1 Strategy (전략) — "알고리즘을 갈아 끼운다"

### 어떤 문제를 푸나

배송비 정책이 **고객 등급/이벤트/채널마다 다르고, 자주 바뀝니다.**
`if grade == "VIP": ... elif event == "무료배송데이": ...`가 계속 늘어납니다.

### 코드

```python
from abc import ABC, abstractmethod


class ShippingPolicy(ABC):
    """배송비 계산 전략 인터페이스"""

    @abstractmethod
    def calculate(self, amount: int) -> int:
        ...


class StandardPolicy(ShippingPolicy):
    def calculate(self, amount: int) -> int:
        return 0 if amount >= 50_000 else 3_000


class VipPolicy(ShippingPolicy):
    def calculate(self, amount: int) -> int:
        return 0 if amount >= 30_000 else 1_500


class FreeShippingEventPolicy(ShippingPolicy):
    def calculate(self, amount: int) -> int:
        return 0


class Checkout:
    def __init__(self, policy: ShippingPolicy):
        self._policy = policy          # 전략을 주입받는다

    def total(self, amount: int) -> int:
        return amount + self._policy.calculate(amount)


# 사용
print(Checkout(StandardPolicy()).total(25_000))            # 28000
print(Checkout(VipPolicy()).total(25_000))                 # 26500
print(Checkout(FreeShippingEventPolicy()).total(25_000))   # 25000
```

### 무엇이 좋아졌나

- **새 정책 추가 시 기존 코드를 열지 않습니다.** 클래스 하나 추가하면 끝 (개방-폐쇄 원칙).
- 각 정책을 개별적으로 테스트할 수 있습니다.
- 런타임에 정책 교체가 가능합니다 (`checkout._policy = VipPolicy()`).

### 언제 쓰나 / 언제 쓰지 마나

| 쓴다 | 안 쓴다 |
|---|---|
| 같은 목적, 다른 방식이 3개 이상 | 분기가 2개고 앞으로도 안 늘어날 때 |
| 정책이 자주 추가/변경됨 | 그냥 `if`가 훨씬 읽기 쉬울 때 |

> 🐍 **파이썬 팁**: 파이썬에서는 클래스 없이 **함수만으로도 Strategy가 됩니다.**

```python
def standard(amount): return 0 if amount >= 50_000 else 3_000
def vip(amount):      return 0 if amount >= 30_000 else 1_500


def total(amount, policy=standard):
    return amount + policy(amount)


print(total(25_000))        # 28000
print(total(25_000, vip))   # 26500
```

상태(설정값)를 들고 있을 필요가 없다면 **함수 버전이 더 파이썬답습니다.**
자바 책의 클래스 계층을 그대로 옮기지 마세요.

---

## 2.2 Factory (팩토리) — "생성 로직을 한곳에 모은다"

### 어떤 문제를 푸나

채널별 주문 파서를 만드는 코드가 여기저기 흩어져 있습니다.
채널이 추가되면 그 `if` 블록들을 전부 찾아 고쳐야 합니다.

### 코드

```python
from abc import ABC, abstractmethod


class OrderParser(ABC):
    @abstractmethod
    def parse(self, raw: dict) -> dict:
        ...


class CoupangParser(OrderParser):
    def parse(self, raw: dict) -> dict:
        return {
            "order_no": raw["orderId"],
            "amount": int(raw["totalPrice"]),
            "channel": "쿠팡",
        }


class NaverParser(OrderParser):
    def parse(self, raw: dict) -> dict:
        return {
            "order_no": raw["productOrderId"],
            "amount": int(raw["totalPaymentAmount"]),
            "channel": "네이버",
        }


class ParserFactory:
    """생성 규칙을 이 클래스 한 곳에만 둔다"""

    _registry = {
        "쿠팡": CoupangParser,
        "네이버": NaverParser,
    }

    @classmethod
    def create(cls, channel: str) -> OrderParser:
        parser_cls = cls._registry.get(channel)
        if parser_cls is None:
            raise ValueError(f"지원하지 않는 채널: {channel}")
        return parser_cls()

    @classmethod
    def register(cls, channel: str, parser_cls):
        """신규 채널 연동 시 여기로 등록"""
        cls._registry[channel] = parser_cls


# 사용 — 호출부는 어떤 클래스가 만들어지는지 몰라도 된다
parser = ParserFactory.create("쿠팡")
print(parser.parse({"orderId": "C-1", "totalPrice": "35000"}))
# {'order_no': 'C-1', 'amount': 35000, 'channel': '쿠팡'}
```

### 무엇이 좋아졌나

- **"어떤 구현체를 쓸지"라는 결정이 한 곳에 모입니다.** 채널 추가 = `_registry`에 한 줄.
- 호출부는 `OrderParser` 인터페이스만 알면 됩니다. 결합도가 낮아집니다.

### 주의

팩토리 자체가 거대한 `if` 덩어리가 되면 문제를 옮기기만 한 것입니다.
위 예제처럼 **딕셔너리 레지스트리**로 두면 그 함정을 피할 수 있습니다.

---

## 2.3 Adapter (어댑터) — "안 맞는 인터페이스를 끼워 맞춘다"

### 어떤 문제를 푸나

우리 시스템은 `send(to, message)` 인터페이스를 기대하는데,
새로 도입한 외부 SMS 업체 SDK는 `dispatch(phone_number, body, sender_id)`입니다.
게다가 이 업체는 1년 뒤 바뀔지도 모릅니다.

이럴 때 **우리 코드 전체를 외부 SDK 모양에 맞추면 안 됩니다.** 어댑터를 하나 끼웁니다.

### 코드

```python
from abc import ABC, abstractmethod


# --- 우리가 원하는 표준 인터페이스 ---
class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> bool:
        ...


# --- 외부 SDK (우리가 못 고침) ---
class VendorSmsSDK:
    def dispatch(self, phone_number, body, sender_id):
        print(f"[SMS] {sender_id} -> {phone_number}: {body}")
        return {"result_code": "0000"}


class LegacyErpMailer:
    """레거시 ERP의 사내 메일 발송 모듈 (인터페이스가 또 다름)"""
    def send_mail(self, addr, title, content):
        print(f"[MAIL] {addr} / {title} / {content}")
        return 1  # 1 = 성공


# --- 어댑터: 외부 모양 → 우리 모양 ---
class SmsAdapter(Notifier):
    def __init__(self, sdk: VendorSmsSDK, sender_id: str):
        self._sdk = sdk
        self._sender_id = sender_id

    def send(self, to: str, message: str) -> bool:
        res = self._sdk.dispatch(to, message, self._sender_id)
        return res["result_code"] == "0000"


class MailAdapter(Notifier):
    def __init__(self, mailer: LegacyErpMailer):
        self._mailer = mailer

    def send(self, to: str, message: str) -> bool:
        return self._mailer.send_mail(to, "[배송 안내]", message) == 1


# --- 사용하는 쪽은 Notifier만 안다 ---
def notify_shipped(notifiers: list, contact: str, order_no: str):
    for n in notifiers:
        n.send(contact, f"주문 {order_no} 상품이 출고되었습니다.")


notify_shipped(
    [SmsAdapter(VendorSmsSDK(), "0264400000"), MailAdapter(LegacyErpMailer())],
    "010-1234-5678",
    "ORD-2026-0818",
)
```

### 무엇이 좋아졌나

- SMS 업체를 교체해도 **`SmsAdapter` 파일 하나만** 고칩니다.
- 외부 시스템의 이상한 규약(`result_code == "0000"`, `return 1`)이 **어댑터 안에 격리**됩니다.

> 실무에서 레거시(ERP·PLM·물류사 API)와 신규 시스템을 붙일 때 압도적으로 많이 쓰는 패턴입니다.
> **"레거시를 감싸라, 레거시에 맞추지 말고."**

---

## 2.4 Decorator (데코레이터) — "기능을 겹겹이 덧씌운다"

### 어떤 문제를 푸나

외부 API 호출에 **재시도**와 **소요시간 로깅**을 붙이고 싶습니다.
그런데 그런 함수가 20개입니다. 20개 함수 안에 전부 `try/except + time.time()`을 복붙할 순 없습니다.

### 코드 (파이썬 데코레이터 문법 활용)

```python
import time
import functools


def retry(times: int = 3, delay: float = 0.1):
    """실패 시 재시도"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"  [retry] {func.__name__} {attempt}회 실패: {e}")
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def log_elapsed(func):
    """소요 시간 로깅"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = (time.perf_counter() - started) * 1000
            print(f"  [time] {func.__name__} {elapsed:.1f}ms")
    return wrapper


# --- 핵심 로직은 그대로, 부가 기능만 얹는다 ---
_call_count = 0


@log_elapsed
@retry(times=3)
def fetch_inventory(sku: str) -> int:
    """WMS에서 재고 조회 (가끔 실패한다고 가정)"""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ConnectionError("WMS 응답 없음")
    return 120


print(fetch_inventory("TOFU-300G"))
```

### 무엇이 좋아졌나

- `fetch_inventory`는 **"재고를 조회한다"는 본질에만** 집중합니다.
- 재시도/로깅은 재사용 가능한 부품이 되어 다른 19개 함수에도 한 줄로 붙습니다.
- **부가 관심사(로깅·인증·캐싱·트랜잭션)를 핵심 로직에서 분리**하는 것이 이 패턴의 목적입니다.

### 주의

데코레이터를 5개씩 쌓으면 **실행 순서를 아무도 모르게 됩니다.**
적용 순서는 **아래에서 위로** (`retry`가 먼저 감싸고, 그 결과를 `log_elapsed`가 감쌈)입니다.
2~3개를 넘기지 마세요.

---

## 2.5 Observer (옵저버) — "상태가 변하면 관심 있는 쪽에 알린다"

### 어떤 문제를 푸나

주문 상태가 '출고'로 바뀌면 → 고객 알림톡, 재고 차감, 정산 데이터 적재, 사내 대시보드 갱신이 필요합니다.
이걸 `ship()` 함수 안에 전부 넣으면, **알림 채널 하나 추가할 때마다 주문 도메인 코드를 건드려야 합니다.**

### 코드

```python
from abc import ABC, abstractmethod


class OrderEventListener(ABC):
    @abstractmethod
    def on_shipped(self, order_no: str) -> None:
        ...


class CustomerNotifier(OrderEventListener):
    def on_shipped(self, order_no: str) -> None:
        print(f"  → 고객 알림톡 발송: {order_no}")


class InventoryUpdater(OrderEventListener):
    def on_shipped(self, order_no: str) -> None:
        print(f"  → 재고 차감 반영: {order_no}")


class SettlementLogger(OrderEventListener):
    def on_shipped(self, order_no: str) -> None:
        print(f"  → 정산 원장 기록: {order_no}")


class Order:
    def __init__(self, order_no: str):
        self.order_no = order_no
        self.status = "PAID"
        self._listeners: list[OrderEventListener] = []

    def subscribe(self, listener: OrderEventListener) -> None:
        self._listeners.append(listener)

    def ship(self) -> None:
        self.status = "SHIPPED"
        print(f"주문 {self.order_no} 출고 처리")
        for listener in self._listeners:      # 관심 있는 쪽에 통보만 한다
            listener.on_shipped(self.order_no)


order = Order("ORD-2026-0818")
order.subscribe(CustomerNotifier())
order.subscribe(InventoryUpdater())
order.subscribe(SettlementLogger())
order.ship()
```

### 무엇이 좋아졌나

- `Order`는 **누가 듣고 있는지 모릅니다.** 그냥 "출고됐다"고 방송할 뿐입니다.
- 신규 후속 처리(예: 배송사 API 연동) 추가 시 **`Order` 코드를 열지 않습니다.**

### 주의 (중요)

- **디버깅이 어려워집니다.** "왜 이 함수가 호출됐지?"의 답이 코드에 안 보입니다.
- 리스너 중 하나가 예외를 던지면 뒤쪽 리스너가 실행되지 않습니다. → 실무에서는 각 호출을 `try/except`로 감싸거나 메시지 큐로 분리합니다.
- 구독 해제(`unsubscribe`)를 안 하면 **메모리 누수**가 납니다.

---

## 2.6 Template Method (템플릿 메서드) — "골격은 고정, 일부만 바꾼다"

### 어떤 문제를 푸나

일별 배치 작업들이 **"조회 → 변환 → 적재 → 로그"** 라는 뼈대는 똑같은데,
조회 대상과 변환 규칙만 다릅니다. 배치가 10개면 뼈대 코드가 10번 복붙됩니다.

### 코드

```python
from abc import ABC, abstractmethod


class DailyBatch(ABC):
    """모든 일일 배치의 공통 골격"""

    def run(self, target_date: str) -> None:      # ← 이 메서드가 '템플릿'
        print(f"[{self.name}] 배치 시작 ({target_date})")
        rows = self.extract(target_date)
        result = self.transform(rows)
        self.load(result)
        print(f"[{self.name}] 완료 — {len(result)}건\n")

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def extract(self, target_date: str) -> list: ...

    @abstractmethod
    def transform(self, rows: list) -> list: ...

    def load(self, result: list) -> None:
        """기본 구현 제공 — 필요하면 하위 클래스가 덮어씀"""
        print(f"  DW 적재: {len(result)}건")


class SalesBatch(DailyBatch):
    name = "일별매출집계"

    def extract(self, target_date):
        return [{"ch": "쿠팡", "amt": 1_200_000}, {"ch": "자사몰", "amt": 800_000}]

    def transform(self, rows):
        return [{"channel": r["ch"], "net": int(r["amt"] * 0.9)} for r in rows]


class InventoryBatch(DailyBatch):
    name = "재고스냅샷"

    def extract(self, target_date):
        return [{"sku": "TOFU-300G", "qty": 120}]

    def transform(self, rows):
        return [r for r in rows if r["qty"] > 0]

    def load(self, result):                        # 이 배치만 적재 방식이 다름
        print(f"  Snowflake 적재: {len(result)}건")


for batch in (SalesBatch(), InventoryBatch()):
    batch.run("2026-08-18")
```

### 무엇이 좋아졌나

- 실행 순서·로깅·에러 처리 같은 **공통 뼈대가 한 곳(`run`)에만** 존재합니다.
- 새 배치는 `extract`/`transform`만 쓰면 됩니다. 뼈대를 잘못 짤 여지가 없습니다.

### Strategy와의 차이 (자주 묻는 질문)

| | Template Method | Strategy |
|---|---|---|
| 방식 | **상속**으로 일부를 채움 | **조합(주입)**으로 통째로 교체 |
| 유연성 | 낮음 (컴파일 타임 고정) | 높음 (런타임 교체 가능) |
| 적합 | 절차가 확실히 고정된 경우 | 알고리즘 자체가 바뀌는 경우 |

---

## 2.7 Repository — "데이터 접근을 격리한다"

GoF 23개 패턴엔 없지만, **실무에서 가장 자주 쓰게 될 패턴**이라 넣습니다.

### 어떤 문제를 푸나

비즈니스 로직 함수 안에 SQL이 박혀 있으면:
- 테스트할 때마다 DB가 필요합니다
- Oracle에서 다른 저장소로 옮길 때 로직 전체를 뜯어야 합니다

### 코드

```python
from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def find_by_no(self, order_no: str) -> dict | None: ...

    @abstractmethod
    def save(self, order: dict) -> None: ...


class OracleOrderRepository(OrderRepository):
    def __init__(self, conn):
        self._conn = conn

    def find_by_no(self, order_no):
        # 실제 구현: SELECT * FROM ORDERS WHERE ORDER_NO = :1
        cur = self._conn.cursor()
        cur.execute("SELECT order_no, amount FROM orders WHERE order_no = :1", [order_no])
        row = cur.fetchone()
        return {"order_no": row[0], "amount": row[1]} if row else None

    def save(self, order):
        ...


class InMemoryOrderRepository(OrderRepository):
    """테스트용 — DB 없이 돌아간다"""

    def __init__(self):
        self._store = {}

    def find_by_no(self, order_no):
        return self._store.get(order_no)

    def save(self, order):
        self._store[order["order_no"]] = order


# --- 비즈니스 로직은 인터페이스에만 의존 ---
class OrderService:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def apply_discount(self, order_no: str, rate: float) -> int:
        order = self._repo.find_by_no(order_no)
        if order is None:
            raise LookupError(f"주문 없음: {order_no}")
        order["amount"] = int(order["amount"] * (1 - rate))
        self._repo.save(order)
        return order["amount"]


# 테스트 — DB 한 줄도 안 띄우고 로직 검증
repo = InMemoryOrderRepository()
repo.save({"order_no": "ORD-1", "amount": 50_000})
print(OrderService(repo).apply_discount("ORD-1", 0.1))   # 45000
```

### 무엇이 좋아졌나

- **테스트 속도가 수십 배 빨라집니다.** DB 없이 로직만 검증합니다.
- SQL이 한 곳에 모여 튜닝과 리뷰가 쉬워집니다.

> 이것이 **의존성 주입(DI)** 과 **의존성 역전 원칙(DIP)** 의 실물입니다.
> "구체적인 것(Oracle)이 아니라 추상적인 것(Repository 인터페이스)에 의존하라."

---

# 3부. 실무 적용 가이드

## 3.1 파이썬에서는 이렇게 하는 게 더 낫다

자바 책에 나오는 패턴을 그대로 옮기면 파이썬에서는 과하게 무거워집니다.

| 자바식 | 파이썬식 |
|---|---|
| Singleton 클래스 (`__new__` 오버라이드) | **모듈**을 쓰세요. 파이썬 모듈은 한 번만 로드되는 싱글턴입니다. `config.py`에 값을 두고 `import config` |
| Strategy 인터페이스 + 구현 클래스 | 상태가 없다면 **그냥 함수**를 넘기세요 (함수가 일급 객체) |
| Abstract Factory | `dict` 레지스트리 + `functools.partial` |
| Builder | `dataclass` + 기본값 + 키워드 인자 |
| `ABC` 상속 강제 | `typing.Protocol` (덕 타이핑 + 타입 체크) |

`Protocol` 예시 — 상속 없이 인터페이스를 정의합니다.

```python
from typing import Protocol


class Notifier(Protocol):
    def send(self, to: str, message: str) -> bool: ...


class SlackNotifier:          # Notifier를 상속하지 않았지만
    def send(self, to, message):   # 모양이 같으므로 타입 체커가 통과시킴
        print(f"[slack] {to}: {message}")
        return True


def notify(notifier: Notifier, to: str, msg: str):
    notifier.send(to, msg)


notify(SlackNotifier(), "#ax-alert", "배치 완료")
```

## 3.2 가장 흔한 안티패턴: 패턴 과용

> 주니어가 패턴을 배운 직후 가장 위험합니다. **모든 곳에 패턴을 넣고 싶어집니다.**

```python
# ❌ 이런 코드를 만들지 마세요
class AbstractGreetingStrategyFactoryProvider:
    ...
```

**판단 기준 세 가지**

1. **지금 실제로 변하고 있는가?** "나중에 바뀔 수도 있으니까"는 근거가 아닙니다. 실제로 3번째 변경이 왔을 때 도입하세요.
2. **패턴 적용 후 코드가 더 짧고 읽기 쉬운가?** 파일이 1개에서 5개로 늘고 이해가 어려워졌다면 잘못 쓴 겁니다.
3. **동료가 5분 안에 이해하는가?** 설명이 필요한 구조는 아직 이른 구조입니다.

> **YAGNI (You Aren't Gonna Need It)** — 필요해질 때 넣으세요.
> 잘못된 추상화는 중복보다 비쌉니다. 중복은 지우면 되지만, 잘못된 추상화는 전부 뜯어야 합니다.

## 3.3 주니어를 위한 30일 실천 계획

| 주차 | 할 일 |
|---|---|
| **1주차** | 내가 최근 짠 함수 중 **가장 긴 것 하나**를 골라 함수 추출만 해본다. 테스트 먼저 붙이고. |
| **2주차** | 매직 넘버·중첩 if를 찾아 상수/가드 절로 정리. `refactor:` 커밋을 3개 이상 만든다. |
| **3주차** | 팀 코드에서 `if channel == ...` 같은 반복 분기를 찾아 딕셔너리 디스패치로 바꿔본다. |
| **4주차** | 외부 시스템 호출부 하나를 **Adapter로 감싸고**, 테스트용 가짜 구현체를 만들어 테스트를 짜본다. |

## 3.4 한 장 요약

**리팩토링**

- 동작 불변, 구조 개선. 기능 추가와 절대 섞지 않는다
- 테스트가 먼저. 작게 바꾸고 자주 돌린다
- 냄새 6종: 긴 함수 / 매직 넘버 / 중첩 조건문 / 긴 파라미터 / 반복 분기 / 기능 편애

**디자인 패턴**

| 패턴 | 한 줄 요약 | 이럴 때 |
|---|---|---|
| Strategy | 알고리즘을 갈아 끼운다 | 정책이 여러 개고 자주 바뀔 때 |
| Factory | 생성 규칙을 한곳에 모은다 | 조건에 따라 다른 객체를 만들 때 |
| Adapter | 안 맞는 인터페이스를 끼워 맞춘다 | 레거시·외부 API 연동 |
| Decorator | 기능을 덧씌운다 | 로깅·재시도·캐싱 등 부가 관심사 |
| Observer | 변화를 구독자에게 알린다 | 하나의 사건에 후속 처리 여럿 |
| Template Method | 골격은 고정, 일부만 바꾼다 | 절차가 같은 배치·파이프라인 |
| Repository | 데이터 접근을 격리한다 | 로직을 DB 없이 테스트하고 싶을 때 |

**마지막 한 문장**

> 좋은 설계는 처음부터 완벽하게 나오지 않습니다.
> **동작하게 만들고 → 올바르게 만들고 → 빠르게 만든다.** 그 사이를 잇는 게 리팩토링입니다.

---

## 더 읽어볼 것

- 마틴 파울러, 『리팩터링 2판』 — 냄새와 기법의 사전. 필요할 때 찾아보는 용도
- 로버트 마틴, 『클린 코드』 — 이름 짓기와 함수 챕터만 읽어도 값어치
- refactoring.guru — 패턴별 다이어그램과 다국어 예제 (한국어 지원)
