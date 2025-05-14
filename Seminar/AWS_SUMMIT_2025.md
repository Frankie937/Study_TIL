## < 2025 AWS SUMMIT 5/14~5/15 > 

---
## DAY 1 

< 기조연설>  

### aws 책임자 

* 생성형 ai 도입이 가속화 
카카오페이 손해보험 - ai기반 손해사정및 보험금 바로 지급 
우아한형제들 amazon nova 메타 자동분류 
스타벅스 - 전국 매장 the silot 3개월만에 구축 
tmap 모빌리티 - 전체 시스템 aws로 마이그레이션 

aws market place 한국에 열림 
aws 공공기관에 클라우드 서비스 도입 가능 - 인터넷진흥원 
amazon q-developer 한국어 뿐만 아니라 다국어지원 가능 

### ioT VP 야세르 
어플리케이션 
인메모리 
gpu 구동 - 엔비디아와 긴밀한 파트너십 
혁신을 일직선으로 나아가지 않는다
생성형ai 는 계속 바뀌고 있다 

많응 메타데이터 ice berg 이용 
스케일이 커지면 management가 어려워짐 
새로운 버킷 타입생성 

lake house data 
sage maker 
applicatino개발 수월해짐 


### 현대카드 evp 
기술에 대한 투자 필수 
카드사의 데이터는 daily life data  전 영역을 알 수 있는 영역 
어떻게 체계화 할 것인가? 
d-tag 구조로  
데이터구조를 만들어서 

다른 회사에서는 vertical 

universe platform 
온프렘에서 보통 만들었으나 
이 플랫폼부터 amazon기능들을 사용하기 시작 - 일본에게 수출 함 
--> 금융업계 ai 소프트웨어 수출 최초

리소스에 대한 의존성을 aws 덕분에 자유롭게 배포 가능 
지금 가장 화두가 되고 있는 것 Agentic AI 
super agent - sub agent 
commodity 화 -> 누구나 갖다쓸 수 있게 됨 
이러한 영역들 있는 것 쓰면 됨 

각 회사가 갖고 있는 data와 인사이트는 
각 회사 고유의 영역이고 그것으로 부터 경쟁력이 있게 됨! 
agent가 그 데이터를 잘 갖다 쓸 수 있도록 잘 정제하는 게 중요


### 
생성형 ai 끊임없이 계속 출시 및 새로 생성 
aws bedrock 
amazon nova 모델 
검색기반 생성 RAG 
생성형 ai 구축하면서 rag - 비정형데이터 최적화 
high tech 기술 건설/엔지니어링 등 첨단회사



--- 

### 통신 산업의 미래, Agentic AI가 바꾼다!
고객등의 프라이버시 온
불분명한 데이터 많음 
보이스 피싱 스팸 
고객의 pain point 
우리의 기대대
마케팅 전략을 수립 > 운영계획 
시장조사와 사용자조사사례 
젠지 세대 

---

### Amazon Bedrock 기반Text-to-SQL로 완성하는 데이터 혁신: 당근페이의 핀테크 성공전략

2023년 amazon bedrock 출시 - 기업형 생성형 ai 활용 가능하도록 
amazon nova - llm 활용할 수 있도록 - 빠르게 생성형 ai 도입
ai 산업 예산:  450억 달러 > 2000억 달러 

(당근페이)  
Text-to-SQL 도입 
반복되는 요청 잦음 
자연어로 질문 > sql 변환 
text-to-sql 변화 

