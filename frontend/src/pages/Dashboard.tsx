import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { motion } from 'framer-motion'

import { quotesApi, type QuoteResponse } from '@/api/quotes.api'
import CategoryTile from '@/components/CategoryTile'
import ProgressRing from '@/components/ProgressRing'
import { Card, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/stores/authStore'
import { useDataStore } from '@/stores/dataStore'

const FALLBACK_QUOTE: QuoteResponse = { id: '', text: 'Keep building.', author: 'Career OS' }

export default function Dashboard() {
  const { user } = useAuthStore()
  const { categories, getOverallProgress, getAllSkills, getSkillProgress } = useDataStore()
  const [quote, setQuote] = useState<QuoteResponse>(FALLBACK_QUOTE)

  useEffect(() => {
    quotesApi.getToday().then((q) => {
      if (q) setQuote(q)
    }).catch(() => { })
  }, [])

  const allSkills = getAllSkills()
  const overallProgress = getOverallProgress()
  const completedSkills = allSkills.filter((s) => getSkillProgress(s.id) === 100).length
  const inProgressSkills = allSkills.filter((s) => {
    const p = getSkillProgress(s.id)
    return p > 0 && p < 100
  }).length

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

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-display font-semibold text-text-primary">
              Mission Control
            </h1>
            <p className="text-sm text-text-secondary mt-0.5">
              Welcome back, {user?.name?.split(' ')[0] ?? 'Engineer'}.
            </p>
          </div>
        </div>
      </motion.div>

      <Separator className="bg-border-hairline" />

      {/* Top Stats Row */}
      <motion.div variants={container} initial="hidden" animate="show" className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Progress Ring Card */}
        <motion.div variants={item}>
          <Card>
            <CardContent className="p-6 flex flex-col items-center justify-center">
              <ProgressRing value={overallProgress} size={160} strokeWidth={10} label="Overall" sublabel={`${completedSkills} of ${allSkills.length} skills`} />
            </CardContent>
          </Card>
        </motion.div>

        {/* Skill Count Tiles + Quote Card */}
        <motion.div variants={item}>
          <Card className="h-full">
            <CardContent className="p-5 space-y-4">
              <h4 className="text-xs text-text-muted uppercase tracking-wider font-medium">Skill Status</h4>
              <div className="grid grid-cols-3 gap-3">
                <Link to="/categories" className={cn('p-3 rounded-lg bg-bg-panel-raised text-center hover:bg-bg-panel transition-colors cursor-pointer')}>
                  <p className="text-2xl font-display font-bold tabular text-accent-signal">{allSkills.length}</p>
                  <p className="text-[10px] text-text-muted uppercase tracking-wider">Total</p>
                </Link>
                <Link to="/categories?status=in-progress" className={cn('p-3 rounded-lg bg-bg-panel-raised text-center hover:bg-bg-panel transition-colors cursor-pointer')}>
                  <p className="text-2xl font-display font-bold tabular text-accent-warn">{inProgressSkills}</p>
                  <p className="text-[10px] text-text-muted uppercase tracking-wider">Active</p>
                </Link>
                <Link to="/categories?status=completed" className={cn('p-3 rounded-lg bg-bg-panel-raised text-center hover:bg-bg-panel transition-colors cursor-pointer')}>
                  <p className="text-2xl font-display font-bold tabular text-success">{completedSkills}</p>
                  <p className="text-[10px] text-text-muted uppercase tracking-wider">Done</p>
                </Link>
              </div>
              <Separator className="bg-border-hairline" />
              <blockquote>
                <p className="text-base font-bold text-text-primary italic leading-relaxed">"{quote.text}"</p>
                <footer className="text-xs text-text-muted mt-2 font-mono">— {quote.author}</footer>
              </blockquote>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>

      {/* Category Grid */}
      <motion.div variants={container} initial="hidden" animate="show">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-medium text-text-secondary uppercase tracking-wider">Categories</h2>
        </div>
        <motion.div variants={container} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
          {categories.map((cat) => (
            <motion.div key={cat.id} variants={item}>
              <CategoryTile category={cat} progress={useDataStore.getState().getCategoryProgress(cat.id)} />
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  )
}
