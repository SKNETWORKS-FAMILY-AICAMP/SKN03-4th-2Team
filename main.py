import os
from dotenv import load_dotenv
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langagent.workflow import workflow  # 컴파일할 워크플로우

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정 확인
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 추가하세요.")

# Streamlit UI 설정
st.title("지하철역 경로 서비스🚇")

# 메모리 초기화 (MemorySaver)
if "checkpointer" not in st.session_state:
    st.session_state.checkpointer = MemorySaver()

# 워크플로우 컴파일
if "app" not in st.session_state:
    st.session_state.app = workflow.compile(checkpointer=st.session_state.checkpointer)

# 세션 상태 초기화 (메시지 기록)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 메시지를 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 사용자 입력 처리
user_input = st.chat_input("출발역과 도착지역을 입력해주세요")
if user_input:
    # 사용자 메시지 생성 및 세션 상태에 추가
    user_message = {"role": "user", "content": user_input}
    st.session_state.messages.append(user_message)

    # 사용자 입력 표시
    with st.chat_message("user"):
        st.write(user_input)

    # LangGraph와 MemorySaver를 사용해 AI 응답 생성
    try:
        # 워크플로우를 사용해 상태 기반 응답 생성
        state = st.session_state.app.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config={"configurable": {"thread_id": 42}}
        )
        assistant_response = state["messages"][-1].content if state else "응답을 생성하지 못했습니다."
    except Exception as e:
        assistant_response = f"응답 생성 중 오류 발생: {e}"

    # AI 응답 표시
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # AI 응답을 세션 상태에 추가
    assistant_message = {"role": "assistant", "content": assistant_response}
    st.session_state.messages.append(assistant_message)
