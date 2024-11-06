from dotenv import load_dotenv
import streamlit as st
from langchain_common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from langchain_common.prompt import create_message
from langchain_common.chain import get_message_of_llm

load_dotenv()

st.set_page_config(
    page_title="AI 진로 상담사",
    page_icon="🎯",
    layout="wide"
)

if st.button("대화 초기화"):
    st.session_state.messages = []
    st.session_state.responses = {
        "interest": "",
        "strengths": "",
        "subjects": ""
    }
    st.session_state.current_question_index = 0
    st.rerun()

# Initialize state variables if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []
if "responses" not in st.session_state:
    st.session_state.responses = {
        "interest": "",
        "strengths": "",
        "subjects": ""
    }
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Predefined questions
questions = [
    "너의 관심 분야가 뭐야?",
    "강점과 약점은 뭐야?",
    "좋아하는 과목은 뭐야?"
]

# Display past messages and questions
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

# Ask the current question

if st.session_state.current_question_index < len(questions):
    current_question = questions[st.session_state.current_question_index]
    with st.chat_message(CHATBOT_ROLE.assistant.name):
        st.write(current_question)

# User input handling
prompt = st.chat_input(" 입력해주세요  ")
if prompt:
    user_message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    if user_message:
        # Display user input
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # Save user response under the correct key
        if st.session_state.current_question_index == 0:
            st.session_state.responses["interest"] = prompt
        elif st.session_state.current_question_index == 1:
            st.session_state.responses["strengths"] = prompt
        elif st.session_state.current_question_index == 2:
            st.session_state.responses["subjects"] = prompt

        # Move to the next question
        st.session_state.current_question_index += 1
        st.rerun()

        # 입력값이 존재한다며, 
    if st.session_state.current_question_index == 3:
        # 화면에 표현
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # 챗봇 답변 
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            assistant_response = st.write_stream(get_message_of_llm(st.session_state.messages))
            # 이력 추가 
            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response))

