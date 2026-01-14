import React, { useCallback, useState } from 'react'
import { Upload, FileAudio, X } from 'lucide-react'

interface UploadZoneProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
  onClear: () => void
  uploading: boolean
  onUpload: () => void
}

export function UploadZone({ onFileSelect, selectedFile, onClear, uploading, onUpload }: UploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0])
    }
  }, [onFileSelect])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0])
    }
  }

  if (selectedFile) {
    return (
      <div className="card-ios p-8 animate-fade-in">
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl mb-6 border border-gray-100">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-ios-blue/10 rounded-xl flex items-center justify-center">
              <FileAudio className="w-6 h-6 text-ios-blue" />
            </div>
            <div>
              <p className="font-semibold text-gray-900">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
            </div>
          </div>
          {!uploading && (
            <button 
              onClick={onClear}
              className="p-2 hover:bg-gray-200 rounded-full transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          )}
        </div>
        
        <button
          onClick={onUpload}
          disabled={uploading}
          className="w-full btn-ios flex items-center justify-center space-x-2"
        >
          {uploading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>처리 중...</span>
            </>
          ) : (
            <span>분석 시작하기</span>
          )}
        </button>
      </div>
    )
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative overflow-hidden transition-all duration-300 ease-out
        card-ios border-2 border-dashed
        ${isDragging ? 'border-ios-blue bg-ios-blue/5 scale-[1.02]' : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'}
      `}
    >
      <label className="flex flex-col items-center justify-center w-full h-80 cursor-pointer">
        <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4">
          <div className={`
            w-20 h-20 rounded-full flex items-center justify-center mb-6 transition-colors duration-300
            ${isDragging ? 'bg-ios-blue text-white' : 'bg-gray-100 text-gray-400'}
          `}>
            <Upload className="w-8 h-8" />
          </div>
          <p className="mb-2 text-xl font-medium text-gray-900">
            오디오 파일을 드래그하여 놓으세요
          </p>
          <p className="text-gray-500">
            또는 클릭하여 파일 선택
          </p>
          <p className="mt-4 text-xs font-medium text-gray-400 uppercase tracking-wider">
            MP3, WAV, M4A 지원
          </p>
        </div>
        <input 
          type="file" 
          className="hidden" 
          onChange={handleChange} 
          accept="audio/*" 
        />
      </label>
    </div>
  )
}

