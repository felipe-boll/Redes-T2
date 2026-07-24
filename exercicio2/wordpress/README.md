# 🌐 Exercício 2: Implantação de Aplicação WordPress com Docker Compose

Este exercício consiste na configuração, orquestração e execução de uma aplicação **WordPress** completa utilizando exclusivamente imagens oficiais e prontas do Docker Hub, orquestradas via `compose.yaml`.

---

## 🛠️ Tecnologias e Imagens Utilizadas

- **Aplicação:** `wordpress:latest` (Imagem oficial Docker Hub)
- **Banco de Dados:** `mariadb:10.6` / `mysql:8.0` (Imagem oficial Docker Hub)
- **Orquestração:** Docker Compose
- **Variáveis de Ambiente:** `.env`

---

## 📐 Arquitetura da Solução

- **Serviço `wordpress`:** Expõe a porta WEB para acesso do usuário no host e comunica com o banco de dados.
- **Serviço `db` (MariaDB/MySQL):** Isolado na rede interna sem exposição de portas para o host.
- **Persistência de Dados:**
  - Volume para os arquivos do WordPress (`wp_data`).
  - Volume para os dados do banco de dados (`db_data`).

---

## 📂 Estrutura do Projeto

```text
wordpress/
├── .env
├── .env.example
├── compose.yaml
└── README.md
```

---

## 🚀 Como Executar

1. Crie o arquivo `.env` com base no `.env.example`:

```bash
cp .env.example .env
```

2. Caso necessário, ajuste as credenciais e senhas no arquivo `.env`.

3. Suba o ambiente executando:

```bash
docker compose up -d
```

4. Acesse o painel de instalação do WordPress:

```text
http://localhost:8080
```

---

## 💾 Persistência de Dados

Tanto os uploads/arquivos do WordPress quanto o banco de dados utilizam volumes nomeados do Docker.

Para verificar que os dados não são perdidos:

1. Finalize a instalação do WordPress e crie um post de teste.
2. Remova os containers:

```bash
docker compose down
```

3. Inicie os containers novamente:

```bash
docker compose up -d
```

4. Recarregue a página; todas as configurações e posts criados permanecerão intactos.