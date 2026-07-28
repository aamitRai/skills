import { useState, useMemo } from 'react'
import { useSearchParams } from 'react-router'
import { motion } from 'framer-motion'
import { Search, SlidersHorizontal, X, Plus } from 'lucide-react'

import CategoryTile from '@/components/CategoryTile'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { useDataStore } from '@/stores/dataStore'

const STATUS_OPTIONS = [
  { value: null, label: 'All' },
  { value: 'not-started', label: 'Not Started' },
  { value: 'in-progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
] as const

const SORT_OPTIONS = [
  { value: 'name', label: 'Name' },
  { value: 'progress', label: 'Progress' },
  { value: 'skills', label: 'Skill Count' },
] as const

export default function Categories() {
  const { categories, getCategoryProgress, createCategory } = useDataStore()
  const [searchParams, setSearchParams] = useSearchParams()
  const statusFilter = searchParams.get('status')
  const [search, setSearch] = useState(searchParams.get('q') ?? '')
  const [sort, setSort] = useState(searchParams.get('sort') ?? 'name')
  const [showFilters, setShowFilters] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [newName, setNewName] = useState('')
  const [newIcon, setNewIcon] = useState('📁')

  const ICON_OPTIONS = ['📁', '🤖', '⚡', '💻', '🧠', '📊', '☁️', '🔄', '🔧', '🎨', '🔒', '🤝', '📱', '🛠️', '📐', '🔬']

  const filtered = useMemo(() => {
    let result = categories

    // Search filter
    if (search.trim()) {
      const q = search.toLowerCase()
      result = result.filter(
        (c) =>
          c.name.toLowerCase().includes(q) ||
          c.skills.some((s) => s.name.toLowerCase().includes(q)),
      )
    }

    // Status filter
    if (statusFilter) {
      result = result.filter((c) => {
        const p = getCategoryProgress(c.id)
        if (statusFilter === 'completed') return p === 100
        if (statusFilter === 'not-started') return p === 0
        return p > 0 && p < 100
      })
    }

    // Sort
    result = [...result].sort((a, b) => {
      if (sort === 'name') return a.name.localeCompare(b.name)
      if (sort === 'progress') return getCategoryProgress(b.id) - getCategoryProgress(a.id)
      return b.skills.length - a.skills.length
    })

    return result
  }, [categories, search, statusFilter, sort, getCategoryProgress])

  const activeFilters = !!(statusFilter || search)

  const handleStatusChange = (value: string | null) => {
    if (value) setSearchParams({ ...Object.fromEntries(searchParams), status: value })
    else {
      const copy = Object.fromEntries(searchParams)
      delete copy.status
      setSearchParams(copy)
    }
  }

  const handleSortChange = (value: string) => {
    setSort(value)
    setSearchParams({ ...Object.fromEntries(searchParams), sort: value })
  }

  const handleSearch = (value: string) => {
    setSearch(value)
    const params = Object.fromEntries(searchParams)
    if (value) {
      setSearchParams({ ...params, q: value })
    } else {
      delete params.q
      setSearchParams(params)
    }
  }

  const clearFilters = () => {
    setSearch('')
    setSort('name')
    setSearchParams({})
  }

  const handleCreateCategory = async () => {
    if (!newName.trim()) return
    await createCategory(newName.trim(), newIcon)
    setNewName('')
    setNewIcon('📁')
    setCreateOpen(false)
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-semibold text-text-primary">Categories</h1>
          <p className="text-sm text-text-secondary mt-1">
            {categories.length} categories · {categories.reduce((sum, c) => sum + c.skills.length, 0)} skills
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative flex-1 sm:flex-initial">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
            <Input
              placeholder="Search categories or skills..."
              value={search}
              onChange={(e) => handleSearch(e.target.value)}
              className="pl-9 w-full sm:w-64 h-8 text-sm"
            />
          </div>
          <Button
            variant="outline"
            size="sm"
            className="h-8 gap-1.5"
            onClick={() => setShowFilters(!showFilters)}
          >
            <SlidersHorizontal size={14} />
            Filters
          </Button>
          <Dialog open={createOpen} onOpenChange={setCreateOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="h-8 gap-1.5">
                <Plus size={14} />
                New
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create Category</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label>Name</Label>
                  <Input
                    placeholder="e.g. Machine Learning"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleCreateCategory()}
                    autoFocus
                  />
                </div>
                <div className="space-y-2">
                  <Label>Icon</Label>
                  <div className="flex flex-wrap gap-2">
                    {ICON_OPTIONS.map((icon) => (
                      <button
                        key={icon}
                        type="button"
                        onClick={() => setNewIcon(icon)}
                        className={`w-9 h-9 rounded-md text-lg flex items-center justify-center transition-colors ${
                          newIcon === icon
                            ? 'bg-accent-signal/20 border border-accent-signal'
                            : 'bg-bg-panel-raised border border-border-hairline hover:border-accent-signal/50'
                        }`}
                      >
                        {icon}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
              <DialogFooter>
                <Button variant="ghost" onClick={() => setCreateOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleCreateCategory} disabled={!newName.trim()}>
                  Create
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Filter Bar */}
      {showFilters && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
        >
          <Card>
            <CardContent className="p-4 space-y-4">
              {/* Status Filter */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-text-muted uppercase tracking-wider font-medium">Status</span>
                {STATUS_OPTIONS.map((opt) => (
                  <Badge
                    key={opt.value ?? 'all'}
                    variant={statusFilter === opt.value ? 'signal' : 'secondary'}
                    className="cursor-pointer text-xs hover:bg-accent-signal/20 transition-colors"
                    onClick={() => handleStatusChange(opt.value)}
                  >
                    {opt.label}
                  </Badge>
                ))}
              </div>
              {/* Sort */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-text-muted uppercase tracking-wider font-medium">Sort by</span>
                {SORT_OPTIONS.map((opt) => (
                  <Badge
                    key={opt.value}
                    variant={sort === opt.value ? 'signal' : 'secondary'}
                    className="cursor-pointer text-xs hover:bg-accent-signal/20 transition-colors"
                    onClick={() => handleSortChange(opt.value)}
                  >
                    {opt.label}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Active Filters */}
      {activeFilters && (
        <div className="flex items-center gap-2">
          {statusFilter && (
            <Badge variant="signal" className="text-xs gap-1">
              Status: {statusFilter}
              <X size={10} className="cursor-pointer" onClick={() => handleStatusChange(null)} />
            </Badge>
          )}
          {search && (
            <Badge variant="signal" className="text-xs gap-1">
              Search: "{search}"
              <X size={10} className="cursor-pointer" onClick={() => handleSearch('')} />
            </Badge>
          )}
          <Button variant="ghost" size="sm" className="text-xs h-6 px-2" onClick={clearFilters}>
            Clear all
          </Button>
        </div>
      )}

      {/* Category Grid */}
      {filtered.length === 0 ? (
        <div className="text-center py-12">
          {categories.length === 0 ? (
            <>
              <p className="text-text-secondary">No categories yet.</p>
              <Button className="mt-4" onClick={() => setCreateOpen(true)}>
                <Plus size={16} />
                Create your first category
              </Button>
            </>
          ) : (
            <>
              <p className="text-text-secondary">No categories match your filters.</p>
              {activeFilters && (
                <Button variant="ghost" className="mt-2" onClick={clearFilters}>
                  Clear filters
                </Button>
              )}
            </>
          )}
        </div>
      ) : (
        <motion.div variants={container} initial="hidden" animate="show" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((category) => {
            const progress = getCategoryProgress(category.id)
            return (
              <motion.div key={category.id} variants={item}>
                <CategoryTile category={category} progress={progress} />
              </motion.div>
            )
          })}
        </motion.div>
      )}
    </div>
  )
}
