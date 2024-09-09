@echo off

:: Start the FastAPI backend
start cmd /k "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Start the SearXNG Docker instance
start cmd /k "cd searxng-docker && docker-compose up"

:: Start the Next.js frontend
start cmd /k "cd frontend && npm run dev"

echo All services have been started!
pause
