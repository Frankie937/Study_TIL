* 공부하다가 create_react_agent와 create_tool_calling_agent의 차이가 무엇일지 궁금해서 찾아봄
(원문: https://forum.langchain.com/t/create-react-agent-vs-create-tool-calling-agent/1014)


두 에이전트 모두 동일한 모델을 사용하기 때문에 기본 추론 기능은 동일하지만, 가시성과 제어 측면에서 차이가 있음 
- create_react_agent액션/사고/관찰 루프를 통해 추론을 외부화하여 각 단계를 확인하고, 디버깅하고, 심지어 프로세스 중간에 개입할 수 있도록 지원하므로, 투명성 확보나 경로 수정에 대한 세밀한 제어가 필요할 때 특히 유용함
- create_tool_calling_agent 동일한 모델 기능을 통해 내부적으로 추론을 수행하지만, 추론을 직접 검사하거나 변경할 수 없으므로 간단한 도구 오케스트레이션에서는 더 빠르고 깔끔하지만, 잘못된 단계로 진행될 경우 디버깅하기가 더 어려움.

즉, 에이전트가 경로를 수정해야 하는 상황에서는, create_react_agent 어디에서 문제가 발생하는지 정확히 파악하고 잠재적으로 올바른 길로 안내할 수 있으므로 이 방법이 더 좋음
