import { cn } from '@/lib/utils'

function Skeleton({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-bg-panel-raised', className)}
      {...props}
    />
  )
}

export { Skeleton }
