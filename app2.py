import os
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_upstage import ChatUpstage
from langchain_classic import hub
from langchain_classic.chains import RetrievalQA

# 1. 환경 변수 로드 (.env 파일에서 UPSTAGE_API_KEY를 가져옴)
load_dotenv()

# 2. 문서 로드 및 분할
print("1. 'tax.docx' 문서를 로드하고 분할하는 중...")
loader = Docx2txtLoader('./tax.docx')
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)
document2_list = loader.load_and_split(text_splitter=text_splitter)
print(f"-> 총 {len(document2_list)}개의 문서 조각으로 분할됨")

# 3. 임베딩 및 벡터 DB 생성
print("2. Upstage 임베딩 모델로 문서를 벡터화하는 중...")
embedding = UpstageEmbeddings(model='solar-embedding-1-large')

# 4. ChromaDB에 벡터 저장 (메모리 기반)
# (참고: from_documents는 매번 실행 시 DB를 새로 만듭니다. 
# 가장 간단하며, persist_directory를 사용하지 않아 빠릅니다.)
print("3. ChromaDB 벡터 저장소를 생성하는 중...")
database = Chroma.from_documents(
    documents=document2_list, 
    embedding=embedding
)

# 5. 프롬프트 및 LLM 로드
print("4. RAG 프롬프트와 Upstage LLM을 로드하는 중...")
prompt2 = hub.pull("rlm/rag-prompt")
llm = ChatUpstage()

# 6. RAG 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=database.as_retriever(),
    chain_type_kwargs={"prompt" : prompt2}
)

# 7. 질문 및 답변 실행
query = '연봉 5천만원인 직장인의 소득세는 얼마인가요?'
print(f"\n5. 질문 실행: {query}")
ai_message2 = qa_chain.invoke({"query": query})

# 8. 결과 출력
print("\n[AI 답변]")
print(ai_message2['result'])