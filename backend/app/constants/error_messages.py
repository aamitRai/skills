"""HTTP error messages returned to clients via HTTPException.detail."""

# ─── Auth ────────────────────────────────────────────────────────────────────

ERR_INVALID_CREDENTIALS = "Invalid email or password"
ERR_NOT_AUTHENTICATED = "Missing or invalid authorization header"
ERR_TOKEN_INVALID = "Invalid or expired token"
ERR_TOKEN_DECODE_FAILED = "Failed to decode token"
ERR_USER_NOT_FOUND = "User not found"
ERR_EMAIL_REGISTERED = "Email already registered"

# ─── Categories ──────────────────────────────────────────────────────────────

ERR_CATEGORY_NOT_FOUND = "Category not found"
ERR_CATEGORY_DUPLICATE = "A category with this name already exists"

# ─── Skills ──────────────────────────────────────────────────────────────────

ERR_SKILL_NOT_FOUND = "Skill not found"
ERR_SKILL_DUPLICATE = "A skill with this name already exists in this category"

# ─── Comments ────────────────────────────────────────────────────────────────

ERR_COMMENT_NOT_FOUND = "Comment not found"

# ─── General ─────────────────────────────────────────────────────────────────

ERR_INTERNAL = "An unexpected error occurred"
