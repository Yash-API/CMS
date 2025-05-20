#!/bin/sh

# Function to test postgres connection
wait_for_postgres() {
    until PGPASSWORD=yash1009 psql -h db -U postgres -d Chatbot -c '\q' 2>/dev/null; do
        echo "Waiting for postgres..."
        sleep 1
    done
}
# Wait for postgres
wait_for_postgres
echo "PostgreSQL started"

# Run migrations
alembic upgrade head

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
