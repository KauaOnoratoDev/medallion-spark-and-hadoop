DROP DATABASE IF EXISTS retail;
CREATE DATABASE retail;

\c retail;
-- Tabelas

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_time TIMESTAMP NOT NULL,
    branch VARCHAR(50) NOT NULL
);

CREATE TABLE ordershistory (
    history_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(10) NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id)
);

-- Cria o usuário do aplicativo
DROP USER IF EXISTS appuser;

CREATE USER appuser WITH PASSWORD 'apppassword';
GRANT USAGE ON SCHEMA public TO appuser;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO appuser;
GRANT INSERT,
UPDATE,
SELECT
    ON ALL TABLES IN SCHEMA public TO appuser;

-- Cria o usuário do spark
DROP USER IF EXISTS sparkuser;

CREATE USER sparkuser WITH PASSWORD 'sparkpassword';
GRANT USAGE ON SCHEMA public TO sparkuser;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO sparkuser;
GRANT SELECT
    ON ALL TABLES IN SCHEMA public TO sparkuser;
