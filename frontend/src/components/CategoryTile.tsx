import { Link } from 'react-router'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { useDataStore } from '@/stores/dataStore'
import type { CategoryResponse } from '@/api/categories.api'

interface CategoryTileProps {
  category: CategoryResponse
  progress: number
}

export default function CategoryTile({ category, progress }: CategoryTileProps) {
  const progressMap = useDataStore((state) => state.progressMap)

  // Compute last-7-day sparkline data from lastUpdated timestamps
  const sparkline = category.skills.map((skill) => {
    const entry = progressMap[skill.id]
    if (!entry || !entry.last_updated) return 0
    const daysAgo = (Date.now() - new Date(entry.last_updated).getTime()) / (1000 * 60 * 60 * 24)
    return daysAgo <= 7 ? entry.progress : 0
  })

  const maxSpark = Math.max(...sparkline, 1)

  const completedCount = category.skills.filter(
    (s) => progressMap[s.id]?.status === 'completed',
  ).length

  return (
    <Link to={`/category/${category.id}`}>
      <Card className="hover:border-accent-signal/30 transition-colors group cursor-pointer">
        <CardContent className="p-4 space-y-3">
          {/* Header */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{category.icon}</span>
              <h3 className="font-display font-semibold text-text-primary group-hover:text-accent-signal transition-colors text-sm">
                {category.name}
              </h3>
            </div>
            <span className="text-lg font-display font-bold tabular text-accent-signal">
              {progress}%
            </span>
          </div>

          {/* Sparkline */}
          <div className="flex items-end gap-0.5 h-8">
            {sparkline.map((val, i) => (
              <div
                key={i}
                className="flex-1 rounded-sm bg-accent-signal/30 hover:bg-accent-signal/50 transition-colors min-h-[2px]"
                style={{ height: `${Math.max((val / maxSpark) * 100, 4)}%` }}
                title={`${category.skills[i]?.name}: ${val}%`}
              />
            ))}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between text-xs text-text-muted">
            <span>{category.skills.length} skills</span>
            {completedCount > 0 && (
              <Badge variant="signal" className="text-[10px]">
                {completedCount} done
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
