"""Log message format strings used across the application."""

# ─── Auth ────────────────────────────────────────────────────────────────────

LOG_LOGIN_FAILED = "[Auth] Login failed: %s"
LOG_USER_LOGGED_IN = "[Auth] User logged in: %s"
LOG_PROFILE_UPDATED = "[Auth] Profile updated: %s"
LOG_SETTINGS_UPDATED = "[Auth] Settings updated: %s"
LOG_USER_REGISTERED = "[Auth] User registered: %s"

# ─── Categories ──────────────────────────────────────────────────────────────

LOG_CATEGORY_CREATED = "[Category] Created: %s"
LOG_CATEGORY_UPDATED = "[Category] Updated: %s"
LOG_CATEGORY_DELETED = "[Category] Deleted: %s"

# ─── Skills ──────────────────────────────────────────────────────────────────

LOG_SKILL_ADDED = "[Skill] Added: %s"
LOG_SKILL_UPDATED = "[Skill] Updated: %s"
LOG_SKILL_DELETED = "[Skill] Deleted: %s"

# ─── Progress ────────────────────────────────────────────────────────────────

LOG_PROGRESS_UPDATED = "[Progress] Updated: %s"

# ─── Comments ────────────────────────────────────────────────────────────────

LOG_COMMENT_CREATED = "[Comment] Created: %s"
LOG_COMMENT_DELETED = "[Comment] Deleted: %s"

# ─── Dashboard ───────────────────────────────────────────────────────────────

LOG_DASHBOARD_SUMMARY_COMPUTED = "[Dashboard] Summary computed for user: %s"
LOG_ACTIVITY_FEED_COMPUTED = "[Dashboard] Activity feed computed for user: %s"

# ─── Admin ───────────────────────────────────────────────────────────────────

LOG_BOOTSTRAP_USER_CREATED = "[Admin] Bootstrap user created: %s"
LOG_BOOTSTRAP_CATEGORIES_IMPORTED = "[Admin] Categories imported: %d"
LOG_BOOTSTRAP_SKILLS_IMPORTED = "[Admin] Skills imported: %d"
LOG_BOOTSTRAP_QUOTES_IMPORTED = "[Admin] Quotes imported: %d"
LOG_BOOTSTRAP_FAILED = "[Admin] Bootstrap failed: %s"