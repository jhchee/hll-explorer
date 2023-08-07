#!/bin/bash -e

echo "Creating hll extension"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION hll;
EOSQL