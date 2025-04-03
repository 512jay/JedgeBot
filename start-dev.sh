#!/bin/bash

# 🚀 Navigate to the root of the project
cd "$(dirname "$0")"

# ✅ Launch frontend (Vite)
echo "🟢 Starting frontend..."
(cd frontend && npm run dev) &

# ✅ Launch backend (FastAPI via uvicorn)
echo "🟣 Starting backend..."
(cd backend && poetry run uvicorn main:app --reload) &

# ✅ Open VS Code workspace
echo "💻 Opening VS Code workspace..."
code jedgebot.code-workspace
