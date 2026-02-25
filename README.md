# Guild-AI-New: Small Business Executive Suite 🚀

**The natively migrated, high-performance engine for decentralized small business intelligence.**

This repository contains the complete, native implementation of the Guild-AI platform, successfully migrated from the legacy ADK codebase. It features a sophisticated multi-agent orchestration system, real-time activity visualization, and deep educational transparency.

## 🏛️ Architecture Overview

The system is built on a modular "Native Intelligence" architecture, leveraging specialized agents that collaborate under the guidance of the **Orchestrator Agent**.

- **Agent Theater**: A real-time, event-driven UI that visualizes agent reasoning ("Why") and technical execution ("How").
- **Evaluator League**: A built-in verification layer that ensures quality across Brand, Facts, and SEO.
- **Master Workflows**: High-level autonomous sequences like `grand_opening` that coordinate Marketing, Sales, and Research.
- **Event Bus & Persistence**: High-frequency event streaming with Redis-backed persistence for production scalability.

## 📁 Directory Structure

- `services/api`: Backend FastAPI services and agent logic.
- `services/web`: React-based frontend with Framer Motion animations.
- `services/core`: The "Brain" - registry, models, LLM integration, and workflows.
- `adk/`: Autonomous Development Kit - pre-built specialized agent capabilities.
- `scripts/`: Verification and utility scripts for lifecycle management.

## 🚀 Getting Started

### Local Setup
1. **Initialize Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Launch Services**:
   ```bash
   # Launch Backend
   python main.py
   
   # Launch Frontend
   cd services/web && npm install && npm run dev
   ```

### Production Readiness
The project is container-ready with multi-stage builds.
```bash
docker build -t guild-ai-new .
```

## 🔐 Security & Persistence
- **Secure Logging**: PII-aware logging in `services/core/security`.
- **Redis Cache**: Automated event buffering for the Theater UI.
- **Vertex AI / GPT-4**: Configurable LLM backends with circuit-breaker fallbacks.

## 🏛️ Repository Handover
Natively migrated and initialized as a fresh Git repository.
- **Remote**: `https://github.com/ArnovZ080/Guild-AI-New.git`

---
*Built with ❤️ for the future of Small Business Intelligence.*
