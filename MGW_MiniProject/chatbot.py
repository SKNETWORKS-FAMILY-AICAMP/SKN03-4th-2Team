from dotenv import load_dotenv

# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

from langchain_common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from langchain_common.prompt import create_message, create_prompt
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict

from langchain.tools import tool
from langchain.agents import create_tool_calling_agent
from langchain_openai import ChatOpenAI  # LLM을 가져옵니다.

# web ui/ux
import streamlit as st

st.title("Chat Bot")


# 도구 생성
@tool
def search_movies(query: str) -> List[Dict[str, str]]:
    """Search Movies by input keyword"""
    movies_tool = TavilySearchResults(
        max_results=6,
        include_answer=True,
        include_raw_content=True,
        include_domains=["google.com", "naver.com"],
    )
    return movies_tool.invoke({"query": query})


# 사용자 입력에 기반한 프롬프트 생성
def get_prompt(user_input: str):
    return create_prompt(user_input)


# LLM 인스턴스 생성 (OpenAI API 키가 필요합니다)
llm = ChatOpenAI(temperature=0.7)


if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

# 사용자 입력
prompt = st.chat_input("입력해주세요")

# 에이전트 생성
agent = create_tool_calling_agent(llm=llm, tools=search_movies, prompt=prompt)
# 사용자 입력이 있다면,
if prompt:
    user_message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)

    if user_message:
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # 프롬프트 생성
        agent_prompt = create_prompt(prompt, agent_scratchpad="")

        # 에이전트 생성
        agent = create_tool_calling_agent(
            llm=llm, tools=search_movies, prompt=agent_prompt
        )

        # 에이전트를 사용하여 응답을 얻음
        assistant_response = agent.invoke({"input": prompt, "agent_scratchpad": ""})

        # 챗봇 답변을 화면에 표시
        with st.chat_message(CHATBOT_ROLE.assistant.name):
            st.write(assistant_response)
            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response)
            )

        # 필요에 따라 검색 결과를 추가로 가져오는 기능을 포함할 수 있습니다.
        # 예:
        # search_results = search_movies(prompt)
        # 이 부분은 조건에 따라 추가로 구현할 수 있습니다.
