import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router'

import { format } from 'date-fns'
import { ArrowLeft, Plus, Trash2, Pencil, Check } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Slider } from '@/components/ui/slider'
import { Textarea } from '@/components/ui/textarea'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { commentApi, type CommentResponse } from '@/api/comments.api'
import { useDataStore } from '@/stores/dataStore'
import { useTimelineStore } from '@/stores/timelineStore'
import type { SkillResponse } from '@/api/categories.api'

const priorityVariant: Record<string, 'signal' | 'warn' | 'destructive' | 'default'> = {
  critical: 'destructive',
  high: 'warn',
  medium: 'signal',
  low: 'default',
}

const PRIORITY_OPTIONS = ['low', 'medium', 'high', 'critical'] as const
const DIFFICULTY_OPTIONS = ['beginner', 'intermediate', 'advanced', 'expert'] as const

export default function SkillDetail() {
  const { skillId } = useParams()
  const navigate = useNavigate()
  const { getSkillById, getSkillProgress, updateSkill, deleteSkill, updateProgress } = useDataStore()
  const addLine = useTimelineStore((state) => state.addLine)
  const skill = getSkillById(skillId ?? '')
  const [comments, setComments] = useState<CommentResponse[]>([])
  const [newComment, setNewComment] = useState('')
  const [editing, setEditing] = useState(false)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editForm, setEditForm] = useState<Partial<SkillResponse>>({})

  // Optimistic local progress state so slider updates immediately
  const [localProgress, setLocalProgress] = useState(getSkillProgress(skillId ?? ''))

  // Find parent category
  const parentCategory = useDataStore.getState().categories.find((c) =>
    c.skills.find((s) => s.id === skillId),
  )
  const categoryIcon = parentCategory?.icon ?? ''
  const categoryName = parentCategory?.name ?? ''

  // Load comments on mount
  useEffect(() => {
    if (!skillId) return
    commentApi.getBySkillId(skillId).then(setComments).catch(() => setComments([]))
  }, [skillId])

  if (!skill) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <p className="text-text-secondary">Skill not found.</p>
          <Link to="/categories">
            <Button variant="ghost" className="mt-4">
              <ArrowLeft size={16} />
              Back to Categories
            </Button>
          </Link>
        </div>
      </div>
    )
  }

  const handleProgressChange = (value: number[]) => {
    const p = value[0]
    setLocalProgress(p)
  }

  const handleProgressCommit = (value: number[]) => {
    const p = value[0]
    updateProgress(skillId!, p)
    addLine(`${skill.name} → ${p}%`, 'progress')
  }

  const handleAddComment = async () => {
    if (!newComment.trim() || !skillId) return
    await commentApi.create(skillId, { text: newComment.trim() })
    const updated = await commentApi.getBySkillId(skillId)
    setComments(updated)
    addLine(`Comment added to ${skill.name}`, 'comment')
    setNewComment('')
  }

  const handleDeleteComment = async (commentId: string) => {
    if (!skillId) return
    await commentApi.delete(skillId, commentId)
    setComments((prev) => prev.filter((c) => c.id !== commentId))
  }

  const handleSaveEdit = async () => {
    await updateSkill(skillId!, {
      priority: editForm.priority ?? skill.priority,
      difficulty: editForm.difficulty ?? skill.difficulty,
    })
    addLine(`${skill.name} updated`, 'status')
    setEditing(false)
    setEditForm({})
  }

  const handleDeleteSkill = async () => {
    await deleteSkill(skillId!)
    addLine(`${skill.name} deleted`, 'status')
    navigate(`/category/${parentCategory?.id ?? '/categories'}`)
  }

  const currentPriority = editForm.priority ?? skill.priority
  const currentDifficulty = editForm.difficulty ?? skill.difficulty

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Link
          to={`/category/${parentCategory?.id ?? '/categories'}`}
          className="inline-flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary transition-colors"
        >
          <ArrowLeft size={16} />
          Back
        </Link>
        <div className="mt-4 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-sm text-text-secondary mb-2">
              <span>{categoryIcon}</span>
              <span>{categoryName}</span>
            </div>
            <h1 className="text-2xl font-display font-semibold text-text-primary">{skill.name}</h1>
            {editing ? (
              <div className="flex items-center gap-3 mt-3 flex-wrap">
                <Select value={currentPriority} onValueChange={(v) => setEditForm(f => ({ ...f, priority: v as SkillResponse['priority'] }))}>
                  <SelectTrigger className="h-7 w-28 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {PRIORITY_OPTIONS.map((p) => (
                      <SelectItem key={p} value={p}>{p}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select value={currentDifficulty} onValueChange={(v) => setEditForm(f => ({ ...f, difficulty: v as SkillResponse['difficulty'] }))}>
                  <SelectTrigger className="h-7 w-32 text-xs">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {DIFFICULTY_OPTIONS.map((d) => (
                      <SelectItem key={d} value={d}>{d}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button size="sm" variant="ghost" onClick={handleSaveEdit} className="h-7 gap-1 text-xs">
                  <Check size={12} />
                  Save
                </Button>
                <Button size="sm" variant="ghost" onClick={() => { setEditing(false); setEditForm({}) }} className="h-7 text-xs">
                  Cancel
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2 mt-2">
                <Badge variant={priorityVariant[skill.priority] ?? 'default'}>{skill.priority}</Badge>
                <Badge variant="secondary">{skill.difficulty}</Badge>
                <button
                  onClick={() => {
                    setEditForm({ priority: skill.priority, difficulty: skill.difficulty })
                    setEditing(true)
                  }}
                  className="text-text-muted hover:text-text-primary transition-colors ml-1"
                  aria-label="Edit skill"
                >
                  <Pencil size={13} />
                </button>
              </div>
            )}
          </div>
          <Dialog open={deleteOpen} onOpenChange={setDeleteOpen}>
            <DialogTrigger asChild>
              <Button variant="destructive" size="sm">
                <Trash2 size={14} />
                Delete
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Delete Skill?</DialogTitle>
                <DialogDescription>
                  This will permanently delete <strong>{skill.name}</strong> and all associated progress and comments. This cannot be undone.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button variant="ghost" onClick={() => setDeleteOpen(false)}>
                  Cancel
                </Button>
                <Button variant="destructive" onClick={handleDeleteSkill}>
                  Delete Skill
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Progress Card */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-display font-semibold text-text-primary">Progress</h2>
            <span className="text-3xl font-display font-semibold tabular text-accent-signal">
              {localProgress}%
            </span>
          </div>

          <Slider
            value={[localProgress]}
            max={100}
            step={1}
            onValueChange={handleProgressChange}
            onValueCommit={handleProgressCommit}
            aria-label={`${skill.name} progress`}
          />

          <Progress value={localProgress} />

          <div className="flex items-center justify-between text-sm text-text-secondary">
            <span>
              {localProgress === 0 ? 'Not started' : localProgress === 100 ? 'Completed' : 'In progress'}
            </span>
            <span>{localProgress}% complete</span>
          </div>
        </CardContent>
      </Card>

      {/* Comments */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="font-display font-semibold text-text-primary">
            Comments ({comments.length})
          </h2>

          {/* Add comment */}
          <div className="space-y-2">
            <Textarea
              placeholder="Add a note..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              rows={3}
            />
            <Button size="sm" onClick={handleAddComment}>
              <Plus size={14} />
              Add Comment
            </Button>
          </div>

          {/* Comments list */}
          <div className="space-y-3">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className="p-3 rounded-md bg-bg-panel-raised border border-border-hairline space-y-1"
              >
                <p className="text-sm text-text-primary">{comment.text}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-text-muted font-mono">
                    {format(new Date(comment.created_at), 'MMM d, yyyy HH:mm')}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleDeleteComment(comment.id)}
                    className="text-text-muted hover:text-accent-critical transition-colors"
                    aria-label="Delete comment"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
            {comments.length === 0 && (
              <p className="text-sm text-text-muted text-center py-4">No comments yet.</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
