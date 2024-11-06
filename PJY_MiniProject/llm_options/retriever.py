from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.tools.retriever import create_retriever_tool

def get_retriever_tool():
    file_path = "C:\dev\github\SKN03-4th-2Team\SKN03-4th-2Team\PJY_MiniProject\data\다이어트.txt"
    # 파일의 경로 입력
    loader = TextLoader(file_path, encoding='utf-8')
    # 텍스트 분할기를 사용하여 문서를 분할합니다.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # 문서를 로드하고 분할합니다.
    split_docs = loader.load_and_split(text_splitter)

    # VectorStore를 생성, 임베딩
    vector = FAISS.from_documents(split_docs, OpenAIEmbeddings())

    # Retriever를 생성합니다.
    retriever = vector.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        name="txt_search",
        description="다이어트 관련 질문은 이 유능한 다이어트 챗봇에 부탁드릴게요",
    )
    return retriever_tool