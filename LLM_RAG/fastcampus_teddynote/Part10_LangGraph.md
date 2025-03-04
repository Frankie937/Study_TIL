### Ch1. LangGraph 개요

### Ch2. LangGraph 핵심 기능

08-09- 중간 단계의 상태 수동 업데이트 

- tool messages id 중요
- reducer 기능이 있기 때문에 id가 다르면 추가해주지만, id가 같으면 교체시켜줌

(add_message reducer 기능 )

(** 참고: query 부분이 지금 웹 검색에 넣을 검색 내용인데 구글링 문법으로 검색어 + [ site: 사이트주소 ] 로 검색하면 그 웹 사이트 한 정해서 검색해줌! )

![image](https://github.com/user-attachments/assets/81a7ebce-06a5-4f35-afa6-cb5daf3fe7d8)

-> 이 기능의 요지는, 검색할 query를 llm이 만드는데 그 query가 대부분 맘에 안들 때가 있다. 그때 interrupt해서 직접 검색 query를  수정할 수 있는 프로세스를 만들 수 있음

