#!/bin/bash

# Load env vars from .env
export $(grep -v '^#' .env | xargs)

# Connect to PostgreSQL using env vars
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME"
