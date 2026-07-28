import { jsonFetch } from './client'

export interface CategoryResponse {
  id: string
  name: string
  icon: string
  skills: SkillResponse[]
  created_at: string
  updated_at: string
}

export interface SkillResponse {
  id: string
  category_id: string
  name: string
  index: number
  priority: string
  difficulty: string
  estimated_hours: number | null
  created_at: string
  updated_at: string
}

export interface CategoryCreatePayload {
  name: string
  icon: string
}

export interface CategoryUpdatePayload {
  name?: string
  icon?: string
}

export interface SkillCreatePayload {
  name: string
  index?: number
  priority?: string
  difficulty?: string
  estimated_hours?: number | null
}

export interface SkillUpdatePayload {
  name?: string
  index?: number
  priority?: string
  difficulty?: string
  estimated_hours?: number | null
}

export interface SkillMovePayload {
  direction: 'up' | 'down'
}

export interface SkillMoveResponse {
  message: string
}

export const categoryApi = {
  async getAll(): Promise<CategoryResponse[]> {
    return jsonFetch<CategoryResponse[]>('/api/categories/')
  },

  async getById(categoryId: string): Promise<CategoryResponse> {
    return jsonFetch<CategoryResponse>(`/api/categories/${categoryId}`)
  },

  async create(payload: CategoryCreatePayload): Promise<CategoryResponse> {
    return jsonFetch<CategoryResponse>('/api/categories/', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async update(
    categoryId: string,
    payload: CategoryUpdatePayload,
  ): Promise<CategoryResponse> {
    return jsonFetch<CategoryResponse>(`/api/categories/${categoryId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  async delete(categoryId: string): Promise<void> {
    await jsonFetch<void>(`/api/categories/${categoryId}`, {
      method: 'DELETE',
    })
  },
}

export const skillApi = {
  async create(
    categoryId: string,
    payload: SkillCreatePayload,
  ): Promise<SkillResponse> {
    return jsonFetch<SkillResponse>(`/api/categories/${categoryId}/skills`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async getById(skillId: string): Promise<SkillResponse> {
    return jsonFetch<SkillResponse>(`/api/skills/${skillId}`)
  },

  async update(
    skillId: string,
    payload: SkillUpdatePayload,
  ): Promise<SkillResponse> {
    return jsonFetch<SkillResponse>(`/api/skills/${skillId}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  async delete(skillId: string): Promise<void> {
    await jsonFetch<void>(`/api/skills/${skillId}`, {
      method: 'DELETE',
    })
  },

  async move(
    skillId: string,
    payload: SkillMovePayload,
  ): Promise<SkillMoveResponse> {
    return jsonFetch<SkillMoveResponse>(`/api/skills/${skillId}/move`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },
}
