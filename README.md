# ScaleDown Commerce AI

Production-grade, microservice-based e-commerce recommendation and RAG platform.

## Prerequisites

- Docker Desktop (for backend services)
- Node.js 18+ (for frontend)
- Git

## Quick Start

### Backend Setup

1. Ensure Docker Desktop is running
2. Start all backend services:

```bash
docker compose -f infra/docker-compose.yaml up --build
```

The backend services will be available at:
- API Gateway: `http://localhost:8000`
- ScaleDown Client: `http://localhost:8005`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- RabbitMQ: `localhost:5672`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the root directory with:

```
SCALEDOWN__API_KEY=your_api_key_here
```

## Architecture

See `docs/architecture.md` for the ASCII and Mermaid diagrams.

## Services

- **API Gateway** - Main entry point for all API requests
- **Auth Service** - Authentication and authorization
- **Scraper Service** - Web scraping for product data
- **Compression Router Service** - Request routing and compression
- **ScaleDown Client Service** - Client SDK integration
- **Quality Validator Service** - Data quality validation
- **Product Service** - Product catalog management
- **Embedding Service** - Vector embeddings for ML
- **RAG Service** - Retrieval-Augmented Generation
- **Recommendation Service** - Product recommendations
- **Price Intelligence Service** - Price analysis and optimization
- **Spatial Reasoning Service** - Location-based features
- **Review Analysis Service** - Customer review processing
- **Admin / Model Ops Service** - Model management and operations

## Development

### Frontend Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Backend Commands

- `docker compose -f infra/docker-compose.yaml up` - Start services
- `docker compose -f infra/docker-compose.yaml down` - Stop services
- `docker compose -f infra/docker-compose.yaml logs` - View logs

## Tech Stack

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python 3.11
- PostgreSQL with pgvector
- Redis
- RabbitMQ
- PyTorch
- Sentence Transformers
