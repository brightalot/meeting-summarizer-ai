import { CheckCircle2, Circle, Loader2, ArrowRight } from 'lucide-react'

interface ProcessingStatusProps {
  status: string
  transcript: string | null
  summary: string | null
  notionUrl: string | null
}

export function ProcessingStatus({ status, transcript, summary, notionUrl }: ProcessingStatusProps) {
  const steps = [
    {
      id: 'transcript',
      label: '음성 텍스트 변환',
      completed: !!transcript,
      current: status === 'PROCESSING' && !transcript,
    },
    {
      id: 'summary',
      label: 'AI 요약 생성',
      completed: !!summary,
      current: status === 'PROCESSING' && !!transcript && !summary,
    },
    {
      id: 'notion',
      label: 'Notion 페이지 작성',
      completed: !!notionUrl,
      current: status === 'PROCESSING' && !!summary && !notionUrl,
    }
  ]

  return (
    <div className="card-ios p-8 mt-8 animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-xl font-bold text-gray-900">처리 진행상황</h2>
        <span className={`
          px-4 py-1.5 rounded-full text-sm font-semibold tracking-wide
          ${status === 'COMPLETED' ? 'bg-ios-green/10 text-ios-green' : 
            status === 'FAILED' ? 'bg-ios-red/10 text-ios-red' : 
            'bg-ios-yellow/10 text-ios-yellow'}
        `}>
          {status === 'COMPLETED' ? '완료됨' : 
           status === 'FAILED' ? '실패' : 
           '처리 중...'}
        </span>
      </div>

      <div className="relative">
        {/* Connector Line */}
        <div className="absolute left-6 top-6 bottom-6 w-0.5 bg-gray-100" />

        <div className="space-y-8 relative">
          {steps.map((step) => (
            <div key={step.id} className="flex items-center">
              <div className={`
                relative z-10 w-12 h-12 rounded-full flex items-center justify-center border-4 transition-all duration-500
                ${step.completed ? 'bg-ios-green border-ios-green/20' : 
                  step.current ? 'bg-white border-ios-blue' : 
                  'bg-gray-50 border-white'}
              `}>
                {step.completed ? (
                  <CheckCircle2 className="w-6 h-6 text-white" />
                ) : step.current ? (
                  <Loader2 className="w-6 h-6 text-ios-blue animate-spin" />
                ) : (
                  <Circle className="w-6 h-6 text-gray-300" />
                )}
              </div>
              <div className="ml-6 flex-1">
                <p className={`
                  text-lg font-medium transition-colors duration-300
                  ${step.completed || step.current ? 'text-gray-900' : 'text-gray-400'}
                `}>
                  {step.label}
                </p>
                {step.current && (
                  <p className="text-sm text-ios-blue mt-1 animate-pulse">
                    작업 진행 중...
                  </p>
                )}
              </div>
              {step.completed && (
                <div className="text-gray-300">
                   <ArrowRight className="w-5 h-5" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

