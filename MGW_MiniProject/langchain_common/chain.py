import time
import streamlit as st
from .prompt import create_prompt
from .model import create_llm


@st.cache_resource
def create_chain(user_input: str):  # user_input을 인자로 받도록 수정
    return create_prompt(user_input) | create_llm()


def get_message_of_llm(user_input: str):
    try:
        for chunk in create_chain(user_input).stream({"user_input": user_input}):
            if chunk.content is not None:
                yield chunk.content
                time.sleep(0.08)
    except Exception as e:
        st.error(f"LLM 호출 중 오류 발생: {e}")  # 오류 메시지 표시
