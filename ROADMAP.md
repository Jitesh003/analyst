# Roadmap

Two 45-minute sessions a week. **49 sessions left** of 52, so roughly five and a
half months. Each session leaves the repo working.

`[you]` = you type it, by hand. See the 15% rule in CLAUDE.md.
`[cc]`  = Claude Code writes it.

---

## Done

| # | Session | Learned |
|---|---|---|
| 0.1 | venv, deps, `.env`, `ask()` | token counts belong in the first call, not the last |
| 1.1 | SEC corpus fetcher, 112 filings | cache everything, throttle yourself, print what you parsed |
| 1.2 | Extraction schema + prompt | a thin prompt that you tested beats a thorough one you didn't |

---

## Stage 1 — Structured extraction (2 left)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 1.3 | Retry on malformed output and on 503 | `[you]` | two failure types, two different fixes: retry now vs back off |
| 1.4 | Run all 112. Read every failure | `[you]` | a batch must save as it goes, or one crash costs everything |

---

## Stage 2 — Eval harness (4) — DOES NOT MOVE

| # | Session | Who | What it teaches |
|---|---|---|---|
| 2.1 | 20 golden Q&As, by hand, no model help | `[you]` | what "a right answer" even means when the answer is prose |
| 2.2 | `score.py` — the comparison logic | `[you]` | exact match fails; grading generated text is the hard part |
| 2.3 | Pass rate + `evals/results/` format | `[you]` | why every number is stored with its model and date |
| 2.4 | Baseline run. Record it | `[you]` | a bad number beats no number, and yours will be bad |

---

## Stage 3 — Naive RAG (6)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 3.1 | Postgres + pgvector running | `[cc]` | why meaning needs a database and an index |
| 3.2 | `chunk()` — boundaries, overlap | `[you]` | where you cut the text decides what can ever be found |
| 3.3 | `embed()` + store vectors | `[you]` | what an embedding is: meaning as coordinates |
| 3.4 | `search()` — top-k, distances | `[you]` | "closest" and "most relevant" are not the same thing |
| 3.5 | Answer from retrieved context | `[you]` | grounding — making it use only what you gave it |
| 3.6 | Eval + start the failure taxonomy | `[you]` | classifying *why* it was wrong is the senior-engineer artifact |

---

## Stage 4 — Retrieval quality (6)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 4.1 | Diagnose the Stage 3 failures | `[you]` | reading failures instead of averaging them |
| 4.2 | Keyword / BM25 alongside vectors | `[you]` | vectors are bad at exact terms; keyword search isn't obsolete |
| 4.3 | Hybrid merge + scoring | `[you]` | combining two rankings that disagree |
| 4.4 | Reranking | `[you]` | paying a smarter model to re-sort a shortlist |
| 4.5 | Chunking experiments, each measured | `[you]` | that a change you believed in did nothing |
| 4.6 | Before/after write-up. Keep the losers | `[cc]` format | the failed changes are the credible part |

---

## Stage 5 — Tool use (5)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 5.1 | XBRL into a real schema | `[cc]` | modelling the structured half |
| 5.2 | Tool schemas | `[you]` | the description *is* the interface the model sees |
| 5.3 | NL→SQL tool | `[you]` | generating SQL safely: read-only, bounded, validated |
| 5.4 | Retrieval tool + the router | `[you]` | choosing a tool — this is where "agent" begins |
| 5.5 | Eval with tools | `[you]` | a new failure: right answer, wrong tool |

---

## Stage 6 — Single agent (6)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 6.1 | ReAct loop: plan → call → observe | `[you]` | 40 lines of code, one genuinely new idea |
| 6.2 | Termination condition | `[you]` | how a loop knows to stop, and the cost when it doesn't |
| 6.3 | Memory across steps | `[you]` | what to carry forward, and why more isn't better |
| 6.4 | Timeouts, tool errors, retries | `[you]` | failure handling *inside* a loop is a different problem |
| 6.5 | Eval | `[you]` | whether the agent actually beat the one-shot pipeline |
| 6.6 | Taxonomy: loop failures | `[you]` | naming the ways a loop goes wrong |

---

## Stage 7 — Observability (4)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 7.1 | Per-step traces | `[cc]` | debugging something that isn't deterministic |
| 7.2 | Token / cost / latency per step | `[cc]` | what one query costs and where the time goes |
| 7.3 | Failure taxonomy formalised | `[you]` | ad-hoc notes become categories with counts |
| 7.4 | Trend report across runs | `[cc]` | the trend is the evidence, not the snapshot |

---

## Stage 8 — Multi-agent (8)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 8.1 | Shared state design | `[you]` | how agents coordinate without corrupting each other |
| 8.2 | Planner | `[you]` | decomposing a question into answerable pieces |
| 8.3 | Researcher(s) | `[you]` | running sub-tasks, and in parallel |
| 8.4 | Critic | `[you]` | a model checking a model — and when that fails |
| 8.5 | Writer | `[you]` | synthesis into one answer with one voice |
| 8.6 | Citation checks | `[you]` | every claim traces to a source, or it's cut |
| 8.7 | Cost per agent | `[you]` | finding which agent burns the budget |
| 8.8 | Eval vs the single agent | `[you]` | being willing to report that complexity didn't pay |

---

## Stage 9 — Ship (6)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 9.1 | FastAPI endpoints | `[cc]` | the pipeline behind an interface |
| 9.2 | Streaming responses | `[cc]` | what progressive output costs in complexity |
| 9.3 | Next.js UI | `[cc]` | — |
| 9.4 | UI polish | `[cc]` | — |
| 9.5 | Deploy | `[cc]` | secrets, environments, cold starts |
| 9.6 | Public repo hygiene, secret sweep | `[cc]` | making it something a stranger can clone and run |

---

## Stage 10 — Write-up (2)

| # | Session | Who | What it teaches |
|---|---|---|---|
| 10.1 | README + architecture diagram | `[cc]` draft | explaining it to someone who wasn't there |
| 10.2 | Numbers, taxonomy, interview prep | `[you]` | the project round is 45 minutes of "why did you choose that" |

---

## The honesty check

End of every stage: explain it from memory, repo closed. What it does, why it's
built that way, what you tried that didn't work.

Can't? Something was outsourced. Rewrite that piece by hand.

## Numbers to know cold by Stage 10

Baseline pass rate · pass rate after reranking · p95 latency · cost per query ·
top three failure categories.

## Open decisions

- [x] Corpus — SEC 10-Ks, 16 D2C/consumer companies, 2019–2026
- [ ] WSL vs Windows — decide before 3.1 (Postgres)
