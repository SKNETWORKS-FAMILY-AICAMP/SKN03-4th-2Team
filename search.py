import os
import openai
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv
import pickle

# 환경 변수 로드 및 API 키 설정
load_dotenv()  # .env 파일에서 API 키 로드
openai.api_key = os.getenv("OPENAI_API_KEY")

# 파일 경로 설정
file_path = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/tcc_ceds_music.csv"
embedding_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/embeddings.npy"
faiss_index_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/faiss_index.pkl"

# 데이터 로드
data = pd.read_csv(file_path)

# 텍스트 결합
data['combined_text'] = data.apply(lambda row: f"Artist: {row['artist_name']}, Track: {row['track_name']}, Genre: {row['genre']}, Lyrics: {row['lyrics']}", axis=1)

# 임베딩 모델 초기화
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 임베딩 로드 또는 생성
if os.path.exists(embedding_file):
    embeddings = np.load(embedding_file)
else:
    embeddings = embedding_model.encode(data['combined_text'].tolist())
    np.save(embedding_file, embeddings)

# FAISS 인덱스 로드 또는 생성
dimension = embeddings.shape[1]
if os.path.exists(faiss_index_file):
    with open(faiss_index_file, "rb") as f:
        index = pickle.load(f)
else:
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    with open(faiss_index_file, "wb") as f:
        pickle.dump(index, f)

# 유사한 문서 검색 함수
def search_similar_documents(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = data.iloc[indices[0]]
    return results['combined_text'].tolist()  # 검색된 텍스트를 리스트로 반환

# LLM을 통한 답변 생성 함수 (ChatCompletion 사용)
def generate_answer(query):
    # 1. 유사한 문서 검색
    similar_texts = search_similar_documents(query)
    
    # 2. 프롬프트 생성
    context = "\n".join(similar_texts)
    prompt = f"Here is some information about music:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    # 3. OpenAI ChatCompletion API 호출
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in answering questions based on provided music data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    
    # 4. 생성된 답변 반환
    answer = response.choices[0].message.content.strip()
    return answer

# 예제 질문
question = "What are some popular romantic songs from the 1950s?"
answer = generate_answer(question)
print("Answer:", answer)
