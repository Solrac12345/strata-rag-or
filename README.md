
# Strata RAG Orchestrator

> Production-oriented multi-agent RAG system (FastAPI + AWS serverless stubs).

## Overview / Aperçu
**EN**: Clean architecture showcasing multi-agent orchestration (Routing + QA with RAG), a simple RAG pipeline, FastAPI service, AWS stubs (Bedrock, S3, DynamoDB, Lambda), tests, Docker, CI, and Terraform IaC.

**FR**: Architecture propre démontrant l'orchestration multi-agents (Routage + QA avec RAG), un pipeline RAG simple, un service FastAPI, des stubs AWS (Bedrock, S3, DynamoDB, Lambda), des tests, Docker, CI et Terraform.

## Folder layout / Structure des dossiers
**EN**
StrataRAG Orchestrator is a multi-agent RAG (Retrieval-Augmented Generation) system built for AWS.

What it does in one sentence:
It receives a user question, routes it to the right AI agent, retrieves relevant documents, and generates a grounded answer using an LLM.

How it works (flow):

User query → API (/orchestrate)
                ↓
         RoutingAgent  →  decides which agent handles it (currently: QA)
                ↓
           QAAgent
             ├── Retriever  →  embeds the query, searches vector store, finds relevant docs
             └── LLMService →  sends context + question to Bedrock, gets answer
                ↓
         Response: { answer, sources, routed_agent }
The 3 layers:
api/ — FastAPI REST endpoints (/health, /orchestrate, /embed)
app/ — Business logic: agents, orchestrator, RAG pipeline (embeddings, vector store, retriever, document store)
infrastructure/ — AWS integrations (Bedrock LLM, S3 for KB files, DynamoDB for persistence, Lambda handler for serverless)

Deployment:
Local: uvicorn or docker-compose
AWS: Lambda + API Gateway + DynamoDB, defined in Terraform, with CI via GitHub Actions

Key design choice:
Everything runs locally with stubs (fake embeddings, fake LLM responses, in-memory vector store). Flip BEDROCK_USE_REAL=true and deploy to AWS to use real Bedrock models — no code changes needed.

---------------------------------------------------------------------------------------------------------------------------------------------------
**FR**
StrataRAG Orchestrator est un système RAG (Retrieval-Augmented Generation) multi-agents conçu pour AWS.

Ce qu’il fait en une phrase :
Il reçoit une question de l’utilisateur, l’achemine vers le bon agent d’IA, récupère les documents pertinents et génère une réponse ancrée en utilisant un LLM.

Comment ça marche (flow) :

API de requête utilisateur (/orchestrer)
                
         RoutingAgent décide quel agent s’en occupe (actuellement : QA)
                
           QAAgent
             Retriever intègre la requête, recherche dans le magasin de vecteurs, trouve des documents pertinents
             LLMService envoie le contexte + question à Bedrock, obtient la réponse
                
         Réponse : { réponse, sources, agent routed_agent }
Les 3 couches :
api/ — points de terminaison REST FastAPI (/santé, /orchestrer, /embed)
app/ — Logique métier : agents, orchestrateur, pipeline RAG (embeddings, vector store, retriever, document store)
infrastructure / — intégrations AWS (Bedrock LLM, S3 pour les fichiers KB, DynamoDB pour la persistance, gestionnaire Lambda pour le serverless)

Déploiement :
Local : uvicorn ou docker-compose
AWS : Lambda + API Gateway + DynamoDB, défini dans Terraform, avec CI via GitHub Actions

Choix de conception clé :
Tout fonctionne localement avec des stubs (fausses incorporations, fausses réponses LLM, magasin de vecteurs en mémoire). Retournez BEDROCK_USE_REAL=true et déployez-le sur AWS pour utiliser des modèles Bedrock réels — aucun changement de code nécessaire.
