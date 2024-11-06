import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# 파일 경로 설정
text_file = r"C:\dev\github\SKN03-4th-2Team\SKN03-4th-2Team\PJY_MiniProject\data\다이어트.txt"
embedding_file = r'C:\dev\github\SKN03-4th-2Team\SKN03-4th-2Team\PJY_MiniProject\data\embeddings.npy'
faiss_index_file = r'C:\dev\github\SKN03-4th-2Team\SKN03-4th-2Team\PJY_MiniProject\data\faiss_index.index'

# 임베딩 모델 초기화
embedding_model = SentenceTransformer('all-MiniLM-L12-v2')

# 텍스트 파일에서 문장 읽기
if os.path.exists(text_file):
    with open(text_file, 'r', encoding='utf-8') as f:
        sentences = f.readlines()
    # 각 문장에서 개행 문자 제거
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
else:
    raise FileNotFoundError(f"텍스트 파일 '{text_file}'이 존재하지 않습니다.")

# 임베딩 파일이 존재하는지 확인
if os.path.exists(embedding_file):
    # 파일이 존재하면 로드
    embeddings_array = np.load(embedding_file)
    print("기존 임베딩 파일 로드 완료:")
else:
    # 파일이 존재하지 않으면 임베딩 생성
    embeddings_array = embedding_model.encode(sentences)
    # 생성된 임베딩을 파일로 저장
    np.save(embedding_file, embeddings_array)
    print("새로운 임베딩 파일 생성 및 저장 완료:")

# FAISS 인덱스 생성 및 저장
dimension = embeddings_array.shape[1]
if not os.path.exists(faiss_index_file):
    index = faiss.IndexFlatL2(dimension)  # L2 거리 기반 인덱스
    index.add(embeddings_array)  # 임베딩 추가
    faiss.write_index(index, faiss_index_file)  # FAISS 인덱스를 파일로 저장
    print("FAISS index 저장")
else:
    index = faiss.read_index(faiss_index_file)  # FAISS 인덱스 파일 로드
    print("FAISS index 로드")

# 검색 함수 정의
def search_similar_diet_methods(query, top_k=3):
    # 쿼리를 임베딩으로 변환
    query_embedding = embedding_model.encode([query])

    # FAISS 인덱스를 통해 유사한 방법 검색
    distances, indices = index.search(np.array(query_embedding), top_k)

    # 결과를 가져옵니다.
    results = [sentences[i] for i in indices[0]]  # sentences 사용
    return results

# 예시
query = "체중 감량을 위한 방법이 뭐야?"
similar_methods = search_similar_diet_methods(query)
print(similar_methods)
