import { useState } from 'react'
import { Link } from 'react-router'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Slider } from '@/components/ui/slider'
import { ArrowUp, ArrowDown, Trash2, Flag, Layers } from 'lucide-react'
import type { SkillResponse } from '@/api/categories.api'

const priorityVariant: Record<string, 'signal' | 'warn' | 'destructive' | 'default'> = {
  critical: 'destructive',
  high: 'warn',
  medium: 'signal',
  low: 'default',
}

interface SkillCardProps {
  skill: SkillResponse
  progress: number
  onProgressChange?: (skillId: string, value: number[]) => void
  onProgressCommit?: (skillId: string, value: number[]) => void
  onDelete?: () => void
  onMoveUp?: () => void
  onMoveDown?: () => void
  disableMoveUp?: boolean
  disableMoveDown?: boolean
  moveLoading?: boolean
}

export default function SkillCard({
  skill,
  progress,
  onProgressChange,
  onProgressCommit,
  onDelete,
  onMoveUp,
  onMoveDown,
  disableMoveUp,
  disableMoveDown,
  moveLoading,
}: SkillCardProps) {
  const [editing, setEditing] = useState(false)

  const displayProgress = progress === 0 ? 'Not Started' : `${progress}%`

  return (
    <Card className="group border-border/50 hover:border-accent-signal/40 hover:shadow-lg hover:shadow-accent-signal/5 transition-all duration-200 hover:-translate-y-0.5">
      <CardContent className="p-3.5 space-y-2.5">
        {/* Top row: name + actions */}
        <div className="flex items-center justify-between gap-3">
          <div className="flex-1 min-w-0">
            <Link to={`/skill/${skill.id}`} className="block">
              <h3 className="font-semibold text-sm text-text-primary group-hover:text-accent-signal transition-colors truncate">
                {skill.name}
              </h3>
            </Link>
            <div className="flex items-center gap-1.5 mt-1">
              <Badge variant={priorityVariant[skill.priority] ?? 'default'} className="text-[10px] px-1.5 py-0 h-5 gap-1 font-medium">
                <Flag size={9} />
                {skill.priority}
              </Badge>
              <Badge variant="secondary" className="text-[10px] px-1.5 py-0 h-5 gap-1 font-medium">
                <Layers size={9} />
                {skill.difficulty}
              </Badge>
            </div>
          </div>

          {/* Right side: progress + move + delete */}
          <div className="flex items-center gap-3 shrink-0">
            <span className={`text-sm font-bold tabular-nums ${
              progress === 0 ? 'text-text-muted' :
              progress === 100 ? 'text-accent-signal' :
              'text-accent-signal'
            }`}>
              {displayProgress}
            </span>

            {/* Move controls */}
            {(onMoveUp || onMoveDown) && (
              <div className="flex flex-col gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={onMoveUp}
                  disabled={disableMoveUp || moveLoading}
                  className="p-1 rounded hover:bg-accent/10 text-text-muted hover:text-text-primary transition-colors disabled:opacity-20 disabled:cursor-not-allowed disabled:hover:bg-transparent"
                  aria-label="Move skill up"
                  title="Move up"
                >
                  <ArrowUp size={13} />
                </button>
                <button
                  onClick={onMoveDown}
                  disabled={disableMoveDown || moveLoading}
                  className="p-1 rounded hover:bg-accent/10 text-text-muted hover:text-text-primary transition-colors disabled:opacity-20 disabled:cursor-not-allowed disabled:hover:bg-transparent"
                  aria-label="Move skill down"
                  title="Move down"
                >
                  <ArrowDown size={13} />
                </button>
              </div>
            )}

            {/* Delete */}
            {onDelete && (
              <button
                onClick={onDelete}
                className="p-1 rounded hover:bg-accent-critical/10 text-text-muted hover:text-accent-critical transition-colors opacity-0 group-hover:opacity-100"
                aria-label="Delete skill"
                title="Delete skill"
              >
                <Trash2 size={13} />
              </button>
            )}
          </div>
        </div>

        {/* Progress bar */}
        {onProgressChange ? (
          <div>
            {editing ? (
              <div className="flex items-center gap-3">
                <Slider
                  value={[progress]}
                  max={100}
                  step={1}
                  onValueChange={(value) => onProgressChange(skill.id, value)}
                  onValueCommit={(value) => onProgressCommit?.(skill.id, value)}
                  className="flex-1"
                />
                <button
                  onClick={() => setEditing(false)}
                  className="text-text-muted hover:text-text-primary transition-colors text-xs font-medium"
                >
                  Done
                </button>
              </div>
            ) : (
              <div className="relative" onClick={() => setEditing(true)}>
                <Progress value={progress} className="h-2" />
                <div className="absolute inset-0 cursor-pointer opacity-0" title="Click to edit progress" />
              </div>
            )}
          </div>
        ) : (
          <Progress value={progress} className="h-2" />
        )}
      </CardContent>
    </Card>
  )
}
