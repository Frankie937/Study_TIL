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

