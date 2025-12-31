import { useState, useRef, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

interface ProgressInfo {
  current: number
  total: number
  current_file: string
  percentage: number
}

interface ProcessingStatus {
  status: 'uploading' | 'queued' | 'processing' | 'completed' | 'failed'
  filename: string
  session_id: string
  download_name?: string
  error?: string
  progress?: ProgressInfo
}

interface UploadResult {
  success: boolean
  message: string
  downloadName?: string
  sessionId?: string
}

// Track multiple active sessions
interface ActiveSession {
  session_id: string
  filename: string
  status: ProcessingStatus
}

// Track completed downloads
interface CompletedDownload {
  session_id: string
  filename: string
  download_name: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const [activeSessions, setActiveSessions] = useState<ActiveSession[]>([])
  const [completedDownloads, setCompletedDownloads] = useState<CompletedDownload[]>([])
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const pollingIntervalRef = useRef<number | null>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    if (droppedFile && droppedFile.name.endsWith('.zip')) {
      setFile(droppedFile)
      setUploadResult(null)
    } else {
      setUploadResult({
        success: false,
        message: 'Only ZIP files are allowed.'
      })
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile && selectedFile.name.endsWith('.zip')) {
      setFile(selectedFile)
      setUploadResult(null)
    } else if (selectedFile) {
      setUploadResult({
        success: false,
        message: 'Only ZIP files are allowed.'
      })
    }
  }

  // Poll for all active session statuses
  const pollAllSessions = useCallback(async () => {
    const updatedSessions: ActiveSession[] = []
    const completedSessions: ActiveSession[] = []
    const failedSessions: ActiveSession[] = []
    
    for (const session of activeSessions) {
      try {
        const response = await fetch(`${API_BASE_URL}/status/${session.session_id}`)
        if (response.ok) {
          const status: ProcessingStatus = await response.json()
          
          if (status.status === 'completed' || status.status === 'failed') {
            completedSessions.push({ ...session, status })
          } else {
            updatedSessions.push({ ...session, status })
          }
        } else if (response.status === 404) {
          // Session not found on server (server may have restarted)
          // Mark as failed and remove from active sessions
          failedSessions.push({
            ...session,
            status: {
              ...session.status,
              status: 'failed',
              error: 'Session expired. Server may have restarted. Please re-upload.'
            }
          })
        } else {
          // Keep in active for other errors
          updatedSessions.push(session)
        }
      } catch (error) {
        console.error(`Failed to poll session ${session.session_id}:`, error)
        updatedSessions.push(session)
      }
    }
    
    setActiveSessions(updatedSessions)
    
    // Handle completed sessions - add to completed downloads list
    const newCompletedDownloads: CompletedDownload[] = []
    for (const completed of completedSessions) {
      if (completed.status.status === 'completed' && completed.status.download_name) {
        newCompletedDownloads.push({
          session_id: completed.session_id,
          filename: completed.filename,
          download_name: completed.status.download_name
        })
      } else if (completed.status.status === 'failed') {
        setUploadResult({
          success: false,
          message: completed.status.error || `Processing failed for "${completed.filename}"`
        })
      }
    }
    
    // Add new completed downloads to the list
    if (newCompletedDownloads.length > 0) {
      setCompletedDownloads(prev => [...prev, ...newCompletedDownloads])
    }
    
    // Handle failed/expired sessions
    for (const failed of failedSessions) {
      setUploadResult({
        success: false,
        message: failed.status.error || `Session expired for "${failed.filename}"`
      })
    }
    
    // Stop polling if no more active sessions
    if (updatedSessions.length === 0 && pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
      pollingIntervalRef.current = null
    }
  }, [activeSessions])

  // Start/stop polling based on active sessions
  useEffect(() => {
    if (activeSessions.length > 0 && !pollingIntervalRef.current) {
      pollingIntervalRef.current = window.setInterval(pollAllSessions, 2000)
    } else if (activeSessions.length === 0 && pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
      pollingIntervalRef.current = null
    }
    
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current)
        pollingIntervalRef.current = null
      }
    }
  }, [activeSessions.length, pollAllSessions])

  const handleUpload = async () => {
    if (!file) return

    // Capture file reference before clearing
    const fileToUpload = file
    const uploadedFilename = fileToUpload.name
    
    // Clear file immediately so user can select another
    setFile(null)
    setUploadResult({
      success: true,
      message: `Uploading "${uploadedFilename}"...`
    })

    const formData = new FormData()
    formData.append('file', fileToUpload)

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const data = await response.json()
        
        // If status is not completed, add to active sessions for polling
        if (data.status !== 'completed') {
          const newSession: ActiveSession = {
            session_id: data.session_id,
            filename: uploadedFilename,
            status: {
              status: data.status,
              filename: uploadedFilename,
              session_id: data.session_id
            }
          }
          setActiveSessions(prev => [...prev, newSession])
          setUploadResult({
            success: true,
            message: `"${uploadedFilename}" queued for processing. You can upload more files.`,
            sessionId: data.session_id
          })
        } else {
          setUploadResult({
            success: true,
            message: data.message,
            downloadName: data.download_name,
            sessionId: data.session_id
          })
        }
      } else {
        const error = await response.json()
        setUploadResult({
          success: false,
          message: error.detail || 'Upload failed'
        })
      }
    } catch {
      setUploadResult({
        success: false,
        message: 'Failed to connect to server'
      })
    }
  }

  const handleDownload = async (name: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/download/${name}`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${name}.zip`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        a.remove()
      } else {
        setUploadResult({
          success: false,
          message: 'Download failed'
        })
      }
    } catch {
      setUploadResult({
        success: false,
        message: 'Failed to download file'
      })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-linear-to-br from-red-500 via-yellow-500 to-green-500 rounded-lg"></div>
            <span className="text-xl font-semibold text-gray-800">DocsGenerator</span>
            <span className="text-sm text-gray-500 ml-1">Pro</span>
          </div>
          
        </div>
      </nav>

      {/* Main Content */}
      <main className="mt-20 w-full max-w-4xl">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
          Generate Documentation
        </h1>

        {/* Upload Zone */}
        <div
          className={`relative rounded-2xl border-2 border-dashed transition-all duration-300 ${
            isDragging
              ? 'border-red-400 bg-red-50'
              : 'border-gray-300 bg-red-500 hover:bg-red-600'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center py-16 px-8">
            {/* Icon */}
            <div className="flex items-center gap-2 mb-6">
              <svg className="w-12 h-12 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <svg className="w-8 h-8 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8" />
              </svg>
            </div>

            {/* Choose Files Button */}
            <div className="flex items-center gap-2 mb-4">
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-2 bg-white text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors shadow-sm"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                CHOOSE FILES
              </button>
              <button className="bg-white text-gray-700 p-3 rounded-lg hover:bg-gray-100 transition-colors shadow-sm">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept=".zip"
              onChange={handleFileChange}
              className="hidden"
            />

            <p className="text-white opacity-90 text-sm">
              or drop files here
            </p>

            {/* Selected File */}
            {file && (
              <div className="mt-6 bg-white rounded-lg px-4 py-3 flex items-center gap-3 shadow-sm">
                <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8" />
                </svg>
                <span className="text-gray-700 font-medium">{file.name}</span>
                <button
                  onClick={() => setFile(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Upload Button */}
        {file && (
          <div className="mt-6 flex justify-center">
            <button
              onClick={handleUpload}
              className="px-8 py-3 rounded-lg font-semibold text-white transition-all bg-green-500 hover:bg-green-600 shadow-lg hover:shadow-xl"
            >
              Generate Documentation
            </button>
          </div>
        )}

        {/* Active Sessions - Multiple Processing Jobs */}
        {activeSessions.length > 0 && (
          <div className="mt-6 space-y-3">
            <h3 className="text-lg font-semibold text-gray-700">Processing Queue ({activeSessions.length})</h3>
            {activeSessions.map((session) => (
              <div key={session.session_id} className="p-4 rounded-lg bg-blue-50 border border-blue-200">
                <div className="flex items-center gap-3">
                  <svg className="animate-spin w-5 h-5 text-blue-500 shrink-0" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="text-blue-700 font-medium truncate">{session.filename}</span>
                      <span className="text-blue-600 text-sm capitalize ml-2">{session.status.status}</span>
                    </div>
                    {session.status.progress && (
                      <div className="mt-2">
                        <div className="flex items-center justify-between text-xs text-blue-600 mb-1">
                          <span className="truncate max-w-xs">{session.status.progress.current_file}</span>
                          <span>{session.status.progress.current}/{session.status.progress.total} files ({session.status.progress.percentage}%)</span>
                        </div>
                        <div className="w-full bg-blue-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${session.status.progress.percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Completed Downloads */}
        {completedDownloads.length > 0 && (
          <div className="mt-6 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-700">
                Completed ({completedDownloads.length})
              </h3>
              <button
                onClick={() => setCompletedDownloads([])}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Clear all
              </button>
            </div>
            {completedDownloads.map((download) => (
              <div key={download.session_id} className="p-4 rounded-lg bg-green-50 border border-green-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="text-green-700 font-medium">{download.filename}</span>
                  </div>
                  <button
                    onClick={() => handleDownload(download.download_name)}
                    className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error Message */}
        {uploadResult && !uploadResult.success && (
          <div className="mt-6 p-4 rounded-lg bg-red-50 border border-red-200">
            <div className="flex items-center gap-3">
              <svg className="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-red-700">
                {uploadResult.message}
              </span>
            </div>
          </div>
        )}

        {/* Upload Status Message (non-error) */}
        {uploadResult && uploadResult.success && !uploadResult.downloadName && (
          <div className="mt-6 p-4 rounded-lg bg-green-50 border border-green-200">
            <div className="flex items-center gap-3">
              <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-green-700">
                {uploadResult.message}
              </span>
            </div>
          </div>
        )}

        {/* Features */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-center gap-3">
            <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-gray-600">AI-powered documentation</span>
          </div>
          <div className="flex items-center gap-3">
            <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-gray-600">Supports multiple languages</span>
          </div>
          <div className="flex items-center gap-3">
            <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-gray-600">Markdown & JSON output</span>
          </div>
        </div>

        {/* Description */}
        <p className="mt-8 text-gray-600 text-center max-w-2xl mx-auto">
          Generate comprehensive documentation for your code projects. Upload a ZIP file containing your source code, 
          and our AI will analyze it to create detailed documentation including function summaries, 
          class descriptions, and dependency graphs.
        </p>
      </main>
    </div>
  )
}

export default App
