import { useState } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { Upload, Code, Loader2, Send } from 'lucide-react'
import { toast } from 'react-toastify'
import { checkCode, uploadFile } from '../services/api'

const CodeInput = ({ onResults, isLoading, setIsLoading }) => {
  const [code, setCode] = useState('')
  const [activeTab, setActiveTab] = useState('paste') // 'paste' or 'upload'
  const [dragActive, setDragActive] = useState(false)

  const handleCheckCode = async () => {
    if (!code.trim()) {
      toast.error('Please enter some code to check')
      return
    }

    setIsLoading(true)
    try {
      const result = await checkCode(code)
      onResults(result)
      toast.success('Analysis complete!')
    } catch (error) {
      toast.error(error.message || 'Failed to check code')
      onResults(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (file) => {
    if (!file) return

    // Validate file type
    const validExtensions = ['.py', '.txt', '.js', '.java', '.cpp', '.c', '.go', '.rs']
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    
    if (!validExtensions.includes(fileExtension)) {
      toast.error(`Invalid file type. Please upload a code file (${validExtensions.join(', ')})`)
      return
    }

    setIsLoading(true)
    try {
      const result = await uploadFile(file)
      onResults(result)
      toast.success(`File "${file.name}" analyzed successfully!`)
    } catch (error) {
      toast.error(error.message || 'Failed to upload file')
      onResults(null)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0])
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
      {/* Tabs */}
      <div className="flex border-b border-gray-200 bg-gray-50">
        <button
          onClick={() => setActiveTab('paste')}
          className={`flex-1 px-6 py-4 font-medium transition-colors ${
            activeTab === 'paste'
              ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
        >
          <div className="flex items-center justify-center space-x-2">
            <Code className="w-5 h-5" />
            <span>Paste Code</span>
          </div>
        </button>
        <button
          onClick={() => setActiveTab('upload')}
          className={`flex-1 px-6 py-4 font-medium transition-colors ${
            activeTab === 'upload'
              ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
          }`}
        >
          <div className="flex items-center justify-center space-x-2">
            <Upload className="w-5 h-5" />
            <span>Upload File</span>
          </div>
        </button>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'paste' ? (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter your code
              </label>
              <div className="border border-gray-300 rounded-lg overflow-hidden">
                <CodeMirror
                  value={code}
                  height="400px"
                  extensions={[python()]}
                  onChange={(value) => setCode(value)}
                  placeholder="# Paste your Python code here..."
                  theme="light"
                  basicSetup={{
                    lineNumbers: true,
                    highlightActiveLineGutter: true,
                    highlightSpecialChars: true,
                    foldGutter: true,
                    drawSelection: true,
                    dropCursor: true,
                    allowMultipleSelections: true,
                    indentOnInput: true,
                    bracketMatching: true,
                    closeBrackets: true,
                    autocompletion: true,
                    rectangularSelection: true,
                    crosshairCursor: true,
                    highlightActiveLine: true,
                    highlightSelectionMatches: true,
                    closeBracketsKeymap: true,
                    searchKeymap: true,
                    foldKeymap: true,
                    completionKeymap: true,
                    lintKeymap: true,
                  }}
                />
              </div>
            </div>

            <button
              onClick={handleCheckCode}
              disabled={isLoading || !code.trim()}
              className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Check for Plagiarism</span>
                </>
              )}
            </button>
          </div>
        ) : (
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${
              dragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <Upload className={`w-16 h-16 mx-auto mb-4 ${
              dragActive ? 'text-primary-600' : 'text-gray-400'
            }`} />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {dragActive ? 'Drop your file here' : 'Upload a code file'}
            </h3>
            <p className="text-gray-600 mb-6">
              Drag and drop or click to browse
            </p>
            <label className="inline-block">
              <input
                type="file"
                onChange={handleFileInput}
                accept=".py,.txt,.js,.java,.cpp,.c,.go,.rs"
                className="hidden"
                disabled={isLoading}
              />
              <span className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-semibold py-3 px-8 rounded-lg cursor-pointer inline-flex items-center space-x-2 transition-colors">
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Upload className="w-5 h-5" />
                    <span>Select File</span>
                  </>
                )}
              </span>
            </label>
            <p className="text-sm text-gray-500 mt-4">
              Supported: .py, .txt, .js, .java, .cpp, .c, .go, .rs
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default CodeInput

