# 🚇 지하철 경로 안내 서비스


### 📜 프로젝트 개요 ###

우리나라 지하철의 경우 호선의 수가 많고 광범위하게 존재한다.
따라서 목적지까지 가는 다양한 루트가 존재하므로 그 중 최적의 노선을 제공하는 챗봇을 개발하였다.

<br/>

### ⌛ 개발 기간 ###
2024.11.6 ~ 2024.11.7 (2일)


<br/>

### ✔️ 수행결과 ###

1. 출발지와 목적지 입력 시 호선 및 환승 루트 제공
  <img src="https://github.com/user-attachments/assets/41ddf1cf-87a2-4e0f-94a1-ef0a32efb7d8"/>
  
<br/>
<br/>

2. 소요시간과 요금 추가 정보 제공
  <img src="https://github.com/user-attachments/assets/736fe0f1-b2e6-46a6-af15-515187dfe0a7"/>
  
<br/>
<br/>

### ⛓️ Lang Graph Display ###
- Agent에서 tool 실행
- Conditional Edge 구
  
  <img src="https://github.com/user-attachments/assets/8bf07035-82e4-4d33-ad2e-a5c8ecb5bb75"/>

<br/>
<br/>

### 🏗️ Architecture  ###
   <img src="https://github.com/user-attachments/assets/92abc0ca-9dc8-4b47-8de9-0941fc0a5ff9"/>

<br/>
<br/>

### ❓ 개선사항  ###
1. VECTOR DB에 없는 정보는 잘 반영하지 않음 -> 알맞는 데이터 추가 적재
2. 사용자 INPUT에 맞게 PROMPT 수정
3. TAVILY API 사용하여 외부 검색 툴 추가하려 했으나 반복되는 오류로 RETRIVER만 사용함 -> 추후에 오류 해결 후 검색 툴 추가 요망 






