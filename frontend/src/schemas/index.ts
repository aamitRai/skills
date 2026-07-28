import { z } from 'zod'

// ── User ──
export const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
  name: z.string().min(1),
  title: z.string(),
})
export type User = z.infer<typeof UserSchema>

// ── Skill ──
export const SkillSchema = z.object({
  id: z.string(),
  name: z.string(),
  priority: z.enum(['low', 'medium', 'high', 'critical']),
  difficulty: z.enum(['beginner', 'intermediate', 'advanced', 'expert']),
})
export type Skill = z.infer<typeof SkillSchema>

// ── Category ──
export const CategorySchema = z.object({
  id: z.string(),
  name: z.string(),
  icon: z.string(),
  skills: z.array(SkillSchema),
})
export type Category = z.infer<typeof CategorySchema>

export const CategoriesSchema = z.object({
  categories: z.array(CategorySchema),
})
export type CategoriesData = z.infer<typeof CategoriesSchema>

// ── Categories Store (localStorage) ──
export const CategoriesStoreSchema = z.object({
  categories: z.array(CategorySchema),
})
export type CategoriesStore = z.infer<typeof CategoriesStoreSchema>

// ── Progress (localStorage) ──
export const SkillProgressSchema = z.object({
  progress: z.number().min(0).max(100),
  status: z.enum(['not-started', 'in-progress', 'completed']),
  lastUpdated: z.string().datetime(),
})
export type SkillProgress = z.infer<typeof SkillProgressSchema>

export const ProgressStoreSchema = z.record(
  z.string(),
  SkillProgressSchema,
)
export type ProgressStore = z.infer<typeof ProgressStoreSchema>

// ── Comment ──
export const CommentSchema = z.object({
  id: z.string(),
  skillId: z.string(),
  text: z.string().min(1),
  createdAt: z.string().datetime(),
})
export type Comment = z.infer<typeof CommentSchema>

export const CommentsStoreSchema = z.record(
  z.string(),
  z.array(CommentSchema),
)
export type CommentsStore = z.infer<typeof CommentsStoreSchema>

// ── Auth Session (localStorage) ──
export const AuthSessionSchema = z.object({
  email: z.string().email(),
  name: z.string(),
  title: z.string().optional(),
  expiresAt: z.string().datetime(),
})
export type AuthSession = z.infer<typeof AuthSessionSchema>

// ── Settings (localStorage) ──
export const SettingsSchema = z.object({
  theme: z.enum(['dark', 'light']).default('dark'),
  remember: z.boolean().default(true),
})
export type Settings = z.infer<typeof SettingsSchema>

// ── Quote (static JSON) ──
export const QuoteSchema = z.object({
  text: z.string(),
  author: z.string(),
})
export type Quote = z.infer<typeof QuoteSchema>

export const QuotesDataSchema = z.object({
  quotes: z.array(QuoteSchema),
})
export type QuotesData = z.infer<typeof QuotesDataSchema>

// ── Log Line (timeline) ──
export const LogLineSchema = z.object({
  id: z.string(),
  timestamp: z.string().datetime(),
  message: z.string(),
  type: z.enum(['progress', 'comment', 'status']),
})
export type LogLine = z.infer<typeof LogLineSchema>
