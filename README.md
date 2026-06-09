# CortexParse

CortexParse is a privacy-first, AI-native document intelligence platform that uses multimodal LLMs and workflow orchestration to extract structured information from documents.

Unlike traditional OCR solutions that only convert images into text, CortexParse focuses on understanding documents through AI-driven extraction, confidence-aware validation, refinement workflows, and human-in-the-loop escalation.

---

## Current Capabilities

### Document Processing

- PDF support
- PNG support
- JPG/JPEG support
- Structured documents
- Semi-structured documents
- Handwritten documents

### AI Extraction

- Multimodal document understanding
- Adaptive model routing
- Schema-driven extraction
- Field-level confidence scoring
- Template-aware extraction

### Workflow Orchestration

- LangGraph-based workflows
- Parallel document and template loading
- Confidence-aware validation
- Semantic correction
- Deterministic refinement
- Human-in-the-loop escalation

### Storage & Messaging

- MinIO document storage
- MinIO template storage
- RabbitMQ integration
- Sync and async processing modes

---

## Architecture

```text
                    ┌───────────────┐
                    │   Document    │
                    └───────┬───────┘
                            │
                            ▼

               ┌─────────────────────────┐
               │ Parallel Loading        │
               │                         │
               │ Document + Template     │
               └───────────┬─────────────┘
                           │
                           ▼

                ┌──────────────────────┐
                │ Classification       │
                └──────────┬───────────┘
                           │
                           ▼

                ┌──────────────────────┐
                │ Adaptive Routing     │
                └──────────┬───────────┘
                           │
                           ▼

                ┌──────────────────────┐
                │ Extraction           │
                └──────────┬───────────┘
                           │
                           ▼

                ┌──────────────────────┐
                │ Validation           │
                └──────────┬───────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼

      Publisher                  Semantic Correction
                                         │
                                         ▼

                              Deterministic Refinement
                                         │
                                         ▼

                                   Human Review
```

---

## Tech Stack

### Backend

- FastAPI
- LangGraph
- Pydantic

### AI

- Ollama
- Qwen2.5-VL:3B
- Qwen2.5-VL:7B
- Qwen2.5:3B

### Storage

- MinIO

### Messaging

- RabbitMQ

### Frontend

- React
- TypeScript
- Vite

### Infrastructure

- Docker Compose

---

## Supported Templates

Current template types:

- Logo
- PAN Card
- Aadhaar Card
- Generic Form
- Structured / Handwritten Prescription

Templates are stored and loaded dynamically from MinIO.

---

## Privacy-First Design

CortexParse is designed with privacy as a core principle.

- No permanent storage of extracted document contents
- No storage of extracted PII
- Ephemeral document processing
- Human review only when confidence thresholds are not met

---

## Project Structure

```text
cortexparse/
├── apps/
├── graph/
├── prompts/
├── shared/
└── training/
    └── synthetic-documents/
        ├── aadhaar/
        ├── ids/
        ├── invoices/
        ├── logos/
        ├── pan/
        └── receipts/
```

---

## Development Status

### Completed

- LangGraph workflow orchestration
- Ollama integration
- Multimodal extraction
- Adaptive model routing
- Confidence-aware validation
- Semantic correction
- Deterministic refinement
- Human review escalation
- PDF preprocessing
- Parallel workflow execution
- Template-aware extraction
- MinIO template management

### Planned

#### Phase 6

- Event-driven processing
- RabbitMQ consumers
- Workflow event streams

#### Phase 7

- Human review UI
- Field-level approval workflows

#### Phase 8

- Learning and adaptation
- Synthetic training datasets
- Confidence tuning

#### Phase 9

- Enterprise hardening
- Metrics
- Tracing
- Observability

#### Phase 10

- Deployment
- Benchmarking
- Demo showcase

---

## Status

🚧 Under active development.
