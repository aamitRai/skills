import { useEffect, useRef, useState } from 'react'
import { RouterProvider } from 'react-router'

import { useAuthStore } from '@/stores/authStore'
import { useDataStore } from '@/stores/dataStore'
import { useUIStore } from '@/stores/uiStore'
import router from './router'

function App() {
  const initialized = useRef(false)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (initialized.current) return
    initialized.current = true

    Promise.all([
      useAuthStore.getState().init(),
      useUIStore.getState().init(),
    ]).then(() => {
      // Only load data if user is authenticated
      if (useAuthStore.getState().isLoggedIn) {
        useDataStore.getState().load()
      }
      setReady(true)
    })
  }, [])

  if (!ready) {
    return null
  }

  return <RouterProvider router={router} />
}

export default App
