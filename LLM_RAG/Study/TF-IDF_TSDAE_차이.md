
(아직 정리중) 

### TF-IDF 
TF-IDF는 전통적인 통계 기반의 문서 표현 기법으로, 각 단어가 문서에서 얼마나 중요한지를 수치로 나타냄.
TF (Term Frequency): 단어가 문서에 얼마나 자주 등장하는지를 나타냄.
IDF (Inverse Document Frequency): 전체 문서에서 특정 단어가 얼마나 희귀한지를 측정.

* 장점
  - 계산이 빠르고 간단하다.
  - 해석이 직관적이다.
  - 희귀하지만 중요한 단어를 잘 잡아낸다.
  
* 단점
  - 단어 순서나 문맥을 고려하지 않는다.
  - 의미적으로 유사한 단어를 구분하지 못한다.
  - 차원이 매우 크다 (희소 벡터).

* 공식:
![image](https://github.com/user-attachments/assets/ddb1f63b-bbeb-44cc-b3be-c86dba4a0fbf)


### TSDAE

* 장점
  - 문장의 의미를 잘 보존하는 임베딩 생성
  - 문맥/단어 순서 고려
  - 유사 문장 간 간격이 좁아져서 검색/추천에 유리

* 단점
  - 사전 훈련 필요 (자체 도메인에 맞춘 튜닝 필요)
  - 리소스 많이 사용 (GPU 필요)
  - 학습 데이터 품질에 민감
    

### TF-IDF vs TSDAE: 차이점 비교
![image](https://github.com/user-attachments/assets/7a5b409c-60e0-422a-95b3-ffdedaa1784c)



