# Meeting Summarizer AI API 명세서

## 기본 정보

- **Base URL**: `http://localhost:8000`
- **API Version**: `v1`
- **Content-Type**: `application/json` (multipart/form-data for file uploads)

---

## 엔드포인트 목록

### 1. 루트 엔드포인트

#### `GET /`

API 서버의 기본 엔드포인트입니다.

**응답**

```json
{
  "message": "Welcome to NoteSync AI API"
}
```

**응답 코드**: `200 OK`

---

### 2. 헬스 체크

#### `GET /health`

서버 상태를 확인하는 엔드포인트입니다.

**응답**

```json
{
  "status": "ok"
}
```

**응답 코드**: `200 OK`

---

### 3. 회의 오디오 파일 업로드

#### `POST /api/v1/meetings/upload`

회의 오디오 파일을 업로드하고 처리 파이프라인을 시작합니다.

**요청**

- **Content-Type**: `multipart/form-data`
- **Body**:
  - `file` (required): 오디오 파일 (WAV, MP3 등)

**요청 예시**

```bash
curl -X POST "http://localhost:8000/api/v1/meetings/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meeting_audio.wav"
```

**응답**

```json
{
  "id": "82c1b3ea-708b-4d89-b1c7-a27733611677",
  "status": "PENDING"
}
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string (UUID) | 생성된 회의 레코드의 고유 ID |
| `status` | string | 회의 처리 상태 (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`) |

**응답 코드**

- `200 OK`: 파일 업로드 성공
- `400 Bad Request`: 잘못된 요청 (파일이 없거나 형식이 잘못됨)
- `500 Internal Server Error`: 서버 오류

**참고사항**

- 파일 업로드 후 백그라운드에서 자동으로 처리 파이프라인이 시작됩니다.
- 처리 상태는 `GET /api/v1/meetings/{meeting_id}` 엔드포인트를 통해 확인할 수 있습니다.

---

### 4. 회의 정보 조회

#### `GET /api/v1/meetings/{meeting_id}`

특정 회의의 상세 정보를 조회합니다.

**경로 파라미터**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `meeting_id` | UUID | 조회할 회의의 고유 ID |

**요청 예시**

```bash
curl -X GET "http://localhost:8000/api/v1/meetings/82c1b3ea-708b-4d89-b1c7-a27733611677"
```

**응답**

```json
{
  "id": "82c1b3ea-708b-4d89-b1c7-a27733611677",
  "title": "meeting_audio.wav",
  "file_path": "uploads/82c1b3ea-708b-4d89-b1c7-a27733611677.wav",
  "transcript": "안녕하세요. 오늘 회의 주제는...",
  "summary": "오늘 회의에서는 다음 사항들을 논의했습니다...",
  "status": "COMPLETED",
  "notion_page_url": "https://www.notion.so/...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**응답 필드**

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string (UUID) | 회의의 고유 ID |
| `title` | string | 회의 제목 (업로드된 파일명) |
| `file_path` | string | 서버에 저장된 오디오 파일 경로 |
| `transcript` | string \| null | 음성 인식 결과 텍스트 (처리 완료 시) |
| `summary` | string \| null | 회의 요약 내용 (처리 완료 시) |
| `status` | string | 처리 상태 (`PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`) |
| `notion_page_url` | string \| null | Notion에 생성된 페이지 URL (완료 시) |
| `created_at` | string (ISO 8601) | 회의 레코드 생성 시간 |

**응답 코드**

- `200 OK`: 조회 성공
- `404 Not Found`: 해당 ID의 회의를 찾을 수 없음
- `500 Internal Server Error`: 서버 오류

---

## 데이터 모델

### MeetingStatus Enum

회의 처리 상태를 나타내는 열거형입니다.

| 값 | 설명 |
|----|------|
| `PENDING` | 대기 중 (업로드 완료, 처리 대기) |
| `PROCESSING` | 처리 중 (STT, 요약, Notion 업로드 진행 중) |
| `COMPLETED` | 완료 (모든 처리가 완료됨) |
| `FAILED` | 실패 (처리 중 오류 발생) |

### Meeting 모델

회의 정보를 담는 데이터 모델입니다.

```typescript
interface Meeting {
  id: string;              // UUID
  title: string | null;    // 회의 제목
  file_path: string;       // 파일 경로
  transcript: string | null;  // 음성 인식 결과
  summary: string | null;     // 회의 요약
  status: MeetingStatus;      // 처리 상태
  notion_page_url: string | null;  // Notion 페이지 URL
  created_at: string;          // 생성 시간 (ISO 8601)
}
```

---

## 에러 응답 형식

에러 발생 시 다음 형식으로 응답됩니다:

```json
{
  "detail": "에러 메시지"
}
```

**일반적인 에러 코드**

- `400 Bad Request`: 잘못된 요청 파라미터
- `404 Not Found`: 리소스를 찾을 수 없음
- `422 Unprocessable Entity`: 요청 데이터 검증 실패
- `500 Internal Server Error`: 서버 내부 오류

---

## 처리 플로우

1. **파일 업로드** (`POST /api/v1/meetings/upload`)
   - 오디오 파일을 서버에 업로드
   - Meeting 레코드 생성 (status: `PENDING`)
   - 백그라운드 작업으로 처리 파이프라인 시작

2. **처리 파이프라인** (백그라운드)
   - STT (Speech-to-Text): 오디오를 텍스트로 변환
   - LLM 요약 및 자동 Notion 저장: Google Gemini로 텍스트를 요약하고, 요약 생성 후 자동으로 Notion 페이지 생성
   - 상태 업데이트: `PROCESSING` → `COMPLETED` 또는 `FAILED`

3. **상태 확인** (`GET /api/v1/meetings/{meeting_id}`)
   - 클라이언트는 주기적으로 이 엔드포인트를 호출하여 처리 상태 확인
   - `status`가 `COMPLETED`가 되면 `transcript`, `summary`, `notion_page_url` 필드에 값이 채워짐

---

## 예제 사용 시나리오

### 시나리오 1: 회의 오디오 업로드 및 결과 확인

```bash
# 1. 파일 업로드
curl -X POST "http://localhost:8000/api/v1/meetings/upload" \
  -F "file=@meeting.wav"

# 응답: {"id": "abc-123", "status": "PENDING"}

# 2. 상태 확인 (폴링)
curl -X GET "http://localhost:8000/api/v1/meetings/abc-123"

# 초기 응답: {"id": "abc-123", "status": "PROCESSING", ...}
# 완료 후 응답: {"id": "abc-123", "status": "COMPLETED", "transcript": "...", "summary": "...", "notion_page_url": "..."}
```

---

## 참고사항

- 파일 업로드는 비동기로 처리되므로, 업로드 직후 `status`가 `COMPLETED`가 아닐 수 있습니다.
- 처리 시간은 오디오 파일의 길이에 따라 달라질 수 있습니다.
- `status`가 `FAILED`인 경우, `transcript`나 `summary` 필드는 `null`일 수 있습니다.
- Notion 연동이 설정되지 않은 경우, `notion_page_url`은 `null`일 수 있습니다.

