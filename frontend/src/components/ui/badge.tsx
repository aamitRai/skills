import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-accent-signal/40 focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-border-hairline bg-bg-panel-raised text-text-primary',
        secondary: 'border-border-hairline bg-bg-panel text-text-secondary',
        destructive: 'border-accent-critical/20 bg-accent-critical/10 text-accent-critical',
        outline: 'text-text-secondary border-border-hairline',
        signal: 'border-accent-signal/20 bg-accent-signal/10 text-accent-signal',
        warn: 'border-accent-warn/20 bg-accent-warn/10 text-accent-warn',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
