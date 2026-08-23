
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
