# NoteSync AI (Meeting Summarizer Agent)

NoteSync AI는 회의 음성을 자동으로 텍스트로 변환(STT)하고, 핵심 내용을 요약하여 Notion 페이지로 정리해주는 AI 에이전트입니다.

## 🚀 주요 기능

1.  **음성 인식 (STT)**: OpenAI Whisper API를 사용하여 고품질의 한국어 음성 인식.
2.  **지능형 요약 (LLM)**: Google Gemini Pro/Flash 모델을 활용하여 회의 내용을 구조화된 마크다운(요약, 주요 논의, 결정 사항, 액션 아이템)으로 요약.
3.  **Notion 자동화 (MCP)**: 요약된 내용을 사용자의 Notion 데이터베이스에 자동으로 페이지로 생성.
4.  **UI/UX**: React 기반의 웹 인터페이스로 파일 업로드 및 실시간 진행 상태 확인.

## 🛠 기술 스택

-   **Frontend**: React, TypeScript, Vite, Tailwind CSS
-   **Backend**: FastAPI, SQLAlchemy (Async), Pydantic
-   **Database**: PostgreSQL
-   **Infrastructure**: Docker, Docker Compose, Nginx
-   **AI Services**: OpenAI Whisper, Google Gemini
-   **Integration**: Notion API

## 🏁 시작하기 (Getting Started)

### 1. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 변수들을 설정하세요.

```ini
# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=notesync

# AI API Keys
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...

# Notion Integration
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...
```

### 2. Notion 설정 방법

1.  **Integration 생성**: [Notion My Integrations](https://www.notion.so/my-integrations)에서 새 통합을 생성하고 `Internal Integration Secret`을 발급받습니다 (`NOTION_API_KEY`).
2.  **데이터베이스 ID 확인**: Notion 데이터베이스 페이지를 웹 브라우저로 열었을 때 URL에서 `https://www.notion.so/myworkspace/{database_id}?v=...` 부분의 `database_id`를 복사합니다 (`NOTION_DATABASE_ID`).
3.  **연동 권한 부여**: 해당 데이터베이스 페이지 우측 상단 `...` 메뉴 -> `Connect to` (연결) -> 위에서 만든 Integration 선택.

### 3. 실행 방법

Docker Compose를 사용하여 전체 서비스를 실행합니다.

```bash
docker-compose up --build
```

-   **Frontend**: http://localhost:3000
-   **Backend API**: http://localhost:8000/docs

## 🧪 테스트 방법

가상의 회의 음성 파일을 생성하여 파이프라인을 테스트할 수 있습니다.

### 1. 테스트용 음성 파일 생성

```bash
# 의존성 설치 (로컬)
pip install edge-tts pydub
# ffmpeg 설치 필요 (Mac: brew install ffmpeg)

# 스크립트 실행
python scripts/create_test_audio.py
```

`conversation_gendered.wav` 파일이 생성됩니다.

### 2. 업로드 및 결과 확인

1.  http://localhost:3000 접속.
2.  생성된 `conversation_gendered.wav` 파일 업로드.
3.  Transcribing -> Generating Summary -> Creating Notion Page 단계가 완료될 때까지 대기.
4.  완료 후 Notion 페이지 링크 클릭하여 결과 확인.

## 📝 결과 예시

**Notion 페이지 생성 결과:**

# 회의 요약
이번 스프린트 진행 상황을 공유하고, 백엔드 STT 서비스(Whisper API) 연동 및 프론트엔드 UI/기능 구현 현황을 점검했습니다.

## 주요 논의 사항
- 백엔드 API 개발 완료 및 STT 서비스 연동 테스트 진행 상황 공유
- Whisper API의 응답 속도(10분 분량 기준 약 30초) 및 MVP 적합성 논의
- 프론트엔드 React 컴포넌트 구조, 파일 업로드 UI 및 상태 표시 기능 구현 완료 현황

## 결정된 사항
- Whisper API의 응답 속도는 MVP 기준으로 충분하다고 판단함.
- 이번 주까지 통합 테스트가 가능하도록 일정을 조율하기로 함.

## 액션 아이템
- [ ] (담당자) : 이번 주까지 통합 테스트 가능하도록 일정 조율 및 준비
- [ ] (담당자) : 내일 오후 개발 서버에 배포 및 1차 테스트 진행
