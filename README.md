# NoteSync AI (Meeting Summarizer Agent)

NoteSync AI는 회의 음성을 자동으로 텍스트로 변환(STT)하고, 핵심 내용을 요약하여 Notion 페이지로 정리해주는 AI 에이전트입니다.

## 🚀 주요 기능

1. **음성 인식 (STT)**: OpenAI Whisper API를 사용하여 고품질의 한국어 음성 인식
2. **지능형 요약 (LLM)**: Google Gemini 2.5 Flash 모델을 활용하여 회의 내용을 구조화된 마크다운(요약, 주요 논의, 결정 사항, 액션 아이템)으로 요약
3. **Notion 자동화**: 요약된 내용을 사용자의 Notion 데이터베이스에 자동으로 페이지로 생성
4. **실시간 상태 추적**: React 기반의 웹 인터페이스로 파일 업로드 및 실시간 진행 상태 확인

## 🛠 기술 스택

- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy (Async), Pydantic
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose
- **AI Services**: OpenAI Whisper API, Google Gemini 2.5 Flash
- **Integration**: Notion API (via MCP - Model Context Protocol)

## 📋 프로젝트 구조

```
meeting-summarizer-ai/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── core/           # 설정 및 데이터베이스
│   │   ├── models/         # 데이터베이스 모델
│   │   ├── services/       # 비즈니스 로직 (STT, LLM, Notion)
│   │   └── mcp/            # MCP 클라이언트
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React 프론트엔드
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml      # 로컬 개발 환경
└── scripts/                # 유틸리티 스크립트
```

## 🏁 시작하기

### 로컬 개발 환경 설정

#### 1. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 변수들을 설정하세요.

```ini
# Database (Docker Compose 사용 시)
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=notesync
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/notesync

# AI API Keys
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...

# Notion Integration
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...

# Optional: Teams Webhook
TEAMS_WEBHOOK_URL=https://...
```

#### 2. Notion 설정 방법

1. **Integration 생성**: [Notion My Integrations](https://www.notion.so/my-integrations)에서 새 통합을 생성하고 `Internal Integration Secret`을 발급받습니다 (`NOTION_API_KEY`)
2. **데이터베이스 ID 확인**: Notion 데이터베이스 페이지를 웹 브라우저로 열었을 때 URL에서 `https://www.notion.so/myworkspace/{database_id}?v=...` 부분의 `database_id`를 복사합니다 (`NOTION_DATABASE_ID`)
3. **연동 권한 부여**: 해당 데이터베이스 페이지 우측 상단 `...` 메뉴 -> `Connect to` (연결) -> 위에서 만든 Integration 선택

#### 3. Docker Compose로 실행

```bash
# 전체 서비스 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

#### 4. 로컬 개발 (Docker 없이)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧪 테스트

### 테스트용 음성 파일 생성

```bash
# 의존성 설치 (로컬)
pip install edge-tts pydub
# ffmpeg 설치 필요 (Mac: brew install ffmpeg)

# 스크립트 실행
python scripts/create_test_audio.py
```

`conversation_gendered.wav` 파일이 생성됩니다.

### 테스트 시나리오

1. http://localhost:3000 접속
2. 생성된 `conversation_gendered.wav` 파일 업로드
3. 다음 단계가 순차적으로 완료되는지 확인:
   - ✅ Transcribing Audio
   - ✅ Generating Summary
   - ✅ Creating Notion Page
4. 완료 후 Notion 페이지 링크 클릭하여 결과 확인

## 📚 API 문서

자세한 API 명세서는 [API.md](./API.md)를 참조하세요.

주요 엔드포인트:
- `POST /api/v1/meetings/upload` - 오디오 파일 업로드
- `GET /api/v1/meetings/{meeting_id}` - 회의 정보 조회
- `GET /health` - 헬스 체크

## 📝 처리 플로우

1. **파일 업로드**: 사용자가 오디오 파일을 업로드하면 서버에 저장되고 DB에 `PENDING` 상태로 레코드 생성
2. **백그라운드 처리**: FastAPI `BackgroundTasks`로 비동기 처리 시작
3. **STT 처리**: OpenAI Whisper API로 음성을 텍스트로 변환
4. **요약 생성 및 Notion 저장**: Google Gemini가 Function Calling을 사용하여:
   - 회의 내용을 요약 및 구조화
   - **Gemini가 직접 Notion 페이지 생성 함수를 호출**하여 자동으로 저장
5. **상태 업데이트**: 처리 완료 시 `COMPLETED` 상태로 변경

### 🤖 자동화 워크플로우

이 프로젝트는 **자동화된 워크플로우**를 제공합니다:
- Gemini LLM이 회의 내용을 요약
- 요약 생성 후 자동으로 Notion 페이지 생성
- 마크다운 형식의 요약을 Notion 블록 구조로 자동 변환

## 🔌 Notion MCP 아키텍처

이 프로젝트는 **MCP (Model Context Protocol)** 아키텍처를 사용하여 Notion과 상호작용합니다.

### 동작 구조

```
Gemini LLM
    ↓ (요약 생성)
NotionMCPClient (app/mcp/notion_mcp_client.py)
    ↓
NotionService (app/services/notion_service.py)
    ↓ (마크다운 파싱 및 블록 변환)
Notion API
```

### 핵심 특징

- **자동 저장**: Gemini가 요약 생성 후 자동으로 Notion에 저장
- **MCP 아키텍처**: MCP 클라이언트를 통해 Notion과 상호작용
- **구조화된 블록**: 마크다운을 Notion 블록 구조로 자동 변환

## 💾 데이터베이스 확인

PostgreSQL에 저장된 회의 데이터를 확인하는 방법:

### Python 스크립트 사용 (권장)

```bash
cd backend

# 최근 10개 회의 조회
python scripts/view_meetings.py

# 통계 정보 조회
python scripts/view_meetings.py --stats

# 특정 회의 상세 조회
python scripts/view_meetings.py --id {meeting_id}

# 상태별 조회
python scripts/view_meetings.py --status COMPLETED
```

### psql로 직접 접속

```bash
# Docker 컨테이너 접속
docker exec -it notesync-db psql -U user -d notesync

# SQL 쿼리 예시
SELECT * FROM meetings ORDER BY created_at DESC LIMIT 10;
```


## 🔧 문제 해결

### 데이터베이스 연결 오류

- Docker Compose 사용 시: `DATABASE_URL`에 `db` 호스트명 사용 (예: `postgresql+asyncpg://user:password@db:5432/notesync`)
- 로컬 개발 시: `localhost:5432` 사용

### 파일 업로드 실패

- 파일 크기 제한 확인 (FastAPI 기본값: 100MB)
- `uploads/` 디렉토리 권한 확인
- 프로덕션 환경에서는 객체 스토리지(S3, R2) 사용 권장

### Notion 페이지 생성 실패

- `NOTION_API_KEY`와 `NOTION_DATABASE_ID` 확인
- Notion Integration이 데이터베이스에 연결되어 있는지 확인
- Notion API 권한 확인

