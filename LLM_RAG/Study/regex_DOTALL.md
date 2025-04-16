### re.DOTALL의 역할 
- re.search(pattern, string, re.DOTALL) 이렇게 쓰면, .이 줄바꿈도 포함해서 문서 전체를 하나의 덩어리로 탐색하게 된다. 


### re.DOTALL을 사용하는 이유 
- string 인자가 여러 줄로 구성돼 있을 수 있기 때문에 줄바꿈을 포함한 매칭이 필요함
- re.DOTALL이 없으면 .이 줄바꿈 앞까지만 매칭되므로 멀티라인 string이 잘리거나 매칭 안 됨.



### 차이 
![image](https://github.com/user-attachments/assets/79ba50c1-d002-489b-bec5-5d072201faaf)
