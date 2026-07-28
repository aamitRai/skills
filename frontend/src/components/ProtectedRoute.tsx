import { Navigate, Outlet, useLocation } from 'react-router'

import { useAuthStore } from '@/stores/authStore'

export default function ProtectedRoute() {
  const { isLoggedIn, initializing } = useAuthStore()
  const location = useLocation()

  // Wait for auth to finish initializing
  if (initializing) {
    return null
  }

  if (!isLoggedIn) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <Outlet />
}
