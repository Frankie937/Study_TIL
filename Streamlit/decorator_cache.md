#### @st.cache_resource() 데코레이터의 역할

@st.cache_resource()는 Streamlit에서 리소스를 캐싱하기 위한 데코레이터입니다.
이 기능을 사용하면 데이터베이스 연결, 머신러닝 모델 로드, API 클라이언트 생성 같은 비용이 많이 드는 작업을 캐싱하여
앱이 실행될 때마다 다시 생성하지 않고, 기존에 캐싱된 리소스를 재사용할 수 있습니다.

#### @st.cache_resource()를 사용하는 이유
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

# ✅ 데이터베이스 연결을 캐싱하여 반복적인 재연결을 방지
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
