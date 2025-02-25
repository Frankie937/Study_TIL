#### 1. @st.cache_resource() 데코레이터의 역할

- @st.cache_resource()는 Streamlit에서 리소스를 캐싱하기 위한 데코레이터
- 이 기능을 사용하면 데이터베이스 연결, 머신러닝 모델 로드, API 클라이언트 생성 같은 비용이 많이 드는 작업을 캐싱하여 앱이 실행될 때마다 다시 생성하지 않고, 기존에 캐싱된 리소스를 재사용할 수 있음

#### 2. @st.cache_resource()를 사용하는 이유
1. 성능 향상
무거운 리소스를 한 번만 로드하고, 이후에는 재사용하여 실행 속도를 높일 수 있음.
2. 불필요한 중복 연산 방지
예를 들어, 데이터베이스 연결을 매번 새로 생성하면 비효율적이지만, 한 번 생성한 연결을 재사용하면 비용 절감 가능.
3. 앱 상태 유지
Streamlit은 사용자가 버튼을 클릭하거나 입력할 때마다 새롭게 실행되지만,
@st.cache_resource()를 사용하면 해당 리소스는 앱이 다시 실행되어도 초기화되지 않고 유지됨.


##### 예제 코드 1: 데이터베이스 연결 캐싱
```python
import streamlit as st
import sqlite3

#  데이터베이스 연결을 캐싱하여 반복적인 재연결을 방지
@st.cache_resource()
def get_database_connection():
    conn = sqlite3.connect("example.db")  # SQLite 데이터베이스 연결
    return conn

st.title("Streamlit Cache Resource Example")

# 캐싱된 데이터베이스 연결 사용
conn = get_database_connection()
cursor = conn.cursor()

# 테이블 생성 (없다면)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
""")
conn.commit()

# 데이터 입력 폼
name = st.text_input("Enter your name:")
if st.button("Add User"):
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    st.success(f"User {name} added!")

# 사용자 목록 출력
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
st.write("### User List:")
for user in users:
    st.write(f"- {user[1]}")
```

-> @st.cache_resource()가 적용된 get_database_connection() 함수는 한 번만 실행되며, 이후에는 캐싱된 데이터베이스 연결 객체를 반환함
-> 사용자가 이름을 입력하고 "Add User" 버튼을 클릭해도 데이터베이스 연결이 새로 생성되지 않고 기존 연결을 재사용함


#### 예제 코드 2: 머신러닝 모델 로드 캐싱
(아래 코드는 무거운 머신러닝 모델을 한 번만 로드하고, 이후에는 캐싱된 모델을 재사용하는 예제)

```python
import streamlit as st
from transformers import pipeline

# 무거운 모델 로드를 캐싱하여 반복적인 로딩을 방지
@st.cache_resource()
def load_sentiment_model():
    return pipeline("sentiment-analysis")

st.title("Sentiment Analysis with Cached Model")

# 캐싱된 모델 가져오기
model = load_sentiment_model()

# 입력 텍스트
user_input = st.text_area("Enter a sentence to analyze:")

# 감정 분석 실행
if st.button("Analyze Sentiment"):
    result = model(user_input)
    st.write("### Result:")
    st.json(result)
```

-> @st.cache_resource()를 사용하여 load_sentiment_model()에서 Hugging Face의 pipeline("sentiment-analysis") 모델을 캐싱
-> 모델을 한 번 로드한 후에는 캐싱된 모델을 그대로 재사용하여 성능을 최적화
-> 사용자가 새로운 문장을 입력하고 "Analyze Sentiment" 버튼을 눌러도 모델을 다시 로드하지 않고 기존 모델을 사용함 

#### 예제 코드 3: 캐싱을 무효화(초기화)하는 방법 
```python
# 1) 수동으로 초기화하는 방법
import streamlit as st
import os

if st.button("Clear Cache"):
    st.cache_resource.clear()  # 캐싱된 리소스 초기화
    st.write("Cache Cleared!")

# 2) hash_funcs를 활용한 조건부 캐싱 무효화
os.environ["CACHE_VERSION"] = "1"  # 캐시 버전 관리

@st.cache_resource(hash_funcs={str: lambda _: os.environ["CACHE_VERSION"]})
def expensive_resource():
    return "Heavy Computation Result"

st.write(expensive_resource())

#  캐시 버전 변경 버튼
if st.button("Invalidate Cache"):
    os.environ["CACHE_VERSION"] = str(int(os.environ["CACHE_VERSION"]) + 1)
    st.experimental_rerun()  # 앱 새로고침

# 3) ttl을 활용한 자동 캐싱 만료
import streamlit as st
import time

@st.cache_resource()
def get_cached_time():
    return time.time()

st.write(f"Cached Timestamp: {get_cached_time()}")

# 10초마다 캐시 무효화
if time.time() - get_cached_time() > 10:
    st.cache_resource.clear()
    st.experimental_rerun()

```
-> "Clear Cache" 버튼을 클릭하면 캐시가 초기화됨. 이후 다시 실행하면 리소스를 처음부터 다시 로드함.
-> "Invalidate Cache" 버튼을 누르면 환경 변수를 변경하여 캐시가 무효화됨./ st.experimental_rerun()을 사용해 앱을 새로고침하여 새로운 리소스를 로드함.
-> Streamlit 자체적으로 @st.cache_resource(ttl=초 단위) 옵션을 지원하지 않지만,시간 기반으로 캐시를 무효화하려면 datetime을 활용하면 됨 (캐싱된 time.time() 값을 유지하다가 10초가 지나면 자동으로 캐시를 무효화하고 새 값을 로드함.)



### 3. @st.cache() vs @st.cache_resource() 차이점
- @st.cache()는 '함수의 반환값(데이터)'을 캐싱하고, @st.cache_resource()는 '리소스(객체) 자체'를 캐싱한다. 
- @st.cache()는 주로 간단하게 데이터프레임, 계산 결과를 캐싱할 때 사용하고, @st.cache_resource()는 데이터베이스 연결, 머신러닝 모델, API 클라이언트와 같은 무거운 리소스를 캐싱하는 데 유용함.
- @st.cache_resource()는 앱이 새로 실행되더라도 리소스를 다시 생성하지 않고 재사용할 수 있어 성능이 향상됨. 기존 @st.cache()와 다르게 객체(리소스) 자체를 캐싱하는 용도로 사용됨.
```python

import streamlit as st
from transformers import pipeline

# 무거운 모델 로드 캐싱
@st.cache_resource()
def load_model():
    return pipeline("sentiment-analysis")

model = load_model()

# 모델 예측 결과 캐싱
@st.cache()
def predict_sentiment(text):
    return model(text)

text = st.text_area("Enter text:")
if st.button("Analyze"):
    st.write(predict_sentiment(text))

```
