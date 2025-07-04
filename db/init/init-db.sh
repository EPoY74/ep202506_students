#!/bin/bash
set -e

echo "Инициализация БД..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';
    CREATE DATABASE $DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    \connect $DB_NAME

    GRANT USAGE, CREATE ON SCHEMA public TO $DB_USER;
    ALTER USER $DB_USER WITH SUPERUSER CREATEDB;
EOSQL

echo "ДБ инициализирована!"