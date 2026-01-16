# < 인스트럭트한국 밋업 20250125  >

nonce- 창업에 관심있는 개발자들 커뮤니티 

디스코드 채널 - 

유튜브 채널 @instructkr

community-project 

## < 발표자 소개 >

## 고석현 (Sionic AI): Java 외에 다른 언어를 쓰면 호흡이 곤란해지는 병에 걸렸는데 AI 회사 같은 걸 추구하면 안 되는 걸까

Java & Kotlin 언어로 자연어 처리에서 진행하는 이야기를 들려 줍니다. 특히 production level 에서 파이썬 기반 딥러닝 코드를 JVM 언어로 포팅하여 서빙하는 경험에 대해 이야기 합니다.

- ai를 영리로 추구하다보면 비즈니스 로직, 코드, 버그와 계속 충돌
    - 콜백 지옥, 마이크로서비스 지옥 k8s… 등
    - 해결: 동시성 모델, 도메인 모델, 의존성 생명주기 관리
    - python 모든 게 가능하나 자유도가 굉장히 높은 언어
    - ONNX 상호변환 가능하나 3년전 커밋이 마지막
    - java-tensorflow
    - web gpu
    - 의존성 문제로 하게 됨
    - 기존의 통념과 달리 ‘적당한’시스템 단순확가 필요

## 김지수 (kuotient, 올거나이즈): Qwen2.5 한국어 모델 개발기

"Qwen2.5 한국어 모델 개발기"를 통해 혁신적인 언어 모델 개발 과정을 공유합니다. 특히 m-ArenaHard에서 37.60이라는 인상적인 성능 향상을 이끈 과정이 주목됩니다. SFT, Merging, Alignment 등 전반적인 학습 파이프라인을 다루며, 레이어 교체와 On-policy 전략 도입 등 국내 최초로 시도된 기술적 혁신도 함께 소개됩니다. 8B 이하 모델 중 최고 성능을 기록한 비결을 상세히 들려줄 예정입니다.

1. 왜 만들었나요?
    1. 고객사 요청 task - 보고서작성, 요약, rag 등 - 
    2. human preference 가 높은 모델 cohere communitydㅔ서 m-ArenaHard(ko)를 중심으로 평가 진행 
2. 목표
3. 파이프라인 구조- 6stage 
    1. Model- base model selection 
        1. Qwen 3B base 모델에서 시작 - poc하기 좋은 사이즈, 한국어 무난하게 잘함 
        2. 강력한 성능 , chatml, fuction call 지원, 개발자 친화적인 라이선스, 여러 라이브러리 지원 등 
    2. Dataset -  Hard Question Evolution 
        1. 합성데이터
        2. evolkit 방법론 사용 
            1. 그러나 첫번째 시도에서 한국어 seed 데이터셋으로 데이터셋 합성했으나 퀄리티가 좋지 않음 
            2. 영어 seed 데이터로 영어 instruct 데이터 생성 후 번역 (InstaTrans) 논문 참고하여 structered ouput 사용 
        3. kanana개발기에서 봤듯이, 실제로 쓸 법한 진짜 데이터가 중요 
            1. KoAIpaca-RealQA
    3. Supervised fine tuning (SFT)
        1. 순위 사진 
        2. 진짜 쓸 법한 데이터 → human preference 부분에서 차이 큼 
    4. merging
        1. first merging의 목적 : 한국어 SFT 모델 + 기존모델 Synergy
        2. 순위 사진 > 병합 방법이 꼭 들어가야 함 
    5. alignment tuning
        1. RLOO (Reinforce Leave One out)
        2. Onine DPO Trainer (TRL에 구현된) 
        3. Online-RLHF의 interative DPO 
            1. 논문 사진 
            2. 
    6. merging 
        1. alignmnet tax 해결 
        2. exaone 모델 
4. 6Stage 파이프라인
5. 결과
6. 마치며
    1. 하이퍼파라미터 찾는 과정이 굉장이 중요한 요소 
    2. 데이터셋은 최대한 다양하게 (clustering -k means 기법 사용등 다양한 데이터셋 설계 기법들)  
    3. 영어 학습된 reward 모델 사용해도 문제 없음 

QnA

- 고객사 데이터

## 이승유 (dopeornope, 마커 AI): LLM 가이던스 및 Quantization

"LLM 가이던스 및 Quantization"을 주제로, 급속도로 발전하는 LLM 기술의 최신 동향을 조명합니다. 최근 활발히 연구되는 LLM 가이던스와 quantization 기술의 개념과 발전 방향성에 대한 통찰력 있는 분석을 제공합니다.

