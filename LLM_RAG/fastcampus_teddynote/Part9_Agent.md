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
```

```python
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


