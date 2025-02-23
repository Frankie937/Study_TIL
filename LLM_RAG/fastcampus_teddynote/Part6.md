### Ch1. 사전에 정의된 체인(Chain)

06. SQL 쿼리 생성기

```python
# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

# LangSmith 추적을 설정합니다. https://smith.langchain.com
# !pip install langchain-teddynote
from langchain_teddynote import logging

# 프로젝트 이름을 입력합니다.
logging.langsmith("SQL")

from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# SQLite 데이터베이스에 연결합니다.
db = SQLDatabase.from_uri("sqlite:///data/finance.db")

# model 은 gpt-3.5-turbo 를 지정
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 도구
execute_query = QuerySQLDataBaseTool(db=db)

# SQL 쿼리 생성 체인
write_query = create_sql_query_chain(llm, db)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()

# 생성한 쿼리를 실행하고 결과를 출력하기 위한 체인을 생성합니다.
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)
```

- Agent 방식

```python
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

# model 은 gpt-3.5-turbo 를 지정
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# SQLite 데이터베이스에 연결합니다.
db = SQLDatabase.from_uri("sqlite:///data/finance.db")

# Agent 생성
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True) 

# 실행 결과 확인
agent_executor.invoke(
    {"input": "테디와 셜리의 transaction 의 합계를 구하고 비교하세요"}
)
```
