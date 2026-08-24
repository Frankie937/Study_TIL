
# Docker & Kubernetes 기반 AI 서비스 배포 완벽 가이드

## 1. 전체 CI/CD & 배포 아키텍처 흐름




[개발자 PC / 개발용 컨테이너]
│
│ (1) git push
▼
[Git 저장소 (GitHub / GitLab)]
│
│ (2) Webhook 알림 & Source Clone
▼
[독립된 CI 서버 (Jenkins)]
│
├─► (3) docker build (Dockerfile 읽기)
├─► (4) docker push (중앙 Registry로 업로드)
└─► (5) kubectl apply (Kubernetes로 배포 명령 전송)
│
▼
[Kubernetes 클러스터]
(새 도커 이미지 다운로드 후 무중단 배포)



---

## 2. 프로젝트 파일 구조 (Git Repository Root)

```text
my-ai-app/
├── main.py              # FastAPI 웹 서버 메인 코드
├── requirements.txt     # 파이썬 의존성 패키지 목록
├── Dockerfile           # 도커 이미지 빌드 명세서
├── deployment.yaml      # 쿠버네티스 배포 설정 파일
└── utils/
    └── agent.py         # AI Agent 로직 모듈

```

---

## 3. 핵심 실무 예시 코드

### ① `requirements.txt` (생성 명령어: `pip freeze > requirements.txt`)

```text
fastapi==0.109.0
uvicorn==0.27.0
langchain==0.1.0
openai==1.10.0

```

### ② `main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(prompt: str):
    return {"result": f"AI 응답: {prompt}"}

# 쿠버네티스 Liveness Probe용 경로
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# 쿠버네티스 Readiness Probe용 경로 (모델 로딩 확인용)
@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

```

### ③ `Dockerfile`

```dockerfile
# 1. Base 파이썬 이미지 선택
FROM python:3.10-slim

# 2. 컨테이너 내 가상 작업 디렉토리 설정 (절대경로)
WORKDIR /app

# 3. 의존성 파일 복사 및 설치 (--no-cache-dir로 용량 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Git 루트의 모든 소스코드(.)를 컨테이너 내부 /app(.)으로 복사
COPY . .

# 5. 컨테이너 런타임 시 실행할 메인 서버 구동 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

