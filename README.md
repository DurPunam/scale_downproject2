# ScaleDown Commerce AI

Production-grade, microservice-based e-commerce recommendation and RAG platform.

## Quickstart

```bash
docker compose -f infra/docker-compose.yaml up --build
```

## Architecture

See `docs/architecture.md` for the ASCII and Mermaid diagrams.

## Services

- API Gateway
- Auth Service
- Scraper Service
- Compression Router Service
- ScaleDown Client Service
- Quality Validator Service
- Product Service
- Embedding Service
- RAG Service
- Recommendation Service
- Price Intelligence Service
- Spatial Reasoning Service
- Review Analysis Service
- Admin / Model Ops Service
