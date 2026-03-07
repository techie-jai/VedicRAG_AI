import React from 'react'
import { BookMarked } from 'lucide-react'

export default function SourceCard({ source }) {
  return (
    <div className="bg-slate-700/30 border border-slate-600 rounded p-3 text-sm">
      <div className="flex gap-2 mb-2">
        <BookMarked className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <p className="text-slate-200 line-clamp-2">{source.text}</p>
          {source.metadata && Object.keys(source.metadata).length > 0 && (
            <div className="mt-2 text-xs text-slate-400 space-y-1">
              {Object.entries(source.metadata).map(([key, value]) => (
                <div key={key}>
                  <span className="font-semibold">{key}:</span> {String(value).substring(0, 50)}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
