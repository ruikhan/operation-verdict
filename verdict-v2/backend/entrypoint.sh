#!/bin/bash
set -e

echo "⏳ Waiting for PostgreSQL..."
python - <<'EOF'
import sys, time, os
import psycopg2

for attempt in range(30):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST', 'db'),
            port=os.environ.get('DB_PORT', '5432'),
        )
        conn.close()
        print("✅ Database is ready.")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        print(f"   Attempt {attempt + 1}/30: {e}")
        time.sleep(2)

print("❌ Could not connect to database.")
sys.exit(1)
EOF

echo "🔄 Running migrations..."
python manage.py migrate --noinput

echo "🌱 Seeding game data..."
python manage.py seed_data

echo "🚀 Starting server..."
exec "$@"
