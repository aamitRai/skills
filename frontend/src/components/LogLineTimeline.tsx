import { format } from 'date-fns'
import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'
import type { LogLine } from '@/schemas'

const typeConfig: Record<LogLine['type'], { label: string; color: string }> = {
  progress: { label: 'PROG', color: 'text-accent-signal' },
  comment: { label: 'COMM', color: 'text-info' },
  status: { label: 'STAT', color: 'text-accent-warn' },
}

interface LogLineTimelineProps {
  lines: LogLine[]
  maxItems?: number
}

export default function LogLineTimeline({ lines, maxItems = 50 }: LogLineTimelineProps) {
  const displayLines = lines.slice(0, maxItems)

  if (displayLines.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-8 text-text-muted">
        <p className="text-sm font-mono">[NO LOGS]</p>
        <p className="text-xs mt-1">Activity will appear here</p>
      </div>
    )
  }

  return (
    <ScrollArea className="h-full">
      <div className="space-y-0.5 font-mono text-xs">
        {displayLines.map((line) => {
          const config = typeConfig[line.type]
          const time = format(new Date(line.timestamp), 'HH:mm:ss')

          return (
            <div
              key={line.id}
              className="flex items-center gap-2 px-3 py-1.5 rounded hover:bg-bg-panel-raised/50 transition-colors"
            >
              <span className="text-text-muted shrink-0">[{time}]</span>
              <span className={cn('shrink-0 w-10', config.color)}>
                {config.label}
              </span>
              <span className="text-text-secondary truncate">{line.message}</span>
            </div>
          )
        })}
      </div>
    </ScrollArea>
  )
}
