from langchain.chat_models import ChatOpenAI
from langchain_common.constant import CHATBOT_ROLE, CHATBOT_MESSAGE
from langchain_common.prompt import create_message
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from streamlit.components.v1 import html

import streamlit as st

# .env 파일 로드
from dotenv import load_dotenv

load_dotenv()

# Tavily 검색 초기화
search = TavilySearchResults(k=5)

st.markdown(
    """
    <style>
        body {
            background-color: #B2F2BB;  /* 원하는 배경색으로 수정 */
            margin: 0;
            padding: 0;
        }
        .streamlit-expanderHeader {
            background-color: #B2F2BB;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# 세션 상태에 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []


# 제목 스타일
st.title("Personal Debtor Protection Act Chat Bot")
st.markdown(
    """
    <style>
        .title {
            font-size: 2rem;
            color: #0072B2;
            text-align: center;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# 사이드바 추가
with st.sidebar:
    st.header("Settings")
    st.write("이곳에서 챗봇 설정을 조정할 수 있습니다.")
    st.selectbox("모델 선택", ["GPT-3.5", "GPT-4o-mini"])

# 채팅 상자 스타일
st.markdown(
    """
    <style>
        .user-message {
            background-color: #D6EAF8;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        .assistant-message {
            background-color: #FAD7A0;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# # 메시지 출력
# for message in st.session_state.messages:
#     if message[CHATBOT_MESSAGE.role.name] == "user":
#         with st.chat_message("user"):
#             st.markdown(f'<div class="user-message">{message[CHATBOT_MESSAGE.content.name]}</div>', unsafe_allow_html=True)
#     elif message[CHATBOT_MESSAGE.role.name] == "assistant":
#         with st.chat_message("assistant"):
#             st.markdown(f'<div class="assistant-message">{message[CHATBOT_MESSAGE.content.name]}</div>', unsafe_allow_html=True)


# 화면에 저장된 메시지 표시
for message in st.session_state.messages:
    if message[CHATBOT_MESSAGE.role.name] in CHATBOT_ROLE.__members__:
        with st.chat_message(message[CHATBOT_MESSAGE.role.name]):
            st.markdown(message[CHATBOT_MESSAGE.content.name])

# RAG를 위한 PDF 문서 로딩
pdf_loader = PyMuPDFLoader("개인금융채권관리및금융채무자보호.pdf")
documents = pdf_loader.load()

# 문서 분할 및 임베딩
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
docs = text_splitter.split_documents(documents)

# # 첫 번째 분할 내용 확인 (디버깅용)
# st.write("PDF 문서 첫 번째 분할 내용:", docs[2].page_content)  # docs[0]을 통해 첫 번째 문서 조각 확인

# 임베딩 및 벡터 스토어 생성
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)

# LLM 모델 초기화 (ChatOpenAI로 설정)
llm = ChatOpenAI(model="gpt-4o-mini")  # 또는 원하는 모델로 대체

# RAG 체인 생성
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=vector_store.as_retriever(), memory=memory
)

# 사용자 입력 받기
prompt = st.chat_input("메시지 JayGPT")

if prompt:
    user_message = create_message(role=CHATBOT_ROLE.user, prompt=prompt)
    if user_message:
        with st.chat_message(CHATBOT_ROLE.user.name):
            st.write(prompt)
        st.session_state.messages.append(user_message)

        # 실시간 질문인지 여부 확인
        if any(keyword in prompt.lower() for keyword in ["최근", "최신", "요즘"]):
            search_results = search.invoke(prompt)

            # 실시간 검색 결과가 없을 경우 PDF에서 검색
            if not search_results:  # 실시간 검색 결과가 없을 경우
                rag_response = rag_chain(
                    {"question": prompt, "chat_history": st.session_state.messages}
                )
                assistant_response = rag_response["answer"]
            else:
                # 실시간 검색 결과가 있는 경우
                assistant_result = "### 검색 결과:\n\n"
                for result in search_results:
                    content = result.get("content", "내용 없음")
                    url = result.get("url", "#")
                    assistant_result += f"**내용**: {content}\n\n"
                    assistant_result += f"**링크**: [{url}]({url})\n\n---\n\n"
                assistant_response = assistant_result

            # 결과 출력
            with st.chat_message(CHATBOT_ROLE.assistant.name):
                st.markdown(assistant_response)
            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response)
            )

        else:
            # 실시간 검색이 아닌 경우 RAG 체인을 사용하여 PDF 내용에서 답변 생성
            rag_response = rag_chain(
                {"question": prompt, "chat_history": st.session_state.messages}
            )
            assistant_response = rag_response["answer"]

            with st.chat_message(CHATBOT_ROLE.assistant.name):
                st.write(assistant_response)

            st.session_state.messages.append(
                create_message(role=CHATBOT_ROLE.assistant, prompt=assistant_response)
            )
