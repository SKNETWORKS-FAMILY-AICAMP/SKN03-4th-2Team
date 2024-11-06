import faiss
from langchain_community.vectorstores import FAISS
import re
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from .model import create_llm
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict
from langchain.tools import tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List, Dict
from .model import create_llm


SUMMARY_TEMPLATE = """
다음 텍스트를 한 문장으로 간단히 요약해주세요:
{text}
"""

def create_DB():
    """직업 추천 노드"""
    # CSV 파일 읽기
    loader = CSVLoader('data/직업세세분류.CSV', encoding='cp949')
    data = loader.load()
    summary_prompt = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["text"])
    summary_chain = LLMChain(llm=create_llm(), prompt=summary_prompt)
    job_names = []

    # data 리스트 순회
    for item in data:
        # 각 page_content에서 'KNOW직업명: ' 이후의 텍스트 추출
        match = re.search(r'KNOW직업명: (.+)', item.page_content)
        search_results = search_detail(match)
        if match:
            job_names.append(match.group(1))
            job_name = match.group(1)
            
            # 웹 검색 수행 및 요약
            search_results = search_detail(job_name)
            combined_text = " ".join([result.get("content", "") for result in search_results])
            summary = summary_chain.run(text=combined_text)
            
            # 직업명과 요약된 상세 정보를 결합
            enriched_job_info = f"{job_name} - {summary.strip()}"
            job_names.append(enriched_job_info)


    # 임베딩 모델 초기화 (예: OpenAI Embeddings)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # 벡터 DB (예: FAISS) 초기화 및 데이터 추가
    vector_db = FAISS.from_texts(job_names, embeddings)
    # 벡터 DB 저장 (옵션)
    vector_db.save_local('./langchain_common/faiss_index') 

    return vector_db

# 도구 생성

def search_detail(query: str) -> List[Dict[str, str]]:
    """Search News by input keyword"""
    search_detail_tool = TavilySearchResults(
        max_results=6,
        include_answer=True,
        include_raw_content=True,
        # include_images=True,
        # search_depth="advanced", # or "basic"
        include_domains=["google.com", "naver.com"],
        # exclude_domains = []
    )
    return search_detail_tool

