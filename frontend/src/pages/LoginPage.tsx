import { useActionState, useEffect, useState } from 'react'
import { useNavigate } from 'react-router'

import { Brain, Eye, EyeOff, Loader2 } from 'lucide-react'

import { useAuthStore } from '@/stores/authStore'

const initialState = {
  error: '',
  email: '',
}

async function loginAction(
  _prevState: typeof initialState,
  formData: FormData,
): Promise<typeof initialState> {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  if (!email || !password) {
    return { error: 'Email and password are required.', email }
  }

  try {
    const { login } = useAuthStore.getState()
    await login(email, password)
    return { error: '', email: '' }
  } catch {
    return { error: 'Invalid email or password.', email }
  }
}

export default function LoginPage() {
  const [state, formAction, pending] = useActionState(loginAction, initialState)
  const navigate = useNavigate()
  const { isLoggedIn } = useAuthStore()
  const [showPassword, setShowPassword] = useState(false)

  // Redirect if already logged in
  useEffect(() => {
    if (isLoggedIn) {
      navigate('/', { replace: true })
    }
  }, [isLoggedIn, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg-base px-4">
      <div className="w-full max-w-md space-y-8">
        {/* Logo */}
        <div className="text-center space-y-2">
          <div className="flex justify-center">
            <div className="w-14 h-14 rounded-xl bg-accent-signal/10 flex items-center justify-center">
              <Brain className="w-8 h-8 text-accent-signal" />
            </div>
          </div>
          <h1 className="text-2xl font-display font-semibold text-text-primary">
            Career OS
          </h1>
          <p className="text-sm text-text-secondary">
            Sign in to your mission control
          </p>
        </div>

        {/* Form */}
        <form action={formAction} className="space-y-5">
          {state.error && (
            <div className="p-3 rounded-md bg-accent-critical/10 border border-accent-critical/20 text-accent-critical text-sm" role="alert">
              {state.error}
            </div>
          )}

          <div className="space-y-1.5">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-text-secondary"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              defaultValue={state.email}
              required
              autoComplete="email"
              className="w-full px-3 py-2.5 rounded-md bg-bg-panel border border-border-hairline text-text-primary text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-signal/40 focus:border-accent-signal/40 transition-colors"
              placeholder="engineer@career.os"
            />
          </div>

          <div className="space-y-1.5">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-text-secondary"
            >
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                required
                autoComplete="current-password"
                className="w-full px-3 py-2.5 rounded-md bg-bg-panel border border-border-hairline text-text-primary text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-accent-signal/40 focus:border-accent-signal/40 transition-colors pr-10"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-secondary transition-colors"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={pending}
            className="w-full py-2.5 rounded-md bg-accent-signal/10 text-accent-signal font-medium text-sm hover:bg-accent-signal/20 focus:outline-none focus:ring-2 focus:ring-accent-signal/40 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {pending ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Signing in...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>


      </div>
    </div>
  )
}
