
# 🧠 Retrievify System

A **production-ready Retrieval-Augmented Generation (RAG)** system combining powerful LLMs with semantic search and observability.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Dockerized](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 Overview

Built with:

- 🔥 **FastAPI** – high-performance APIs  
- 🧮 **PostgreSQL + pgvector** – vector database  
- 🧠 **LLMs via OpenAI, Cohere, or Ollama** – Q&A and embeddings  
- 📊 **Prometheus + Grafana** – full observability  
- 🌐 **NGINX** – reverse proxy  
- 🐳 **Docker Compose** – for container orchestration  

---

## 📦 Features

- 📄 Upload documents (PDF, TXT, etc.)
- 🔗 Chunk & embed with OpenAI, Cohere, or local models
- 🔍 Semantic search using cosine similarity
- 🧠 LLM-based Q&A interface
- 📈 Real-time monitoring dashboards
- 🔌 Pluggable LLM providers (OpenAI, Cohere, Ollama)

---

## 🏗️ Architecture


```
                     ┌────────────┐
                     │   Client   │
                     └─────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   NGINX     │
                    └──────┬──────┘
                           │
                     ┌─────▼──────┐
                     │  FastAPI   │◄──────────────┐
                     └─────┬──────┘               │
 ┌──────────────┐         │                       │
 │ PostgreSQL + │◄────────┘                       │
 │  pgvector    │       Semantic Search           │
 └──────────────┘                                  ▼
                         ┌─────────────┬─────────────┐
                         │   OpenAI    │   Cohere    │
                         └─────┬───────┴──────┬──────┘
                               │              │
                            ┌──▼─────┐     ┌───▼──────┐
                            │ Ollama │     │  Local   │
                            │ LLMs   │     │ Models   │
                            └────────┘     └──────────┘

````

---

## ⚡ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/somaiaahmed/Retrievify.git
cd Retrievify
````

### 2. Set environment variables

Create the following files in `/env/`:

* `.env.app` – FastAPI settings
* `.env.postgres` – PostgreSQL DB config
* `.env.postgres-exporter` – Prometheus metrics
* `.env.grafana` – Grafana setup

Sample `.env.app`:

```env
OPENAI_API_KEY=sk-...
COHERE_API_KEY=...
OLLAMA_URL=http://host.docker.internal:11434
EMBEDDING_MODEL=openai
GENERATION_MODEL=cohere
```

### 3. Launch the system

```bash
docker compose up --build
```

Services:

* FastAPI → [http://localhost:8000](http://localhost:8000)
* Prometheus → [http://localhost:9090](http://localhost:9090)
* Grafana → [http://localhost:3000](http://localhost:3000)
* Ollama (manual) → [http://localhost:11434](http://localhost:11434)

---

## 🔌 API Endpoints

| Endpoint          | Method | Description               |
| ----------------- | ------ | ------------------------- |
| `data/upload`         | POST   | Upload documents          |
| `data/process`        | POST   | Chunk + embed + index     |
| `/nlp/index/push` | POST   | Add new docs to the index |
| `/nlp/index/info` | GET    | View index metadata       |
| `/nlp/index/search`         | POST   | Perform semantic search   |
| `/nlp/index/answer`         | POST   | Retrieve answer using LLM |

### 📤 Example

```bash
curl -X POST http://localhost:8000/nlp/index/answer/{project_id} \
-H "Content-Type: application/json" \
-d '{"query": "What is the capital of France?"}'
```

---

## 📊 Monitoring Dashboards

| Tool           | URL                                            | Purpose                    |
| -------------- | ---------------------------------------------- | -------------------------- |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Metrics scraping engine    |
| **Grafana**    | [http://localhost:3000](http://localhost:3000) | Dashboards & visualization |

Grafana Login:

```bash
Username: admin
Password: admin
```

Dashboards included:

* API request latency
* PostgreSQL query performance
* System health (CPU, memory, disk)
* LLM usage & latency (if instrumented)

---

## 🧰 Tech Stack

* **API**: FastAPI, Python
* **Vector DB**: PostgreSQL + pgvector
* **LLMs**: OpenAI / Cohere / Ollama (local)
* **Monitoring**: Prometheus, Grafana, node\_exporter
* **DevOps**: Docker Compose, NGINX

---


## 🖥️ Dev Setup

### Requirements

* Python 3.10+
* Conda or Python venv
* Docker & Docker Compose

### Local Installation

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

```bash
conda create -n rag python=3.10
conda activate rag
pip install -r requirements.txt
```

### Customize Shell (Optional)

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

---


## 🗂️ Project Structure

```plaintext
Retrievify/
├── .vscode/                    # VSCode settings
├── docker/                     # Docker, NGINX, Prometheus setup
│   ├── env/                    # Environment configs
│   ├── minirag/                # App Docker context
│   ├── nginx/                  # NGINX reverse proxy config
│   ├── prometheus/             # Prometheus config files
│   ├── docker-compose.yml      # Docker Compose config
│   └── README.md               # Docker-specific documentation
├── src/                        # Source code for FastAPI app
│   ├── controllers/            # Business logic & endpoint handlers
│   ├── helpers/                # Utility functions
│   ├── models/                 # Pydantic + ORM models
│   ├── routes/                 # API route definitions
│   ├── stores/                 # Database interaction logic
│   ├── utils/                  # Helper utilities (metrics)
│   ├── .env.example            # Sample env file
│   ├── main.py                 # FastAPI entry point
│   └── requirements.txt        # Python dependencies
├── .gitignore
└── README.md
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

