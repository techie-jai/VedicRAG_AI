import React from 'react'
import { AlertCircle, CheckCircle, RefreshCw } from 'lucide-react'

export default function HealthStatus({ health, onRetry }) {
  if (!health) return null

  const isHealthy = health.status === 'healthy'

  return (
    <div className={`border-b ${isHealthy ? 'border-green-900/50 bg-green-900/10' : 'border-red-900/50 bg-red-900/10'}`}>
      <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          {isHealthy ? (
            <CheckCircle className="w-5 h-5 text-green-400" />
          ) : (
            <AlertCircle className="w-5 h-5 text-red-400" />
          )}
          <div className="text-sm">
            {isHealthy ? (
              <p className="text-green-300">
                System operational • Ollama: {health.ollama_base_url} • ChromaDB: {health.chroma_host}:{health.chroma_port}
              </p>
            ) : (
              <p className="text-red-300">
                System not ready. Please check if all services are running.
              </p>
            )}
          </div>
        </div>
        {!isHealthy && (
          <button
            onClick={onRetry}
            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm text-white transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        )}
      </div>
    </div>
  )
}