- Quantization
    - 모델 경량화 방법론
        - Pruning
            - 뉴런들을 가지치기하는 방법 - 어떤 기준으로 가지치기할 지가 중요
                - usturcture pruninig
                - sturcture pruning
                - magnitude pruning
                - Lp norm based pruning
                - sensitivity
                - the minitron approach
                - 필요없는 블럭을 날리는 게 모델 경량화에 도움이 된다고 함
                - risk minimizing이 목표
        - Knowledge Distillation
            - 
        - quantization -
            - 핵심 : 경량화 - pruning 보다 성능 좋게 (pruning은 성능에 위험이 있을 수 있기에_
            - (outlier값을 잘 제어하는 게 중요)
                - precision을 낮추어서
                - data type을 줄여도
                - before quantization
                - after quantization
                - quantization의 error: 양자화 하고 복원할 때의 차이인데 이게 outlier때문에 발생하는 영향이 크기에 이상치값을 잘 찾아야함
                    - caligration (교정) - 이 이상치값의 범위를 잘 찾아내는 게 중요
                    - activation에 초점 두어야 함 (영향을 많이 미침)
                        - AWQ
                    - super weight : 딱 하나의 뉴런을 건드렸더니 모델이 망가지는 결과를 통해 시사한 바
                        - activation에 초점을 두어야 함

- LLM Guidance
    - 파인튜닝 필요할까? 필요는 하겠으나 성능을 보장해주지 않음
    - inference cost
    - Chain-of-Thought
    - reasoning
    - activation Transformation (ACT)
    - Twisted SMC(Sequential Monte Carlo)
        - sequency probabiliy
        - 파인튜닝이 필요가 없다
        - potential이 중요해짐
        - o1처럼 test time cost를 들이는 방식으로 구축…
        - llm은 확률모형으로 바라봐야 한다

## 유용상: KRX 금융 언어 모델 경진대회 후기

"KRX 금융 언어 모델 경진대회 후기"를 통해 도메인 특화 모델 개발의 실전 노하우를 공유합니다. MCQA 벤치마크 성능 향상을 위한 domain adaptation과 continual pretraining 전략, 그리고 safety auditing에 대한 깊이 있는 내용을 다룹니다.

QnA방식으로 추론핦 수 있는 환경을 만들어서 채점을 함 

- 실제 효과적이었던 데이터셋
    - 실제 시험 문제 혹은 공부용 자료
    - 시험출제 요강 등 활용해 seed 데이터 만들고 증강
    - 저퀄리티 데이터에 정제(rule-based, quality filter) 적용하여 활용
    - mcqa
    - PoE: 4지선다 중 아닌 것 먼저 제외시키고 하는 방식이랑 비슷 (먼저 마스킹하고 추론하도록)
    - 유해성 질문에 대한 방어 - MLE, RTO

## 최선웅: RAG 개발 프로젝트 이야기

실제 RAG 개발 프로젝트의 생생한 현장 경험을 공유합니다. 특히 프로젝트 진행 과정에서 발견된 문제점들을 솔직하게 짚어보고, 이를 통해 얻은 교훈과 개선 방향을 제시할 예정입니다.

- Rag의 flywheel
- TDD in RAG
    - Test case : 고객들이 할 법한 질문, 정답/ 오답 레이블
    - 초기설정 잘해야 한다 autorag
    - 테스트 케이스를 synthetic하게 어떻게 ?
    - 실제 production에는 도움이 될 것인가?

## 장영준 (yjoonjang) : 한국어 임베딩 모델- KURE

"한국어 임베딩 모델" [huggingface.co/nlpai-lab](https://huggingface.co/nlpai-lab) 을 주제로 다양한 임베딩 모델의 특징과 실제 학습 과정에서의 핵심 포인트를 공유합니다. 임베딩 모델의 선택부터 학습까지, 실무에 바로 적용할 수 있는 인사이트를 전달할 예정입니다.

- 임베딩모델이란 ?
    - representation
    - 기존 임베딩 모델 개발방식
        - mlm pretraining
        - hard negative mining
            - dense retriever , bm25
            - 배치사이즈가 클 수록 이점이 있는데, gradient cache 기법
- 하이퍼파라미터 성능
    - GIST
- 시사점
    - GIST whgek
    - 배치사이즈 늘린다고 해서 선형적으로 성능이 증가하지 않음
    - epoch늘리면 성능 좋아지긴 하나 굉장히 미비함
- 베스트 시나리오
    - 높으 퀄리티의 hard negative 준비
    - batch sampling을 가능한 negative 고려하여 구성
    - GISTembedLoss 사용

- 검색의 미래 (개인적 생각)
    - reranker
    - cross lingual retrieval
        - 영어로 검색 - 영어의 양질의 문서가 많기 때문
        - ODQA에서도 LLM에 양질의 영어 문서로
        - cross-lingual 모델
    - 
    
- Agent 관련 논문 몇 개 읽고 느낀점
    - slm들을 잘 오케스트레이션 해서 얼마나 좋은 성능을 낼 것인가
    - 프롬프트에 의존할 수 밖 없음
    - 검색의 기능도 중요해짐

## 정세민 (Sionic AI) : Graph RAG로 Recsys 만들기 - Storm fooding

"Graph RAG로 Recsys 만들기 - Storm fooding"을 주제로, 그래프 기반 RAG 시스템을 활용한 추천 시스템 개발 경험을 공유합니다. 시스템 설계부터 구현까지의 전체 과정을 다룰 예정입니다.

## 김동규 (Jeffrey Kim, AutoRAG) : 깃허브 스타 3천개 받아보기

"깃허브 스타 3천개 받아보기"라는 주제로, AutoRAG 오픈소스 프로젝트의 성장 스토리를 들려줍니다. 프로젝트의 시작부터 성공적인 오픈소스화까지의 여정과 앞으로의 발전 방향을 공유합니다.

## 유대곤 (dragonkue) : Retriever 모델 구축 경험 공유(semantic, ensemble, reranker)

다국어 Semantic Retriever, Reranker 의 한국어 성능을 높인 저만의 노하우를 공유합니다. dragonkue 님은 세간에 유명한 https://huggingface.co/dragonkue/BGE-m3-ko 임베딩 모델과 https://huggingface.co/dragonkue/bge-reranker-v2-m3-ko 리랭커 모델을 공개하신 바 있습니다.

## 박정환 ([instruct.kr](https://instruct.kr/), Wanot AI) : 토큰 생성이 항상 정답은 아니다 - Task에 따른 파인튜닝 방법 탐구

일반적으로 파인튜닝을 진행할때에 next token prediction을 training objective로 설정한다. 하지만 대부분에 task에서는 그것이 최선이 아닐 수 있다. 본 발표에서는 모델의 출력부를 변형하여 task에 적합한 training objective를 설정하고, 그것을 next token prediction(CE)와 비교해본다.
