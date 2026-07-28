import { useState } from 'react'
import { Link, Outlet, useLocation } from 'react-router'

import {
  Brain,
  FolderOpen,
  LayoutDashboard,
  LogOut,
  Menu,
  Settings,
  User,
  X,
} from 'lucide-react'

import { useAuthStore } from '@/stores/authStore'
import { useUIStore } from '@/stores/uiStore'

const navItems = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard },
  { label: 'Categories', path: '/categories', icon: FolderOpen },
  { label: 'Profile', path: '/profile', icon: User },
  { label: 'Settings', path: '/settings', icon: Settings },
]

export default function AppLayout() {
  // No props needed
  const { logout, session } = useAuthStore()
  const { sidebarCollapsed, toggleSidebar } = useUIStore()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen flex bg-bg-base text-text-primary">
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:sticky top-0 left-0 z-50 lg:z-auto
          h-screen bg-bg-panel border-r border-border-hairline
          flex flex-col
          transition-all duration-300 ease-in-out
          ${sidebarCollapsed ? 'lg:w-16' : 'lg:w-64'}
          ${mobileOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-border-hairline">
          {!sidebarCollapsed && (
            <Link to="/" className="flex items-center gap-2">
              <Brain className="w-6 h-6 text-accent-signal" />
              <span className="font-display font-semibold text-lg tracking-tight">
                Career OS
              </span>
            </Link>
          )}
          <button
            type="button"
            onClick={toggleSidebar}
            className="hidden lg:flex p-1.5 rounded-md hover:bg-bg-panel-raised text-text-secondary transition-colors"
            aria-label="Toggle sidebar"
          >
            {sidebarCollapsed ? <Menu size={18} /> : <Menu size={18} />}
          </button>
          <button
            type="button"
            onClick={() => setMobileOpen(false)}
            className="lg:hidden p-1.5 rounded-md hover:bg-bg-panel-raised text-text-secondary"
            aria-label="Close sidebar"
          >
            <X size={18} />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
          {navItems.map(({ label, path, icon: Icon }) => {
            const isActive =
              location.pathname === path ||
              (path !== '/' && location.pathname.startsWith(path))
            return (
              <Link
                key={path}
                to={path}
                onClick={() => setMobileOpen(false)}
                className={`
                  flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors
                  ${
                    isActive
                      ? 'bg-accent-signal/10 text-accent-signal'
                      : 'text-text-secondary hover:text-text-primary hover:bg-bg-panel-raised'
                  }
                `}
                title={sidebarCollapsed ? label : undefined}
              >
                <Icon size={18} className="shrink-0" />
                {!sidebarCollapsed && label}
              </Link>
            )
          })}
        </nav>

        {/* User + Logout */}
        <div className="p-3 border-t border-border-hairline">
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 rounded-full bg-accent-signal/20 flex items-center justify-center text-accent-signal text-xs font-bold shrink-0">
              {session?.name?.charAt(0)?.toUpperCase() ?? 'A'}
            </div>
            {!sidebarCollapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-text-primary truncate">
                  {session?.name ?? 'User'}
                </p>
                <p className="text-xs text-text-muted truncate">
                  {session?.email ?? ''}
                </p>
              </div>
            )}
          </div>
          <button
            type="button"
            onClick={handleLogout}
            className={`
              mt-2 flex items-center gap-2 px-3 py-2 rounded-md text-sm text-text-secondary
              hover:text-accent-critical hover:bg-accent-critical/10 transition-colors w-full
              ${sidebarCollapsed ? 'justify-center' : ''}
            `}
            title={sidebarCollapsed ? 'Logout' : undefined}
          >
            <LogOut size={16} />
            {!sidebarCollapsed && 'Logout'}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 min-w-0">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center gap-3 p-4 border-b border-border-hairline bg-bg-panel">
          <button
            type="button"
            onClick={() => setMobileOpen(true)}
            className="p-1.5 rounded-md hover:bg-bg-panel-raised text-text-secondary"
            aria-label="Open sidebar"
          >
            <Menu size={20} />
          </button>
          <Brain className="w-5 h-5 text-accent-signal" />
          <span className="font-display font-semibold">Career OS</span>
        </div>

        <div className="p-4 lg:p-6 max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
