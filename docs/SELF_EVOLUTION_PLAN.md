# Dark Factory Self-Evolution Loop — Detailed Plan
*Authored: 2026-02-27 22:40 UTC by m2*

## The Goal
A system that detects its own gaps, synthesises solutions, deploys them, and measures results — with human approval at policy level only.

## Loop Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                    DARK FACTORY LOOP                            │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Monitor  │───▶│  Detect  │───▶│Synthesise│───▶│  Deploy  │ │
│  │ (cron)   │    │  (gap)   │    │(workflow)│    │ (Coolify)│ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       ▲                                               │        │
│       └───────────────── Measure ◀────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

## Sprint 1 — Memory Foundation (Week 1, Priority: CRITICAL)

### 1a. Org-Level Memory Namespace
**Problem**: Agents are silos. Knowledge doesn't cross namespaces.
**Solution**: Add `org_memory` Qdrant collection shared across all agents.
**Implementation**:
```bash
# Extend memory.sh to support --namespace flag
memory.sh store "..." --namespace org    # writes to org_memory
memory.sh search "..." --namespace org   # searches org_memory
memory.sh search "..." --namespace all   # searches agent + org + user
```
**Tasks**:
- [ ] Add `COLLECTION_NAME=org_memory` default shared collection to memory API
- [ ] Extend `memory.sh` with `--namespace [agent|org|user:<id>|all]`
- [ ] Seed org_memory with current MEMORY.md distilled content
- [ ] Add org_memory ingest to daily reflection cron
- [ ] Verify read access from alfred container

### 1b. Conversation Corpus Pipeline
**Problem**: Every conversation evaporates unless manually stored.
**Solution**: Session end hook exports to JSONL → nightly Qdrant ingest.
**Implementation**:
```bash
# OpenClaw session end hook (hooks/session-end.sh)
#!/bin/bash
SESSION_ID="$1"
openclaw sessions export "$SESSION_ID" --format jsonl >> \
  ~/.openclaw/workspace/archives/conversations/$(date +%Y-%m).jsonl

# Nightly ingest cron (02:30 UTC)
memory.sh ingest ~/.openclaw/workspace/archives/conversations/$(date +%Y-%m).jsonl \
  --namespace org --dedupe --quality-filter 0.5
```
**Tasks**:
- [ ] Create `archives/conversations/` directory structure
- [ ] Write `hooks/session-end.sh` export script
- [ ] Register hook in openclaw.json
- [ ] Write quality filter (skip exchanges < 100 tokens, no info density)
- [ ] Set up nightly 02:30 UTC ingest cron
- [ ] Verify conversation is searchable 24h after session

## Sprint 2 — Capability Registry (Week 2)

### 2a. Agent Skill Inventory
**Problem**: No way to query "which agent can handle X".
**Solution**: Extend fleet heartbeat with skill manifest. Store in Redis.
**Data structure**:
```json
{
  "agent": "alfred",
  "skills": ["research", "planka", "m2-memory", "browser"],
  "current_task": "BenchmarkSuite v2 run",
  "load": 0.3,
  "specialties": ["literature review", "data analysis"],
  "last_heartbeat": 1772230000
}
```
**API**:
```
GET /api/capabilities          → all agents + skills
GET /api/capabilities/alfred   → alfred's current state
POST /api/route?task=research  → returns best-fit agent
```
**Tasks**:
- [ ] Extend fleet heartbeat bash snippet to include skills array
- [ ] Add capability endpoint to fleet-dashboard FastAPI
- [ ] Build simple routing heuristic (load × skill match score)
- [ ] Wire m2 orchestrator to query /api/capabilities before dispatching

## Sprint 3 — Gap Detection + Synthesis (Week 3-4)

### 3a. Gap Detection Meta-Agent
**Problem**: No automated monitoring of system health → KPI gaps.
**Solution**: Cron meta-agent that watches KPIs and opens Planka cards.
**Watches**:
- Planka: Blocked cards > 2 for >48h → escalate
- Fleet: Agent down > 2 heartbeat cycles → alert
- Memory: Ingest lag > 48h → alert
- CI/CD: Last successful build > 7 days → alert
- Token cost: Agent > 2x average cost per session → investigate
**Implementation**:
```bash
# gap-detector.sh (runs every 4h via cron)
# 1. Query all KPIs
# 2. Compare to thresholds
# 3. For each gap: planka-pm.sh add "Gap: <description>" "Auto-detected..." now
# 4. Escalate to m2 via BGE proxy
```

### 3b. Workflow Synthesis Agent
**Problem**: Gaps get detected but solutions are manual.
**Solution**: LLM synthesises workflow.md from gap description.
**Flow**:
```
Gap card (Planka) → workflow-synth.sh "$GAP_DESC" → workflow.md
→ dark-factory-engine/bin/compile → skill/ → human approval (Telegram)
→ git push → Coolify auto-deploy → health check → monitor
```

## Sprint 4 — Closed CI/CD Loop (Week 4-5)

### 4a. Fix Act Runner
```yaml
# .gitea/workflows/build.yml repair
# Problem: DinD socket not exposing correctly
# Fix: Use privileged mode + explicit DOCKER_HOST
services:
  dind:
    image: docker:dind
    privileged: true  # ← was missing
    env:
      DOCKER_TLS_CERTDIR: ""
```

### 4b. Full Loop Test
1. Push to m2-desktop `base` branch
2. Act runner builds → pushes to registry
3. Coolify webhook triggers redeploy
4. Health check passes → new agents spawn with updated image
5. Health check fails → auto-rollback + alert

## Completion Criteria
The Dark Factory is "done" when:
- A gap is detected → card created → workflow synthesised → skill compiled → deployed
- With ZERO human intervention except policy-level approval (Telegram button)
- Time from gap detection to deployed fix < 2 hours (automated)

## Current Status: 45% → Target: 100% by Week 5
| Component | Status | Sprint |
|-----------|--------|--------|
| Workflow compiler | ✅ Done | 0 |
| Coolify deploy | ✅ Done | 0 |
| Monitor (load) | ✅ Done | 0 (tonight) |
| Fleet heartbeat | ✅ Done | 0 (tonight) |
| Org memory | 🔄 In Progress | 1 |
| Conversation corpus | 🔄 In Progress | 1 |
| Capability registry | 📅 Next | 2 |
| Gap detection | 📅 Next | 3 |
| Workflow synthesis | 📅 Planned | 3 |
| CI/CD loop | 📅 Planned | 4 |
| Full loop test | 📅 Planned | 5 |
