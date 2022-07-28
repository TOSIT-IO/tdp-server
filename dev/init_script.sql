CREATE DATABASE keycloak;
-- default database is tdp_dev_db
CREATE SCHEMA tdp;
-- set default schema for tdp user
ALTER ROLE tdp_user SET search_path TO tdp,public;
