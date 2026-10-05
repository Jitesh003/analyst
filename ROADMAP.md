# Roadmap

Two 45-minute sessions a week. ~52 sessions total, so roughly **six months**.
Each session leaves the repo working.

`[you]` = you type it, by hand. See the 15% rule in CLAUDE.md.
`[cc]`  = Claude Code writes it.

---

## Stage 0 — Skeleton (1/2 used) ✅

| # | Session | Who |
|---|---|---|
| 0.1 | venv, pinned deps, `.env`, `ask()` with token logging | `[you]` ask() |

Done 2026-09-22, one session early.

---

## Stage 1 — Structured extraction (4)

| # | Session | Who |
|---|---|---|
| 1.1 | ~~Corpus + loader~~ done early | `[cc]` ✅ |
| 1.2 | Target schema + the extraction prompt | `[you]` |
| 1.3 | Parse + validate. Retry on malformed output | `[you]` |
| 1.4 | Run the whole corpus. Read every failure | `[you]` |

**Done when:** a document becomes typed JSON, and a malformed response
retries instead of crashing.

---

## Stage 2 — Eval harness (4) — DOES NOT MOVE

| # | Session | Who |
|---|---|---|
| 2.1 | Write 20 golden Q&As by hand. No model help | `[you]` |
| 2.2 | `score.py` — the comparison logic | `[you]` |
| 2.3 | Pass-rate + `evals/results/` file format | `[you]` scorer |
| 2.4 | Baseline run. Record the number. It will be bad | `[you]` |

**Done when:** `score.py` prints a pass rate. Every result file records the
pinned model name next to the number, or the number means nothing later.

---

## Stage 3 — Naive RAG (6)

| # | Session | Who |
|---|---|---|
| 3.1 | Postgres + pgvector running | `[cc]` |
| 3.2 | `chunk()` — boundaries and overlap | `[you]` |
| 3.3 | `embed()` + store vectors | `[you]` |
| 3.4 | `search()` — top-k, distance handling | `[you]` |
| 3.5 | Answer from retrieved context. The prompt | `[you]` |
| 3.6 | Eval run. Start the failure taxonomy | `[you]` |

**Done when:** chunk → embed → pgvector → top-k → answer, with an eval number.

---

## Stage 4 — Retrieval quality (6)

| # | Session | Who |
|---|---|---|
| 4.1 | Diagnose the Stage 3 failures. Where is it losing? | `[you]` |
| 4.2 | Keyword/BM25 retrieval alongside vectors | `[you]` |
| 4.3 | Hybrid merge + scoring | `[you]` |
| 4.4 | Reranking | `[you]` |
| 4.5 | Chunking experiments — measure each one | `[you]` |
| 4.6 | Before/after write-up. Keep the losers | `[cc]` format |

**Done when:** you can state what reranking bought you, as a number.

---

## Stage 5 — Tool use (5)

| # | Session | Who |
|---|---|---|
| 5.1 | Structured DB: schema + load | `[cc]` |
| 5.2 | Tool schemas | `[you]` |
| 5.3 | NL→SQL tool | `[you]` |
| 5.4 | Retrieval tool + the router that picks one | `[you]` |
| 5.5 | Eval with tools. New failure category: wrong tool | `[you]` |

---

## Stage 6 — Single agent (6)

| # | Session | Who |
|---|---|---|
| 6.1 | ReAct loop: plan → call → observe → repeat | `[you]` |
| 6.2 | Termination condition. Make it loop first | `[you]` |
| 6.3 | Memory / scratchpad across steps | `[you]` |
| 6.4 | Timeouts, retries, tool failure handling | `[you]` |
| 6.5 | Eval | `[you]` |
| 6.6 | Taxonomy update: loop failures | `[you]` |

---

## Stage 7 — Observability (4)

| # | Session | Who |
|---|---|---|
| 7.1 | Per-step traces | `[cc]` plumbing |
| 7.2 | Token / cost / latency per step | `[cc]` plumbing |
| 7.3 | Failure taxonomy formalised | `[you]` |
| 7.4 | Report across runs — trend, not snapshot | `[cc]` |

**Done when:** you can say what one query costs and where the time goes.

---

## Stage 8 — Multi-agent (8)

| # | Session | Who |
|---|---|---|
| 8.1 | Shared state design | `[you]` |
| 8.2 | Planner | `[you]` |
| 8.3 | Researcher(s) | `[you]` |
| 8.4 | Critic | `[you]` |
| 8.5 | Writer | `[you]` |
| 8.6 | Citation checks | `[you]` |
| 8.7 | Cost per agent. Find the expensive one | `[you]` |
| 8.8 | Eval vs single agent. It may lose — say so | `[you]` |

Hand-roll first. Only then consider a framework, and compare.

---

## Stage 9 — Ship (6)

| # | Session | Who |
|---|---|---|
| 9.1 | FastAPI endpoints | `[cc]` |
| 9.2 | Streaming responses | `[cc]` |
| 9.3 | Next.js UI | `[cc]` |
| 9.4 | UI polish | `[cc]` |
| 9.5 | Deploy | `[cc]` |
| 9.6 | Public repo hygiene. Secret sweep | `[cc]` |

---

## Stage 10 — Write-up (2)

| # | Session | Who |
|---|---|---|
| 10.1 | README + architecture diagram | `[cc]` draft |
| 10.2 | Real numbers + taxonomy + interview prep | `[you]` |

---

## The honesty check

End of every stage: explain it from memory, repo closed. What it does, why it's
built that way, what you tried that didn't work.

Can't? Something was outsourced. Rewrite that piece by hand.

## Numbers to know cold by Stage 10

Baseline pass rate · pass rate after reranking · p95 latency · cost per query ·
top three failure categories.

## Open decisions

- [x] Corpus — SEC 10-Ks, 16 D2C/consumer companies, 2019+ (`analyst/corpus.py`)
- [ ] WSL vs Windows — decide before 3.1 (Postgres)
