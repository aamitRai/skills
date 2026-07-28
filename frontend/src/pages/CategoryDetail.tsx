import { useCallback, useRef, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router'
import { motion } from 'framer-motion'
import { ArrowLeft, Plus, Trash2, Pencil } from 'lucide-react'
import { toast } from 'sonner'

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
  DialogDescription,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import SkillCard from '@/components/SkillCard'
import { useDataStore } from '@/stores/dataStore'
import { useTimelineStore } from '@/stores/timelineStore'

const PRIORITY_OPTIONS = ['low', 'medium', 'high', 'critical'] as const
const DIFFICULTY_OPTIONS = ['beginner', 'intermediate', 'advanced', 'expert'] as const

export default function CategoryDetail() {
  const { categoryId } = useParams()
  const navigate = useNavigate()
  const {
    getCategoryById,
    getSkillProgress,
    addSkill,
    deleteSkill,
    moveSkill,
    renameCategory,
    deleteCategory,
    updateProgress,
  } = useDataStore()
  const addLine = useTimelineStore((state) => state.addLine)
  const category = getCategoryById(categoryId ?? '')
  const debounceRef = useRef<Record<string, ReturnType<typeof setTimeout>>>({})

  // Add skill form state
  const [addOpen, setAddOpen] = useState(false)
  const [newSkillName, setNewSkillName] = useState('')
  const [newSkillPriority, setNewSkillPriority] = useState<'low' | 'medium' | 'high' | 'critical'>('medium')
  const [newSkillDifficulty, setNewSkillDifficulty] = useState<'beginner' | 'intermediate' | 'advanced' | 'expert'>('intermediate')

  // Delete category dialog
  const [deleteCatOpen, setDeleteCatOpen] = useState(false)

  // Rename category inline
  const [renaming, setRenaming] = useState(false)
  const [renameValue, setRenameValue] = useState('')

  // Move skill loading state
  const [moveLoadingId, setMoveLoadingId] = useState<string | null>(null)

  // All hooks must be above any early returns
  const handleProgressChange = useCallback((skillId: string, value: number[]) => {
    const progress = value[0]

    if (debounceRef.current[skillId]) clearTimeout(debounceRef.current[skillId])
    debounceRef.current[skillId] = setTimeout(() => {
      updateProgress(skillId, progress)
    }, 300)
  }, [updateProgress])

  const handleProgressCommit = useCallback((skillId: string, value: number[]) => {
    const progress = value[0]
    const skill = useDataStore.getState().getSkillById(skillId)
    addLine(`${skill?.name ?? skillId} → ${progress}%`, 'progress')
  }, [addLine])

  if (!category) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <p className="text-text-secondary">Category not found.</p>
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

  const handleAddSkill = async () => {
    if (!newSkillName.trim()) return
    await addSkill(categoryId!, {
      name: newSkillName.trim(),
      priority: newSkillPriority,
      difficulty: newSkillDifficulty,
    })
    addLine(`Skill "${newSkillName.trim()}" added to ${category.name}`, 'status')
    setNewSkillName('')
    setNewSkillPriority('medium')
    setNewSkillDifficulty('intermediate')
    setAddOpen(false)
  }

  const handleDeleteSkill = async (skillId: string) => {
    const skill = useDataStore.getState().getSkillById(skillId)
    await deleteSkill(skillId)
    addLine(`Skill "${skill?.name ?? skillId}" deleted`, 'status')
  }

  const handleMoveSkill = async (skillId: string, direction: 'up' | 'down') => {
    setMoveLoadingId(skillId)
    try {
      await moveSkill(skillId, direction)
    } catch (err) {
      toast.error('Failed to move skill')
    } finally {
      setMoveLoadingId(null)
    }
  }

  const handleRenameCategory = async () => {
    if (!renameValue.trim()) return
    await renameCategory(categoryId!, renameValue.trim())
    addLine(`Category renamed to "${renameValue.trim()}"`, 'status')
    setRenaming(false)
  }

  const handleDeleteCategory = async () => {
    await deleteCategory(categoryId!)
    addLine(`Category "${category.name}" deleted`, 'status')
    navigate('/categories')
  }

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.04 },
    },
  } as const
  const item = {
    hidden: { opacity: 0, y: 12 },
    show: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' as const } },
  } as const

  // Compute average progress for the category
  const avgProgress = category.skills.length > 0
    ? Math.round(category.skills.reduce((sum, s) => sum + getSkillProgress(s.id), 0) / category.skills.length)
    : 0

  return (
    <div className="space-y-5">
      {/* Header */}
      <div>
        <Link to="/categories" className="inline-flex items-center gap-1.5 text-xs font-medium text-text-muted hover:text-text-primary transition-colors">
          <ArrowLeft size={14} />
          Back to Categories
        </Link>
        <div className="mt-3 flex items-start gap-3">
          <span className="text-3xl mt-0.5">{category.icon}</span>
          <div className="flex-1">
            {renaming ? (
              <div className="flex items-center gap-2">
                <Input
                  value={renameValue}
                  onChange={(e) => setRenameValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleRenameCategory()
                    if (e.key === 'Escape') { setRenaming(false); setRenameValue(category.name) }
                  }}
                  onBlur={() => handleRenameCategory()}
                  autoFocus
                  className="h-8 text-xl font-display font-semibold"
                />
              </div>
            ) : (
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-2xl font-display font-semibold text-text-primary">{category.name}</h1>
                  <button
                    onClick={() => { setRenameValue(category.name); setRenaming(true) }}
                    className="text-text-muted hover:text-text-primary transition-colors"
                    aria-label="Rename category"
                  >
                    <Pencil size={14} />
                  </button>
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-sm text-text-secondary">{category.skills.length} skill{category.skills.length !== 1 ? 's' : ''}</span>
                  <span className="text-text-muted">•</span>
                  <span className="text-sm text-text-secondary">{avgProgress}% average progress</span>
                </div>
              </div>
            )}
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <Dialog open={addOpen} onOpenChange={setAddOpen}>
              <DialogTrigger asChild>
                <Button size="sm" className="gap-1.5">
                  <Plus size={14} />
                  Add Skill
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add Skill</DialogTitle>
                  <DialogDescription>Add a new skill to {category.name}</DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label>Name</Label>
                    <Input
                      placeholder="e.g. PyTorch"
                      value={newSkillName}
                      onChange={(e) => setNewSkillName(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleAddSkill()}
                      autoFocus
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Priority</Label>
                      <Select value={newSkillPriority} onValueChange={(v) => setNewSkillPriority(v as any)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {PRIORITY_OPTIONS.map((p) => (
                            <SelectItem key={p} value={p}>{p}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Difficulty</Label>
                      <Select value={newSkillDifficulty} onValueChange={(v) => setNewSkillDifficulty(v as any)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {DIFFICULTY_OPTIONS.map((d) => (
                            <SelectItem key={d} value={d}>{d}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
                <DialogFooter>
                  <Button variant="ghost" onClick={() => setAddOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleAddSkill} disabled={!newSkillName.trim()}>
                    Add Skill
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            <Dialog open={deleteCatOpen} onOpenChange={setDeleteCatOpen}>
              <DialogTrigger asChild>
                <Button variant="destructive" size="sm">
                  <Trash2 size={14} />
                  Delete
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Delete Category?</DialogTitle>
                  <DialogDescription>
                    This will permanently delete <strong>{category.name}</strong> and all {category.skills.length} skills within it. This cannot be undone.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <Button variant="ghost" onClick={() => setDeleteCatOpen(false)}>
                    Cancel
                  </Button>
                  <Button variant="destructive" onClick={handleDeleteCategory}>
                    Delete Category
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </div>

      {/* Skills list */}
      {category.skills.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-text-secondary text-sm">No skills in this category yet.</p>
          <Button className="mt-3" size="sm" onClick={() => setAddOpen(true)}>
            <Plus size={14} />
            Add your first skill
          </Button>
        </div>
      ) : (
        <motion.div variants={container} initial="hidden" animate="show" className="space-y-2">
          {category.skills.map((skill, index) => {
            const progress = getSkillProgress(skill.id)
            const isMoveLoading = moveLoadingId === skill.id

            return (
              <motion.div key={skill.id} variants={item}>
                <SkillCard
                  skill={skill}
                  progress={progress}
                  onProgressChange={handleProgressChange}
                  onProgressCommit={handleProgressCommit}
                  onDelete={() => handleDeleteSkill(skill.id)}
                  onMoveUp={() => handleMoveSkill(skill.id, 'up')}
                  onMoveDown={() => handleMoveSkill(skill.id, 'down')}
                  disableMoveUp={index === 0}
                  disableMoveDown={index === category.skills.length - 1}
                  moveLoading={isMoveLoading}
                />
              </motion.div>
            )
          })}
        </motion.div>
      )}
    </div>
  )
}
