import { useState, useEffect } from 'react'
import axios from 'axios'
import { AlertCircle } from 'lucide-react'
import { Header } from './components/Header'
import { UploadZone } from './components/UploadZone'
import { ProcessingStatus } from './components/ProcessingStatus'
import { ResultCard } from './components/ResultCard'

interface Meeting {
  id: string
  title: string
  status: string
  file_path: string
  transcript: string | null
  summary: string | null
  notion_page_url: string | null
  created_at: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [currentMeetingId, setCurrentMeetingId] = useState<string | null>(null)
  const [meeting, setMeeting] = useState<Meeting | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setError(null)
  }

  const handleClearFile = () => {
    setFile(null)
    setError(null)
    setMeeting(null)
    setCurrentMeetingId(null)
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/v1/meetings/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setCurrentMeetingId(response.data.id)
      // 초기 상태 설정을 위해 즉시 조회
      setMeeting({
        ...response.data,
        status: 'PROCESSING' 
      })
    } catch (err) {
      setError('업로드에 실패했습니다. 다시 시도해주세요.')
      console.error(err)
    } finally {
      setUploading(false)
    }
  }

  useEffect(() => {
    let interval: number

    if (currentMeetingId && meeting?.status !== 'COMPLETED' && meeting?.status !== 'FAILED') {
      interval = setInterval(async () => {
        try {
          const response = await axios.get(`/api/v1/meetings/${currentMeetingId}`)
          setMeeting(response.data)
        } catch (err) {
          console.error(err)
        }
      }, 2000)
    }

    return () => clearInterval(interval)
  }, [currentMeetingId, meeting?.status])

  return (
    <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-ios-background to-white">
      <div className="max-w-2xl mx-auto space-y-8">
        <Header />

        <div className="space-y-6">
          {!meeting && (
            <UploadZone 
              onFileSelect={handleFileSelect}
              selectedFile={file}
              onClear={handleClearFile}
              uploading={uploading}
              onUpload={handleUpload}
            />
          )}

          {error && (
            <div className="animate-fade-in p-4 bg-red-50 border border-red-100 rounded-2xl flex items-center text-red-600">
              <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0" />
              <span className="text-sm font-medium">{error}</span>
            </div>
          )}

          {meeting && (
            <>
              <ProcessingStatus 
                status={meeting.status}
                transcript={meeting.transcript}
                summary={meeting.summary}
                notionUrl={meeting.notion_page_url}
              />

              {meeting.status === 'COMPLETED' && meeting.notion_page_url && (
                <div className="animate-slide-up">
                  <ResultCard 
                    notionUrl={meeting.notion_page_url}
                    createdAt={meeting.created_at}
                    title={meeting.title}
                  />
                  
                  <div className="mt-8 text-center">
                    <button 
                      onClick={handleClearFile}
                      className="text-gray-500 hover:text-gray-900 font-medium transition-colors text-sm"
                    >
                      다른 회의 기록하기
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
