#### **llm관련 오픈채팅방에서 추천받은 한국어 PDF 인식 잘하는 오픈소스 관련 문의답변 정리  

Q: 한국어 PDF 인식 잘하는 오픈소스를 찾고 있습니다. EasyOCR, PaddleOCR 등 사용 경험이 좋았던 오픈소스 추천해 주실 수 있을까요?

A: 이미지 전처리 시 PaddleOCR 훌륭합니다.

Q: 보통 rag하실 때 어떤 파서 주로 쓰시나요? 지금 그냥 llama parser이용해서 pdf만 하고있는데 더 좋은게 있을까해서요. 

A: 아래 3개 정도 추천 더 드립니다. 
Pymupdf4llm
Docling
Gemini api 
MegaParse
(* 관련링크: https://github.com/QuivrHQ/MegaParse )

* MegaParse 관련 링크 요약봇 내용
  - MegaParse는 PDF, DOCX, PPTX 등 다양한 문서 형식을 LLM에 최적화된 형태로 파싱하는 오픈소스 파서입니다. 정보 손실 없이 빠르고 효율적인 파싱을 제공합니다.
  - 지원 파일 형식은 PDF, PowerPoint, Word이며, 표, 목차, 머리말, 꼬리말, 이미지 등의 콘텐츠를 추출합니다. Python 3.11 이상 및 추가 라이브러리 설치가 필요합니다.
  - API 사용도 가능하며, `make dev` 명령어로 개발 서버를 실행하여 다양한 엔드포인트를 통해 파싱 기능을 활용할 수 있습니다. 벤치마크 결과는 다른 파서 대비 높은 유사도 비율을 보입니다.
