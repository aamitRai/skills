#!/bin/bash

PROJECT_ROOT="/Users/amitrai/Documents/GitHub/skills"

# Start Backend
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd \"$PROJECT_ROOT/backend\" && source venv/bin/activate && uvicorn app.main:app --reload"
end tell
EOF

# Start Frontend
osascript <<EOF
tell application "Terminal"
    do script "cd \"$PROJECT_ROOT/frontend\" && npm run dev"
end tell
EOF