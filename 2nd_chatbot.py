from dotenv import load_dotenv

# .env 파일에 등록된 변수(데이터)를 os 환경변수에 적용
load_dotenv()

from langchain_common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from langchain_common.prompt import create_message
from langchain_common.chain import get_message_of_llm
from langchain_community.tools.tavily_search import TavilySearchResults

# web ui/ux
import streamlit as st

st.title("Chat Bot")


search = TavilySearchResults(k=5)


if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메세지를 화면에 표현
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

# 사용자 입력
prompt = st.chat_input("입력해주세요")
# 사용자 입력이 있다면,
if prompt:
    user_message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)

    # 입력값이 존재한다면,
    if user_message:
        # 화면에 표현
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # 검색 결과 가져오기
        search_results = search.invoke(prompt)

        # 검색 결과가 리스트인지 확인
        if isinstance(search_results, list):
            # 검색 결과 포맷팅 및 출력
            search_results_text = "\n".join(
                [
                    f"{result.get('content')}: {result.get('url')} \n"
                    for result in search_results
                ]
            )
            assistant_result = f"{search_results_text}\n"
        else:
            # 검색 결과가 예상한 형식이 아닐 경우 오류 메시지 설정
            assistant_result = "ERR"

        if assistant_result == "ERR":
            # 챗봇 답변
            with st.chat_message(CHATBOT_ROLE.assistant.name):
                assistant_response = st.write_stream(get_message_of_llm(prompt))
                # 이력 추가
                st.session_state.messages.append(
                    create_message(
                        role=CHATBOT_ROLE.assistant, prompt=assistant_response
                    )
                )
        else:
            with st.chat_message(CHATBOT_ROLE.assistant.name):
                assistant_result
                # 이력 추가
                st.session_state.messages.append(
                    create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_result)
                )
