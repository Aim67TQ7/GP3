# GP3 Agent Examples

Complete, production-ready GP3 agent definitions. Each file is a deployable agent spec.

---

## The Shortest Path to a Working Agent

Drop any `.gp3.md` file directly into an LLM and ask it to build the agent.

**Example prompt:**

> Here is a GP3-encoded agent specification. Build a Python implementation using FastAPI. The agent should run as a cron job, query the database on schedule, and write structured observations to an agent_runs table.

The LLM reads the K-blocks, understands the routing logic, load triggers, integration requirements, and success criteria — and builds to spec. No translation layer. No reformatting. The GP3 file is the prompt.

This works because GP3 encodes intent, not syntax. The trilingual structure (CJK headers for concept density, English for technical precision, symbolic operators for logic) is already optimized for LLM context windows. The model reads GP3 the same way it reads well-structured code.

---

## What Each File Contains

Every example in this directory is a valid `.gp3.md` file with:

- A `# GP3 v1.0 | {name}` header
- K-blocks numbered from K0, each with an `id` and `load` trigger
- Real routing logic, not placeholder text
- A footer attributing the file

The `.gp3.md` extension means the same content as `.gp3` (the IANA-registered format), rendered as markdown for human readability and GitHub display.

---

## Examples

### `minimal.gp3.md` — Inquiry Router
2 K-blocks. The floor for a functional agent. Shows K0 identity + K1 routing with no extra overhead. Use this as a starting template.

### `manufacturing-scheduler.gp3.md` — Production Scheduler
5 K-blocks. Cron-driven job sequencing for a job shop. Shows domain-specific CJK headers (`序列最適化`, `容量分析`, `資材連携`), multi-step protocols, and constraint handling. Drop into Claude and ask for a FastAPI + Postgres implementation.

### `credit-hold-monitor.gp3.md` — AR Credit Monitor
4 K-blocks. Scheduled cron harness. Shows the RULE_4 verification pattern: `source_of_truth`, `success_criteria`, `verification_method`, and the full status enum (`success | partial | unverified | error | george_killed`). The K3 block makes agent accuracy self-reported, not assumed.

---

## Prompts That Work

**Build it:**
> Read this GP3 agent spec and build a Python implementation. Use FastAPI, Supabase for the database, and write one row to agent_runs per execution with status and token usage.

**Extend it:**
> Here is a GP3 agent spec. Add a K-block for Slack notification when escalation conditions are met. Keep the new block under 150 tokens and set load=on_escalation.

**Explain it:**
> Translate this GP3 file to plain English. Walk through each K-block and explain what the agent does, what decisions it makes, and what it escalates.

**Convert your own:**
> Here is a system prompt I wrote in plain English. Re-encode it in GP3 format following the trilingual structure in these examples.

---

## Full Documentation

| Resource | URL |
|---|---|
| Format Specification | [gp3.app/spec](https://gp3.app/spec) |
| Authoring Guide | [gp3.app/docs](https://gp3.app/docs) |
| AXUH Runtime | [gp3.app/AXUH](https://gp3.app/AXUH) |
| Online Converter | [converter.gp3.app](https://converter.gp3.app) |

---

n0v8v LLC | GP3 v1.0
