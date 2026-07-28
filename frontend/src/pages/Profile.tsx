import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog'
import { Pencil, Brain, Target } from 'lucide-react'
import { useAuthStore } from '@/stores/authStore'
import { useDataStore } from '@/stores/dataStore'

export default function Profile() {
  const { user, updateProfile } = useAuthStore()
  const { getOverallProgress, getAllSkills } = useDataStore()
  const [editOpen, setEditOpen] = useState(false)
  const [editName, setEditName] = useState(user?.name ?? '')
  const [editTitle, setEditTitle] = useState(user?.title ?? 'AI Engineer')

  const allSkills = getAllSkills()
  const completedSkills = allSkills.filter(
    (s) => useDataStore.getState().getSkillProgress(s.id) === 100,
  ).length

  const handleSave = async () => {
    if (editName.trim()) {
      await updateProfile({ name: editName.trim(), title: editTitle.trim() })
      setEditOpen(false)
    }
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-semibold text-text-primary">Profile</h1>
        <Dialog open={editOpen} onOpenChange={setEditOpen}>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm" className="gap-1.5">
              <Pencil size={14} />
              Edit
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Profile</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  placeholder="Your name"
                />
              </div>
              <div className="space-y-2">
                <Label>Title</Label>
                <Input
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  placeholder="e.g. AI Engineer"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="ghost" onClick={() => setEditOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleSave} disabled={!editName.trim()}>
                Save
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Profile Card */}
      <Card>
        <CardContent className="p-6 space-y-6">
          <div className="flex items-center gap-4">
            <Avatar className="h-16 w-16">
              <AvatarFallback className="bg-accent-signal/20 text-accent-signal text-xl font-bold">
                {user?.name?.charAt(0)?.toUpperCase() ?? 'A'}
              </AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-xl font-display font-semibold text-text-primary">
                {user?.name ?? 'User'}
              </h2>
              <p className="text-sm text-text-secondary">{user?.title ?? 'AI Engineer'}</p>
              <p className="text-xs text-text-muted font-mono mt-0.5">{user?.email ?? ''}</p>
            </div>
          </div>

          <Separator className="bg-border-hairline" />

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-3 p-3 rounded-md bg-bg-panel-raised">
              <Target className="w-5 h-5 text-accent-signal shrink-0" />
              <div>
                <p className="text-xs text-text-muted">Overall Progress</p>
                <p className="text-lg font-display font-semibold tabular text-text-primary">
                  {getOverallProgress()}%
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-md bg-bg-panel-raised">
              <Brain className="w-5 h-5 text-accent-signal shrink-0" />
              <div>
                <p className="text-xs text-text-muted">Skills Completed</p>
                <p className="text-lg font-display font-semibold tabular text-text-primary">
                  {completedSkills}/{allSkills.length}
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
