import time
import streamlit as st
import faiss
from .prompt import create_prompt
from .model import create_llm
from .embedding import create_DB

# 체인 생성 = 프롬프트 + 모델
@st.cache_resource
def create_chain():
    return create_prompt() | create_llm() 

def get_message_of_llm(user_input:str):
    for chunk in create_chain().stream({"user_input": user_input}):
        if chunk.content is not None:
            yield chunk.content
            time.sleep(0.05)


def recommend_jobs(user_input:str) -> str:
    """Use the model and vector database to recommend jobs."""
    vector_db = create_DB()
    results = vector_db.similarity_search(user_input, k=3)

    job_names = [result['page_content'] for result in results]

    response = create_llm().invoke(new_prompt)

    response = create_llm().invoke(f"다음 사용자 정보에 기반하여 추천할 직업:\n{user_input}\n추천 직업:\n{', '.join(job_names)}")
    
    return response.content


