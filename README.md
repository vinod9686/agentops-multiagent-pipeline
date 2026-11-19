# 🚀 Multi-Agent Microservices, Fault Tolerance & AgentOps Observability

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Desktop%20%2F%20Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.159.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2.16-FF6F00?logo=chainlink&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-LPU%20Inference-F05A28?logo=speedtest&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/Academic-PES%20University-blue)](#)

> **Course:** B.Tech CSE (AI & ML) — Machine Learning System Design and AgentOps (MLSDAP)  
> **Student Name:** Vinod  
> **Student SRN:** `PES1UG25AM817`  
> **Assigned Lab 2 Topic:** `latency` | **Injected Writer Failure Rate ($p$):** `0.5`

---

## 📌 Executive Summary

This repository contains the complete production-grade source code, Docker containerization recipes, fault injection suites, and observability frameworks developed across **Unit 4 (AgentOps & ML System Design)**.

The project demonstrates how to transition AI agents from standalone experimental scripts into **distributed, self-healing, observable microservice architectures** running inside containerized production environments.

---

## 📂 Why Two Directories? (`agentops_lab1` vs `agentops_lab2`)

The curriculum systematically advances from single-agent hosting to distributed multi-agent resilience:

| Dimension | `agentops_lab1` (Single Agent Hosting) | `agentops_lab2` (Multi-Agent Pipeline & Reliability) |
| :--- | :--- | :--- |
| **System Scope** | Single agent microservice wrapped in FastAPI. | 4-container distributed microservice cluster managed via Docker Compose. |
| **Core Objective** | Containerization, REST interface, and layer caching. | Fault tolerance, inter-service networking, and observability. |
| **Agents Involved** | 1 agent (`unit_agent` / `text_agent`) with tool binding. | 3 specialized agents (`Researcher`, `Writer`, `Reviewer`) + 1 `Orchestrator`. |
| **Failure Handling** | Basic HTTP 502/400 exception handling. | Exponential backoff, randomized jitter, and graceful degradation. |
| **Network Model** | Single container host-port forwarding (`-p 8000:8000`). | Isolated bridge network with service-name DNS (`http://writer:8000`). |
| **Observability** | Single request latency measurement. | Structured JSON Lines logging (`events.jsonl`) computing Task Success Rate, P95 Latency, Retry Rate, and Container Uptime. |

---

## 🛠️ Tech Stack & Architecture Rationales

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT TIER                                    │
│                 Browser Web UI (HTML5 / Vanilla JS Fetch)                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP POST / REST
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    DOCKER COMPOSE ISOLATED BRIDGE NETWORK                   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    PIPELINE ORCHESTRATOR (:8000)                      │  │
│  │  • FastAPI REST Engine    • LangGraph Sequential StateGraph           │  │
│  │  • Exponential Backoff    • Randomized Jitter (0.5x - 1.5x)           │  │
│  │  • Graceful Degradation   • Structured JSON Lines Logger              │  │
│  └──────┬────────────────────────┬─────────────────────────┬─────────────┘  │
│         │ HTTP                   │ HTTP                    │ HTTP           │
│  ┌──────▼──────────────┐  ┌──────▼──────────────┐  ┌───────▼─────────────┐  │
│  │  RESEARCHER (:8000) │  │    WRITER (:8000)   │  │   REVIEWER (:8000)  │  │
│  │  Tool: lookup_facts │  │  FAULT INJECTION:   │  │  Tool: count_words  │  │
│  │  KB: Domain facts   │  │  FAIL_RATE = 0.5    │  │  Threshold: >= 30w  │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Cloud LPU Inference (or Mock Fallback)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                          EXTERNAL INFERENCE TIER                            │
│                 Groq Cloud API (qwen/qwen3.8-27b / LLaMA 3.3 70B)           │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **LangGraph (v1.2.16):** Selected for its cyclic state graph capabilities. Unlike traditional DAG pipelines, LangGraph supports conditional loops (`agent` $\leftrightarrow$ `tools` and `reviewer` $\rightarrow$ `writer` revision cycles).
2. **FastAPI (v0.159.1) & Uvicorn (v0.54.0):** High-performance asynchronous REST framework. Automatically provides OpenAPI schema validation and interactive Swagger documentation at `/docs`.
3. **Docker & Docker Compose:** Guarantees immutable deployment environments, isolates service dependencies, enables DNS discovery between containers, and manages automated health checks (`healthcheck.py`).
4. **Groq Cloud Inference:** Ultra-fast Language Processing Units (LPUs) provide near-instantaneous inference (sub-50ms token generation), essential for preventing multi-hop agent pipelines from exceeding timeout budgets.
5. **JSON Lines Observability (`events.jsonl`):** Append-only, thread-safe structured event streaming that decouples runtime logging from metrics aggregation.

---

## 📂 Repository Layout

```
.
├── .gitignore                          # Global protection for .env, virtualenvs, logs
├── README.md                           # Industry-standard documentation (this file)
├── agentops_lab1/                      # Unit 4 Lab 1: Hosting & Containerization
│   ├── requirements.txt                # Pinned dependencies
│   ├── unit_agent/                     # Practice Experiment 1A: Unit Converter
│   │   ├── .env.example                # Configuration template
│   │   ├── config.py                   # Centralized environment loader
│   │   ├── llm.py                      # Groq LLM + Mock fallback provider
│   │   ├── tools.py                    # Unit converter tool (length, mass, temp)
│   │   ├── agent.py                    # LangGraph StateGraph agent loop
│   │   ├── main.py                     # FastAPI REST server
│   │   ├── Dockerfile                  # Multi-layer cached build recipe
│   │   └── static/index.html           # Web interface consuming /run
│   ├── text_agent/                     # Student Experiment 1B: Text Helper
│   │   ├── .env.example                # Config template with STUDENT_SRN
│   │   ├── config.py                   # Reads SRN and MAX_INPUT_CHARS
│   │   ├── tools.py                    # analyze_text & find_longest_word
│   │   ├── agent.py                    # Multi-tool agent graph
│   │   ├── main.py                     # Stamped with student SRN + length checks
│   │   └── Dockerfile                  # Container image definition
│   └── deliverables/                   # Generated artifacts & submissions
│       ├── PES1UG25AM817_Lab_Report.md # Full Markdown report
│       ├── PES1UG25AM817_Unit4_Lab1_Deliverables.docx # Word submission
│       ├── PES1UG25AM817_agent_flow.png # Architecture flow diagram
│       └── *.png                       # Screenshots 1 through 8
│
└── agentops_lab2/                      # Unit 4 Lab 2: Multi-Agent Reliability
    ├── requirements.txt                # Pinned dependencies + requests
    ├── pipeline_lab/                   # Practice Experiment 2A: Compose Pipeline
    │   ├── docker-compose.yml          # 4-container cluster configuration
    │   ├── roles.py                    # Domain Knowledge Base & role prompts
    │   ├── agent_main.py               # Parameterized agent service (ROLE-based)
    │   ├── orchestrator.py             # Pipeline orchestrator with retry loops
    │   ├── run_batch.py                # Batch benchmark script (10/20 runs)
    │   └── metrics.py                  # AgentOps metrics calculation engine
    ├── pipeline_lab_b/                 # Student Experiment 2B: Reliability & Faults
    │   ├── .env.example                # Config with WRITER_FAIL_RATE=0.5
    │   ├── roles.py                    # Assigned topic: 'latency' (4 domain facts)
    │   ├── orchestrator.py             # Graceful degradation + Jitter backoff
    │   ├── docker-compose.yml          # Compose specification with health checks
    │   └── metrics.py                  # Custom metric: avg revisions per run
    └── deliverables/                   # Generated artifacts & submissions
        ├── PES1UG25AM817_Lab2_Report.md # Full Markdown report
        ├── PES1UG25AM817_Unit4_Lab2_Deliverables.docx # Word submission
        ├── PES1UG25AM817_failure_flow.png # Pipeline & failure flow diagram
        └── *.png                       # Screenshots 1 through 9
```

---

## 🔑 Prerequisites & Environment Setup

### 1. System Requirements
* **OS:** Windows 10/11 (64-bit) with WSL 2, macOS (Apple Silicon/Intel), or Linux (Ubuntu 22.04+).
* **Docker Desktop:** Version 29+ with Docker Compose v5+. Ensure Docker Engine is running.
* **Python Runtime:** Python 3.11 (64-bit).

### 2. How to Obtain a Free Groq API Key
1. Visit the [Groq Console](https://console.groq.com/) and register for a free account (no credit card required).
2. Go to **API Keys** ➔ **Create API Key**. Name it (e.g. `agentops-lab`) and copy the generated key (starts with `gsk_`).
3. Store this key in your local private notes.
4. *(Optional)* Both labs include an offline mock engine (`USE_MOCK_LLM=true`) that runs the entire agent workflow and tool loops without requiring an active API key or internet connection.

---

## 🚀 Step-by-Step Configuration & Execution

### Part 1: Lab 1 — Single Agent Hosting & Containerization

```powershell
# 1. Navigate to Lab 1
cd agentops_lab1\text_agent

# 2. Configure environment
Copy-Item .env.example .env
# Edit .env and insert your GROQ_API_KEY and STUDENT_SRN

# 3. Build Docker image with layer caching
docker build -t student-agent:PES1UG25AM817 .

# 4. Run container with externalized configuration
docker run --rm -p 8000:8000 --env-file .env --name student-agent student-agent:PES1UG25AM817

# 5. Access in browser
# Web Interface: http://localhost:8000
# Health Check:  http://localhost:8000/health
# Swagger Docs:  http://localhost:8000/docs
```

---

### Part 2: Lab 2 — Multi-Agent Pipeline with Docker Compose

```powershell
# 1. Stop any existing container on port 8000
docker stop student-agent

# 2. Navigate to Lab 2 Student Activity
cd ..\..\agentops_lab2\pipeline_lab_b

# 3. Configure personal environment (SRN ending in 7 -> topic: latency, fail_rate: 0.5)
Copy-Item .env.example .env

# 4. Launch the 4-container cluster with Docker Compose
docker compose up --build -d

# 5. Verify all containers are healthy
docker compose ps

# 6. Verify fault injection rate is active
docker compose config | Select-String FAIL_RATE

# 7. Test in browser
# Open: http://localhost:8000
# Enter topic: latency -> Click "Run pipeline" -> Shows APPROVED
# Click "Check services" -> Shows all agents UP
```

---

## 🔬 Reliability Engineering & Fault Injection (Lab 2B)

### 1. Graceful Degradation Test (Reviewer Outage)
In traditional pipelines, if an optional downstream service fails, the entire request crashes. Here, the system gracefully degrades:
```powershell
# Stop the reviewer container
docker compose stop reviewer

# Run pipeline for topic "latency" on http://localhost:8000
# Result: Status changes to DEGRADED. The draft is preserved and delivered to the user.
# Check services reports: reviewer: DOWN.

# Restart reviewer container
docker compose start reviewer
# Status returns to APPROVED upon recovery.
```

### 2. Step 9 Reliability Benchmark: Impact of Retries
Under an injected **50% failure rate** on the Writer service ($p = 0.5$):

```powershell
# Run 20 batch requests across MAX_RETRIES = 0, 1, 3
python run_batch.py 20
python metrics.py --last 20
```

#### Measured Experimental Benchmark Data:
| MAX_RETRIES | Theoretical Failure $p^{R+1}$ | Task Success Rate | Failed Runs | Retry Rate | Avg Latency | P95 Latency |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`0`** | $0.50$ (50.0%) | **35.0%** (7/20) | 12 | 0.0% | 39 ms | 78 ms |
| **`1`** | $0.25$ (25.0%) | **60.0%** (12/20) | 6 | 24.1% | 418 ms | 772 ms |
| **`3`** | $0.0625$ (6.25%) | **90.0%** (18/20)* | 0 | 10.9% | 287 ms | 787 ms |

*\*Note: The remaining 2 non-approved runs at $R=3$ were intentional 'kubernetes' test cases, which are rejected by design due to absence of knowledge base facts.*

### 3. Student Modification Task: Randomized Jitter
To solve the **thundering herd problem** where simultaneous retries overwhelm recovering services, randomized jitter was implemented in `orchestrator.py`:
$$\text{wait} = \text{BACKOFF\_S} \times 2^{\text{attempt}} \times \text{Uniform}(0.5, 1.5)$$

---

## 📊 Observability Metrics Explained

The `metrics.py` script parses `logs/events.jsonl` to calculate core AgentOps telemetry:
1. **Task Success Rate (%):**
   $$\text{Success Rate} = \frac{\text{Approved Runs}}{\text{Total Runs}} \times 100$$
2. **Response Latency (Average & 95th Percentile):**
   * Average latency measures typical performance.
   * **P95 Latency** measures the upper 95% latency threshold, uncovering tail latency spikes hidden by simple averages.
3. **Retry Rate (%):**
   $$\text{Retry Rate} = \frac{\sum \text{Retry Attempts}}{\sum \text{Initial Attempts}} \times 100$$
4. **Container Uptime:**
   Queried live via the orchestrator's `/services` endpoint, identifying service health and detecting unexpected container restarts.

---

## 🎓 Academic Submission Artifacts

Complete academic deliverables (including embedded screenshots, architecture diagrams, code, and Viva Voce answers) are available in each lab's `deliverables/` folder:

* **Lab 1 Deliverables:** [`agentops_lab1/deliverables/`](agentops_lab1/deliverables/)
  * Report: [`PES1UG25AM817_Unit4_Lab1_Deliverables.docx`](agentops_lab1/deliverables/PES1UG25AM817_Unit4_Lab1_Deliverables.docx)
  * Flow Diagram: [`PES1UG25AM817_agent_flow.png`](agentops_lab1/deliverables/PES1UG25AM817_agent_flow.png)
* **Lab 2 Deliverables:** [`agentops_lab2/deliverables/`](agentops_lab2/deliverables/)
  * Report: [`PES1UG25AM817_Unit4_Lab2_Deliverables.docx`](agentops_lab2/deliverables/PES1UG25AM817_Unit4_Lab2_Deliverables.docx)
  * Flow Diagram: [`PES1UG25AM817_failure_flow.png`](agentops_lab2/deliverables/PES1UG25AM817_failure_flow.png)

---

## 🔒 Security Best Practices
* `.env` files containing live API credentials are strictly excluded from git tracking via `.gitignore` and from Docker images via `.dockerignore`.
* Sanitize all keys to `xxxx` prior to sharing configurations (see `.env.submit`).
