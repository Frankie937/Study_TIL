### SPCS ? 
Snowpark Container Service 
Snowflake에서 컨테이너 이미지를 등록하고 배포하도록 돕는 런타임 환경 


### SPCS 기능 요소 
* Image Management
  - snowflake image repository + registry 컨테이너 이미지를 저장하고 관리하는 snowflake의 저장소 및 레지스트리
  - Multiple Image tags : 컨테이너 이미지에 여러 태그를 지정하여 관리 
* Service Management
  - Multi-Container Servicess: 다중 컨테이너 서비스
  - 민감한 정보를 안전하게 관리하기 위한 snowflake 보안 기능
  - 인라인 또는 템플릿 형태의 YAML을 사용하여 서비스 설정을 정의하고 관리
  - Service Replica Scale-out: 성능과 가용성을 향상 
* Compute
  - 10가지 컴퓨팅 풀옵션 (aws/azure)
  - GPU_VN_L을 포함한 온디맨드 GPU 할당
  - 컴퓨팅 풀 노드 스케일 아웃 
* Orchestration
  - 저장 프로시저 기반의 작업 실행
* Networking
  - Optional Public Egress :  선택적으로 퍼블릭 발신 설정
  - Optional Public Ingress : 외부 네트워크로 부터 선택적으로 퍼블릭 수신 엔드포인트 설정
  - VPC내 서비스 간 통신 
* Security
  - 역할 기반 접근 제어(RBAC)를 통해 풀, 이미지, 서비스 접근 제어
  - OAuth 인증을 사용하여 엔드포인트 접근을 제어
  - 역할 기반으로 서비스 간 통신 제어
  - 데이터 접근을 위한 범위 지정 서비스 인증 토큰 사용
* Storage
  - Transient Root Volume, Block Storage
  - Persistnet Stage or Block-storage Volume Mounts
  - 원격 스토리지의 Hybrid, FDN, Iceberg 테이블, stage 등 지원 
* Observability
  - 서비스의 지표 및 로그에 접근하여 모니터링 및 분석 
  
