
(원문- https://devocean.sk.com/blog/techBoardDetail.do?ID=165922&boardType=techBlog, https://tibetsandfox.tistory.com/43)


* Python은 GIL의 때문에 Thread를 사용해서 한순간에 여러 요청을 처리할 수 없습니다. 그러기 때문에 Multiprocessing을 사용해야 합니다.

(** GIL(Global Interpreter Lock) 이란?
GIL은 파이썬에만 존재하는 독특한 개념으로 파이썬에서 멀티스레딩을 할 때 다수의 스레드가 동시에 파이썬 바이트 코드를 실행하지 못하게 막는 일종의 뮤텍스(Mutex)입니다. 파이썬으로 작성된 프로세스는 한 시점에 하나의 스레드에만 모든 자원을 할당하고 다른 스레드는 접근할 수 없게 막아버리는데, 이 역할을 GIL이 수행합니다.
즉, 멀티스레딩을 하더라도 파이썬에선 우리가 생각하는 것처럼 여러 스레드가 동시에 작업을 하진 않습니다.)


* Uvicron 
  - Python으로 돌아가는 프로그램이다.
  - Process를 만들 때 spawn방식을 사용해서 window 에서도 사용할 수 있다.
  - Socket을 공유하는 Process를 통해서 N개의 Request를 동시에 처리할 수 있다.
  - async함수를 사용해야지만 asyncio를 통해서 비동기처리가 가능하다.(sync함수도 가능하지만, blocking이됨)
