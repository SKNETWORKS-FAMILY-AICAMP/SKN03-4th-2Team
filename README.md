# 내부 문서 (음악 데이터) 기반 질의 응답 시스템 구현 

데이터 로드,

데의터의 각 행에 대해 artist_name, track_nam, genre, lyrics 열의 내용을 결합하여 combined_text 열에 저장한다.
결합된 텍스트는 각 노래에 대한 설명이 포함된 텍스트, 임베딩 생성에 사용된다.

임베딩 모델 초기화

임베딩 파일 로드 및 생성

FAISS 인덱스 생성 및 로드

임베딩의 차원을 dimension 에 저장, FAISS 인덱스 파일의 확인, 

유사한 문서 검색 함수

OpenAI API 를 통한 답변 생성 함수

search_silmier_documents 함수를 호출해 사용자 질문과 관련된 문서를 검색한다.

프롬프트 생성 : 검색된 문서를 바탕으로 프롬프트를 생성한다. 

OpenAI API 호출

내부 문서 기반으로 LLM 을 통한 외부와의 검색으로 결과를 출력해준다.

위 내용들의 langGraph 를 통한 구현

## 파일 설명 

data_embedding : 내부 데이터의 전처리, 벡터화 등을 통해 유사한 문서를 바로 찾을 수 있도록

search : LangGraph 구현 전 로직의 완성, 벡터화된 내부 문서 호출 - 사용자 질문에 가장 가까운 문서(노래) 탐색 - 탐색된 내용 기반 prompt 탐색, LLM 전달

langGraphSearch : search.py 의 langGraph 를 통한 구현

아직은 아주 간단한 내외부 문서 질의응답 시스템의 일부를 구현했음, 추가해야 할 점으로 메모리 관리, 그래프 분기 조건이 사용될 수 있을 점이 무엇이 있을지에 대한 고민
