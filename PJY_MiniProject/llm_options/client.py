from langchain_openai import ChatOpenAI
import streamlit as st
from .model_parameter import langchain_param

@st.cache_resource
def get_client(model_id: str = "gpt-4o-mini"):
    try:
        return ChatOpenAI(model=model_id, **langchain_param())
    except Exception as e:
        st.error(f"ChatOpenAI를 불러오지 못했습니다.: {e}")
        return None
