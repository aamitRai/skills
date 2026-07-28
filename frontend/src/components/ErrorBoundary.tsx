import { useRouteError } from 'react-router'

export default function ErrorBoundary() {
  // No props needed
  const error = useRouteError() as Error | undefined

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg-base">
      <div className="text-center space-y-4 max-w-md px-4">
        <div className="text-6xl">⚠️</div>
        <h1 className="text-2xl font-semibold font-display text-text-primary">
          Something went wrong
        </h1>
        <p className="text-text-secondary text-sm">
          {error?.message ?? 'An unexpected error occurred.'}
        </p>
        <button
          type="button"
          className="px-4 py-2 rounded-md bg-accent-signal/10 text-accent-signal text-sm font-medium hover:bg-accent-signal/20 transition-colors"
          onClick={() => window.location.reload()}
        >
          Reload page
        </button>
      </div>
    </div>
  )
}
