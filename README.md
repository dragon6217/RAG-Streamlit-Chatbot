## 🚀 실행 방법 (How to Run)

이 저장소에는 두 개의 주요 스크립트가 있습니다.

### 1. `app.py`: API 연결 검증
* **목적:** Upstage API (`ChatUpstage`)가 `.env` 파일의 API 키로 정상 작동하는지 확인하는 간단한 테스트 스크립트입니다.
* **실행:** `python app.py`

### 2. `app2.py`: CLI 기반 RAG 파이프라인 (메인)
* **목적:** `tax.docx` 문서를 로드, 분할, 임베딩하고 `ChromaDB`에 저장한 뒤, `RetrievalQA` 체인을 통해 질문에 답변하는 **핵심 RAG 로직** 스크립트입니다.
* **실행:** `python app2.py` (이 스크립트가 터미널에 AI의 답변을 출력합니다.)

---

## 🛠️ 메인 스크립트(`app2.py`) 실행 가이드

1.  이 저장소를 클론합니다.
    ```bash
    git clone [https://github.com/](https://github.com/)[Your_ID]/RAG-Streamlit-Chatbot.git
    cd RAG-Streamlit-Chatbot
    ```

2. (권장) `pyenv` 가상환경 생성
    이 프로젝트는 `.python-version` 파일을 통해 `pyenv`가 특정 가상환경을 자동으로 활성화하도록 설정되어 있습니다.

    방문자는 `pyenv`를 사용하여 `RAG-Streamlit-Chatbot`이라는 이름으로 Python 3.10.x 버전의 가상환경을 **먼저 생성해야 합니다**:

    ```bash
    # (예시) pyenv로 Python 3.10.19 설치
    pyenv install 3.10.19
    # 'RAG-Streamlit-Chatbot' 이름으로 가상환경 생성
    pyenv virtualenv 3.10.19 RAG-Streamlit-Chatbot
    ```

3.  필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

4.  **(중요) API 키 설정**
    * 프로젝트 루트에 `.env` 파일을 생성하고, Upstage API 키를 추가합니다.
    ```
    UPSTAGE_API_KEY="sk-..."
    ```

5. 샘플 문서 확인
    이 레포지토리에는 RAG 테스트를 위한 샘플 문서인 `tax.docx` (소득세법) 파일이 포함되어 있습니다. 
    `app2.py`는 이 파일을 직접 로드하여 실행됩니다.

6.  메인 스크립트를 실행합니다.
    ```bash
    python app2.py
    ```
    * 스크립트가 실행되면, 코드 6~8단계를 거쳐 터미널에 AI의 답변이 출력됩니다.