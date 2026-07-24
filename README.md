# 🐋 Trabalho T2: Containerização e Orquestração com Docker

**Aluno:** Felipe Chaves Boll  
**Disciplina:** Redes de Computadores — IFPR  

Este repositório contém a resolução da segunda tarefa prática da disciplina. O objetivo é aplicar na prática os conceitos de **Docker**, **Dockerfile**, **Volumes**, **Isolamento de Redes** e orquestração de múltiplos containers com o **Docker Compose**.

---

## 📂 Estrutura do Repositório

```
Redes-T2/
├── README.md                      # Este guia
├── aula/                          # Material original fornecido pelo professor (não modificado)
├── exercicio1/                    # EXERCÍCIO 1: Achados & Perdidos - Campus IFPR
│   ├── docker-compose.yaml        # Orquestração dos 3 serviços + redes + volumes
│   ├── .env                       # Variáveis de ambiente (usuário e senha do banco)
│   ├── README.md                  # Documentação detalhada do Exercício 1
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── app.py                 # API REST em Python/Flask
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── Dockerfile
│   │   ├── app.py                 # Interface web em Python/Flask
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html         # Página principal do Quadro de Avisos
│   ├── test/
│   │   ├── Dockerfile
│   │   ├── test.py                # Testes de integração automáticos
│   │   └── requirements.txt
│   └── db/
│       └── init.sql               # Script de criação da tabela no banco
└── exercicio2/                    # EXERCÍCIO 2: WordPress + MySQL
    ├── compose.yaml               # Orquestração do WordPress e banco MySQL
    ├── .env                       # Senhas e configurações do banco
    ├── .env.example               # Exemplo de configuração
    └── README.md                  # Documentação detalhada do Exercício 2
```

---

## 🚀 Como Executar

### Pré-requisito
Ter o **Docker Desktop** instalado e em execução.

---

### 📋 Exercício 1 — Achados & Perdidos (Campus IFPR)

Sistema de Quadro de Avisos para itens achados e perdidos no campus escolar.

```bash
cd exercicio1
docker compose up --build
```

Aguarde os serviços iniciarem. Quando o container de testes exibir `=== Todos os testes passaram! ===`, acesse no navegador:

👉 **http://localhost:8080**

Para parar:
```bash
docker compose down
```

> **Teste de persistência:** Cadastre um aviso, rode `docker compose down` e depois `docker compose up` novamente. Os dados continuarão salvos graças ao volume nomeado `db_data`.

---

### 📝 Exercício 2 — WordPress + MySQL

Plataforma de criação de sites WordPress com banco de dados MySQL.

```bash
cd exercicio2
docker compose up -d
```

Acesse no navegador e conclua o assistente de instalação:

👉 **http://localhost:8081**

Para parar:
```bash
docker compose down
```

---

## 🏗️ Arquitetura do Exercício 1

```
┌──────────────────────────────────────────────┐
│                  HOST (seu PC)               │
│  Navegador → localhost:8080                  │
│                    │                         │
│         ┌──────────▼──────────┐              │
│         │  [frontend_net]     │              │
│         │                     │              │
│         │  ┌──────────────┐   │              │
│         │  │   frontend   │   │              │
│         │  │  Flask :5000 │   │              │
│         │  └──────┬───────┘   │              │
│         │         │           │              │
│         │  ┌──────▼───────┐   │              │
│         │  │   backend    │   │              │
│         │  │  Flask :5000 │   │              │
│         │  └──────┬───────┘   │              │
│         └─────────┼───────────┘              │
│                   │                          │
│         ┌─────────▼───────────┐              │
│         │    [db_net]         │              │
│         │  internal: true     │              │
│         │  ┌──────────────┐   │              │
│         │  │  PostgreSQL  │   │              │
│         │  │     :5432    │   │              │
│         │  └──────────────┘   │              │
│         └─────────────────────┘              │
└──────────────────────────────────────────────┘
```

**Regras de rede:**
- O `frontend` se comunica com o `backend` via rede `frontend_net`
- O `backend` se comunica com o banco via rede `db_net` (`internal: true`)
- O `frontend` **não tem acesso direto** ao banco de dados
- O banco **não expõe portas** para o host

---

## 🛠️ Comandos Úteis

| Comando | Descrição |
|---|---|
| `docker compose up --build` | Constrói as imagens e sobe os containers |
| `docker compose up -d` | Sobe em segundo plano (sem travar o terminal) |
| `docker compose logs -f` | Exibe os logs em tempo real |
| `docker compose down` | Para e remove os containers (dados persistem) |
| `docker compose down -v` | Para, remove containers e apaga os volumes |
| `docker compose exec frontend ping db` | Testa isolamento de rede (deve falhar) |
