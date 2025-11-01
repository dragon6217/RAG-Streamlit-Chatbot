## 🚀 실행 방법 (How to Run)

이 저장소에는 두 개의 주요 스크립트가 있습니다.

### 1. `app.py`: API 연결 검증
* **목적:** Upstage API (`ChatUpstage`)가 `.env` 파일의 API 키로 정상 작동하는지 확인하는 간단한 테스트 스크립트입니다. (프로젝트의 `c1` 커밋에 해당)
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

2.  (권장) `pyenv` 가상환경을 생성 및 활성화합니다.
    *(이 프로젝트는 Python 3.10.19 버전을 기준으로 합니다.)*
    ```bash
    # pyenv를 사용한다면 .python-version 파일이 자동으로 인식됩니다.
    python3 -m venv .venv
    source .venv/bin/activate
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

5.  **(필수) 샘플 문서 준비**
    * `tax.docx` (소득세법) 파일을 이 폴더에 다운로드하여 위치시킵니다.
    * (참고: 이 파일은 저작권 문제로 레포지토리에 포함하지 않았습니다.)

6.  메인 스크립트를 실행합니다.
    ```bash
    python app2.py
    ```
    * 스크립트가 실행되면, 코드 6~8단계를 거쳐 터미널에 AI의 답변이 출력됩니다.