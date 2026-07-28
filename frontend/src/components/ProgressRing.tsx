import { useEffect, useRef } from 'react'

interface ProgressRingProps {
  value: number
  size?: number
  strokeWidth?: number
  label?: string
  sublabel?: string
}

export default function ProgressRing({
  value,
  size = 160,
  strokeWidth = 10,
  label,
  sublabel,
}: ProgressRingProps) {
  const circleRef = useRef<SVGCircleElement>(null)

  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (Math.min(value, 100) / 100) * circumference

  useEffect(() => {
    const circle = circleRef.current
    if (!circle) return

    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (prefersReduced) {
      circle.style.strokeDashoffset = String(offset)
      return
    }

    circle.style.transition = 'stroke-dashoffset 600ms cubic-bezier(0.4, 0, 0.2, 1)'
    circle.style.strokeDashoffset = String(offset)
  }, [offset])

  const color = value === 100 ? 'var(--color-success)' : 'var(--color-accent-signal)'

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={size} height={size} className="-rotate-90" viewBox={`0 0 ${size} ${size}`}>
        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--color-border-hairline)"
          strokeWidth={strokeWidth}
        />
        {/* Progress arc */}
        <circle
          ref={circleRef}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
        />
      </svg>

      {/* Center content */}
      <div className="absolute flex flex-col items-center justify-center" style={{ width: size, height: size }}>
        <span className="text-3xl font-display font-bold tabular text-text-primary">
          {Math.round(value)}%
        </span>
        {label && (
          <span className="text-xs text-text-secondary font-medium">{label}</span>
        )}
      </div>

      {sublabel && (
        <span className="text-xs text-text-muted font-mono">{sublabel}</span>
      )}
    </div>
  )
}
