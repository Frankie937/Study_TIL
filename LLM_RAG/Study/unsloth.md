#### **llm관련 오픈채팅방에서 양자화 관련 호환문제 문의 답변 정리 




Q: LLM 양자화랑 파인튜닝을 해보고 있는데, bitsandbytes, triton, peft 등 관련 라이브러리 호환 때문에 실행 중에 에러가 발생하는 것 같은데, 일반적으로 양자화나 파인튜닝에 사용하는 라이브러리 버전이 있을까요?

A: unsloth 추천드립니다. unsloth 안에 양자화와 lora 학습 관련 라이브러리 설정들이 다 들어 있습니다. 
single gpu 환경에서는 초심자분께는 unsloth을 확실히 추천드립니다. (멀티 GPU 환경 지원 안합니다.)

(* unsloth 관련 정리 블로그: https://devocean.sk.com/blog/techBoardDetail.do?ID=166285&boardType=techBlog) 
