const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

interface ApiOptions extends RequestInit {
  unauthenticated?: boolean
}

function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

export async function apiFetch(path: string, options: ApiOptions = {}): Promise<Response> {
  const { unauthenticated, headers: customHeaders, ...rest } = options

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(customHeaders as Record<string, string>),
  }

  if (!unauthenticated) {
    const token = getToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...rest,
    headers,
  })

  if (response.status === 401 && !unauthenticated) {
    localStorage.removeItem('auth_token')
    window.location.href = '/login'
  }

  return response
}

export async function jsonFetch<T>(path: string, options: ApiOptions = {}): Promise<T> {
  const response = await apiFetch(path, options)
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export { API_BASE }
