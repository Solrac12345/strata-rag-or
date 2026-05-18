# Strata RAG Orchestrator

Multi-agent RAG (Retrieval-Augmented Generation) system built on FastAPI and AWS.

Receives a user question, routes it to the right AI agent, retrieves relevant documents, and generates a grounded answer using an LLM.
i need to push these changes
## Problem & Solution

### 🔍 The Problem
- **Hallucination & Unverifiable Outputs:** Standard LLMs generate plausible but ungrounded responses, making them unsuitable for production workflows that require accuracy, auditability, and source traceability.
- **Cloud-Blocked Development:** Relying on live AI services (e.g., AWS Bedrock) during local development slows iteration, increases costs, and makes testing non-deterministic.
- **Rigid AI Pipelines:** Single-model architectures can't scale to diverse tasks (QA, summarization, classification) without major refactoring or breaking existing contracts.
- **Deployment & Compliance Gaps:** Missing API contract validation, environment parity, and request tracing lead to brittle CI/CD pipelines and audit risks in regulated environments.

### ✅ The Solution
`strata-rag-or` is a **modular, production-ready RAG orchestrator** engineered to eliminate these bottlenecks:
- **Grounded Retrieval:** Every response is anchored to retrieved documents, with explicit source IDs for full traceability and hallucination reduction.
- **Stub-First Development:** Deterministic, offline mocks for embeddings and LLMs enable fast, cost-free local iteration. Switch to real AWS Bedrock with zero code changes via `BEDROCK_USE_REAL=true`.
- **Extensible Multi-Agent Routing:** A clean `RoutingAgent → TaskAgent` architecture allows new capabilities (e.g., summarization, validation, translation) to be added without modifying the core pipeline.
- **Engineering Rigor:** FastAPI + Pydantic contracts, Docker/Terraform deployment, CI/CD gating, and structured logging ensure reliability, reproducibility, and seamless promotion from development to production.

## Flow

```
User query → POST /orchestrate
                 ↓
          RoutingAgent → picks the right agent (currently: QA)
                 ↓
             QAAgent
               ├── Retriever  → embeds query, searches vector store, returns relevant docs
               └── LLMService → sends context + question to Bedrock, gets answer
                 ↓
          Response: { answer, sources, routed_agent }
```

## Project structure

```
api/              FastAPI endpoints (/health, /orchestrate, /embed) + request/response schemas
app/
  agents/         RoutingAgent, QAAgent (+ base class)
  orchestrator/   ties agents together
  rag/            embeddings, vector store, retriever, document store, loader
  services/       LLM service (Bedrock wrapper)
  core/           config & logging
infrastructure/   AWS clients — Bedrock, S3, DynamoDB, Lambda handler
deploy/           Dockerfile, docker-compose, Terraform, GitHub Actions CI
tests/            pytest suite
```

## Running locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```
```in another terminal 
Terminal Bash

curl http://127.0.0.1:8000/health

For POST to /orchestrate:

rag-query '{"query":"What is RAG?"}' | python -m json.tool

And /embed:

rag-embed '{"text":"hello world"}' | python -m json.tool

```

```
Check API is running:

# If you changed requirements.txt or Dockerfile:
docker compose -f deploy/docker-compose.yml up --build

# Otherwise just restart:
docker compose -f deploy/docker-compose.yml restart api

curl http://localhost:8080/health
Should return: {"status":"ok","env":"local"}

Ask a question:

curl -s -X POST http://localhost:8080/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}' | python -m json.tool

This will return:

{
  "answer": "...",
  "routed_agent": "qa_agent",
  "sources": ["source1", "source2"]
}

```
Everything runs with stubs by default (fake embeddings, fake LLM, in-memory vector store).
Set `BEDROCK_USE_REAL=true` to use real AWS Bedrock models — no code changes needed.

## Deployment

- **Local**: `uvicorn` or `docker-compose`
- **AWS**: Lambda + API Gateway + DynamoDB, defined in Terraform, CI via GitHub Actions

## License

This project is licensed under the [MIT License](LICENSE).