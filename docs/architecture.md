## System Architecture

ASCII diagram:

+--------------------+       +-------------------+       +-------------------+
|  Web / Mobile UI   | ----> |   API Gateway     | ----> |   Auth Service    |
+--------------------+       +-------------------+       +-------------------+
          |                              |                          |
          |                              v                          v
          |                      +---------------+          +---------------+
          |                      | Product Svc   |          | Admin / MLOps |
          |                      +---------------+          +---------------+
          |                              |                          |
          |                              v                          v
          |                      +---------------+          +---------------+
          |                      | RAG Service   |          | Review Analysis|
          |                      +---------------+          +---------------+
          |                              |                          |
          |                              v                          v
          |                      +---------------+          +---------------+
          |                      | Reco Service  |          | Price Intel   |
          |                      +---------------+          +---------------+
          |                              |                          |
          |                              v                          v
          |                      +---------------+          +---------------+
          |                      | Spatial Svc   |          | Embedding Svc |
          |                      +---------------+          +---------------+
          |                              |                          |
          |                              v                          v
          |                   +--------------------+     +------------------+
          |                   | Quality Validator  |     | Compression Router|
          |                   +--------------------+     +------------------+
          |                              |                          |
          |                              v                          v
          |                   +--------------------+     +------------------+
          |                   | ScaleDown Client   |     | Scraper Service  |
          |                   +--------------------+     +------------------+
          |                              |
          |                              v
          |                   +--------------------+
          |                   | External ScaleDown |
          |                   | API (v2 batch)     |
          |                   +--------------------+
          |
          v
 +------------------+   +-------------------+   +-------------------+
 | Postgres+pgvector|<->| Redis (L1 cache)  |<->| Disk Cache (L2)    |
 +------------------+   +-------------------+   +-------------------+
          ^
          |
  +------------------+
  | Kafka / RabbitMQ |
  +------------------+

Observability: Prometheus + Grafana + Loki + OpenTelemetry
CI/CD: GitHub Actions, Containers: Docker, Orchestration: Kubernetes (HPA)

Mermaid diagram:

```mermaid
flowchart LR
  UI[Web / Mobile UI] --> GW[API Gateway]
  GW --> AUTH[Auth Service]
  GW --> PROD[Product Service]
  GW --> RAG[RAG Service]
  GW --> RECO[Recommendation Service]
  GW --> PRICE[Price Intelligence Service]
  GW --> SPATIAL[Spatial Reasoning Service]
  GW --> REVIEW[Review Analysis Service]
  GW --> ADMIN[Admin / Model Ops Service]

  SCRAPER[Scraper Service] --> COMP[Compression Router]
  COMP --> SDCLIENT[ScaleDown Client]
  SDCLIENT --> SDEXT[ScaleDown API v2]
  SDCLIENT --> VAL[Quality Validator]
  VAL --> EMB[Embedding Service]
  EMB --> RAG
  EMB --> RECO

  PROD --> PG[(Postgres + pgvector)]
  RAG --> PG
  RECO --> PG
  PRICE --> PG
  REVIEW --> PG

  GW --> CACHEL1[(Redis L1)]
  CACHEL1 <--> CACHEL2[(Disk Cache L2)]

  QUEUE[(Kafka / RabbitMQ)] --> SCRAPER
  QUEUE --> COMP
  QUEUE --> EMB
  QUEUE --> RECO

  subgraph Observability
    PROM[Prometheus] --> GRAF[Grafana]
    LOKI[Loki]
    OTEL[OpenTelemetry]
  end

  GW --> OTEL
  PROD --> OTEL
  RECO --> OTEL
  RAG --> OTEL
  EMB --> OTEL
```
