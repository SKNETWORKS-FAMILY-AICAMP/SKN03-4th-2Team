import os 
import streamlit as st
from common.message import create_message
from common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from dotenv import load_dotenv

load_dotenv()

st.title("다이어트 Chat Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현 
for message in st.session_state.messages:
    try:
        if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
            with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
                st.markdown(message[CHATBOT_MESSAGE.content.name])
    except KeyError as e:
        st.error(f"메시지 처리 중 오류 발생: {e}")

# ... (기존 코드 유지)

# 사용자 입력
prompt = st.chat_input("입력해주세요")
if prompt:
    message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    
    if message:
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)

        # 챗봇 답변 
        assistant_response = response_from_llm(prompt=prompt, message_history=st.session_state.messages)
        
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            st.write(assistant_response)  # assistant_response가 문자열임을 가정

        # 이력 추가 
        st.session_state.messages.append(
            create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response)
        )