import { createBrowserRouter } from 'react-router'

import AppLayout from '@/components/AppLayout'
import ErrorBoundary from '@/components/ErrorBoundary'
import ProtectedRoute from '@/components/ProtectedRoute'
import Categories from '@/pages/Categories'
import CategoryDetail from '@/pages/CategoryDetail'
import Dashboard from '@/pages/Dashboard'
import LoginPage from '@/pages/LoginPage'
import Profile from '@/pages/Profile'
import Settings from '@/pages/Settings'
import SkillDetail from '@/pages/SkillDetail'

const router = createBrowserRouter(
  [
    {
      path: '/login',
      element: <LoginPage />,
      errorElement: <ErrorBoundary />,
    },
    {
      element: <AppLayout />,
      errorElement: <ErrorBoundary />,
      children: [
        {
          element: <ProtectedRoute />,
          children: [
            { path: '/', element: <Dashboard /> },
            { path: '/categories', element: <Categories /> },
            { path: '/category/:categoryId', element: <CategoryDetail /> },
            { path: '/skill/:skillId', element: <SkillDetail /> },
            { path: '/profile', element: <Profile /> },
            { path: '/settings', element: <Settings /> },
          ],
        },
      ],
    },
    {
      path: '*',
      element: <LoginPage />,
    },
  ],
  {
    basename: '/',
  },
)

export default router
