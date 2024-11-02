import numpy as np
import pandas as pd
import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer

# 데이터 로드
file_path = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/tcc_ceds_music.csv"
data = pd.read_csv(file_path)

# 텍스트 결합
data['combined_text'] = data.apply(lambda row: f"Artist: {row['artist_name']}, Track: {row['track_name']}, Genre: {row['genre']}, Lyrics: {row['lyrics']}", axis=1)

# 임베딩 모델 초기화
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# 임베딩 파일이 있는지 확인
embedding_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/embeddings.npy"
if not os.path.exists(embedding_file):
    # 임베딩 생성 및 저장
    embeddings = embedding_model.encode(data['combined_text'].tolist())
    np.save(embedding_file, embeddings)
    print("Embeddings saved.")
else:
    # 기존 임베딩 파일 로드
    embeddings = np.load(embedding_file)
    print("Embeddings loaded.")

# FAISS 인덱스 생성 및 저장
dimension = embeddings.shape[1]
faiss_index_file = "C:/Users/owner/Desktop/LLM miniproject/langGraphChatbot/data/faiss_index.pkl"
if not os.path.exists(faiss_index_file):
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    with open(faiss_index_file, "wb") as f:
        pickle.dump(index, f)
    print("FAISS index saved.")
else:
    with open(faiss_index_file, "rb") as f:
        index = pickle.load(f)
    print("FAISS index loaded.")

# 검색 함수 정의
def search_similar_songs(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    results = data.iloc[indices[0]]
    return results[['artist_name', 'track_name', 'genre', 'lyrics']]

# 예시 질문
question = "Tell me about a romantic pop song from the 1950s."
result = search_similar_songs(question)
print(result)
