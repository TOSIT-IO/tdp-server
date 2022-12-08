CREATE USER keycloak WITH PASSWORD 'keycloak';
CREATE USER tdp_user WITH PASSWORD 'tdp_password';
---
CREATE DATABASE keycloak;
\connect keycloak
CREATE SCHEMA keycloak AUTHORIZATION keycloak;
\connect postgres

CREATE DATABASE tdp_dev_db;
\connect tdp_dev_db
CREATE SCHEMA tdp AUTHORIZATION tdp_user;
\connect postgres
---
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA keycloak TO keycloak;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA keycloak TO keycloak;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA tdp TO tdp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA tdp TO tdp_user;
-- set default schema for tdp user
ALTER ROLE tdp_user SET search_path TO tdp,public;
