from langgraph.checkpoint.memory import MemorySaver
from langagent.workflow import workflow  # workflow.py에서 import
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage

# 메모리 초기화
checkpointer = MemorySaver()

# 워크플로우 컴파일
app = workflow.compile(checkpointer=checkpointer)

# 메세지 실행 함수
def run_agent(user_message: str):
    state = app.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config={"configurable": {"thread_id": 42}}
    )
    return state["messages"][-1].content

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        response = run_agent(user_input)
        print("Agent:", response)

