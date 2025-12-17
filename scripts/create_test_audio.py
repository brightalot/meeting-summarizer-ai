import asyncio
import edge_tts
from pydub import AudioSegment
import os

# 발화 목록과 화자 정보
dialogue = [
    ("이번 스프린트 진행 상황 공유 부탁드립니다.", "male"),
    ("네, 현재 백엔드 API 개발은 거의 완료되었습니다. STT 서비스 연동 테스트 중입니다.", "female"),
    ("Whisper API 응답 속도는 괜찮은가요? 사용자 경험에 영향을 줄까 걱정되네요.", "male"),
    ("음성 파일 길이에 따라 다르지만, 10분 분량 기준으로 약 30초 내외로 처리되고 있습니다. MVP 기준으로는 충분하다고 판단됩니다.", "female"),
    ("알겠습니다. 프론트엔드 쪽 진행 상황은 어떤가요?", "male"),
    ("리액트 컴포넌트 구조는 다 잡았고, 파일 업로드 UI랑 상태 표시 기능까지 구현 완료했습니다.", "female"),
    ("노션 연동 부분에서 이슈는 없었나요?", "male"),
    ("네, 초반에 API 키 인증 관련해서 간헐적으로 에러가 발생했었는데, 예외 처리 로직 추가해서 지금은 안정적으로 동작합니다.", "female"),
    ("좋습니다. 그럼 이번 주까지 통합 테스트 가능하도록 일정 맞춰주세요.", "male"),
    ("네 알겠습니다. 내일 오후에 개발 서버에 배포해서 1차 테스트 진행하겠습니다.", "female")
]

# 화자별 음성 설정
voice_map = {
    "male": "ko-KR-InJoonNeural",   # 남성
    "female": "ko-KR-SunHiNeural"   # 여성
}

# 비동기 TTS 처리 함수
async def synthesize_dialogue():
    final = AudioSegment.silent(duration=1000)
    temp_files = []
    
    print("Generating audio segments...")
    for i, (text, speaker) in enumerate(dialogue):
        voice = voice_map[speaker]
        communicate = edge_tts.Communicate(text=text, voice=voice)
        filename = f"edge_line_{i}.mp3"
        await communicate.save(filename)
        temp_files.append(filename)
        
        audio = AudioSegment.from_mp3(filename)
        final += audio + AudioSegment.silent(duration=500)
        print(f"Processed line {i+1}/{len(dialogue)}: {text}")

    output_filename = "conversation_gendered.wav"
    final.export(output_filename, format="wav")
    print(f"\n완료: {output_filename}")

    # Clean up temporary files
    print("Cleaning up temporary files...")
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

# 실행
if __name__ == "__main__":
    asyncio.run(synthesize_dialogue())

