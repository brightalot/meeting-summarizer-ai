import { FileText, ExternalLink, Calendar, Clock } from 'lucide-react'

interface ResultCardProps {
  notionUrl: string
  createdAt: string
  title?: string
}

export function ResultCard({ notionUrl, createdAt, title }: ResultCardProps) {
  const date = new Date(createdAt)
  
  return (
    <div className="card-ios p-1 bg-gradient-to-br from-white to-gray-50 mt-8 overflow-hidden">
      <div className="p-7">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {title || '회의 요약 완료'}
            </h3>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center">
                <Calendar className="w-4 h-4 mr-1.5" />
                {date.toLocaleDateString()}
              </div>
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1.5" />
                {date.toLocaleTimeString()}
              </div>
            </div>
          </div>
          <div className="w-12 h-12 bg-ios-green/10 rounded-2xl flex items-center justify-center">
            <FileText className="w-6 h-6 text-ios-green" />
          </div>
        </div>
        
        <p className="text-gray-600 mb-8 leading-relaxed">
          모든 처리가 완료되었습니다. 아래 버튼을 클릭하여 생성된 Notion 페이지를 확인하세요.
        </p>

        <a 
          href={notionUrl} 
          target="_blank" 
          rel="noopener noreferrer"
          className="w-full group flex items-center justify-center px-6 py-4 bg-gray-900 text-white font-medium rounded-xl transition-all duration-300 hover:bg-black hover:scale-[1.01] active:scale-[0.99] shadow-lg hover:shadow-xl"
        >
          <span>Notion에서 열기</span>
          <ExternalLink className="w-5 h-5 ml-2 opacity-70 group-hover:opacity-100 transition-opacity" />
        </a>
      </div>
    </div>
  )
}

