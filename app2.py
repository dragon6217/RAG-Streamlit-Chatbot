import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_upstage import ChatUpstage
from langchain_classic import hub
from langchain_classic.chains import RetrievalQA

# --- 1. 설정값 (Constants) ---
DOC_PATH = "./tax.docx"
DB_DIR = "./chroma"  # DB를 저장할 폴더 이름 (gitignore에 추가 권장!)

def main():
    # .env 파일에서 API 키 로드
    load_dotenv()
    if os.getenv("UPSTAGE_API_KEY") is None:
        print("오류: UPSTAGE_API_KEY 환경 변수를 찾을 수 없습니다.")
        return

    # --- 2. LLM 및 임베딩 모델 초기화 ---
    try:
        # 임베딩 모델 (질문 벡터화 및 최초 DB 생성 시 사용 - 유료)
        embedding = UpstageEmbeddings(model='solar-embedding-1-large')
        # LLM (답변 생성 시 사용 - 무료)
        llm = ChatUpstage()
    except Exception as e:
        print(f"모델을 초기화하는 중 오류가 발생했습니다: {e}")
        return

    # --- 3. (핵심) 영구 저장된 DB가 있는지 확인하고, 없으면 생성 ---
    if os.path.exists(DB_DIR):
        # 3-A. DB가 이미 존재하면, 로드합니다. (임베딩 비용 X)
        print(f"✅ 기존 DB를 로드합니다. ({DB_DIR})")
        database = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embedding
        )
    else:
        # 3-B. DB가 없으면, 새로 생성합니다. (최초 1회 과금 발생!)
        print(f"⚠️ '{DB_DIR}' 폴더를 찾을 수 없습니다.")
        print("새로운 벡터 DB 생성을 시작합니다... (최초 1회 비용이 발생합니다)")
        
        # 3-B-1. 문서 로드
        if not os.path.exists(DOC_PATH):
            print(f"오류: '{DOC_PATH}' 파일을 찾을 수 없습니다. 문서를 준비해주세요.")
            return
            
        loader = Docx2txtLoader(DOC_PATH)
        document = loader.load()

        # 3-B-2. 문서 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
        )
        document_chunks = text_splitter.split_documents(document)
        print(f"-> 총 {len(document_chunks)}개의 문서 조각으로 분할됨")

        # 3-B-3. 임베딩 및 DB 생성 (!! 과금 발생 !!)
        print("-> Upstage 임베딩 API를 호출하여 문서를 벡터화합니다...")
        database = Chroma.from_documents(
            documents=document_chunks, 
            embedding=embedding,
            persist_directory=DB_DIR  # ‼️ DB를 디스크에 영구 저장!
        )
        print(f"✅ DB 생성 완료 및 '{DB_DIR}' 폴더에 저장됨!")

    # --- 4. RAG 체인 및 프롬프트 설정 ---
    try:
        prompt = hub.pull("rlm/rag-prompt")
    except Exception as e:
        print(f"프롬프트를 pull하는 중 오류 발생: {e}")
        print("RAG 프롬프트(rlm/rag-prompt)를 가져오지 못했습니다. 인터넷 연결을 확인하세요.")
        return
        
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=database.as_retriever(),
        chain_type_kwargs={"prompt" : prompt}
    )

    # --- 5. 무한루프 질문 파트 ---
    print("\n✅ RAG 챗봇이 준비되었습니다. 'tax.docx'의 내용에 대해 질문하세요.")
    print("   종료하려면 'exit' 또는 'quit'을 입력하세요.")
    print("---")

    while True:
        try:
            query = input("질문하세요 : ")
            if query.lower() in ["exit", "quit", "종료"]:
                print("채팅을 종료합니다.")
                break
            
            # (!! 매 질문마다 '쿼리 임베딩' 비용 발생 !!)
            ai_message = qa_chain.invoke({"query": query})
            
            print(f"대답 : {ai_message['result']}")
            print("---")

        except EOFError:
            print("\n채팅을 종료합니다.")
            break
        except Exception as e:
            print(f"질문 처리 중 오류가 발생했습니다: {e}")
            break

if __name__ == "__main__":
    main()