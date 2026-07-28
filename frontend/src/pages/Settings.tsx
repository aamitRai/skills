import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Separator } from '@/components/ui/separator'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { useAuthStore } from '@/stores/authStore'
import { useUIStore } from '@/stores/uiStore'
import { storage } from '@/lib/storage'
import { Moon, Sun, Trash2, LogOut } from 'lucide-react'

export default function Settings() {
  const { logout } = useAuthStore()
  const { theme, setTheme } = useUIStore()
  const [resetOpen, setResetOpen] = useState(false)

  const handleReset = () => {
    storage.clearAll()
    setResetOpen(false)
    window.location.reload()
  }

  const handleLogout = async () => {
    await logout()
    window.location.href = '/login'
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <h1 className="text-2xl font-display font-semibold text-text-primary">Settings</h1>

      {/* Appearance */}
      <Card>
        <CardHeader>
          <CardTitle>Appearance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {theme === 'dark' ? (
                <Moon size={18} className="text-text-secondary" />
              ) : (
                <Sun size={18} className="text-text-secondary" />
              )}
              <div>
                <Label>Dark Mode</Label>
                <p className="text-xs text-text-muted">
                  {theme === 'dark' ? 'Dark theme active' : 'Light theme active'}
                </p>
              </div>
            </div>
            <Switch
              checked={theme === 'dark'}
              onCheckedChange={(checked) => setTheme(checked ? 'dark' : 'light')}
            />
          </div>
        </CardContent>
      </Card>

      {/* Data */}
      <Card>
        <CardHeader>
          <CardTitle>Data</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Separator className="bg-border-hairline" />

          <Dialog open={resetOpen} onOpenChange={setResetOpen}>
            <DialogTrigger asChild>
              <Button variant="destructive" className="w-full justify-start">
                <Trash2 size={16} />
                Reset All Progress
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Reset All Progress?</DialogTitle>
                <DialogDescription>
                  This will permanently delete all your progress and comments. This action cannot be undone.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button variant="ghost" onClick={() => setResetOpen(false)}>
                  Cancel
                </Button>
                <Button variant="destructive" onClick={handleReset}>
                  Reset Everything
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </CardContent>
      </Card>

      {/* Account */}
      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
        </CardHeader>
        <CardContent>
          <Button variant="outline" className="w-full justify-start" onClick={handleLogout}>
            <LogOut size={16} />
            Sign Out
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
