#!/bin/bash
set -e

DATA_DIR=/var/lib/postgresql/data

if [ ! -s "$DATA_DIR/PG_VERSION" ]; then
    echo "Initializing database..."
    mkdir -p "$DATA_DIR"
    chown -R postgres:postgres "$DATA_DIR"
    su postgres -c "initdb -D $DATA_DIR"
fi

su postgres -c "pg_ctl -D $DATA_DIR -o \"-c listen_addresses='localhost'\" -w start"

su postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD'\"" || true
su postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER\"" || true

export DATABASE_URL=${DATABASE_URL:-postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@localhost:5432/$POSTGRES_DB}

flask db upgrade || true

exec python run.py
