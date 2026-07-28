import { jsonFetch } from './client'

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserProfile
}

export interface UserProfile {
  id: string
  email: string
  name: string
  title: string
  avatar_url: string | null
}

export interface SettingsPayload {
  theme?: string
  remember?: boolean
}

export interface SettingsResponse {
  theme: string
  remember: boolean
}

export const authApi = {
  async login(payload: LoginPayload): Promise<LoginResponse> {
    return jsonFetch<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
      unauthenticated: true,
    })
  },

  async logout(): Promise<{ message: string }> {
    return jsonFetch('/api/auth/logout', { method: 'POST' })
  },

  async getMe(): Promise<UserProfile> {
    return jsonFetch<UserProfile>('/api/auth/me')
  },
}

export const userApi = {
  async getProfile(): Promise<UserProfile> {
    return jsonFetch<UserProfile>('/api/users/me/')
  },

  async updateProfile(updates: { name?: string; title?: string }): Promise<UserProfile> {
    return jsonFetch<UserProfile>('/api/users/me/', {
      method: 'PATCH',
      body: JSON.stringify(updates),
    })
  },

  async getSettings(): Promise<SettingsResponse> {
    return jsonFetch<SettingsResponse>('/api/users/me/settings')
  },

  async updateSettings(payload: SettingsPayload): Promise<SettingsResponse> {
    return jsonFetch<SettingsResponse>('/api/users/me/settings', {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
}
