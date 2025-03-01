#### **llm관련 오픈채팅방에서 gguf 모델 변환 관련 문의 답변 정리

Q: GGUF 파일로 변환하면 transformers 라이브러리를 사용한 추론이 안되고 cli만 사용해서 추론이 가능한건가요?

A: gguf로 사용하시려면 아래 예제코드처럼 사용하시면 될 것 같습니다. 
(참고 도큐먼트 링크: https://huggingface.co/docs/transformers/gguf) 

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
filename = "tinyllama-1.1b-chat-v1.0.Q6_K.gguf"

tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=filename)
model = AutoModelForCausalLM.from_pretrained(model_id, gguf_file=filename)
```


* 참고 도큐먼트 관련 내용 요약봇 
  - Transformers는 GGUF 파일 형식을 지원하여 GGML 기반 모델(llama.cpp, whisper.cpp 등)을 불러와 PyTorch 환경에서 미세조정 및 추가 학습을 가능하게 합니다.
  - 이는 모델을 불러올 때 먼저 fp32로 변환하는 방식을 사용합니다.
  - 현재 지원하는 양자화 방식은 F32, F16, BF16 등 다양하며, LLaMa, Mistral, Qwen2 등 여러 인기 모델 아키텍처를 지원합니다.
  - GGUF 파일 디양자화를 위해서는 gguf>=0.10.0 설치가 필요합니다.
  - `AutoTokenizer.from_pretrained` 및 `AutoModelForCausalLM.from_pretrained` 메서드의 `gguf_file` 인자를 사용하여 GGUF 파일을 로드하고, llama.cpp의 `convert-hf-to-gguf.py` 스크립트를 이용하여 다시 GGUF 파일로 변환할 수 있습니다.
