import React, { useState, useRef, useEffect } from 'react'
import { Send, Loader, BookOpen, Zap, AlertCircle } from 'lucide-react'
import QueryInterface from './components/QueryInterface'
import SourceCard from './components/SourceCard'
import Header from './components/Header'
import HealthStatus from './components/HealthStatus'

export default function App() {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [health, setHealth] = useState(null)
  const messagesEndRef = useRef(null)

  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8080'

  useEffect(() => {
    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const checkHealth = async () => {
    try {
      const response = await fetch(`${API_BASE}/health`)
      if (response.ok) {
        const data = await response.json()
        setHealth({ status: 'healthy', ...data })
        setError(null)
      } else {
        setHealth({ status: 'unhealthy' })
        setError('API is not responding correctly')
      }
    } catch (err) {
      setHealth({ status: 'error' })
      setError(`Cannot connect to API: ${err.message}`)
    }
  }

  const handleQuery = async (question) => {
    if (!question.trim()) return

    const userMessage = { type: 'user', content: question }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      const assistantMessage = {
        type: 'assistant',
        content: data.answer,
        sources: data.sources || []
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err.message)
      const errorMessage = {
        type: 'error',
        content: `Failed to get response: ${err.message}`
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />
      <HealthStatus health={health} onRetry={checkHealth} />

      <main className="max-w-4xl mx-auto px-4 py-8">
        {messages.length === 0 ? (
          <div className="space-y-8 py-12">
            <div className="text-center space-y-4">
              <h1 className="text-5xl font-bold gradient-text">
                Digital Nalanda
              </h1>
              <p className="text-xl text-slate-300">
                Explore Ancient Indian Scriptures with AI
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-4 mt-12">
              <div className="glass-effect p-6 rounded-lg space-y-3">
                <BookOpen className="w-8 h-8 text-blue-400" />
                <h3 className="font-semibold">Vedic Knowledge</h3>
                <p className="text-sm text-slate-400">
                  Access curated collection of sacred texts and commentaries
                </p>
              </div>
              <div className="glass-effect p-6 rounded-lg space-y-3">
                <Zap className="w-8 h-8 text-amber-400" />
                <h3 className="font-semibold">AI-Powered Search</h3>
                <p className="text-sm text-slate-400">
                  Ask questions and get contextual answers from scriptures
                </p>
              </div>
              <div className="glass-effect p-6 rounded-lg space-y-3">
                <BookOpen className="w-8 h-8 text-purple-400" />
                <h3 className="font-semibold">Source Citations</h3>
                <p className="text-sm text-slate-400">
                  Every answer is backed by original scripture references
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-6 mb-8">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-2xl ${
                  msg.type === 'user'
                    ? 'bg-blue-600 rounded-lg rounded-tr-none'
                    : msg.type === 'error'
                    ? 'bg-red-900 rounded-lg rounded-tl-none'
                    : 'glass-effect rounded-lg rounded-tl-none'
                } p-4`}>
                  <p className="text-white whitespace-pre-wrap">{msg.content}</p>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <p className="text-sm font-semibold text-slate-300">Sources:</p>
                      {msg.sources.map((source, sidx) => (
                        <SourceCard key={sidx} source={source} />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="glass-effect rounded-lg rounded-tl-none p-4 flex items-center gap-2">
                  <Loader className="w-5 h-5 animate-spin text-blue-400" />
                  <span className="text-slate-300">Searching scriptures...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}

        <QueryInterface onSubmit={handleQuery} disabled={loading} />
      </main>
    </div>
  )
}
