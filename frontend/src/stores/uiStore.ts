import { create } from 'zustand'

import { settingsStorage } from '@/lib/storage'

interface UIState {
  theme: 'dark' | 'light'
  sidebarCollapsed: boolean
  searchQuery: string
  setSearchQuery: (query: string) => void
  toggleSidebar: () => void
  setTheme: (theme: 'dark' | 'light') => void
  init: () => void
}

export const useUIStore = create<UIState>((set) => ({
  theme: 'dark',
  sidebarCollapsed: false,
  searchQuery: '',

  init: () => {
    const settings = settingsStorage.get()
    set({ theme: settings.theme })
    // Apply theme to document
    document.documentElement.classList.toggle('dark', settings.theme === 'dark')
  },

  setSearchQuery: (query: string) => set({ searchQuery: query }),

  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

  setTheme: (theme: 'dark' | 'light') => {
    set({ theme })
    settingsStorage.update({ theme })
    document.documentElement.classList.toggle('dark', theme === 'dark')
  },
}))
