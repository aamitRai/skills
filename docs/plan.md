# Career OS — Project Plan (v2)

**Goal:** A tracking + visualization system for becoming a high-paying AI Engineer.
**Deployment:** Vercel (static/SPA, no backend)
**Data source:** JSON files (seed data, imported on first run)
**Persistence:** LocalStorage (categories, skills, progress, comments, settings, auth session)

---

## 1. Tech Stack

| Layer | Choice |
|---|---|
| Language | TypeScript (strict mode) |
| Framework | React 19 |
| Bundler | Vite |
| Styling | Tailwind CSS v4 |
| Components | shadcn/ui (Radix primitives) |
| Icons | lucide-react |
| Charts | Recharts |
| Animation | Framer Motion (motion/react) |
| State | Zustand (global) + React Query-style local hooks not needed (no server) |
| Forms | React Hook Form + Zod |
| Routing | React Router v7 |
| Persistence | LocalStorage, wrapped in a typed storage adapter |
| Dates | date-fns |
| Deployment | Vercel (static build) |

React 19 specifics to actually use: `useActionState` for the login form, `useOptimistic` for instant slider/progress updates before localStorage write confirms, and the new `ref`-as-prop pattern (no more `forwardRef` boilerplate) across shadcn components.

---

## 2. Design System — "Mission Control"

Rejecting the generic AI-app defaults (cream + terracotta, black + neon, broadsheet). The chosen direction: **an engineer's late-night control room** — a dark instrument panel that treats skills like systems being monitored, not a gamified checklist. This fits an *AI Engineer's* actual mental model (dashboards, logs, uptime) rather than a generic "learning app" look.

### Palette (dark-mode-first)

| Token | Hex | Use |
|---|---|---|
| `--bg-base` | `#0B0E14` | App background |
| `--bg-panel` | `#12161F` | Card/panel surface |
| `--bg-panel-raised` | `#181D29` | Elevated surface (modals, hover) |
| `--border-hairline` | `#242B3A` | 1px dividers, card borders |
| `--accent-signal` | `#4FD1C5` | Primary accent — "signal teal," used for active/in-progress states, primary CTAs |
| `--accent-warn` | `#F5A623` | Priority/attention, warnings |
| `--accent-critical` | `#EF5B5B` | Overdue, not-started-but-urgent |
| `--text-primary` | `#E6E9F0` | Headings, primary text |
| `--text-secondary` | `#8A93A6` | Meta text, labels |
| `--grid-line` | `#1A2030` | Background grid/scanline texture |

Light mode is a secondary, not primary, palette — inverted panel tones (`#F6F7FA` base, `#FFFFFF` panels), same accent hues at slightly deepened saturation for contrast.

### Typography

- **Display / headings:** `Space Grotesk` — geometric, slightly technical, used at restraint (headings, big stats only).
- **Body:** `Inter` — neutral, high legibility for descriptions, comments, table data.
- **Data / mono:** `JetBrains Mono` — used for progress percentages, timestamps, skill IDs, and the "log line" timeline entries. This is the detail that sells the control-room feel.

Type scale: 12 / 14 / 16 / 20 / 28 / 40 / 56, with mono numerals always tabular (`font-variant-numeric: tabular-nums`) so progress numbers don't jitter when animating.

### Layout concept

```
┌─────────────────────────────────────────────┐
│ Top bar: search · avatar                     │
├───────────┬───────────────────────────────────┤
│ Sidebar   │  Dashboard grid                    │
│ (collapse)│  ┌────────────┬────────────┐       │
│ Categories│  │ Goal panel │ Progress   │       │
│ w/ mini   │  ├────────────┼────────────┤       │
│ progress  │  │ Weekly     │ Skill stats│       │
│ bars      │  ├────────────┴────────────┤       │
│           │  │ Category grid (11 tiles) │       │
│           │  ├──────────────────────────┤       │
│           │  │ Timeline (log-line feed) │       │
│           │  └──────────────────────────┘       │
└───────────┴───────────────────────────────────┘
```

Category tiles are not generic cards — each renders as a small **status panel** with a live sparkline of last-7-day progress deltas, like a systems-monitoring tile.

### Signature element

**The Progress Ring + Log Line combo:** the dashboard's overall progress renders as a segmented radial ring (SVG, animated stroke-dashoffset) rather than a flat progress bar — echoing an oscilloscope/telemetry dial. Every state change (slider move, comment add, status flip) writes a monospace "log line" (`[14:32:08] LangGraph → 72%`) into the Timeline, reinforcing the control-room metaphor end to end. This is the one bold move; everything else (cards, tables, forms) stays quiet and disciplined.

### Motion

- Page load: staggered fade+rise for dashboard panels (~40ms stagger, 300ms ease-out), once.
- Progress ring: animates stroke on mount and on value change (600ms cubic-bezier).
- Hover: subtle 1px border glow in accent color, no scale/shadow theatrics.
- Respect `prefers-reduced-motion` — disable stagger and ring animation, snap to final state.

---

## 3. shadcn/ui Components to Install

```
button, card, input, label, checkbox, switch, slider, dialog, sheet,
dropdown-menu, popover, tooltip, tabs, badge, avatar, progress,
separator, scroll-area, toast (sonner), select, textarea, table,
skeleton, alert, command (for global search), collapsible, accordion
```

Custom components built on top of shadcn primitives:
- `ProgressRing` (custom SVG, not shadcn `progress`)
- `SkillCard`
- `CategoryTile`
- `LogLineTimeline`

---

