#!/bin/bash
set -e

echo "=== Configuring PostgreSQL for password auth ==="
PG_HBA="/etc/postgresql/14/main/pg_hba.conf"
cp "$PG_HBA" "${PG_HBA}.bak"
cat "$PG_HBA" | sed 's/peer$/md5/' > /tmp/pg_hba_new
cp /tmp/pg_hba_new "$PG_HBA"
systemctl restart postgresql
echo "PostgreSQL restarted with md5 auth"

echo "=== Testing password connection ==="
su - postgres -c "psql -c \"ALTER USER auto_ai_flow WITH PASSWORD 'aiflow2026';\"" 2>&1 || true
echo "Done"
