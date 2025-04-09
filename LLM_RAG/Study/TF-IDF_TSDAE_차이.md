
(아직 정리중) 

### TF-IDF 
- TF-IDF는 전통적인 통계 기반의 문서 표현 기법으로, 각 단어가 문서에서 얼마나 중요한지를 수치로 나타냄.
- TF (Term Frequency): 단어가 문서에 얼마나 자주 등장하는지를 나타냄.
- IDF (Inverse Document Frequency): 전체 문서에서 특정 단어가 얼마나 희귀한지를 측정.

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
- TSDAE는 Dense Representation을 생성하는 딥러닝 기반 문장 임베딩 방법으로, Siamese 구조의 Autoencoder를 사용하여 문장을 압축하고 복원하면서 의미 정보를 보존한 벡터를 생성.
- Encoder: 문장을 고정된 크기의 벡터로 압축 (BERT, RoBERTa 등 사용 가능)
- Decoder: 벡터를 다시 문장으로 복원
- Noise 추가: 문장을 Dropout 등으로 손상시켜서 복원 능력을 학습

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



