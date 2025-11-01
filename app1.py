import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage

def main():
    # .env 파일에서 API 키 로드
    load_dotenv()
    
    # API 키가 있는지 확인 (없으면 에러 메시지 후 종료)
    if os.getenv("UPSTAGE_API_KEY") is None:
        print("오류: UPSTAGE_API_KEY 환경 변수를 찾을 수 없습니다.")
        print("프로젝트 루트에 .env 파일을 만들고 키를 입력하세요.")
        return

    # 1. LLM 모델 초기화 (기본 무료 모델: solar-1-mini)
    try:
        llm = ChatUpstage()
    except Exception as e:
        print(f"LLM을 초기화하는 중 오류가 발생했습니다: {e}")
        return

    print("✅ ChatUpstage (무료 모델)이 로드되었습니다.")
    print("채팅을 시작합니다. 종료하려면 'exit' 또는 'quit'을 입력하세요.")
    print("---")

    # 2. 무한루프 시작
    while True:
        try:
            # 3. 사용자 입력 받기
            query = input("질문하세요 : ")

            # 4. 종료 명령어 확인
            if query.lower() in ["exit", "quit", "종료"]:
                print("채팅을 종료합니다.")
                break
            
            # 5. LLM에 질문하고 답변 받기
            ai_message = llm.invoke(query)
            
            # 6. 답변 출력
            print(f"대답 : {ai_message.content}")
            print("---")

        except EOFError:
            # 사용자가 Ctrl+D 등으로 강제 종료 시
            print("\n채팅을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break

if __name__ == "__main__":
    main()








'''

from dotenv import load_dotenv 

load_dotenv()
#load_dotenv(dotenv_path='./test-env')

from langchain_upstage import ChatUpstage

llm = ChatUpstage()
#무료모델
#llm = ChatUpstage(model="solar-1-mini")
# 'solar-pro-2' (유료 모델)로 변경
#llm = ChatUpstage(model="solar-pro-2")


#llm.invoke("랭체인이란?")
ai_message=llm.invoke("랭체인이란?")


print(ai_message.content)



# 아래는 권장되지 않음, 매 주피터노트북 마다 아래처럼 번거롭게 설정해줘야함
# import os
# from langchain_openai import ChatOpenAI
# api_key = os.getenv("OPENAI_KEY") .env 파일에서 "OPENAI_API_KEY" 가 아닌 다른 식 - 예> "OPENAI_KEY"로 설정했을때 등

# llm = ChatOpenAI(api_key = api_key)

'''