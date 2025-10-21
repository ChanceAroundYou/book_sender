#!/usr/bin/env sh
set -e

# echo "Waiting for 10 seconds before starting celery services..."
# sleep 10

echo "Starting celery beat in background..."
celery -A app.celery_app.celery_app beat --loglevel=info --pidfile=/tmp/celerybeat.pid &
BEAT_PID=$!
echo "Celery beat started (PID: $BEAT_PID). Starting worker in foreground..."

# Ensure beat is terminated when container receives a stop signal
term_handler() {
  echo "Stopping celery beat (PID: $BEAT_PID)"
  kill -TERM "$BEAT_PID" 2>/dev/null || true
  wait "$BEAT_PID" 2>/dev/null || true
  exit 0
}
trap term_handler TERM INT

exec celery -A app.celery_app.celery_app worker --loglevel=info
