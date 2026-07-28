import { jsonFetch } from './client'

export interface ProgressResponse {
  skill_id: string
  progress: number
  status: string
  last_updated: string
}

export interface ProgressUpdatePayload {
  progress: number
}

export const progressApi = {
  async getAll(): Promise<ProgressResponse[]> {
    return jsonFetch<ProgressResponse[]>('/api/progress')
  },

  async getBySkillId(skillId: string): Promise<ProgressResponse> {
    return jsonFetch<ProgressResponse>(`/api/skills/${skillId}/progress`)
  },

  async update(
    skillId: string,
    payload: ProgressUpdatePayload,
  ): Promise<ProgressResponse> {
    return jsonFetch<ProgressResponse>(`/api/skills/${skillId}/progress`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },
}
