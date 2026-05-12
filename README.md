# GP3

**Glyph-Pipeline-Trilingual** — structured encoding format for AI agent behavioral specifications.  
60-70% token reduction. Zero logic loss. [IANA registered](https://www.iana.org/assignments/media-types) `application/vnd.gp3`.

---

## The Problem

Agent system prompts are written in verbose English prose. Every token in that prose costs money on every single inference. A 2,000-token system prompt, called 10,000 times a month, is 20 million tokens of overhead — before the agent does anything.

## The Approach

GP3 encodes the same logic using three layers simultaneously:

| Layer | What it does | Example |
|---|---|---|
| L1 CJK | Concept-dense structural headers | `身份` replaces "Identity / Role Definition" |
| L2 English | Technical terms, identifiers, variable names | `customer_id`, `order_status` — never compressed |
| L3 Operators | Symbolic logic replacing verbose connectives | `∅` replaces "never / must not / do not" |

**Before — plain English (73 tokens):**
```
You are a customer service agent. When a customer asks about order status,
look up their order in the database. Never guess the order status. If there
is a safety issue, escalate to the supervisor immediately. For complaints
about defective products, collect the part number, lot number, and defect
description, then create a nonconformance record.
```

**After — GP3 (27 tokens):**
```
<K0 id="身份" load="always">
角色: ServiceBot | Customer Service | Manufacturing
役割: order_status, complaint_handling
∅guess_order_status
safety_issue → ↑supervisor | P0
</K0>

<K1 id="路由" load="routing">
intent∋{complaint,defect} → collect {part_no, lot_no, defect_desc} → create_NCR
</K1>
```

Same semantics. 63% fewer tokens.

---

## File Formats

GP3 uses two file variants:

| Extension | Purpose | Use for |
|---|---|---|
| `.gp3` | Agent file. IANA registered `application/vnd.gp3`. | Runtime consumption, AXUH agent definitions, production |
| `.gp3.md` | Human-readable variant. Identical content. | GitHub, editors, Claude conversations, review and sharing |

The `.gp3` file is what the runtime loads. The `.gp3.md` file is how humans read, share, and version-control the same content. Write in `.gp3.md`, deploy as `.gp3`.

---

## File Structure

Every valid GP3 file has three parts:

```
# GP3 v1.0 | {document-name}          ← header (required, within first 512 bytes)

<K0 id="身份" load="always">           ← K-blocks (one or more)
  content
</K0>

---
n0v8v LLC | GP3 v1.0 | {name}.gp3     ← footer (optional)
```

K-blocks are numbered sequentially from K0. Each block has an `id` (CJK identifier) and a `load` trigger that controls when it enters the LLM context window.

**Standard K-block conventions:**

| Block | ID | Category |
|---|---|---|
| K0 | 身份 | Identity — agent name, role, voice, trust boundaries |
| K1 | 路由 | Routing — intent classification, priority mapping |
| K2-K3 | domain-specific | Operational logic — primary agent behavior |
| K4 | 能力 | Capabilities — tools, integrations |
| K5 | 参考 | Reference — metrics, patterns, feedback loops |

**Load triggers:**

| Trigger | When |
|---|---|
| `always` | Every execution. Use for K0 and K1 only. Keep under 200 tokens each. |
| `routing` | During task classification. Handler blocks activated by K1. |
| `generation` | During output generation. Response templates, format rules. |
| `on_{event}` | On specific event — `on_error`, `on_request`. |
| `runtime_only` | Active execution only. Tool definitions, API integrations. |
| `post_exec` | After execution. Logging, metrics, learning loops. |

---

## Operators

| Operator | Meaning | Replaces |
|---|---|---|
| `→` | leads to, routes to | "leads to", "results in", "produces" |
| `∧` | AND | "and", "as well as" |
| `∨` | OR | "or", "alternatively" |
| `∅` | NOT, never, prohibited | "never", "must not", "do not" |
| `∋` | contains, includes | "contains", "includes" |
| `∈` | within range | "between X and Y", "in range of" |
| `@` | triggered at, by | "triggered by", "activated when" |
| `{}` | set, group | "set of", "list of" |
| `\|` | separator, alternative | list delimiter |
| `↑` | escalate | "escalate to", "elevate to" |
| `↓` | de-escalate | "downgrade", "lower to" |
| `≤` / `≥` | at most / at least | "no more than", "at least" |

---

## Quick Start

### Encode a file

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key

python encoder.py my-agent.md --stats
# Output: my-agent.gp3.md
# Input:  ~340 tokens
# Output: ~118 tokens
# Reduction: 65.3%
```

### Validate a file

```bash
python validator.py my-agent.gp3.md
# [PASS] my-agent.gp3.md
```

### Use from stdin

```bash
cat system-prompt.md | python encoder.py - -n my-agent -o my-agent.gp3.md
```

---

## Examples

See the [`examples/`](./examples/) directory for complete, valid GP3 files:

- [`minimal.gp3.md`](./examples/minimal.gp3.md) — smallest valid GP3 file
- [`customer-service-agent.gp3.md`](./examples/customer-service-agent.gp3.md) — full 5-block service agent
- [`manufacturing-scheduler.gp3.md`](./examples/manufacturing-scheduler.gp3.md) — production scheduling with domain CJK headers

More examples at [gp3.app/examples](https://gp3.app/examples).

---

## Documentation

| Resource | URL |
|---|---|
| Format Specification | [gp3.app/spec](https://gp3.app/spec) |
| Authoring Guide | [gp3.app/docs](https://gp3.app/docs) |
| Examples | [gp3.app/examples](https://gp3.app/examples) |
| AXUH Runtime | [gp3.app/AXUH](https://gp3.app/AXUH) |
| Online Converter | [converter.gp3.app](https://converter.gp3.app) |

---

## IANA Registration

The `application/vnd.gp3` media type is registered with the Internet Assigned Numbers Authority.

| Field | Value |
|---|---|
| Media Type | `application/vnd.gp3` |
| File Extension | `.gp3` |
| Magic Number | `# GP3 v` within first 512 bytes |
| Encoding | UTF-8 |
| Author | Robert Clausing, n0v8v LLC |
| Contact | robert@gp3.app |

---

## License

MIT — see [LICENSE](./LICENSE).

GP3 format specification and methodology: n0v8v LLC. All rights reserved.  
This repository contains a reference implementation under MIT license.
