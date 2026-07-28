import { z } from 'zod'

import type {
  AuthSession,
  CategoriesStore,
  CommentsStore,
  ProgressStore,
  Settings,
} from '@/schemas'
import {
  AuthSessionSchema,
  CategoriesStoreSchema,
  CommentsStoreSchema,
  ProgressStoreSchema,
  SettingsSchema,
} from '@/schemas'

const PREFIX = 'careeros:'

interface StorageEntry<T> {
  key: string
  schema: z.ZodType<T>
  fallback: T
}

function get<T>(entry: StorageEntry<T>): T {
  try {
    const raw = localStorage.getItem(entry.key)
    if (!raw) return entry.fallback
    return entry.schema.parse(JSON.parse(raw))
  } catch {
    return entry.fallback
  }
}

function set<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch {
    console.error('Failed to write to localStorage')
  }
}

function remove(key: string): void {
  localStorage.removeItem(key)
}

// ── Auth ──
const AUTH_KEY = `${PREFIX}auth`
export const authStorage = {
  get: () =>
    get<AuthSession>({
      key: AUTH_KEY,
      schema: AuthSessionSchema,
      fallback: null as unknown as AuthSession,
    }),
  set: (value: AuthSession) => set(AUTH_KEY, value),
  clear: () => remove(AUTH_KEY),
  isLoggedIn: () => {
    const session = authStorage.get()
    if (!session) return false
    return new Date(session.expiresAt) > new Date()
  },
}

// ── Progress ──
const PROGRESS_KEY = `${PREFIX}progress`
export const progressStorage = {
  get: (): ProgressStore =>
    get<ProgressStore>({
      key: PROGRESS_KEY,
      schema: ProgressStoreSchema,
      fallback: {},
    }),
  set: (value: ProgressStore) => set(PROGRESS_KEY, value),
  update: (skillId: string, delta: Partial<ProgressStore[string]>) => {
    const current = progressStorage.get()
    const existing = current[skillId] ?? {
      progress: 0,
      status: 'not-started' as const,
      lastUpdated: new Date().toISOString(),
    }
    current[skillId] = { ...existing, ...delta, lastUpdated: new Date().toISOString() }
    progressStorage.set(current)
  },
}

// ── Comments ──
const COMMENTS_KEY = `${PREFIX}comments`
export const commentsStorage = {
  get: (): CommentsStore =>
    get<CommentsStore>({
      key: COMMENTS_KEY,
      schema: CommentsStoreSchema,
      fallback: {},
    }),
  set: (value: CommentsStore) => set(COMMENTS_KEY, value),
  add: (skillId: string, text: string) => {
    const current = commentsStorage.get()
    const comment = {
      id: `${skillId}-${Date.now()}`,
      skillId,
      text,
      createdAt: new Date().toISOString(),
    }
    current[skillId] = [...(current[skillId] ?? []), comment]
    commentsStorage.set(current)
    return comment
  },
  delete: (skillId: string, commentId: string) => {
    const current = commentsStorage.get()
    current[skillId] = (current[skillId] ?? []).filter((c) => c.id !== commentId)
    commentsStorage.set(current)
  },
}

// ── Settings ──
const SETTINGS_KEY = `${PREFIX}settings`
export const settingsStorage = {
  get: (): Settings =>
    get<Settings>({
      key: SETTINGS_KEY,
      schema: SettingsSchema,
      fallback: { theme: 'dark', remember: true },
    }),
  set: (value: Settings) => set(SETTINGS_KEY, value),
  update: (delta: Partial<Settings>) => {
    const current = settingsStorage.get()
    settingsStorage.set({ ...current, ...delta })
  },
}

// ── Categories ──
const CATEGORIES_KEY = `${PREFIX}categories`
export const categoriesStorage = {
  get: (): CategoriesStore =>
    get<CategoriesStore>({
      key: CATEGORIES_KEY,
      schema: CategoriesStoreSchema,
      fallback: { categories: [] },
    }),
  set: (value: CategoriesStore) => set(CATEGORIES_KEY, value),
}

// ── Generic ──
export const storage = {
  remove,
  clearAll: () => {
    Object.keys(localStorage).forEach((key) => {
      if (key.startsWith(PREFIX)) localStorage.removeItem(key)
    })
  },
}
