from langchain.agents import create_openai_functions_agent
from typing import Union
from langgraph.prebuilt.tool_executor import ToolExecutor
from .agentstate import AgentState
from langgraph.graph import START, END, StateGraph
# 상태 타입 정의
# 기본 메시지 설정 노드
def initialize_message_history(state: AgentState) -> AgentState:
    if not state["chat_history"]:
        state["chat_history"].append(
            {
                "role": "assistant",
                "content": "You are a helpful assistant. You must answer in Korean."
            }
        )
    return state

def make_prompt(context: str, query: str) -> str:
    # 다이어트에 관한 정보와 질문을 사용하여 프롬프트를 생성합니다.
    prompt = f"다이어트에 관한 정보:\n{context}\n\n질문: {query}\n답변:"
    return prompt

# 사용자 입력 추가 노드
def add_user_input(state: AgentState) -> AgentState:
    state["chat_history"].append(
        {
            "role": "user",
            "content": state["input"]
        }
    )
    return state

# 에이전트 실행 노드
def run_agent(state: AgentState) -> AgentState:
    # 프롬프트를 생성하기 위해 context를 설정
    context = "다이어트에 관한 일반적인 정보입니다."  # 필요한 경우 업데이트
    prompt = make_prompt(context, state["input"])
    
    agent_runnable = create_openai_functions_agent(None, [], prompt)
    
    # 입력 데이터 구성
    inputs = {
        "input": state["input"],
        "chat_history": state["chat_history"],
        "intermediate_steps": state["intermediate_steps"]
    }
    
    # 에이전트 실행
    state["agent_outcome"] = agent_runnable.invoke(inputs)
    return state

# 도구 실행 노드 (필요할 경우)
def execute_tools(state: AgentState) -> AgentState:
    tool_executor = ToolExecutor([])  # 필요한 도구 목록 추가
    output = tool_executor.invoke(state["agent_outcome"])
    
    state["agent_outcome"]["output"] = output  # 결과 저장
    return state

# 그래프 생성 및 노드 추가
graph = StateGraph(AgentState)

graph.add_node("initialize_message_history", initialize_message_history)
graph.add_node("add_user_input", add_user_input)
graph.add_node("run_agent", run_agent)
graph.add_node("execute_tools", execute_tools)

# 노드 연결
graph.add_edge(START, "initialize_message_history")
graph.add_edge("initialize_message_history", "add_user_input")
graph.add_edge("add_user_input", "run_agent")
graph.add_edge("run_agent", "execute_tools")
graph.add_edge("execute_tools", END)

# 그래프 컴파일
compiled_graph = graph.compile()

# 그래프 실행 예제
def response_from_llm(user_input: str) -> Union[dict, str]:
    initial_state = {
        "input": user_input,
        "chat_history": [],
        "agent_outcome": None,
        "intermediate_steps": []  # 초기 중간 단계 설정
    }
    
    final_result = None
    
    # stream() 메서드를 사용하여 그래프를 실행하고 마지막 결과만 저장
    for result in compiled_graph.stream(initial_state):
        final_result = result  # 루프를 통해 최종 결과를 갱신
    
    return final_result.get("agent_outcome", "No response generated")

# 사용 예
response = response_from_llm("여기에 사용자 입력을 넣으세요.")
print(response)
