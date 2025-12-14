# 🤖 Agent Bible - AI Agent 실습 환경

패스트캠퍼스 **Agent 초격차** 강의를 위한 실습 환경입니다.

## 📋 목차

- [사전 요구사항](#사전-요구사항)
- [설치 방법](#설치-방법)
- [실습 노트북](#실습-노트북)
- [프로젝트 구조](#프로젝트-구조)
- [문제 해결](#문제-해결)

---

## 🔧 사전 요구사항

- **Python 3.10 이상**
- **OpenAI API 키** ([OpenAI Platform](https://platform.openai.com/)에서 발급)
- (선택) LangSmith API 키 - 추적 및 모니터링용

---

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/agent_bible.git
cd agent_bible
```

### 2. 가상환경 생성 및 활성화

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env  # Mac/Linux
copy .env.example .env  # Windows
```

`.env` 파일을 열고 API 키를 입력하세요:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Jupyter Notebook 실행

```bash
jupyter notebook
```

---

## 📚 실습 노트북

| 노트북 | 설명 |
|--------|------|
| `langchain_rag_practice.ipynb` | LangChain을 활용한 RAG 구현 실습 |
| `langgraph_rag_practice.ipynb` | LangGraph를 활용한 RAG 워크플로우 실습 |

---

## 📁 프로젝트 구조

```
agent_bible/
├── docs/                           # 실습용 문서
│   └── DeepSeek_OCR_paper.pdf
├── langchain_rag_practice.ipynb    # LangChain RAG 실습
├── langgraph_rag_practice.ipynb    # LangGraph RAG 실습
├── requirements.txt                # 패키지 의존성
├── .env.example                    # 환경 변수 템플릿
├── .gitignore                      # Git 제외 파일
└── README.md                       # 프로젝트 설명
```

---

## ❗ 문제 해결

### 1. `ModuleNotFoundError` 발생 시

가상환경이 활성화되어 있는지 확인하세요:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. OpenAI API 오류 발생 시

- `.env` 파일에 올바른 API 키가 입력되어 있는지 확인
- API 키에 충분한 크레딧이 있는지 확인

### 3. ChromaDB 관련 오류 발생 시

```bash
pip install --upgrade chromadb
```

---

## 📞 문의

강의 관련 문의는 패스트캠퍼스를 통해 연락해주세요.

---

**Happy Coding! 🎉**

