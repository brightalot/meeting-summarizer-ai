import { useState, useEffect } from 'react'
import axios from 'axios'
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

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

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
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
    } catch (err) {
      setError('Upload failed')
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
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">NoteSync AI</h1>
          <p className="text-gray-600">Upload your meeting recording and let AI do the rest.</p>
        </div>

        <div className="bg-white rounded-lg shadow-xl p-8 mb-8">
          <div className="flex items-center justify-center w-full mb-6">
            <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Upload className="w-12 h-12 text-gray-400 mb-4" />
                <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                <p className="text-xs text-gray-500">MP3, WAV, M4A</p>
              </div>
              <input id="dropzone-file" type="file" className="hidden" onChange={handleFileChange} accept="audio/*" />
            </label>
          </div>

          {file && (
            <div className="flex items-center justify-between mb-6 p-4 bg-blue-50 rounded-lg">
              <span className="text-sm font-medium text-blue-700">{file.name}</span>
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {uploading ? 'Uploading...' : 'Start Processing'}
              </button>
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 bg-red-50 rounded-lg flex items-center">
              <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
              <span className="text-sm text-red-700">{error}</span>
            </div>
          )}
        </div>

        {meeting && (
          <div className="bg-white rounded-lg shadow-xl p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Processing Status</h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium 
                ${meeting.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 
                  meeting.status === 'FAILED' ? 'bg-red-100 text-red-800' : 
                  'bg-yellow-100 text-yellow-800'}`}>
                {meeting.status}
              </span>
            </div>

            <div className="space-y-6">
              <div className="flex items-center">
                {meeting.transcript ? <CheckCircle className="w-5 h-5 text-green-500 mr-3" /> : <Loader2 className="w-5 h-5 text-gray-400 mr-3 animate-spin" />}
                <span className={meeting.transcript ? "text-gray-900" : "text-gray-500"}>Transcribing Audio</span>
              </div>
              <div className="flex items-center">
                {meeting.summary ? <CheckCircle className="w-5 h-5 text-green-500 mr-3" /> : <Loader2 className="w-5 h-5 text-gray-400 mr-3 animate-spin" />}
                <span className={meeting.summary ? "text-gray-900" : "text-gray-500"}>Generating Summary</span>
              </div>
              <div className="flex items-center">
                {meeting.notion_page_url ? <CheckCircle className="w-5 h-5 text-green-500 mr-3" /> : <Loader2 className="w-5 h-5 text-gray-400 mr-3 animate-spin" />}
                <span className={meeting.notion_page_url ? "text-gray-900" : "text-gray-500"}>Creating Notion Page</span>
              </div>

              {meeting.notion_page_url && (
                <div className="mt-8 p-4 bg-gray-50 rounded-lg text-center">
                  <a href={meeting.notion_page_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium">
                    <FileText className="w-5 h-5 mr-2" />
                    Open in Notion
                  </a>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
