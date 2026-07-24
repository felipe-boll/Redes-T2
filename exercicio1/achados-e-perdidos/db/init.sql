-- Script de inicialização do banco de dados
-- Cria a tabela de avisos de achados e perdidos caso não exista
CREATE TABLE IF NOT EXISTS messages (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    text       TEXT NOT NULL,
    ip_client  VARCHAR(45),
    ip_origin  VARCHAR(45),
    created_at TIMESTAMP DEFAULT NOW()
);
