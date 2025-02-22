## Part 5.  바로 사용할 수 있는 체인

### Ch06.

 05번 강의-  "[프로젝트] 무료 오픈모델로 문서기반 QA RAG 시스템 구현”

- ollama
오픈소스 llm 모델을 로컬 pc로 갖고와서 호스팅할 수 있도록 만드는 프레임워크

ollama pull [모델명] # ollama에 있는 모델 다운로드
ollama run [모델명] # ollama로 다운받은 모델 실행
ollama list # 로컬 pc에서 ollama로 다운받은 모델 리스트 확인
ollama create [커스텀모델명] -f modelfile # modelfile을 사용하여 모델 생성
ollama run [커스텀모델명]

- ollama 임베딩 모델
ollama pull bge-m3
1.2G 파일
- 한글 성능 좋은 모델
EXAONE-3.5 모델(gguf): https://huggingface.co/LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct-GGUF
gemma2-27b: https://ollama.com/library/gemma2:27b
EEVE-Korean-10.8B(gguf): https://huggingface.co/teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf
Qwen2.5-7B-Instruct-kowiki-qa-context(gguf): https://huggingface.co/teddylee777/Qwen2.5-7B-Instruct-kowiki-qa-gguf

** 오프소스 모델인 경우에는 프롬프트를 더 자세히 잘 주어야 한다.

- CacheBackedEmbeddings
오픈소스 모델은 성능때문에 캐싱 임베딩을 사용하는 게 속도차원에서 중요 !!

- 프로세스 개선 point 예시
    - 프롬프트 엔지니어링
    - 다양한 모델 테스트 해보기
    - 임베딩 청크 사이즈 변경해보기
    - 벡터 데이터베이스 변경해보기
