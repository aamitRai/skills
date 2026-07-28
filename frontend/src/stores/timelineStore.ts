import { create } from 'zustand'

import type { LogLine } from '@/schemas'

interface TimelineState {
  lines: LogLine[]
  addLine: (message: string, type: LogLine['type']) => void
  clear: () => void
}

export const useTimelineStore = create<TimelineState>((set) => ({
  lines: [],

  addLine: (message: string, type: LogLine['type']) => {
    const line: LogLine = {
      id: `log-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
      timestamp: new Date().toISOString(),
      message,
      type,
    }
    set((state) => ({ lines: [line, ...state.lines].slice(0, 200) }))
  },

  clear: () => set({ lines: [] }),
}))
