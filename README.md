# Strata RAG Orchestrator

Multi-agent RAG (Retrieval-Augmented Generation) system built on FastAPI and AWS.

Receives a user question, routes it to the right AI agent, retrieves relevant documents, and generates a grounded answer using an LLM.

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

Everything runs with stubs by default (fake embeddings, fake LLM, in-memory vector store).
Set `BEDROCK_USE_REAL=true` to use real AWS Bedrock models — no code changes needed.

## Deployment

- **Local**: `uvicorn` or `docker-compose`
- **AWS**: Lambda + API Gateway + DynamoDB, defined in Terraform, CI via GitHub Actions