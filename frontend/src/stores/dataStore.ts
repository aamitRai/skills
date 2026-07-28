import { create } from 'zustand'

import {
  categoryApi,
  skillApi,
  type CategoryResponse,
  type SkillResponse,
} from '@/api/categories.api'
import { progressApi, type ProgressResponse } from '@/api/progress.api'

interface DataState {
  categories: CategoryResponse[]
  progressMap: Record<string, ProgressResponse>
  loading: boolean
  error: string | null
  load: () => Promise<void>
  refresh: () => Promise<void>
  getSkillById: (skillId: string) => SkillResponse | undefined
  getCategoryById: (categoryId: string) => CategoryResponse | undefined
  getAllSkills: () => SkillResponse[]
  getSkillProgress: (skillId: string) => number
  getCategoryProgress: (categoryId: string) => number
  getOverallProgress: () => number
  createCategory: (name: string, icon: string) => Promise<void>
  renameCategory: (categoryId: string, name: string) => Promise<void>
  deleteCategory: (categoryId: string) => Promise<void>
  addSkill: (
    categoryId: string,
    skill: { name: string; priority?: string; difficulty?: string; estimated_hours?: number | null },
  ) => Promise<void>
  updateSkill: (
    skillId: string,
    updates: { name?: string; priority?: string; difficulty?: string; estimated_hours?: number | null },
  ) => Promise<void>
  deleteSkill: (skillId: string) => Promise<void>
  moveSkill: (skillId: string, direction: 'up' | 'down') => Promise<void>
  updateProgress: (skillId: string, progress: number) => Promise<void>
}

export const useDataStore = create<DataState>((set, get) => ({
  categories: [],
  progressMap: {},
  loading: false,
  error: null,

  load: async () => {
    set({ loading: true, error: null })
    try {
      const [categories, progressList] = await Promise.all([
        categoryApi.getAll(),
        progressApi.getAll(),
      ])
      const progressMap: Record<string, ProgressResponse> = {}
      for (const p of progressList) {
        progressMap[p.skill_id] = p
      }
      set({ categories, progressMap, loading: false })
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load data'
      set({ error: message, loading: false })
    }
  },

  refresh: async () => {
    await get().load()
  },

  getSkillById: (skillId: string) => {
    const { categories } = get()
    for (const cat of categories) {
      const skill = cat.skills.find((s) => s.id === skillId)
      if (skill) return skill
    }
    return undefined
  },

  getCategoryById: (categoryId: string) => {
    return get().categories.find((c) => c.id === categoryId)
  },

  getAllSkills: () => {
    return get().categories.flatMap((c) => c.skills)
  },

  getSkillProgress: (skillId: string) => {
    return get().progressMap[skillId]?.progress ?? 0
  },

  getCategoryProgress: (categoryId: string) => {
    const category = get().getCategoryById(categoryId)
    if (!category || category.skills.length === 0) return 0
    const total = category.skills.reduce((sum, skill) => {
      return sum + get().getSkillProgress(skill.id)
    }, 0)
    return Math.round(total / category.skills.length)
  },

  getOverallProgress: () => {
    const allSkills = get().getAllSkills()
    if (allSkills.length === 0) return 0
    const total = allSkills.reduce((sum, skill) => {
      return sum + get().getSkillProgress(skill.id)
    }, 0)
    return Math.round(total / allSkills.length)
  },

  createCategory: async (name: string, icon: string) => {
    const created = await categoryApi.create({ name, icon })
    set((state) => ({
      categories: [...state.categories, created],
    }))
  },

  renameCategory: async (categoryId: string, name: string) => {
    const updated = await categoryApi.update(categoryId, { name })
    set((state) => ({
      categories: state.categories.map((c) =>
        c.id === categoryId ? updated : c,
      ),
    }))
  },

  deleteCategory: async (categoryId: string) => {
    await categoryApi.delete(categoryId)
    set((state) => ({
      categories: state.categories.filter((c) => c.id !== categoryId),
    }))
  },

  addSkill: async (categoryId: string, skill) => {
    const created = await skillApi.create(categoryId, skill)
    set((state) => ({
      categories: state.categories.map((c) =>
        c.id === categoryId
          ? { ...c, skills: [...c.skills, created] }
          : c,
      ),
    }))
  },

  updateSkill: async (skillId: string, updates) => {
    const updated = await skillApi.update(skillId, updates)
    set((state) => ({
      categories: state.categories.map((c) => ({
        ...c,
        skills: c.skills.map((s) =>
          s.id === skillId ? updated : s,
        ),
      })),
    }))
  },

  deleteSkill: async (skillId: string) => {
    await skillApi.delete(skillId)
    set((state) => ({
      categories: state.categories.map((c) => ({
        ...c,
        skills: c.skills.filter((s) => s.id !== skillId),
      })),
      progressMap: Object.fromEntries(
        Object.entries(state.progressMap).filter(
          ([id]) => id !== skillId,
        ),
      ),
    }))
  },

  moveSkill: async (skillId: string, direction: 'up' | 'down') => {
    await skillApi.move(skillId, { direction })
    const state = get()
    const cat = state.categories.find((c) => c.skills.some((s) => s.id === skillId))
    if (cat) {
      const updated = await categoryApi.getById(cat.id)
      set({
        categories: state.categories.map((c) =>
          c.id === cat.id ? updated : c,
        ),
      })
    }
  },

  updateProgress: async (skillId: string, progress: number) => {
    const updated = await progressApi.update(skillId, { progress })
    set((state) => ({
      progressMap: { ...state.progressMap, [skillId]: updated },
    }))
  },
}))
