# 🔍 Achados e Perdidos — Sistema de Avisos Universitários

Aplicação web full-stack containerizada para publicação e visualização de objetos achados e perdidos no campus. O projeto foi desenvolvido para a disciplina de Redes de Computadores, utilizando **Docker** e **Docker Compose** para orquestração e isolamento de rede.

---

## 🛠️ Tecnologias Utilizadas

- **Frontend:** Python (Flask) / HTML5 / CSS3 / Jinja2
- **Backend:** Python (Flask API)
- **Banco de Dados:** PostgreSQL (Imagem oficial Docker)
- **Testes:** Python (Script de teste automatizado/healthcheck)
- **Orquestração:** Docker & Docker Compose

---

## 🏗️ Arquitetura de Redes e Containerização

O projeto é dividido em 3 serviços principais (mais um container de teste), orquestrados via `docker-compose.yaml` com isolamento de rede rigoroso:

1. **`frontend`**: Interface do usuário para publicação e consulta de avisos.
   - Conectado apenas à rede `frontend-net`.
2. **`backend`**: API REST responsável pela lógica de negócio e intermediação do banco.
   - Conectado às redes `frontend-net` e `backend-db-net` (atuando como bridge/proxy).
3. **`db`**: Banco de dados PostgreSQL com inicialização via `init.sql` e persistência via volume nomeado (`postgres_data`).
   - Conectado apenas à rede interna/fechada `backend-db-net` (`internal: true`).
   - **Isolamento de Segurança:** O banco de dados **não** expõe portas para o host nem possui acesso direto do container `frontend`.

---

## 📂 Estrutura do Projeto

```text
achados-e-perdidos/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql
├── frontend/
│   ├── templates/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── test/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test.py
├── .env
├── docker-compose.yaml
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados.

### Passos

1. Certifique-se de que o arquivo `.env` está configurado na raiz (utilize o modelo padrão ou ajuste as credenciais, se necessário).
2. Na raiz do projeto `exercicio1/achados-e-perdidos`, execute:

```bash
docker compose up --build
```

3. Acesse a aplicação em:

```text
http://localhost:5000
```

---

## 🧪 Testando a Persistência e Isolamento de Rede

### Testar Persistência de Dados

1. Publique um aviso no sistema web.
2. Derrube os containers:

```bash
docker compose down
```

3. Suba novamente:

```bash
docker compose up
```

O aviso publicado continuará disponível, pois os dados ficam armazenados no volume nomeado.

### Testar Isolamento do Banco de Dados

Tente pingar ou conectar no serviço `db` a partir do container `frontend`:

```bash
docker compose exec frontend ping db
```

A operação falhará, garantindo o isolamento da rede interna do banco de dados.