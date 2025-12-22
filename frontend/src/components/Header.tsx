import { Mic } from 'lucide-react'

export function Header() {
  return (
    <div className="text-center mb-12 animate-fade-in-down">
      <div className="inline-flex items-center justify-center p-4 bg-white rounded-3xl shadow-ios mb-6">
        <div className="bg-ios-blue/10 p-3 rounded-2xl mr-4">
          <Mic className="w-8 h-8 text-ios-blue" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 tracking-tight">NoteSync AI</h1>
      </div>
      <p className="text-lg text-gray-500 max-w-md mx-auto leading-relaxed">
        미팅 녹음 파일을 업로드하세요.<br/>
        AI가 텍스트 변환, 요약, 그리고 Notion 페이지 생성을 자동으로 처리합니다.
      </p>
    </div>
  )
}

