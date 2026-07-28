# Backend API Plan

## Goal

Replace the frontend's current JSON and localStorage data sources with real backend APIs while keeping the existing UI behavior intact.

## Frontend Analysis

The frontend currently depends on three kinds of data access:

- Static seed files in `public/data/`
- Local storage for mutable app state
- Small derived datasets computed entirely on the client

### What the UI already does

- Authenticates a single user from `public/data/user.json`
- Loads the dashboard category tree from `public/data/categories.json`
- Displays a quote of the day from `public/data/quotes.json`
- Lets the user create, rename, and delete categories
- Lets the user add, edit, and delete skills
- Lets the user update skill progress
- Lets the user add and delete comments on skills
- Lets the user edit profile name and title
- Lets the user toggle theme and reset all local data

### What is already client-only and can stay that way

- Sidebar collapse state
- Search query, filters, and sort state
- Timeline/log rendering
- Dashboard progress aggregation
- Quote rotation logic

These are derived or UI preferences and do not need API endpoints unless we want multi-device sync later.

## Backend Responsibilities

The backend should become the source of truth for:

- Authentication and session lifecycle
- Current user profile
- Categories and skills
- Skill progress
- Skill comments
- Dashboard summary data
- Quote selection or quote pool
- User settings if we want them persisted across devices

## Data Model Notes

The current frontend schemas are close, but the backend should support a slightly richer model:

- `Category`
  - `id`
  - `name`
  - `icon`
  - `skills`
- `Skill`
  - `id`
  - `categoryId`
  - `name`
  - `priority`
  - `difficulty`
  - `estimatedHours` optional, because it exists in seed data but is not yet part of the frontend schema
- `SkillProgress`
  - `skillId`
  - `progress`
  - `status`
  - `lastUpdated`
- `Comment`
  - `id`
  - `skillId`
  - `text`
  - `createdAt`
- `User`
  - `id`
  - `email`
  - `name`
  - `title`
  - `avatarUrl` optional for future use
- `Settings`
  - `theme`
  - `remember`

## API Surface

### Auth

The frontend login form currently posts email and password and expects a session back.

- `POST /api/auth/login`
  - Request: `{ email, password }`
  - Response: session payload plus user profile summary
  - Purpose: create a session and set auth cookie or return token
- `POST /api/auth/logout`
  - Purpose: invalidate the current session
- `GET /api/auth/me`
  - Purpose: return the current authenticated user and session state

### User Profile

The profile page only edits the user's name and title today.

- `GET /api/users/me`
  - Return current profile
- `PATCH /api/users/me`
  - Request: `{ name?, title? }`
  - Return updated profile

### Categories

The categories page and category detail page need full CRUD support.

- `GET /api/categories`
  - Return all categories with nested skills
- `POST /api/categories`
  - Request: `{ name, icon }`
  - Return created category
- `GET /api/categories/:categoryId`
  - Return a single category with nested skills
- `PATCH /api/categories/:categoryId`
  - Request: `{ name?, icon? }`
  - Return updated category
- `DELETE /api/categories/:categoryId`
  - Delete category and cascade delete its skills, progress, and comments

### Skills

The category detail page creates skills, and the skill detail page edits/deletes them.

- `POST /api/categories/:categoryId/skills`
  - Request: `{ name, priority, difficulty, estimatedHours? }`
  - Return created skill
- `GET /api/skills/:skillId`
  - Return a single skill with its category reference
- `PATCH /api/skills/:skillId`
  - Request: `{ name?, priority?, difficulty?, estimatedHours? }`
  - Return updated skill
- `DELETE /api/skills/:skillId`
  - Delete skill and cascade delete progress and comments

### Progress

Progress is currently stored locally and read by both category and skill views.

- `GET /api/progress`
  - Return progress for all skills
- `GET /api/skills/:skillId/progress`
  - Return progress for one skill
- `PUT /api/skills/:skillId/progress`
  - Request: `{ progress }`
  - Backend computes `status` and updates `lastUpdated`

Recommended status mapping:

- `0` -> `not-started`
- `1-99` -> `in-progress`
- `100` -> `completed`

### Comments

The skill detail page needs comment CRUD.

