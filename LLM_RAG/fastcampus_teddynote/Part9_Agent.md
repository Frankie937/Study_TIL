### Ch1.  Tools / Toolkits

01. 랭체인에서 제공하는 다양한 도구(Tools) 툴킷(Toolkits) 활용법 

- PythonREPLTool : 문자열을 실행가능한 python 코드로 변경해서 실행까지 해서 결과를 주는 tool
- TavilySearchResutls : 인터넷 웹 검색 API를 쿼리하고 JSON형식의 결과를 반환해주는 tool 
(https://tavily.com/)
    - max_reulsts 옵션: 검색 결과 개수 지정 (기본값: 5)
    - include_domains 옵션 : 지정한 도메인에서만 검색하도록
        
        ```python
        
        from langchain_community.tools.tavily_search import TavilySearchResults
        # 도구 생성
        tool = TavilySearchResults(
            max_results=6,
            include_answer=True,
            include_raw_content=True,
            # include_images=True,
            # search_depth="advanced", # or "basic"
            include_domains=["github.io", "wikidocs.net"],
            # exclude_domains = []
        )
        ```
        
- 이미지 생성 도구 (DALL-E ) - DallEAPIWrapper
    
    ```python
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
    from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
    from IPython.display import Image
    import os
    
    # ChatOpenAI 모델 초기화
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, max_tokens=1000)
    
    # DALL-E 이미지 생성을 위한 프롬프트 템플릿 정의
    prompt = PromptTemplate.from_template(
        "Generate a detailed IMAGE GENERATION prompt for DALL-E based on the following description. "
        "Return only the prompt, no intro, no explanation, no chatty, no markdown, no code block, no nothing. Just the prompt"
        "Output should be less than 1000 characters. Write in English only."
        "Image Description: \n{image_desc}",
    )
    
    # 프롬프트, LLM, 출력 파서를 연결하는 체인 생성
    chain = prompt | llm | StrOutputParser()
    
    # DALL-E API 래퍼 가져오기 및 래퍼 초기화
    dalle = DallEAPIWrapper(
        model="dall-e-3", # model: 사용할 DALL-E 모델 버전
        size="1024x1024", # size: 생성할 이미지 크기
        quality="standard", # quality: 이미지 품질
        n=1, # n: 생성할 이미지 수
    )
    
    # 질문
    query = "스마트폰을 바라보는 사람들을 풍자한 neo-classicism painting"
    
    # 이미지 생성 및 URL 받기
    # chain.invoke()를 사용하여 이미지 설명을 DALL-E 프롬프트로 변환
    # dalle.run()을 사용하여 실제 이미지 생성
    image_url = dalle.run(chain.invoke({"image_desc": query}))
    
    # 생성된 이미지를 표시합니다.
    Image(url=image_url, width=500)
    ```
    

** 위의 3개 말고도 langchain에 integration 된 도구들이 굉장히 많음!! (langchain의 큰 장점) 
(→ 무료 tool도 굉장히 많고, Paid 되는 tool이더라도 테스트 해볼 수 있도록 무료 credit을 주는 편!)

https://python.langchain.com/docs/integrations/tools/

02. 사용자 정의 도구 (Custom Tools)만드는 법 

LangChain 에서 제공하는 빌트인 도구 외에도 사용자가 직접 도구를 정의하여 사용할 수 있습니다.

이를 위해서는 `langchain.tools` 모듈에서 제공하는 `tool` 데코레이터를 사용하여 함수를 도구로 변환합

- **사용 방법**
    1. 함수 위에 `@tool` 데코레이터 적용
    2. 필요에 따라 데코레이터 매개변수 설정

→ 이 데코레이터를 사용하면 일반 Python 함수를 강력한 도구로 쉽게 변환할 수 있으며, 자동화된 문서화와 유연한 인터페이스 생성이 가능함( 사용자가 생성한 함수에 영어로 doc string을 자세하게 작성하는 것이 중요!!)


### Ch2. Agent 주요기능

01. LLM에 도구 바인딩 (Binding Tools) 

- tool 생성할 때, doc string을 자세하게 영어로 적어주는 게 중요!! (llm이 잘 이해할 수 있게)

```python
import re
import requests
from bs4 import BeautifulSoup
from langchain.agents import tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI


# 도구를 정의합니다.
@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


@tool
def add_function(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b


@tool
def naver_news_crawl(news_url: str) -> str:
    """Crawls a 네이버 (naver.com) news article and returns the body content."""
    # HTTP GET 요청 보내기
    response = requests.get(news_url)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, "html.parser")

        # 원하는 정보 추출
        title = soup.find("h2", id="title_area").get_text()
        content = soup.find("div", id="contents").get_text()
        cleaned_title = re.sub(r"\n{2,}", "\n", title)
        cleaned_content = re.sub(r"\n{2,}", "\n", content)
    else:
        print(f"HTTP 요청 실패. 응답 코드: {response.status_code}")

    return f"{cleaned_title}\n{cleaned_content}"




# Agent 프롬프트 생성
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# 모델 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 이전에 정의한 도구 사용
tools = [get_word_length, add_function, naver_news_crawl] 

# Agent 생성
agent = create_tool_calling_agent(llm, tools, prompt)

# AgentExecutor 생성
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# Agent 실행
result = agent_executor.invoke({"input": "How many letters in the word `teddynote`?"})
# 결과 확인
print(result["output"])

# Agent 실행
result = agent_executor.invoke({"input": "114.5 + 121.2 의 계산 결과는?"})
# 결과 확인
print(result["output"])


# Agent 실행
result = agent_executor.invoke(
    {
        "input": "뉴스 기사를 요약해 줘: https://n.news.naver.com/mnews/hotissue/article/092/0002347672?type=series&cid=2000065"
    }
)
# 결과 확인
print(result["output"])
```
- MessagesPlaceholder는 변수처럼 동적으로 채워질 수 있는 공간(플레이스홀더) 
- variable_name="agent_scratchpad"는 LangChain의 실행 과정에서 추가적인 메시지를 저장하는 역할을 함
- agent_scratchpad는 AI가 사고하는 과정(예: 중간 연산 결과, 체계적 추론 등)을 저장하는 공간
  (예를 들어, 위의 코드에서 '네이버뉴스 요약해달라'는 사용자의 요청이었을 때, agent가 자신의 tools 중에 naver_news_crawl 를 사용하여 크롤링한 뉴스 내용을 저장하는 공간일 될 수 있음 - for llm에게 사용자의 input과 함께 전달하기 위해)
- 일반적으로 LangChain의 에이전트(Agent)에서 사용됨. 이 값은 프롬프트가 실행될 때 동적으로 채워짐



02. Agent, AgentExecutor
- **AgentExecutor**가 필요한 이유?
→  Agent도 나중에 멀티 에이전트 방식으로 가기에 여러 개의 Agent를 핸들링하고 흐름제어하는 컨트롤 관점에서 필요하기에 !!
    - AgentExecutor는 도구를 사용하는 에이전트를 실행하는 클래스입니다.
    - **주요 속성**
        - `agent`: 실행 루프의 각 단계에서 계획을 생성하고 행동을 결정하는 에이전트
        - `tools`: 에이전트가 사용할 수 있는 유효한 도구 목록
        - `return_intermediate_steps`: 최종 출력과 함께 에이전트의 중간 단계 경로를 반환할지 여부
        - `max_iterations`: 실행 루프를 종료하기 전 최대 단계 수
        - `max_execution_time`: 실행 루프에 소요될 수 있는 최대 시간
        - `early_stopping_method`: 에이전트가 `AgentFinish`를 반환하지 않을 때 사용할 조기 종료 방법. ("force" or "generate")
            - `"force"` 는 시간 또는 반복 제한에 도달하여 중지되었다는 문자열을 반환합니다.
            - `"generate"` 는 에이전트의 LLM 체인을 마지막으로 한 번 호출하여 이전 단계에 따라 최종 답변을 생성합니다.
        - `handle_parsing_errors`: 에이전트의 출력 파서에서 발생한 오류 처리 방법. (True, False, 또는 오류 처리 함수)
        - `trim_intermediate_steps`: 중간 단계를 트리밍하는 방법. (-1 trim 하지 않음, 또는 트리밍 함수)
    - **주요 메서드**
        1. `invoke`: 에이전트 실행
        2. `stream`: 최종 출력에 도달하는 데 필요한 단계를 스트리밍
    - **주요 기능**
        1. **도구 검증**: 에이전트와 호환되는 도구인지 확인
        2. **실행 제어**: 최대 반복 횟수 및 실행 시간 제한 설정 가능
        3. **오류 처리**: 출력 파싱 오류에 대한 다양한 처리 옵션 제공
        4. **중간 단계 관리**: 중간 단계 트리밍 및 반환 옵션
        5. **비동기 지원**: 비동기 실행 및 스트리밍 지원
    - **최적화 팁**
        - `max_iterations`와 `max_execution_time`을 적절히 설정하여 실행 시간 관리
        - `trim_intermediate_steps`를 활용하여 메모리 사용량 최적화
        - 복잡한 작업의 경우 `stream` 메서드를 사용하여 단계별 결과 모니터링


03. Agent의 중간 단계 스트리밍(stream) 
- Actioin : AgentAction이라는 객체가 호출되면서 어떤 도구를 써야 할 지 사용할 도구를 결정하여, 실행함
- Observation : 실행한 결과가 observaton에 담기게 됨
- Final Answer : 그 결과가 담긴 Observation을 보고 답변을 생성하게 됨

→ 오류가 나거나 에러 시, Action 과 Observation 단계를 반복하게 됨


04. Agent에 메모리 추가(멀티턴 구현) 
이전의 대화내용을 기억하기 위해서는 `RunnableWithMessageHistory` 를 사용하여 `AgentExecutor` 를 감싸줍니다.
( https://wikidocs.net/254682 : **RunnableWithMessageHistory에 ChatMessageHistory추가 )**

```python
from langchain.tools import tool
from typing import List, Dict, Annotated
from langchain_teddynote.tools import GoogleNews
from langchain_experimental.utilities import PythonREPL
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# 도구 생성
@tool
def search_news(query: str) -> List[Dict[str, str]]:
    """Search Google News by input keyword"""
    news_tool = GoogleNews()
    return news_tool.search_by_keyword(query, k=5)

# 도구 생성
@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate your chart."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    result = ""
    try:
        result = PythonREPL().run(code)
    except BaseException as e:
        print(f"Failed to execute. Error: {repr(e)}")
    finally:
        return result

# tools 정의
tools = [search_news, python_repl_tool]

# 프롬프트 생성
# 프롬프트는 에이전트에게 모델이 수행할 작업을 설명하는 텍스트를 제공합니다. (도구의 이름과 역할을 입력)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Make sure to use the `search_news` tool for searching keyword related news.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# LLM 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Agent 생성
agent = create_tool_calling_agent(llm, tools, prompt)

# AgentExecutor 생성
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
)

# AgentCallbacks와 AgentStreamParser를 langchain_teddynote.messages에서 가져옵니다.
from langchain_teddynote.messages import AgentCallbacks, AgentStreamParser

# 도구 호출 시 실행되는 콜백 함수입니다.
def tool_callback(tool) -> None:
    print("<<<<<<< 도구 호출 >>>>>>")
    print(f"Tool: {tool.get('tool')}")  # 사용된 도구의 이름을 출력합니다.
    print("<<<<<<< 도구 호출 >>>>>>")

# 관찰 결과를 출력하는 콜백 함수입니다.
def observation_callback(observation) -> None:
    print("<<<<<<< 관찰 내용 >>>>>>")
    print(
        f"Observation: {observation.get('observation')[0]}"
    )  # 관찰 내용을 출력합니다.
    print("<<<<<<< 관찰 내용 >>>>>>")
     
# 최종 결과를 출력하는 콜백 함수입니다.
def result_callback(result: str) -> None:
    print("<<<<<<< 최종 답변 >>>>>>")
    print(result)  # 최종 답변을 출력합니다.
    print("<<<<<<< 최종 답변 >>>>>>")

# AgentCallbacks 객체를 생성하여 각 단계별 콜백 함수를 설정합니다.
agent_callbacks = AgentCallbacks(
    tool_callback=tool_callback,
    observation_callback=observation_callback,
    result_callback=result_callback,
)

# AgentStreamParser 객체를 생성하여 에이전트의 실행 과정을 파싱합니다.
agent_stream_parser = AgentStreamParser(agent_callbacks)

# session_id 를 저장할 딕셔너리 생성
store = {}
# session_id 를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in store:  # session_id 가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_ids] = ChatMessageHistory()
    return store[session_ids]  # 해당 세션 ID에 대한 세션 기록 반환

# 채팅 메시지 기록이 추가된 에이전트를 생성합니다.
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # 대화 session_id
    get_session_history,
    # 프롬프트의 질문이 입력되는 key: "input"
    input_messages_key="input",
    # 프롬프트의 메시지가 입력되는 key: "chat_history"
    history_messages_key="chat_history",
)

# 질의에 대한 답변을 스트리밍으로 출력 요청
response = agent_with_chat_history.stream(
    {"input": "안녕? 내 이름은 테디야!"},
    # session_id 설정
    config={"configurable": {"session_id": "abc123"}}, # session_id를 다른 것으로 하면 대화내용 기억 X
)

# 출력 확인
for step in response:
    agent_stream_parser.process_agent_steps(step)
```

### Ch3. Agent 활용

01. Agentic RAG

- 기존의 RAG 방식과는 무엇이 다른가? 
→ 상황에 따라 다르기 때문에 상황에 따라 효율적으로 기존 RAG를 사용하는 게 더 적절할 수 있고 Agentic RAG를 사용하는 것이 더 적절할 수 있음
- Agentic RAG의 가장 큰 장점 ?
    - LLM에 도구를 쥐어질 수 있다는 점 (LLM에게 도구를 쥐어주고 신경 쓸 필요가 없어짐)
    - 하나의 정해진 절차에만 수행을 하는 것이 아니라 **상황에 따라서 유동적으로 LLM이 처리를 할 수 있게끔** 함 (** 이 점이 Agentic RAG, Agent의 핵심!!!)
- Agentic 전체 템플릿 코드
```python
# 필요한 모듈 import
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.document_loaders import PyMuPDFLoader
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_teddynote.messages import AgentStreamParser

########## 1. 도구를 정의합니다 ##########

### 1-1. Search 도구 ###
# TavilySearchResults 클래스의 인스턴스를 생성합니다
# k=6은 검색 결과를 6개까지 가져오겠다는 의미입니다
search = TavilySearchResults(k=6)

### 1-2. PDF 문서 검색 도구 (Retriever) ###
# PDF 파일 로드. 파일의 경로 입력
loader = PyMuPDFLoader("data/SPRI_AI_Brief_2023년12월호_F.pdf")

# 텍스트 분할기를 사용하여 문서를 분할합니다.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# 문서를 로드하고 분할합니다.
split_docs = loader.load_and_split(text_splitter)

# VectorStore를 생성합니다.
vector = FAISS.from_documents(split_docs, OpenAIEmbeddings())

# Retriever를 생성합니다.
retriever = vector.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    name="pdf_search",  # 도구의 이름을 입력합니다l.
    description="use this tool to search information from the PDF document",  # 도구에 대한 설명을 자세히 기입해야 합니다!!
)

### 1-3. tools 리스트에 도구 목록을 추가합니다 ###
# tools 리스트에 search와 retriever_tool을 추가합니다.
tools = [search, retriever_tool]

########## 2. LLM 을 정의합니다 ##########
# LLM 모델을 생성합니다.
llm = ChatOpenAI(model="gpt-4o", temperature=0)

########## 3. Prompt 를 정의합니다 ##########

# Prompt 를 정의합니다 - 이 부분을 수정할 수 있습니다!
# Prompt 정의
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "Make sure to use the `pdf_search` tool for searching information from the PDF document. "
            "If you can't find the information from the PDF document, use the `search` tool for searching information from the web.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

########## 4. Agent 를 정의합니다 ##########

# 에이전트를 생성합니다.
# llm, tools, prompt를 인자로 사용합니다.
agent = create_tool_calling_agent(llm, tools, prompt)

########## 5. AgentExecutor 를 정의합니다 ##########

# AgentExecutor 클래스를 사용하여 agent와 tools를 설정하고, 상세한 로그를 출력하도록 verbose를 True로 설정합니다.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

########## 6. 채팅 기록을 수행하는 메모리를 추가합니다. ##########

# session_id 를 저장할 딕셔너리 생성
store = {}


# session_id 를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in store:  # session_id 가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_ids] = ChatMessageHistory()
    return store[session_ids]  # 해당 세션 ID에 대한 세션 기록 반환


# 채팅 메시지 기록이 추가된 에이전트를 생성합니다.
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # 대화 session_id
    get_session_history,
    # 프롬프트의 질문이 입력되는 key: "input"
    input_messages_key="input",
    # 프롬프트의 메시지가 입력되는 key: "chat_history"
    history_messages_key="chat_history",
)

########## 7. Agent 파서를 정의합니다. ##########
agent_stream_parser = AgentStreamParser()

########## 8. 에이전트를 실행하고 결과를 확인합니다. ##########

# 질의에 대한 답변을 출력합니다.
response = agent_with_chat_history.stream(
    {
        "input": "2024년 프로야구 플레이오프 진출 5개팀을 검색해서 알려주세요. 한글로 답변하세요"
    },
    # 세션 ID를 설정합니다.
    # 여기서는 간단한 메모리 내 ChatMessageHistory를 사용하기 때문에 실제로 사용되지 않습니다
    config={"configurable": {"session_id": "abc456"}},
)

for step in response:
    agent_stream_parser.process_agent_steps(step)
```

02. CSV, EXCEL 파일을 분석하는 데이터분석 Agent 

03. (업무자동화) FileManagementToolkits 를 활용한 파일관리 Agent 

05. [프로젝트] CSV 파일 기반 데이터분석 Agent
