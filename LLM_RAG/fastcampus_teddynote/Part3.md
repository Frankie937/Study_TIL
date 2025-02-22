### ch1. 메모리 (Memory)

02. ConversationBufferMemory

사람의 입력과 ai의 답변을 pair하게 만들어서 저장해주는 역할
```python
memory = ConversationBufferMemory()
memory.load_memory_variables({})["history"] # 문자열로 출력

memory = ConversationBufferMemory(return_messages=True)
memory.load_memory_variables({})["history"] # `HumanMessage` 와 `AIMessage` 객체로 반환
```
