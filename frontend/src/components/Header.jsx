import React from 'react'
import { BookOpen } from 'lucide-react'

export default function Header() {
  return (
    <header className="border-b border-slate-700/50 glass-effect sticky top-0 z-50">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-lg">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Digital Nalanda</h1>
            <p className="text-xs text-slate-400">Vedic RAG System</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-400">Ancient Wisdom</p>
          <p className="text-xs text-slate-500">Modern Technology</p>
        </div>
      </div>
    </header>
  )
}
