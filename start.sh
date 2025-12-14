#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

API_PORT=9696

source "$ROOT_DIR/.venv/bin/activate"

echo "🚀 Start FastAPI :$API_PORT"
python3 -m uvicorn app.api:app \
  --host 127.0.0.1 \
  --port $API_PORT \
  --reload &

API_PID=$!

echo "✅ API   http://127.0.0.1:$API_PORT"


# echo "🎨 Start Mesop:"
# cd "$ROOT_DIR/client"

# "$ROOT_DIR/.venv/bin/mesop" mesop_app.py &

# MESOP_PID=$!


trap "echo '🛑 stopping...'; kill $API_PID $MESOP_PID" SIGINT
wait
