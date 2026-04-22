#!/bin/bash
set -e

echo "=== Starting PostgreSQL Setup ==="

# Ensure PostgreSQL is running
pg_isready -q 2>/dev/null || {
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
}

# Create user and database
sudo -u postgres psql -c "SELECT 1 FROM pg_roles WHERE rolname='auto_ai_flow'" | grep -q 1 || {
    echo "Creating database user: auto_ai_flow"
    sudo -u postgres psql -c "CREATE USER auto_ai_flow WITH PASSWORD 'aiflow2026';"
}

sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw auto_ai_flow || {
    echo "Creating database: auto_ai_flow"
    sudo -u postgres psql -c "CREATE DATABASE auto_ai_flow OWNER auto_ai_flow ENCODING 'UTF8';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE auto_ai_flow TO auto_ai_flow;"
}

echo "=== PostgreSQL Setup Complete ==="

echo "=== Starting Redis Setup ==="
sudo systemctl start redis-server 2>/dev/null || sudo systemctl start redis 2>/dev/null || true
sudo systemctl enable redis-server 2>/dev/null || sudo systemctl enable redis 2>/dev/null || true
redis-cli ping || echo "Redis not responding yet"
echo "=== Redis Setup Complete ==="

echo "=== Verifying Services ==="
echo "PostgreSQL version:"
psql --version
echo "Redis status:"
redis-cli ping
echo "Node.js version:"
node --version
echo "npm version:"
npm --version
echo "Python version:"
python3 --version

echo "=== Testing DB Connection ==="
PGPASSWORD=aiflow2026 psql -h 127.0.0.1 -U auto_ai_flow -d auto_ai_flow -c "SELECT 1 as db_test;" 2>&1 || echo "DB connection test via TCP failed, trying local socket..."
PGPASSWORD=aiflow2026 psql -h localhost -U auto_ai_flow -d auto_ai_flow -c "SELECT 1 as db_test;" 2>&1 || echo "DB connection test via localhost failed"

echo "=== All Services Ready ==="
