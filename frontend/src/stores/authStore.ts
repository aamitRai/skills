import { create } from 'zustand'

import { authApi, userApi, type LoginResponse, type UserProfile } from '@/api/auth.api'

interface AuthState {
  user: UserProfile | null
  token: string | null
  isLoggedIn: boolean
  initializing: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  updateProfile: (updates: { name?: string; title?: string }) => Promise<void>
  init: () => Promise<void>
}

function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

function getUser(): UserProfile | null {
  const raw = localStorage.getItem('auth_user')
  if (!raw || raw === 'undefined') return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isLoggedIn: false,
  initializing: true,

  init: async () => {
    const token = getToken()
    const user = getUser()
    if (token && user) {
      set({ user, token, isLoggedIn: true, initializing: false })
      return
    }
    set({ user: null, token: null, isLoggedIn: false, initializing: false })
  },

  login: async (email: string, password: string) => {
    const response: LoginResponse = await authApi.login({ email, password })
    localStorage.setItem('auth_token', response.access_token)
    localStorage.setItem('auth_user', JSON.stringify(response.user))
    set({
      user: response.user,
      token: response.access_token,
      isLoggedIn: true,
    })
  },

  logout: async () => {
    try {
      await authApi.logout()
    } catch {
      // ignore server error on logout
    }
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
    set({ user: null, token: null, isLoggedIn: false })
  },

  updateProfile: async (updates) => {
    const updated = await authApi.updateProfile(updates)
    localStorage.setItem('auth_user', JSON.stringify(updated))
    set({ user: updated })
  },
}))
