import { jsonFetch } from './client'

export interface DashboardSummary {
  total_categories: number
  total_skills: number
  completed_skills: number
  in_progress_skills: number
  overall_progress: number
  recently_updated: RecentlyUpdatedSkill[]
}

export interface RecentlyUpdatedSkill {
  skill_id: string
  skill_name: string
  category_name: string
  progress: number
  last_updated: string
}

export interface ActivityItem {
  id: string
  type: string
  skill_id: string
  skill_name: string
  category_name: string
  description: string
  timestamp: string
}

export const dashboardApi = {
  async getSummary(): Promise<DashboardSummary> {
    return jsonFetch<DashboardSummary>('/api/dashboard/summary')
  },

  async getActivity(): Promise<ActivityItem[]> {
    return jsonFetch<ActivityItem[]>('/api/dashboard/activity')
  },
}
