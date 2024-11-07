import os
import streamlit as st
from common.message import create_message
from common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from dotenv import load_dotenv
from llm_options.response_handler import response_from_llm
import json

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="다이어트 Chat Bot", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        body {
            background-color: #F3F9F6; /* 밝은 민트색 배경 */
            color: #2D3E3A; /* 어두운 민트 계열 텍스트 색상 */
            font-family: 'Arial', sans-serif;
        }
        .stTextInput>div>input {
            background-color: #E8F6F3; /* 연한 민트색 입력 필드 배경 */
            color: #2D3E3A; /* 어두운 텍스트 색상 */
            border-radius: 20px;
            padding: 12px;
            border: 1px solid #A5D6D0; /* 부드러운 테두리 */
        }
        .stButton>button {
            background-color: #81C784; /* 상쾌한 녹색 버튼 */
            color: white;
            border-radius: 25px;
            padding: 12px 20px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #66BB6A; /* 버튼 호버 시 어두운 녹색 */
        }
        .stChatMessage .assistant {
            background-color: #E8F6F3; /* 연한 민트색 챗봇 메시지 */
            padding: 12px;
            border-radius: 20px;
            color: #2D3E3A; /* 어두운 텍스트 색상 */
        }
        .stChatMessage .user {
            background-color: #FFE082; /* 부드러운 노란색 사용자 메시지 */
            padding: 12px;
            border-radius: 20px;
            color: #2D3E3A; /* 어두운 텍스트 색상 */
        }
        .stChatMessage {
            font-size: 16px; /* 글씨 크기 조정 */
        }
        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; }
            100% { opacity: 0.7; }
        }
    </style>
""", unsafe_allow_html=True)

# 앱 제목
st.markdown("# **다이어트 Chat Bot**", unsafe_allow_html=True)
st.markdown("### 다이어트 관련 질문을 입력해주세요! 😃", unsafe_allow_html=True)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 화면에 표시
for message in st.session_state.messages:
    try:
        if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
            with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
                st.markdown(message[CHATBOT_MESSAGE.content.name])
    except KeyError as e:
        st.error(f"메시지 처리 중 오류 발생: {e}")

# 입력 받기
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("**사용자 입력**")
    prompt = st.text_input("질문을 입력하세요")

with col2:
    st.markdown("**답변**")
    if prompt:
        with st.spinner('챗봇이 답변을 준비하고 있습니다...'):
            # 사용자 메시지 저장
            message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
            if message:
                with st.chat_message(CHATBOT_ROLE.user.name):
                    st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)

            # 챗봇 답변
            assistant_response = response_from_llm(prompt=prompt, message_history=st.session_state.messages)

            # 답변 메시지 표시
            with st.chat_message(CHATBOT_ROLE.assistant.name):
                st.markdown(f'<div class="assistant animate">{assistant_response}</div>', unsafe_allow_html=True)

            # 이력에 추가
            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response)
            )