![image](https://github.com/user-attachments/assets/1bd75eda-9e8d-464a-aca1-2dab57b8b7d9)

![image](https://github.com/user-attachments/assets/f719a7c0-c7ef-4398-b3c4-04b2bad9ca13)

파인튜닝 : 사전훈련된 모델을 커스텀하게 조정하여 커스텀 모델로 진화 

amazon bedrock을 통해 쉽게 가져오고 쉽게 인퍼런스 가능 

text-to-sql 도입 긍정적 변화  
prompt 엔지니어링 
리더보드 상위모델이라 한들, 100퍼센트 정확도는 어려움 
(데이터의 변경사항이 제대로 잘 적용되지 않으면 성능이나 정확도 당연히 떨어짐) 

생성형 ai를 접목해서 text-to-sql을 구축한 과정 

(김탄님) 
당근페이 - Broquery 
-> ai기반 분석봇(브로처럼 친근하게 다가가 데이터관련 질문(쿼리)을 해결해주는 챗봇)
사용자는 슬랙에서 브로커리를 멘션하여 자연어로 질문합니다. 
브로쿼리는 1분 내 요약된 답변과 sql을 줌 
필요한 경우 시각화도 구현해줌 

비개발 직군의 데이터 접근이 굉장히 어려웠음 
귀중한 개발 리소스의 소모도 반복적으로 이루어짐 
이러한 문제들의 핵심 해결방안으로 text-to-sql로 대안을 얻음 
조직 전체의 데이터 활용 역량도 높일 수 있다고 생각 
핵심 요구사항 정의하게 됨 
* 5가지 요구사항
  1.접근성
  2.사용자 의도 파악(질문의도 판단- 단순 키워드 인식만이 아니라, 질문의 맥락과 의미르 이해)
  3. 대화 문맥 인식
  4. 스스로 sql을 점검하는 메커니즘
  5. 정확성(사용편의성도 중요하나 답변의 신뢰도는 타협할 수 없는 부분)

amazon bedock과 조화하여 

인터페이스 슬랙 다이나모db rag 시스템 메타데이터 플랫폼 
![image](https://github.com/user-attachments/assets/9edb247c-262f-4dad-a42d-1322450b8985)
주요 아키텍처 
![image](https://github.com/user-attachments/assets/1b328f14-4978-4d35-ac53-01c50636748e)
* 슬랙 - 접근성 높임
* 에이전트 - 모든 과정을 진두지휘하는 핵심 (사용자의 의도 파악 > sql 생성) 
* 다양한 context 필요
* mcp 서버 : 비즈니스 컨텍스트, 허브의 역할
* 지능형 에이전트로 나아가도록 역할
* 랭체인 & 랭그래프로 구현 - 오케스트레이션 효과적으로 구현
* 복잡한 상호작용을

  ![image](https://github.com/user-attachments/assets/94f2f7a8-06aa-49d5-ae3f-2b288f9c4599)
  * 자연어로 질의 > 필요하면 다이나모db에서 지난 대화를 갖고옴 > 질문 의도 파악 > 의도에 따라 워크플로우 다름 >  
  * 정확한 sql 생성을 위해서 정제하는 과정을 거치는데, 이때 2가지 핵심 기술: 필요한 메타데이터 후보군을 놓치지 않기 위해 오픈서치를 활용한 하이브리드 검색을 (하이브리드 방식은 기존 text 검색기술과 의미기반의 임베딩 벡터db 기술 결합) 

* 리랭커 사용 - 사용자의 원본질문과 각 후보간의 유사도를 다시 판단
  (핵심 필터 역할 - rag시스템의 성능을 한 단계 더 끌어올릴 수 있음)

  * 하이브리드로 넓게 찾고 리랭커로 정교하게 필터 비즈니스적으로
  * 랭그래프는 그래프구조로 효과적으로 관리

  * 다양한 메타데이터 수집 프로세스
      - 분석데이터
      - 설명정보 (메타데이터) - 서비스의 성능과 질을 좌우함
          - 비즈니스 메타데이터 - 비즈니스 용어/맥락 정보로 활용 -설명정보(비즈니스 +보안, 개인 정보_
          - 기술 메타데이터 - 컬럼, 자주 사용하는 sql , 개발자들이 사용하는 문서 등 정보 (컬럼 설명 메타데이터 )
          - 운영 메타데이터 -
  

* 메타데이터의 최신성 관리 굉장히 중요 
![image](https://github.com/user-attachments/assets/eac8dc83-4119-475d-b7e0-5bbb5a4d76a1)

* 좋은 예시를 보여주는 것 중요
-> llm에게  자연어질문 - 고품질 sql의 pair 데이터를 예시로 보여주는 것 중요
-> 이러한 데이터를 회사에서 자산화하는 게 나중에 굉장히 중요해 보임

  ![image](https://github.com/user-attachments/assets/cd27f278-b284-426e-95e9-6d5da5641ce6)

* 또한 용어사전 고도화에 많은 노력을 기울임(단어의 뜻뿐만 아니라 비즈니스의 맥락도 녹아들 수 있도록)
  -> 좋은 예시 데이터가 부족하더라도 좋은 성능을 나타내는 데 굉장히 중요

* 주요 개선영역 4가지
  - 리트리버에서 검색 정확성과 효율성을 높이는데 (하이브리드 서치,키워드 부스팅, ann 등)
  - 파인튜닝 
  - 비즈니스 맥락 정보를 워크플로우 내에서 더욱 정교하게 반영 및 검증
  - 객관적으로 평가체계 고도화 
![image](https://github.com/user-attachments/assets/13676148-e7f0-4ccf-9d71-aeae7f0ead1e)

* 5가지 측면에서 의미있는 변화들 경험
![image](https://github.com/user-attachments/assets/50c33962-f2b6-408f-97a0-68491347673c)

* AWS기반의 text-to-sql 구축과정의 장점
    - 최신 모델을 인프라 구축이나 신경 쓸 필요없이 사용 가능
    - 
![image](https://github.com/user-attachments/assets/1a56f8df-76d5-4c88-ab67-1d998da01995)

* 브로쿼리의 앞으로 계획 - 고도화 및 확장 계획 
![image](https://github.com/user-attachments/assets/41e70279-4e10-43d0-8b06-865e052f560c)

* 더 자세한 내용 - 당근페이 블로그 참고!! 

---

### Multi-Agent AI로 고객 경험 혁신 및 생산성 향상: 하나투어의 생성형 AI 챗봇

(전주형 솔루션즈 아키텍트) 
멀티에이전트 AI로 고객혁신 사례
생성형 AI 기반 서비스 고민 
* 생성형 AI 사례 
  - 24시간 상담사 챗봇 
  - 번역 챗봇
  - 개인 맞춤형 상품 개발 
  - 연구 및 개발 

* 싱글 에이전트 
![image](https://github.com/user-attachments/assets/00ea15d3-aa7a-41bc-a038-c30fdcd71cf7)
복잡한 구조로 계속 추가하고 가다보면 느려지고 한계가 생김
![image](https://github.com/user-attachments/assets/8ae56bbc-1083-4949-b8d1-30aa18b38019)
병목현상 발생, 싱글 에이전트가 전체 시스템을 가담하니 그 에이전트가 무너지면 다 무너짐 (신뢰도 하락) 
-> 일의규모를 줄이고 여러 에이전트를 두자! - 분리형 에이전트 
-> BUT, 한계: 인터페이스가 많아지면서 접근성 어려워짐 , 데이터의 일관성도 어려워짐 
-> 멀티에이전트 콜라보레이션 구조로 LLM 서비스를 생성
-> SUPERVISOR 에이전트 + 여러 전문 에이전트 

![image](https://github.com/user-attachments/assets/012cab08-67d8-4501-ab03-efc9778ba78d)


(김택권 하나투어 CTO) 
* 하이(H-AI) 서비스- 멀티에이전트 서비스
![image](https://github.com/user-attachments/assets/d1ede62a-1a28-4b78-acaf-dc5fe8179de8)
amazon bedrock 사용하여 상담챗봇 생성 - 내부시스템과 연계관련 장점

* 여행정보 특화 추천 특화 에이전트
![image](https://github.com/user-attachments/assets/32520b8b-cad0-4572-9abf-ac956c3bd5ae)
여행정보와 FAQ - 벡터 db 

* 상담챗봇 에이전트 
![image](https://github.com/user-attachments/assets/0fc3e69c-55c4-4db7-b60b-714ab00adb1e)
청킹기준 세우는 것 굉장히 중요

* 예약기반 
![image](https://github.com/user-attachments/assets/af861532-bff1-4037-a5ed-c5c3719500c1)

예약내역데이터 - 민감정보는 제외 - 여행 여정 정보만 

* 한계점 
![image](https://github.com/user-attachments/assets/d071b94b-20bb-4997-bb17-f8bf08ce8a96)
--> 멀티에이전트로 전환 

![image](https://github.com/user-attachments/assets/3ec1bf3e-731f-4449-a692-aac7c95f6c7b)
세션 히스토리 역할 강화 


(성진수- 플랫폼 기획 총괄) 
* 성과 및 서비스 측면에서 이야기하고자 함

---
### AI 기반 대용량 문서 분석 업무 효율화 : LLM 기반 삼성 입찰 안내서 분석 서비스

비정형 데이터가 굉장히 많음 
계약서 - 건설 프로젝트에 있어 핵심문서 

* 3단계 : 설계 - 조달 - 시공 
계약서 안에 이 단계의 내용들이 들어가 있음 
입찰서 > 입찰제안서 > 계약서 
계약서가 업무의 커뮤니케이션 모든 게 담겨있음 
비정형 문서 중 계약서를 가장 먼저 구조화 하고 싶었음 
그러나, 구조화하는게 굉장히 어려움

* 대표적 어려움
  1. 방대한 문서의 양 (입찰서 하나에 적게는 3000페이지~1만페이지) - 사람의 물리적 한계 - 입찰시간은 3-4개월 내... 수천~수조원의 입찰제안서를 만들어내야 하는 데 사실상 불가능... 굉장히 전문용어도 많아서 해석하는 것도 굉장히 어려움 
  2. 언어의 장벽 - 업무가 계속 밀리는 이유 중 하나 
![image](https://github.com/user-attachments/assets/65fc4f2a-fbbd-4479-b2df-2e111b874659)

계약문서 구조화 고도화 작업 
- 위험문구 찾아내는 룰베이스 기반 -한계 (맥락을 이해 못함)
- 생성형ai 등장 > 생성형 ai 활용하여 방대한 양의 문서를 처리할 수 있는 지 기술 검토 시작 > agentic rag 대화형 서비스를 만들게 됨
- 이 항목은 보상을 받을 수 있나요? 정확한 근거자료와 답변을 생성
- 실시간으로 계약서를 이해하는 시대가 오게 됨 

![image](https://github.com/user-attachments/assets/9bafa498-76c1-4d14-845b-4593c20be00e)


* 건설계약문서의 4가지 pain point
  ![image](https://github.com/user-attachments/assets/bb6d8caf-73f5-4a28-a9a1-5608db1eac12)

  - 방대한 문서의 양
  - 다국어
  - 계약 전문 용어 - ai가 일반인들도 이해할 수 있도록 쉽게 풀어서 설명해줌 
  - 번역 - ai가 2-3일만에 번역
  --> 더 빠르고 쉽게 계약서를 이해하고 대응하게 됨

* 3가지 전략
  - 방대한 문서 빠르게 처리
  - 복잡한 문서를 ai가 이해할 수 있도록 구조화
  - 다양한 문서를 정밀하게 디지털화하자
  --> 멀티 에이전트 기술을 도입
* 
![image](https://github.com/user-attachments/assets/f7539681-728e-4f57-ace5-7c2ec53118c6)
사용자 질문에 대해 ai가 의도를 파악하는 게 중요 
복잡한 문서를 ai가 읽고 사용자 질문에 딱 맞는 정보를 정확히 제공하는 것이 중요했음
사용자 친화적인 환경을 구축하는게 중요했음 (답변을 사용자가 볼 때 근거를 바로바로 볼 수 있게끔 구현) 
![image](https://github.com/user-attachments/assets/ea90f103-a2b8-4ac3-961a-27f7bbbbd8d7)

작업의 시간이 70% 단축되었음 
계약서 분석 시간 40명이 10일 동안 -> 에이전트 1개가 3일동안 가능 
연간 50억원 절감 효과 
인력에게 더 고도화된 작업을 하는 데 리소스를 투입 
건설 지식 자산화가 가능하게 됨 
건설이 DT에 다가갈 수 있음을 확인 
건설산업 전반에 디지털 혁신이 가능해졌고, 이제 시작이라 생각 

(aws 김성헌 - 딜리버리 프로페셔널 기술 컨설턴트) 
* EPC 건설 계약 
![image](https://github.com/user-attachments/assets/e9ff562e-439a-4ebf-aa74-a93db868d0d8)

* 문제를 4가지 범주화
![image](https://github.com/user-attachments/assets/c2df3bfa-774d-4cec-a69f-47f9c89a8829)

1. ITB 문서 자체가 큰 고정 과제였음 -문서 양이 많고, 굉장히시간은 적음 -1년에 제안 요청서는 20건 정도 
2. 복잡한 구조
3. 사용자관점에 프로젝트 정의 - 검색의 기술
4. ㅇ

* 질문의 의도에 따라 계약/법적조건/기술적조건 맞는 답변이 나와야 함
* 문서가 구주화 되어야 함
* 다국어 지원이 가능해야 함
* 전문용어 - 도메인에 맞게 의미들을 잘 처리해야 함 (it분야의 파이프라인과 건설분야의 파이프라인은 다름)
* aws 람다 사용 - 각각 병렬처리 가능하도록 (대량의 문서를 병렬로 처리해도 워크플로우를 안전하게 운영 가능)

* 가용성 확보 필요 -멀티 리전 전략 활용
* 인덱싱 프로세스에서 안정적 처리가 가능하도록

* amazon bedrock
* 서버리스 아키텍처 구성- 비용효율적인 구조로
* 람다 - 관리 오버헤드가 거의 없음 , 비용적 측면에서도 사용할 때만 사용 가능하기에 적합한
* 워드, ppt, 엑셀 다양한 포맷 정의
  
* 검색과 리랭커 단계
검색 결과를 정밀하게 평가하는 단계
하이브리드 검색 활용
리랭커 - 검색의 품질평가 - 문서 랭킹 재설정

* 다국어 처리 방안
모든 문서를 영어로 통일하여 처리
(영어데이터에 최적화 되어있기 때문)
동의어 복합어 처리

* 보안
고객의 보안을 최우선시 함
역할기반에 접근권한으로 제어
권한과 역할 세분화
네트워크 중앙화
보안 강화
대화이력 -dinamo db에 저장

* 랭기지 어시스턴트 'LUGA'
  ![image](https://github.com/user-attachments/assets/2f988224-4647-4c5d-81a5-c0e8d0eab312)

