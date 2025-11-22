import { AlertTriangle, CheckCircle, ExternalLink, AlertCircle, Loader2, FileSearch } from 'lucide-react'

const Results = ({ results, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center space-y-4">
          <Loader2 className="w-16 h-16 text-primary-600 animate-spin" />
          <h3 className="text-xl font-semibold text-gray-900">Analyzing your code...</h3>
          <p className="text-gray-600 text-center">
            Our AI is searching through GitHub repositories to detect similarities
          </p>
          <div className="flex space-x-2 mt-4">
            <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
            <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-primary-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
          </div>
        </div>
      </div>
    )
  }

  if (!results) {
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center text-center space-y-4">
          <FileSearch className="w-16 h-16 text-gray-400" />
          <h3 className="text-xl font-semibold text-gray-900">No results yet</h3>
          <p className="text-gray-600 max-w-md">
            Submit your code or upload a file to check for plagiarism. 
            Results will appear here.
          </p>
        </div>
      </div>
    )
  }

  if (!results.success) {
    return (
      <div className="bg-white rounded-2xl shadow-lg border border-red-200 p-8">
        <div className="flex items-start space-x-4">
          <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-xl font-semibold text-red-900 mb-2">Analysis Failed</h3>
            <p className="text-red-700">{results.error || 'An unknown error occurred'}</p>
          </div>
        </div>
      </div>
    )
  }

  const comparisons = results.comparisons || []
  const hasPlagiarism = comparisons.length > 0
  const highSimilarities = comparisons.filter(c => c.similarity_percent >= 70)
  const mediumSimilarities = comparisons.filter(c => c.similarity_percent >= 40 && c.similarity_percent < 70)
  const lowSimilarities = comparisons.filter(c => c.similarity_percent < 40)

  const getSimilarityColor = (percent) => {
    if (percent >= 70) return 'text-red-600'
    if (percent >= 40) return 'text-yellow-600'
    return 'text-green-600'
  }

  const getSimilarityBgColor = (percent) => {
    if (percent >= 70) return 'bg-red-50 border-red-200'
    if (percent >= 40) return 'bg-yellow-50 border-yellow-200'
    return 'bg-green-50 border-green-200'
  }

  const getSimilarityBadgeColor = (percent) => {
    if (percent >= 70) return 'bg-red-100 text-red-800'
    if (percent >= 40) return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
      {/* Header Summary */}
      <div className={`p-6 ${hasPlagiarism ? 
        (highSimilarities.length > 0 ? 'bg-red-50 border-b border-red-200' : 
         mediumSimilarities.length > 0 ? 'bg-yellow-50 border-b border-yellow-200' : 
         'bg-green-50 border-b border-green-200') 
        : 'bg-green-50 border-b border-green-200'}`}>
        <div className="flex items-start space-x-4">
          {hasPlagiarism ? (
            highSimilarities.length > 0 ? (
              <AlertTriangle className="w-10 h-10 text-red-600 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-10 h-10 text-yellow-600 flex-shrink-0" />
            )
          ) : (
            <CheckCircle className="w-10 h-10 text-green-600 flex-shrink-0" />
          )}
          
          <div className="flex-1">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {hasPlagiarism ? 'Similarities Detected' : 'No Plagiarism Detected'}
            </h3>
            <p className="text-gray-700">
              {hasPlagiarism 
                ? `Found ${comparisons.length} potential match${comparisons.length !== 1 ? 'es' : ''} in GitHub repositories`
                : 'Your code appears to be original. No significant similarities found.'}
            </p>
            
            {hasPlagiarism && (
              <div className="flex flex-wrap gap-2 mt-3">
                {highSimilarities.length > 0 && (
                  <span className="px-3 py-1 bg-red-100 text-red-800 text-sm font-medium rounded-full">
                    {highSimilarities.length} High Risk
                  </span>
                )}
                {mediumSimilarities.length > 0 && (
                  <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm font-medium rounded-full">
                    {mediumSimilarities.length} Medium Risk
                  </span>
                )}
                {lowSimilarities.length > 0 && (
                  <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                    {lowSimilarities.length} Low Risk
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Results List */}
      {hasPlagiarism && (
        <div className="p-6 max-h-[600px] overflow-y-auto">
          <div className="space-y-4">
            {comparisons.map((match, index) => (
              <div
                key={index}
                className={`border rounded-xl p-5 transition-all hover:shadow-md ${getSimilarityBgColor(match.similarity_percent)}`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h4 className="font-semibold text-gray-900 text-lg">
                        {match.block_name || `Code Block ${index + 1}`}
                      </h4>
                      <span className={`px-3 py-1 text-sm font-bold rounded-full ${getSimilarityBadgeColor(match.similarity_percent)}`}>
                        {match.similarity_percent}% Similar
                      </span>
                    </div>
                    
                    {match.source_repo && (
                      <p className="text-sm text-gray-700 mb-2">
                        <span className="font-medium">Repository:</span> {match.source_repo}
                      </p>
                    )}
                    
                    {match.reason && (
                      <p className="text-sm text-gray-600 mb-3 italic">
                        "{match.reason}"
                      </p>
                    )}
                  </div>
                </div>

                {match.source_url && (
                  <a
                    href={match.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`inline-flex items-center space-x-2 text-sm font-medium hover:underline ${getSimilarityColor(match.similarity_percent)}`}
                  >
                    <span>View Source</span>
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Results

