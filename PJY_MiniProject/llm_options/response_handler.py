from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentFinish

from .agentstate_option import AgentState
from langgraph.prebuilt.tool_executor import ToolExecutor
from .model_parameter import langchain_param
from .prompt import get_hub_prompt
from langgraph.graph import START, END, StateGraph
from .tools import search
from .retriever import get_retriever_tool
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_resource
def get_client(model_id: str = "gpt-4o-mini"):
    try:
        client = ChatOpenAI(model=model_id, **langchain_param())
        return client
    except Exception as e:
        st.error(f"ChatOpenAI를 불러오지 못했습니다.: {e}")
        print(f"Error details: {e}")  # 콘솔에서 에러 로그 확인
        return None


# 상태 타입 정의
def initialize_message_history(state: AgentState) -> AgentState:
    """기본 메시지 설정 노드"""
    if not state["chat_history"]:
        state["chat_history"].append(
            {
                "role": "assistant",
                "content": "You are a helpful assistant. You must answer in Korean."
            }
        )
    return state


def add_user_input(state: AgentState) -> AgentState:
    """사용자 입력 추가 노드"""
    state["chat_history"].append(
        {
            "role": "user",
            "content": state["input"]
        }
    )
    return state


def run_agent(state: AgentState) -> AgentState:
    """에이전트 실행 노드"""
    tools = [search, get_retriever_tool()]
    agent_runnable = create_openai_functions_agent(get_client(), tools, get_hub_prompt())
    inputs = {"input": state["input"],
            "chat_history": state["chat_history"],
            "intermediate_steps":state["intermediate_steps"]}
    agent_outcome = agent_runnable.invoke(inputs)
    state["agent_outcome"] = agent_outcome
    return state


def execute_tools(state: AgentState) -> AgentState:
    """도구 실행 노드 (필요할 경우)"""
    agent_action = state['agent_outcome']
    tool = [search, get_retriever_tool()]
    tool_executor = ToolExecutor(tool) 
    output = tool_executor.invoke(agent_action)

    state["intermediate_steps"].append((agent_action, str(output)))
    return state


def should_continue(state: AgentState) -> dict:
    """상태에 따라 흐름을 결정하는 노드"""
    if isinstance(state['agent_outcome'], AgentFinish):
        # "end" 상태를 나타내는 반환값을 상태 객체로 반환
        return "end"
    else:
        # "continue" 상태를 나타내는 반환값을 상태 객체로 반환
        return "continue"


# 그래프 생성 및 노드 추가
graph = StateGraph(AgentState)

graph.add_node("initialize_message_history", initialize_message_history)
graph.add_node("add_user_input", add_user_input)
graph.add_node("run_agent", run_agent)
graph.add_node("execute_tools", execute_tools)
graph.add_node("should_continue", should_continue)
graph.set_entry_point("initialize_message_history")
graph.add_conditional_edges(
    "should_continue",  # 조건을 체크할 노드
    {
        "continue": "execute_tools",  # 'continue' 조건이 True일 때 연결할 노드
        "end": END               # 'end' 조건이 True일 때 연결할 노드
    }
)

# 노드 연결
graph.add_edge("initialize_message_history", "add_user_input")
graph.add_edge("add_user_input", "run_agent")
graph.add_edge("run_agent", "execute_tools")
graph.add_edge("execute_tools", "should_continue")
graph.add_edge("should_continue", "run_agent")
# 그래프 컴파일
compiled_graph = graph.compile()

# 그래프 실행 예제
def response_from_llm(prompt, message_history=[]):
    initial_state = {
        "input": prompt,
        "chat_history": message_history,
    }

    output = compiled_graph.invoke(initial_state)

    agent_outcome = output.get("agent_outcome").return_values['output']

    return agent_outcome


# response = response_from_llm("다이어트 방법좀 알려줘")
# print(response)