## 4. Information Architecture / Routes

| Route | Page |
|---|---|
| `/login` | Login |
| `/` | Dashboard |
| `/categories` | Category list (search, filter, sort, create) |
| `/category/:categoryId` | Category detail (add/edit/delete skills, inline progress) |
| `/skill/:skillId` | Skill detail (progress slider, comments, history) |
| `/profile` | Profile |
| `/settings` | Settings |

Route guard: `ProtectedRoute` wrapper checks LocalStorage session; redirects to `/login` if absent/expired.

---

## 5. Data Layer

### 5.1 Static JSON (seed data — imported once on first run)

```
/data
  user.json          # hardcoded credential + profile
  categories.json    # seed categories + skills (imported into localStorage on first run)
  quotes.json        # quote of the day pool
```

Categories and skills are **not read-only**. The JSON file serves as seed data that gets imported into `localStorage` on first run. After that, all category/skill mutations (create, edit, delete) live in `localStorage`.

### 5.2 LocalStorage (mutable source of truth)

```
careeros:auth            → { email, name, expiresAt }
careeros:categories      → Category[] (full CRUD: create, rename, delete categories; add/edit/delete skills)
careeros:progress        → { [skillId]: { progress, status, hoursCompleted, lastUpdated } }
careeros:comments        → { [skillId]: Comment[] }
careeros:settings        → { theme, remember }
careeros:quotes_cache    → Quote[]
```

A single typed `storage.ts` adapter wraps `get/set/remove` with Zod schema validation, so a corrupted localStorage value never crashes the app — falls back to defaults instead.

### 5.3 Category/Skill CRUD Contract

| Operation | Where | How |
|---|---|---|
| **Create category** | `/categories` | Dialog with name + icon picker |
| **Rename category** | `/category/:id` | Inline editable title |
| **Delete category** | `/category/:id` | Settings dialog with confirmation (cascades skills) |
| **Add skill** | `/category/:id` | Form: name, priority, difficulty, estimated hours |
| **Edit skill** | `/skill/:id` | Editable fields in skill detail page |
| **Delete skill** | `/skill/:id` | Confirmation dialog (cascades progress + comments) |
| **Update progress** | `/category/:id` or `/skill/:id` | Slider, optimistic write + debounced commit |

### 5.4 Derived state (computed, not stored)

Overall progress, category progress, and skill aggregates are all **derived** from progress + timestamps at read time via Zustand selectors — never stored redundantly, to avoid drift.

---

## 6. State Management (Zustand stores)

- `useAuthStore` — session, login/logout
- `useDataStore` — categories/skills CRUD, progress reads, derived aggregates (single source read by all pages)
- `useUIStore` — theme, sidebar collapsed, active filters/search query
- `useTimelineStore` — derived log-line feed from progress/comment mutation history

---

## 7. Feature Breakdown by Milestone

**M1 — Foundation**
Vite + React 19 + TS scaffold, Tailwind v4 config with design tokens above, shadcn init, routing, storage adapter, Zod schemas for all JSON shapes.

**M2 — Auth**
Login page (RHF + Zod + `useActionState`), show/hide password, remember me, invalid-credential state, protected routes, logout.

**M3 — Dashboard**
Goal card, ProgressRing (overall), Weekly progress chart (Recharts), Quote of the day, skill count tiles, recently updated list.

**M4 — Categories & Skills (with full CRUD)**
Seed data import from JSON on first run. Category grid with sparkline tiles. Create/rename/delete categories via dialog. Category detail page with add/edit/delete skills form. SkillCard with inline progress slider. `useOptimistic` + debounced localStorage write. Status/priority/difficulty badges.

**M5 — Comments**
Add/edit/delete comment per skill, timestamps, optional markdown render (`react-markdown`).

**M6 — Search & Filters**
Command palette (`cmdk` via shadcn `command`) for global search; filter bar (status/progress/priority) on category pages.

**M7 — Statistics & Timeline**
Stats aggregation views, LogLineTimeline component fed by mutation history.

**M8 — Profile**
Profile page with overall stats, skills completed, user info.

**M9 — Settings**
Theme toggle, reset progress (with confirm dialog), logout. No export/import.

**M10 — Polish**
Motion pass, responsive audit (mobile sidebar → sheet), keyboard focus states, reduced-motion support, empty states, error boundaries, Lighthouse pass.

---

## 8. Non-functional Requirements

- Fully static — no server, deployable as Vercel static output.
- All localStorage reads/writes go through the typed adapter; never accessed ad hoc in components.
- Accessible: visible focus rings, proper label associations on all form controls, `aria-live` on toasts.
- Mobile-first responsive: sidebar collapses to a `Sheet`; category grid reflows to single column.
- Zero layout shift on progress ring animation (reserve size via fixed SVG viewBox).

---

## 9. Decisions Locked

1. **Single hardcoded user, permanently.** No multi-user, no sign-up. `user.json` stays the only identity source; `useAuthStore` never needs to branch on user ID.
2. **No JSON export/import.** Removed from Settings and from M9 scope entirely.
3. **Skill names only, no descriptions.** `description` is dropped from the skill schema and from `SkillCard`. No placeholder copy needed anywhere in the skill data model.
4. **Categories and skills are fully editable.** Seed JSON is imported once on first run into localStorage. All subsequent CRUD (create, rename, delete categories; add, edit, delete skills) lives in localStorage via `categoriesStorage`.
5. **No XP, streaks, or achievements.** Gamification layer removed. Progress tracking is purely percentage-based per skill.