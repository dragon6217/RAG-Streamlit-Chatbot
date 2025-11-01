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