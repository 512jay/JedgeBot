-- Create authentication database
CREATE DATABASE jedgebot_auth;

-- Verify database creation
SELECT datname FROM pg_database WHERE datname = 'jedgebot_auth';
