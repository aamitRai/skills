import { jsonFetch } from './client'

export interface CommentResponse {
  id: string
  skill_id: string
  text: string
  created_at: string
}

export interface CommentCreatePayload {
  text: string
}

export const commentApi = {
  async getBySkillId(skillId: string): Promise<CommentResponse[]> {
    return jsonFetch<CommentResponse[]>(`/api/skills/${skillId}/comments`)
  },

  async create(
    skillId: string,
    payload: CommentCreatePayload,
  ): Promise<CommentResponse> {
    return jsonFetch<CommentResponse>(`/api/skills/${skillId}/comments`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async delete(skillId: string, commentId: string): Promise<void> {
    await jsonFetch<void>(`/api/skills/${skillId}/comments/${commentId}`, {
      method: 'DELETE',
    })
  },
}
