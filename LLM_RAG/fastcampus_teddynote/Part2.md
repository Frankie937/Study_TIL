## Part 2.  체인 파이프라인의 기본 요소

### ch1. 프롬프트

02. yaml 파일로부터 프롬트 템플릿 로드(load_prompt)
  - 프롬프트는 YAML 파일형식으로 저장해두고 관리하는 것을 추천!!

06. 예제 선택기(Example Selector)
  - example_selector의 기능 - prompt에서 가장 유사한 예시를 k개 만큼 추출하는 기능
  → 예시를 너무 많이 넣어버리면 입력 토큰을 너무 많이 사용하게 됨 (비용 증가) 
  → 비용측면 뿐만 아니라, 답변 양식(예시)들이 여러 다양하게 있을텐데 (ex-회의록 형식, 기획안 형식 등등) 그 중에서 요구사항(질문)과 가장 유사한 형식의 답변 양식을 참고해서 답변할 수 있게끔 만들어 주는 용도이기도 함!
![image](https://github.com/user-attachments/assets/bb335dfd-b1d5-4337-a969-5a2c297bfd49)

07. MaxMarginalRelevance(MMR) 알고리즘 
  - 기존에 06번에서 사용했던 알고리즘 SemanticSimilarityExampleSelector는 많이 알고 있는 cosine similarity를 사용한 코사인유사도 계산으로 나오는 가장 유사한 것을 뽑아내는 알고리즘 기법
  - MaxMarginalRelevance 알고리즘은 질문과 유사성이 있으면서도 다양한 예제를 가져오고 싶을 때 사용! (즉, 관련성과 다양성 2가지 측면을 고려함. 먼저 가장 관련성 높은 항목을 선택하고 그 이후 관련성이 높으면서 가장 차별화된 항목들을 찾아 선택하는 구조 - 람다값에 의해 관련성과 차별성을 조절 → 람다값이 클수록 다양성을, 작을수록 다양성을 더 중시한다고 함)
![image](https://github.com/user-attachments/assets/e7033981-f536-4558-bbcb-0612b9950e47)

08. 목적에 맞는 예제 선택기(CustomExampleSelector)
→  테디님이 만드신 CustomExampleSelector
![image](https://github.com/user-attachments/assets/abd2351d-95cb-4e31-b17f-7772e0f873eb)
![image](https://github.com/user-attachments/assets/1c874359-f228-4368-843d-8b346b7221ec)
  → 저 클래스 내부를 보면 search_key 인자를 따로 만들어서, 저 값이 instruction이면 instruction끼리 유사도를 측정하고 input이면 input 끼리 유사도 측정해서 나오도록 함! 
  → 기존 Example Selector들(SemanticSimilarityExampleSelector, MMR )은 모두 유사도 계산시, instruction과 input이 합산된 유사도로 계산되어서 예시가 잘 나오지 않을 때가 많은 문제가 있음

09. LangSmith - Hub
(https://smith.langchain.com/hub?organizationId=02a489e1-23b2-5f26-a131-f2851cc73a9c)
![image](https://github.com/user-attachments/assets/4e5e4ba7-c3e6-4076-916b-de6c540ffb00)
  → 잘 작성된 prompt 가져올 수 있음   
  → 오른쪽 바에서 use case로 골라서 선택하고, top view나 top download 클릭하면 보통 rlm 계정으로 올려진 prompt가 많음. 그것도 평균적으로 좋지만 그 다음꺼 추천한다고 하심

![image](https://github.com/user-attachments/assets/b116aa89-a6b2-49ba-883d-9afbaa226c21)
  →  직접 복사해서 사용해도 좋고 
  → 저렇게 langchain 코드로 갖고올 수도 있음
  
```python
prompt = hub.pull("rlm/rag-prompt:50442af1")
prompt
```
  → 특정 버전을 : 이후로 해시코드 작성해서 다른 버전으로 갖고올 수도 있음 (commit 버튼 눌러보면 버전별 확인 가능)
  → 또한, 자신신이 작성한 prompt를 hub에 업로드도 가능! (아래코드 참고)
```python
from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template(
    "주어진 내용을 바탕으로 다음 문장을 요약하세요. 답변은 반드시 한글로 작성하세요\n\nCONTEXT: {context}\n\nSUMMARY:"
)
prompt
from langchain import hub
# 프롬프트를 허브에 업로드합니다.
hub.push("teddynote/simple-summary-korean", prompt)
```
** 만약 내가 작성한 prompt를 private하게 업로드 하고 싶다면 ‘Make Private’ 기능 사용 
![image](https://github.com/user-attachments/assets/330c14ad-1474-433e-8555-197db7148b87)


### ch3. RAG시작하기

- 01~04 번 내용
#### EP01. [#RAG](https://www.youtube.com/hashtag/rag) 의 동작 과정 쉽게 이해하기!
** 임베딩 ? 
문서의 단락 → 수학적인 표현 즉 좌표계로 변경 
- 문서 임베딩 프로세스 구조
문서 로드 > 문서 split > 쪼개진 문서의 단락을 임베딩 (수학적 표현, 좌표계로 변환) > 벡터DB 저장
(ex 벡터를 사용 - open ai 임베딩모델 1536차원을 사용 → 1536개의 숫자로 표현된다는 의미)

#### EP02. #RAG 의 동작과정 쉽게 이해하기!(실행단계)
** 검색기(Retriever) 단계는 Retrieval-Augmented Generation(RAG) 시스템의 다섯 번째 단계로, 저장된 **벡터 데이터베이스에서 사용자의 질문과 관련된 문서를 검색**하는 과정이다. 이 단계는 **사용자의 질문에 가장 적합한 정보를 신속하게 찾아내는 것**이 목표이고, RAG시스템의 전반적인 성능과 직결되는 매우 중요한 과정이다! 

** 검색기에 사용되는 여러 알고리즘이 많음 (키워드, 의미검색, 하이브리드 서치 등등…)
 ex) Sparse Retriever ('키워드' 검색을 잘하는 검색기), Dense Retriever('의미검색'을 잘하는 검색기) 등 

** 검색기 속도도 중요 (-> 응답시간 단축을 위해)

- 동작방식 (한번 더 복습)
    1. 질문의 벡터화: 사용자의 질문을 벡터 형태로 변환(이 과정은 임베딩 단계와 유사한 기술 사용하여 진행) 변환된 질문 벡터는 후속 검색 작업의 기준점으로 사용 됨
    2. 벡터 유사성 비교: 저장된 문서 벡터들과 질문 벡터사이의 유사성을 계산 (주로 코사인 유사도(cosine similarity), Max Marginal Relevance(MMR) 등의 수학적 방법을 사용하여 수행
    3. 상위 문서 선정: 계산된 유사성 점수를 기준으로 상위 N개의 가장 관련성 높은 문서를 선정함. (이 문서들은 다음 단계에서 사용자의 질문에 대한 답변을 생성하는 데 사용 됨 - 프롬픔트에서 참고 context로서) 
    4. 문서 정보 반환: 선정된 문서들의 정보를 다음 단계(프롬프트 생성)로 전달함. 이 정보에는 문서의 내용, 위치, 메타데이터 등이 포함될 수 있음 

** 원래 RAG를 사용하지 않았을 때는, 기본적인 LLM에서는 LLM 모델에 넣어주는 프롬프트에서 사용자의 질문만 넣었지만 RAG를 사용하는 건 프롬프트에 context를 사용자의 질문과 함께 넣어주는 것
(-> 사용자의 질문에 대한 답변을 생성할 때, 검색된 문서들을 context로 참고하여 답변을 생성하라는 의미- 이게 RAG의 핵심- context를 llm에게 주는 것!!) 

#### EP03. #PDF 문서기반 QA #RAG 구축하기

- 문서로드
    - 메타데이터는 어떤 문서로더를 사용했느냐에 따라 다르다. (**메타데이터를 잘 활용해서 문서를 추출할 때 필터링하거나 유용하게 사용할 수 있기 때문에 메타데이터에 대한 정보와 구조를 로더에 따라 잘 확인하고 활용하는 것 중요요)
    ex) PyMuPDFLoader
![image](https://github.com/user-attachments/assets/fabcb97e-1d8f-4a44-af8a-365a9148cf9c)

```python
# 단계 1: 문서 로드(Load Documents)
loader = PyMuPDFLoader("data/SPRI_AI_Brief_2023년12월호_F.pdf")
docs = loader.load()
```

- 문서 분할
    - RecursiveCharacterTextSplitter 를 범용적으로 많이 사용
    - chunk_size 정할 때 팁: 무조건 크게 설정한다고 좋은 것 아님! 해당 문서의 특성에 따라 같은 맥락이 이어지는 문단이나 단라의 글자 수 단위를 어느정도 파악하고 정해주는 게 베스트인데, 그러나 그 글자수가 항상 일정하지 않기 때문에 대략적으로 넣어줄 수 밖에는 없음…
    
    ```python
    # 단계 2: 문서 분할(Split Documents)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)
    ```
    
- 임베딩

```python
# 단계 3: 임베딩(Embedding) 생성
embeddings = OpenAIEmbeddings()
```

- 벡터 DB 및 저장

```python
# 단계 4: DB 생성(Create DB) 및 저장
# 벡터스토어를 생성합니다.
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
```

- Retriever 생성

```python
# 단계 5: 검색기(Retriever) 생성
# 문서에 포함되어 있는 정보를 검색하고 생성합니다.
retriever = vectorstore.as_retriever()
```

- Prompt 생성

```python

# 단계 6: 프롬프트 생성(Create Prompt)
# 프롬프트를 생성합니다.
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in Korean.

#Context: 
{context}

#Question:
{question}

#Answer:"""
)
```

- LLM 모델 생성

```python
# 단계 7: 언어모델(LLM) 생성
# 모델(LLM) 을 생성합니다.
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
```

- Chain 생성

```python
# 단계 8: 체인(Chain) 생성
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

→ Chain 실행

```python
# 체인 실행(Run Chain)
# 문서에 대한 질의를 입력하고, 답변을 출력합니다.
question = "삼성전자가 자체 개발한 AI 의 이름은?"
response = chain.invoke(question)
print(response)

# stream 형식으로 나오게 하려면 
import langchain_teddynote.messages import stream_response

question = "삼성전자가 자체 개발한 AI 의 이름은?"
response = chain.stream(question)
stream_responese(response)
```

** LangSmith가 중요한 이유?

기존에 답변이 잘못나왔을 때, 답변만 나오기에 해당 원인이나 문제를 분석할 수 없었음 

그러나 LangSmith는 이렇게 참고한 문서들이 몇 개가 있었고 어떤 내용들이었는지 확인할 수 있게 해주기에 어디서 잘못되었던 건지 원인 파악 및 분석이 가능해짐 

참고할 도큐먼트들이 잘못 추출된 것이라면, 검색기가 잘못 된 것이기에 검색기 부분을 수정을 해줘야 하거나 아니면, 검색기 알고리즘의 문제가 아니라 문서를 잘못 로드했을 수도 있고, split에서 잘못된 걸수도 있고, 임베딩이 잘못될 수 도, DB선택이 잘못되었을 수도 있다… 5가지 문제를 종합적으로 봐야 한다!!!! 

그렇기에 이러한 문제를 잘 해결하기 위해서는 하나하나 단계마다 세부적으로 확인하고 이해하고 공부해야 할 필요가 있는 것 !!!(그래서 기본기도 굉장히 중요)
![image](https://github.com/user-attachments/assets/b522a643-8e76-422f-8b76-29437d30ae1a)



 ** 아래와 같이, 답변에 참고한 문서 페이지번호 추가하는 방법!! 
![image](https://github.com/user-attachments/assets/1f652791-c633-4ac8-a019-8a03f346af56)
→ 답변에서 어떤 페이지 참고했는지 정보 추가해서 넣어달라는 것을 prompt로 추가해서 변경 

“You must include ‘page’ number in your answer.”
![image](https://github.com/user-attachments/assets/1d534300-35bd-4cab-a846-174162001d39)

→ 이게 가능한 이유는 사용한 pdf 로더, PyMuPDFLoader에서 metadata에 page 번호가 있기 때문 !!!
![image](https://github.com/user-attachments/assets/4ba85a06-433b-44c4-9570-46fc18392699)

** prompt에서 여러 개의 변수를 입력으로 받을 때 prompt.partial을 사용하기 
ex) prompt-maker.yaml 파일에서  보여지는 것처럼 {task} , {question} 2개의 변수가 입력변수로 받아야 하는 prompt 구조
![image](https://github.com/user-attachments/assets/69cdd026-963e-47f2-b881-f90e0a7559e8)
![image](https://github.com/user-attachments/assets/57b457f8-e534-4afb-aa64-dd0afbb7ab6f)

→ prompt.partial 을 이용해서 변수를 추가 처리 할 수 있음 

- 08번 내용
-01_PDF.py에서 사용되는 pdf-rag.yaml 파일에서 prompt 주요한 팁!! (출처 기록 & 마크다운 테이블 표 형식)
  ![image](https://github.com/user-attachments/assets/2f657d37-e90a-4e32-8b53-5d884d69955a)


### ch4. 출력파서(Output Parser)
- 01번 - PydanticOutputParser
    - 주요 엔티티 추출을 잘 할려면 description을 잘 작성하는 게 중요하다!!
```python
from langchain_core.pydantic_v1 import BaseModel, Field

# 이메일 본문으로부터 주요 엔티티 추출 
class EmailSummary(BaseModel):
    person: str = Field(description="메일을 보낸 사람")
    company: str = Field(description="메일을 보낸 사람의 회사 정보")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")
```

- 10번 - 열거형 출력파서 
→ LLM으로부터 선택지를 주고 그 중에 답변을 받고 싶을 경우에 유용한 출력파서!

** 답변으로 문자열로 받지 않고 Class 객체로 받으면 좋은 점이 정형화 되어있어서 값을 key로 쉽게 꺼낼 수 있고

### ch5. 출력파서 활용 프로젝트

- chain을 2개 생성 하고 검색기능 사용(SerpAPI 활용)하여 만드는 프로젝트
    - 기능 3가지
        - 이메일을 파싱하는 chain 생성
        - 보낸 사람의 추가정보 수집 (검색기능 사용)
        - 이메일 요약 리포트 생성
```python
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_teddynote.prompts import load_prompt

# 검색을 위한 API KEY 설정
os.environ["SERPAPI_API_KEY"] = (
    "[e76de14ee240e0051ed8bb05d5db568dd1dc9cfcaa2b51fd83613829a85bf244"
)
# key값은 https://serpapi.com/manage-api-key 에서 확인하기 

# 이메일 본문으로부터 주요 엔티티 추출 (description 잘 작성하는 게 중요)
class EmailSummary(BaseModel):
    person: str = Field(description="메일을 보낸 사람")
    company: str = Field(description="메일을 보낸 사람의 회사 정보")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")

# API KEY 정보로드
load_dotenv()

st.title("Email 요약기 💬")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

# 체인 생성
def create_email_parsing_chain():
    # PydanticOutputParser 생성
    output_parser = PydanticOutputParser(pydantic_object=EmailSummary)

    prompt = PromptTemplate.from_template(
        """
    You are a helpful assistant. Please answer the following questions in KOREAN.

    #QUESTION:
    다음의 이메일 내용 중에서 주요 내용을 추출해 주세요.

    #EMAIL CONVERSATION:
    {email_conversation}

    #FORMAT:
    {format}
    """
    )

    # format 에 PydanticOutputParser의 부분 포맷팅(partial) 추가
    prompt = prompt.partial(format=output_parser.get_format_instructions())

    # 체인 생성
    chain = prompt | ChatOpenAI(model="gpt-4-turbo") | output_parser

    return chain

def create_report_chain():
    prompt = load_prompt("prompts/email.yaml", encoding="utf-8")

    # 출력 파서
    output_parser = StrOutputParser()

    # 체인 생성
    chain = prompt | ChatOpenAI(model="gpt-4-turbo") | output_parser

    return chain

# 초기화 버튼이 눌리면...
if clear_btn:
    st.session_state["messages"] = []

# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 만약에 사용자 입력이 들어오면...
if user_input:
    # 사용자의 입력
    st.chat_message("user").write(user_input)

    # 1) 이메일을 파싱하는 chain 을 생성
    email_chain = create_email_parsing_chain()
    # email 에서 주요 정보를 추출하는 체인을 실행
    answer = email_chain.invoke({"email_conversation": user_input})

    # 2) 보낸 사람의 추가 정보 수집(검색)
    params = {"engine": "google", "gl": "kr", "hl": "ko", "num": "3"}  # 검색 파라미터
    search = SerpAPIWrapper(params=params)  # 검색 객체 생성
    search_query = f"{answer.person} {answer.company} {answer.email}"  # 검색 쿼리
    search_result = search.run(search_query)  # 검색 실행
    search_result = eval(search_result)  # list 형태로 변환

    # 검색 결과(합치기)
    search_result_string = "\n".join(search_result)

    # 3) 이메일 요약 리포트 생성
    report_chain = create_report_chain()
    report_chain_input = {
        "sender": answer.person,
        "additional_information": search_result_string,
        "company": answer.company,
        "email": answer.email,
        "subject": answer.subject,
        "summary": answer.summary,
        "date": answer.date,
    }

    # 스트리밍 호출
    response = report_chain.stream(report_chain_input)
    with st.chat_message("assistant"):
        # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
        container = st.empty()

        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # 대화기록을 저장한다.
    add_message("user", user_input)
    add_message("assistant", ai_answer)

```

- email.yaml 파일
```yaml
_type: "prompt"
template: |
  당신은 이메일의 주요 정보를 바탕으로 요약 정리해 주는 전문가 입니다.
  당신의 임무는 다음의 이메일 정보를 바탕으로 보고서 형식의 요약을 작성하는 것입니다.
  주어진 정보를 기반으로 양식(format)에 맞추어 요약을 작성해 주세요.

  #Information:
  - Sender: {sender}
  - Additional Information about sender: {additional_information}
  - Company: {company}
  - Email: {email}
  - Subject: {subject}
  - Summary: {summary}
  - Date: {date}

  #Format(in markdown format):
  🙇‍♂️ 보낸 사람:
  - (보낸 사람의 이름, 회사 정보)

  📧 이메일 주소:
  - (보낸 사람의 이메일 주소)

  😍 보낸 사람과 관련하여 검색된 추가 정보:
  - (검색된 추가 정보)

  ✅ 주요 내용:
  - (이메일 제목, 요약)

  ⏰ 일정:
  - (미팅 날짜 및 시간)

  #Answer:
input_variables: ["sender", "additional_information", "company", "email", "subject", "summary", "date"]
```

### ch6. 모델(Model)

05. 토큰 사용량 확인 -> langachain의 get_openai_callback 함수 사용 

```python
# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()
from langchain.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

# 모델을 불러옵니다.
llm = ChatOpenAI(model_name="gpt-4o") 

# callback을 사용하여 추적합니다.
with get_openai_callback() as cb:
    result = llm.invoke("대한민국의 수도는 어디야?")
    result = llm.invoke("대한민국의 수도는 어디야?")
    print(f"총 사용된 토큰수: \t\t{cb.total_tokens}")
    print(f"프롬프트에 사용된 토큰수: \t{cb.prompt_tokens}")
    print(f"답변에 사용된 토큰수: \t{cb.completion_tokens}")
    print(f"호출에 청구된 금액(USD): \t${cb.total_cost}")
```

09. HuggingFace Dedicated Endpoint를 활용한 로컬모델 원격 호스팅 

→ 테디님도 정말 좋아하는 서비스라고 하심

→ 로컬 모델을 호스팅하는 방법 중 하나라고 하심 

→ 비용도 가성비 좋은 GPU 고를 수 있고(**suggested 하는) 사용하기 쉽게 되어있기에, 간단한 테스트 해볼 때 좋은 서비스라고 생각함 !! 

 

1. HuggingFace Local 모델 

→ 기존, 8번은 허깅페이스의 서버에 올려져있는 모델 중 inference api 기능을 제공하는 모델을 (허깅페이스에서 호스팅하는 구조) 로컬 pc에서 돌려본 것이고/ 9번은 허깅페이스의 서버에 올려져 있는 모델 중 inference api 기능을 제공하지 않지만 endpoint url 기능을 제공하는 모델을 (허깅페이스에서 호스팅하는 구조) 로컬 pc에서 돌려 본 것 

→ 이번 10번 강의에서는 허깅페이스에 올려져 있는 오픈 모델을 우리 로컬pc에 다운로드 받아서 추론하는 과정을 볼 예정!! (→ 우리 각자의 로컬 PC 사양이 중요해짐… 그로므로 사양이 좋지 않으면 추론하는 과정에서 ouput 토큰이 출력되는 게 굉장히 느리거나 gpu가 없다면 아예 구동이 안될 수도..ㅠㅠ → 그래서, gpu가 설정이 되어있어야 하고 window를 쓸 경우 cuda 설정이 되어있어야 함) 

### ch7. 모델활용 프로젝트

03. [프로젝트] Ollama 모델을 사용한 RAG 

→ 모델마다 학습 시킨 프롬프트가 다르기 때문에 모델에 맞게 프롬프트를 수정해주는 게 중요!
