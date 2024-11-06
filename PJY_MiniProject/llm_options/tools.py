from langchain_community.tools.tavily_search import TavilySearchResults
from .retriever import get_retriever_tool
# TavilySearchResults 클래스의 인스턴스를 생성합니다
# k=5은 검색 결과를 5개까지 가져오겠다는 의미입니다
from dotenv import load_dotenv

load_dotenv("C:\\dev\\github\\SKN03-4th-2Team\\SKN03-4th-2Team\\PJY_MiniProject\\.env")

search = TavilySearchResults(
    max_results=6,
    include_answer=True,
    include_raw_content=True,
    include_domains=["github.io", "wikidocs.net"],
)

def get_tools():
    return [search, get_retriever_tool()]