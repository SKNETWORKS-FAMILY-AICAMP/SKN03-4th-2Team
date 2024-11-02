import os
import openai
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv
import pickle
from typing import Optional, TypedDict, List
from langgraph.graph import StateGraph, START, END

# 환경 변수 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 파일 경로 설정
file_path = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/tcc_ceds_music.csv"
embedding_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/embeddings.npy"
faiss_index_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/faiss_index.pkl"

# 상태 타입 정의
class State(TypedDict):
    query: Optional[str]
    similar_texts: Optional[List[str]]
    answer: Optional[str]
    index: Optional[faiss.IndexFlatL2]

# 데이터 로드 및 임베딩 모델 초기화
data = pd.read_csv(file_path)
data['combined_text'] = data.apply(lambda row: f"Artist: {row['artist_name']}, Track: {row['track_name']}, Genre: {row['genre']}, Lyrics: {row['lyrics']}", axis=1)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 임베딩 생성 노드
def create_embeddings(state: State) -> State:
    if os.path.exists(embedding_file):
        embeddings = np.load(embedding_file)
    else:
        embeddings = embedding_model.encode(data['combined_text'].tolist())
        np.save(embedding_file, embeddings)

    dimension = embeddings.shape[1]
    if os.path.exists(faiss_index_file):
        with open(faiss_index_file, "rb") as f:
            index = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        with open(faiss_index_file, "wb") as f:
            pickle.dump(index, f)

    state["index"] = index
    return state

# 유사 문서 검색 노드
def search_similar_documents(state: State) -> State:
    query = state["query"]
    query_embedding = embedding_model.encode([query])
    index = state["index"]
    distances, indices = index.search(np.array(query_embedding), k=3)
    results = data.iloc[indices[0]]
    state["similar_texts"] = results['combined_text'].tolist()
    return state

# 답변 생성 노드
def generate_answer(state: State) -> State:
    query = state["query"]
    similar_texts = state["similar_texts"]
    context = "\n".join(similar_texts)
    prompt = f"Here is some information about music:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in answering questions based on provided music data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    
    state["answer"] = response.choices[0].message.content.strip()
    print(state, "확인하기")
    return state

# 그래프 생성 및 노드 추가
graph = StateGraph(State)

graph.add_node("create_embeddings", create_embeddings)
graph.add_node("search_similar_documents", search_similar_documents)
graph.add_node("generate_answer", generate_answer)

# 노드 연결
graph.add_edge(START, "create_embeddings")
graph.add_edge("create_embeddings", "search_similar_documents")
graph.add_edge("search_similar_documents", "generate_answer")
graph.add_edge("generate_answer", END)

# 그래프 컴파일
compiled_graph = graph.compile()

# 그래프 실행 예제
final_result = None  # 마지막 결과를 저장할 변수

# stream() 메서드를 사용하여 그래프를 실행하고 마지막 결과만 저장
for result in compiled_graph.stream(
    {"query": "What are some popular romantic songs from the 1950s?"}
):
    final_result = result  # 루프를 통해 최종 결과를 갱신

# 마지막 결과에서 "answer"만 출력
if final_result:
    print(final_result.get("answer", "No answer generated"))