- `GET /api/skills/:skillId/comments`
  - Return all comments for a skill
- `POST /api/skills/:skillId/comments`
  - Request: `{ text }`
  - Return created comment
- `DELETE /api/skills/:skillId/comments/:commentId`
  - Delete a comment

### Dashboard

The dashboard can be built from categories, skills, progress, and quotes, but a summary endpoint will reduce frontend work and future-proof performance.

- `GET /api/dashboard/summary`
  - Suggested response:
    - total categories
    - total skills
    - completed skills
    - in-progress skills
    - overall progress
    - recently updated skills
- `GET /api/activity`
  - Optional, if we want the timeline to be backed by the server instead of being purely client-side

### Quotes

The dashboard currently rotates quotes from a local JSON file.

- `GET /api/quotes`
  - Return all quotes
- `GET /api/quotes/today`
  - Optional convenience endpoint if we want the backend to choose the daily quote

### Settings

The theme toggle and reset flow are local today, but settings can be persisted server-side later.

- `GET /api/users/me/settings`
- `PATCH /api/users/me/settings`
  - Request: `{ theme?, remember? }`

### Admin / Bootstrap

If we want the backend to own the seed data import, add one bootstrap path.

- `POST /api/admin/bootstrap`
  - Import `user.json`, `categories.json`, and `quotes.json`
  - Should be idempotent and protected

## Suggested Response Shapes

### Category

```json
{
  "id": "ai",
  "name": "AI",
  "icon": "🤖",
  "skills": [
    {
      "id": "prompt-engineering",
      "categoryId": "ai",
      "name": "Prompt Engineering",
      "priority": "high",
      "difficulty": "medium",
      "estimatedHours": 20
    }
  ]
}
```

### Progress

```json
{
  "skillId": "prompt-engineering",
  "progress": 72,
  "status": "in-progress",
  "lastUpdated": "2026-07-27T08:30:00.000Z"
}
```

### Comment

```json
{
  "id": "comment_123",
  "skillId": "prompt-engineering",
  "text": "Need to revisit prompt templates.",
  "createdAt": "2026-07-27T08:30:00.000Z"
}
```

## Build Order

### Phase 1

- Create backend project skeleton
- Add database schema or persistence layer
- Implement auth endpoints
- Implement `GET /api/categories`
- Implement `GET /api/quotes`

### Phase 2

- Implement category CRUD
- Implement skill CRUD
- Add cascade handling for delete operations

### Phase 3

- Implement progress APIs
- Implement comments APIs
- Add dashboard summary endpoint

### Phase 4

- Implement profile and settings persistence
- Add optional activity log endpoint
- Replace frontend localStorage writes with API calls

### Phase 5

- Add validation, error handling, pagination if needed
- Add tests for auth, CRUD, and cascade deletes
- Add seed/bootstrap script

## Migration Notes

The frontend can be migrated incrementally:

1. Keep seed JSON for local development until the backend is ready.
2. Replace `fetchUser`, `fetchCategories`, and `fetchQuotes` with API clients.
3. Move all category and skill mutations from localStorage to backend calls.
4. Keep derived UI state on the client unless a screen truly needs server persistence.
5. Preserve the current route structure so the UI changes stay minimal.

## Open Questions

- Should auth use session cookies or bearer tokens?
- Do we need single-user support only, or multi-user accounts from day one?
- Should comments and progress be soft-deleted or hard-deleted?
- Should quotes remain static seed data or become editable content in the database?
- Do we want the timeline log to be persisted, or keep it client-only?

## Recommended First Implementation

If we want the smallest useful backend first, build these endpoints first:

- `POST /api/auth/login`
- `GET /api/auth/me`
- `GET /api/categories`
- `POST /api/categories`
- `PATCH /api/categories/:categoryId`
- `DELETE /api/categories/:categoryId`
- `POST /api/categories/:categoryId/skills`
- `PATCH /api/skills/:skillId`
- `DELETE /api/skills/:skillId`
- `PUT /api/skills/:skillId/progress`
- `GET /api/skills/:skillId/comments`
- `POST /api/skills/:skillId/comments`
- `DELETE /api/skills/:skillId/comments/:commentId`
- `PATCH /api/users/me`
- `GET /api/quotes`
