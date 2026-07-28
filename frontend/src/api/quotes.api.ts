import { jsonFetch } from './client'

export interface QuoteResponse {
  id: string
  text: string
  author: string
}

export const quotesApi = {
  async getAll(): Promise<QuoteResponse[]> {
    return jsonFetch<QuoteResponse[]>('/api/quotes/')
  },

  async getToday(): Promise<QuoteResponse | null> {
    return jsonFetch<QuoteResponse | null>('/api/quotes/today')
  },
}
