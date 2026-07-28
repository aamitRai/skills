import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const alertVariants = cva(
  'relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-text-primary',
  {
    variants: {
      variant: {
        default: 'bg-bg-panel border-border-hairline text-text-primary',
        destructive: 'bg-accent-critical/10 border-accent-critical/20 text-accent-critical',
        warning: 'bg-accent-warn/10 border-accent-warn/20 text-accent-warn',
        success: 'bg-success/10 border-success/20 text-success',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

function Alert({
  className,
  variant,
  ...props
}: React.ComponentProps<'div'> & VariantProps<typeof alertVariants>) {
  return (
    <div role="alert" className={cn(alertVariants({ variant }), className)} {...props} />
  )
}

function AlertTitle({ className, ...props }: React.ComponentProps<'h5'>) {
  return (
    <h5
      className={cn('mb-1 font-medium leading-none tracking-tight text-text-primary', className)}
      {...props}
    />
  )
}

function AlertDescription({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div className={cn('text-sm [&_p]:leading-relaxed text-text-secondary', className)} {...props} />
  )
}

export { Alert, AlertTitle, AlertDescription }