### ④ `deployment.yaml` (Kubernetes Manifest)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-api
spec:
  replicas: 2  # 고가용성을 위한 Pod 2개 유지
  selector:
    matchLabels:
      app: ai-agent-api
  template:
    metadata:
      labels:
        app: ai-agent-api
    spec:
      containers:
      - name: ai-agent-container
        image: [mycompany-registry.com/ai-agent:v1.2.0](https://mycompany-registry.com/ai-agent:v1.2.0)
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 20
          periodSeconds: 5

```

---

## 4. 핵심 요약

* **`python:3.10-slim` 사용 이유:** 내 서버 버전과 상관없이 프로젝트 동작 검증을 마친 표준 파이썬 환경을 격리하여 사용하기 위함입니다.
* **`WORKDIR /app` & `COPY . .` 의미:** 내 PC/서버의 소스코드를 도커 컨테이너라는 독립된 가상 상자 내부(`/app`)로 복사하여 넣어주는 과정입니다.
* **`--no-cache-dir -r` 의미:** `-r`은 파일 목록 기반 전체 설치이며, `--no-cache-dir`은 임시 다운로드 캐시를 삭제해 도커 이미지 용량을 최소화합니다.
* **`CMD` 명령어의 역할:** 도커 이미지가 컨테이너로 구동되는 시점에 자동으로 파이썬 웹 서버를 실행시킵니다.
* **1 컨테이너 = 1 서비스:** 컨테이너 내부에 Conda 가상환경을 중첩시키는 방식은 비정석적인 방식이며, 1개 컨테이너에 1개 프로젝트를 띄우는 것이 배포 표준입니다.
* **Jenkins와 Kubernetes의 관계:** Jenkins 서버에 쿠버네티스를 설치하는 것이 아니며, Jenkins는 빌드 후 원격 클러스터(Kubernetes)에 `kubectl` 또는 ArgoCD를 통해 **배포 명령만 전달**합니다.

---

**쿠버네티스의 무중단 배포, 컨테이너 자동 재시작(Self-Healing), 다중 컨테이너 구동(Replicas)의 이유**를 체계적으로 정리한 Markdown 문서

# Kubernetes 운영 및 배포 핵심 개념 정리

## 1. 무중단 배포 (Zero-Downtime Deployment)

### 개념
새로운 코드나 버그 수정본을 배포할 때, 서비스 중단 시간(Downtime)을 0초로 만드는 기법입니다. 쿠버네티스는 **롤링 업데이트(Rolling Update)** 방식으로 기존 컨테이너를 하나씩 순차적으로 교체합니다.

### AI 서비스 실무 예시
* **상황:** 사용자 10,000명이 AI 추천 API를 실시간 호출 중인 상황에서 알고리즘 v1.0을 v2.0으로 업데이트.
* **구형 배포 방식의 문제:** 
  기존 서버를 모두 끄고 새 서버를 올리는 동안 `502 Bad Gateway` 에러가 발생합니다. 특히 AI 서비스는 초기 가중치(Weights) 로딩에 수초~수분의 시간이 걸려 중단 시간이 길어집니다.
* **쿠버네티스 롤링 업데이트 흐름:**
  1. 기존 v1.0 컨테이너(A, B, C) 구동 중.
  2. v2.0 컨테이너 D를 새로 1대 생성.
  3. **`readinessProbe`**가 D의 초기화(AI 모델 로딩)가 완전히 끝났는지 확인.
  4. 준비 완료(`200 OK`) 확인 후, 트래픽 일부를 D로 보내고 기존 A 컨테이너를 안전하게 제거.
  5. 이를 순차 반복(E, F)하여 사용자는 **단 0.1초의 서비스 끊김 없이 v2.0으로 전환**.

---

## 2. 컨테이너 자동 재시작 (Self-Healing & Liveness Probe)

### 개념
코드 에러나 메모리 누수(Memory Leak) 등으로 앱이 응답 불능(Hang) 상태에 빠졌을 때, 사람이 직접 개입하지 않아도 **쿠버네티스가 감지하여 컨테이너를 강제 종료 및 재시작**시키는 자가 치유 기능입니다.

### AI Agent 서비스 실무 예시
* **상황:** AI Agent가 복잡한 데이터를 처리하다 파이썬 메모리 누수로 `Deadlock`(무한 대기) 상태에 빠짐.
* **자가 치유 흐름:**
  1. 쿠버네티스가 주기적으로(예: 10초마다) `/healthz` 경로로 **`livenessProbe`** 체크 요청 전송.
  2. 프로세스 먹통으로 연속 3회 이상 응답 실패.
  3. 쿠버네티스가 해당 컨테이너를 즉시 **강제 종료(Kill)하고 새 컨테이너로 자동 재시작**.
  4. 새벽 시간대 장애 발생 시에도 엔지니어 개입 없이 몇 초 만에 정상 상태 복구.

---

## 3. Readiness Probe vs Liveness Probe 비교

| 구분 | **readinessProbe (준비 상태 체크)** | **livenessProbe (생존 상태 체크)** |
| :--- | :--- | :--- |
| **목적** | "지금 트래픽을 넘겨주어도 되는가?" | "컨테이너가 살아서 숨 쉬고 있는가?" |
| **실패 시 동작** | 해당 컨테이너로 가는 **트래픽 전달을 차단** (대기) | 해당 컨테이너를 **강제 종료 후 즉시 재시작** |
| **주요 활용** | **무중단 배포** (초기 모델/데이터 로딩 시간 확보) | **장애 자동 복구** (무한 루프, 메모리 누수 감지) |

---

## 4. 동일한 컨테이너를 여러 개(Multi-Replicas) 띄우는 이유

대형 서비스 및 생산 환경에서는 동일한 도커 이미지로 구동되는 컨테이너를 최소 2~3개 이상 띄워 운영합니다.

```text
               [사용자 요청 (초당 300건)]
                           │
                           ▼
            [쿠버네티스 서비스 (Load Balancer)]
            ┌──────────────┼──────────────┐
            │ (100건)      │ (100건)      │ (100건)
            ▼              ▼              ▼
       [컨테이너 A]   [컨테이너 B]   [컨테이너 C]
       (동일한 코드)  (동일한 코드)  (동일한 코드)
```


### ① 부하 분산 (Load Balancing)

* 단일 컨테이너가 대량의 사용자 요청을 직접 다 처리하면 병목이 발생해 응답 속도가 현저히 떨어집니다.
* 앞단의 로드밸런서(Service)가 트래픽을 컨테이너 A, B, C로 **1/N 분산 전달**하여 안정적인 성능을 유지합니다.

### ② 고가용성 (High Availability) 및 장애 대응

* 특정 물리 서버 장비 고장으로 컨테이너 A가 꺼지더라도, 로드밸런서가 트래픽을 남은 B, C로 즉시 우회시킵니다.
* 사용자는 장애 발생 여부를 인지하지 못한 채 서비스를 계속 이용할 수 있으며, 쿠버네티스는 죽은 A를 대신할 새 컨테이너 A'를 자동으로 즉시 생성합니다.

### ③ 트래픽 기반 자동 확장 (Auto-scaling / HPA)

* 평소 3개로 구동하다가 트래픽이 폭주하여 CPU/GPU 사용량이 기준치(예: 80%)를 넘어서면, 쿠버네티스가 동일한 컨테이너를 자동으로 10개, 20개로 확장(Horizontal Pod Autoscaler)하여 대응합니다.




