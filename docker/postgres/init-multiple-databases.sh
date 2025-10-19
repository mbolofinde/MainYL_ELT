#!/bin/bash
set -e
set -u

function create_user_and_database() {
    local database=$1
    local user=$2
    local password=$3
    echo "  Creating database '$database' with user '$user'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $user WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
        ALTER DATABASE $database OWNER TO $user;
EOSQL
}

if [ -n "$POSTGRES_USER" ]; then
    echo "Multiple database creation requested"

    # Create Airflow metadata database
    create_user_and_database $METADATA_DATABASE_NAME $METADATA_DATABASE_USERNAME $METADATA_DATABASE_PASSWORD
    echo "  Airflow metadata database created"

    # Create Celery backend database
    create_user_and_database $CELERY_BACKEND_NAME $CELERY_BACKEND_USERNAME $CELERY_BACKEND_PASSWORD
    echo "  Celery backend database created"

    # Create ELT database
    create_user_and_database $ELT_DATABASE_NAME $ELT_DATABASE_USERNAME $ELT_DATABASE_PASSWORD
    echo "  ELT database created"

    echo "Multiple databases created successfully"
fi