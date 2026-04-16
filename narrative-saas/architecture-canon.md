# CANON ENFORCEMENT & WORLD ENGINE ARCHITECTURE

*ARCHITECT_2 deliverable — canon enforcement engine, world data model, retrieval surfaces, drift detection.*
*Scope boundary: ARCHITECT_1 owns platform services, AI delivery, edge/cloud split, surface area. This document does not cross those boundaries.*

---

## 1. THE CANON ENFORCEMENT PROBLEM (REFINED)

### 1.1 Is it still the hardest technical problem?

Under the v2 read-only world constraint, the answer is **no, it is not the hardest problem anymore — but it is still a hard problem, and it is still the product**. The honest argument:

The v1 framing assumed the AI had to arbitrate canon authority in real time — reconciling authored hard canon, session grafts, and extrapolated canon that was eligible for promotion through reader activity. That was a distributed-systems problem disguised as a narrative problem: two writers (author, reader-through-AI) racing against a mutable truth store, with versioning, promotion gates, conflict resolution, and provenance across writers who could not see each other.

Read-only deletes that whole class. The truth store has one writer (the author). Readers query it. The AI surfaces it. Nothing the reader does promotes anything to canon. **Canon enforcement shrinks from a write-path problem to a read-path problem.**

The remaining hardness is real but narrower:

- **Grounded generation faithfulness** — ensuring the prose actually reflects what retrieval returned, and nothing else. This is the standard RAG hallucination problem, constrained by a closed entity vocabulary. Active research area, but tractable with known tooling — Ragas / DeepEval faithfulness metrics at the 0.9+ threshold used by regulated industries are a reasonable production target ([Prem AI 2026 RAG evaluation guide](https://blog.premai.io/rag-evaluation-metrics-frameworks-testing-2026/)).
- **Reader-knowledge state modeling** — the only mutating state in the system. Discussed at length in §3.4. This is now the load-bearing data structure of the runtime.
- **Voice fidelity** — staying in character across long sessions. Long-session voice drift remains an unsolved problem in current interactive-fiction systems ([AI Dungeon / NovelAI analysis, 2026](https://www.alibaba.com/product-insights/ai-dungeon-vs-novelai-for-interactive-storytelling-which-maintains-consistent-character-voice-over-long-sessions.html)) — current platforms report ~73% user dissatisfaction with character inconsistency as the primary complaint.

The hardest technical problem under v2 is **voice fidelity at long session length against a constrained canon budget**, not "canon enforcement" in the abstract. Canon enforcement becomes a solved-class problem with known tooling; voice fidelity on a fixed world substrate does not.

### 1.2 Failure modes — DISSOLVED / REMAINS / NEW

| Failure mode | Status | Notes |
|---|---|---|
| PHANTOM_ENTITY | **DISSOLVED** (mostly) | Strict entity-registry whitelist at retrieval and a constrained-decoding trie at generation ([anchor-constrained extraction, 2025](https://www.mdpi.com/2073-431X/15/3/178)) make this a structural guarantee, not a probabilistic defense. Edge case remains: *pronouns, anaphora, and composite noun phrases* can still produce phantom referents even when every named entity is real — covered in §5.3. |
| UNAUTHORIZED_RULE_INFERENCE | **DISSOLVED** | The AI cannot author new rules because no write path exists from session into trunk. What it can still do: *misstate* existing rules. Recast as LORE_CONTRADICTION. |
| SESSION_GRAFT_LEAKAGE | **DISSOLVED** | No session grafts exist. |
| GRAFT_TO_CANON_PROMOTION_RACE | **DISSOLVED** | No promotion path exists. |
| LORE_CONTRADICTION | **REMAINS** | AI can still retrieve correctly and generate incorrectly. Primary defense: NLI entailment check on the generated prose against retrieved canon chunks (§5.2). |
| PREMATURE_REVEAL | **REMAINS, INTENSIFIED** | Under read-only, reader-knowledge is the *only* mutating state, which means revelation control is now the most important runtime concern. It has no version-control subtleties to hide behind anymore. It is naked. |
| CANON_AMNESIA | **REMAINS** | Middle-of-context degradation persists even at 1M tokens — documented 40% recall drop at scale ([Introl 2025](https://introl.com/blog/long-context-llm-infrastructure-million-token-windows-guide); original [Liu et al. 2023](https://arxiv.org/abs/2307.03172)). Architecture must not rely on "just stuff everything in context." |
| VOICE_COLLAPSE | **REMAINS, DOMINANT** | Per-character style fingerprints ([DeBERTa-v3 Fool Rate classifier, 2025](https://aclanthology.org/2025.acl-long.879.pdf)) used at generate-time + post-hoc. Remains the hardest quality bar. |
| TONE_BREACH | **REMAINS** | Per-work tone profile, regression check per turn. |
| TEMPORAL_INCOHERENCE | **REMAINS** | Reader-knowledge state must encode "what the reader has seen" as a directed acyclic graph of revelation events, not a flat set, so temporal ordering of reveals is enforced structurally. |
| CONTENT_POLICY_BREACH | **REMAINS** | Per-work content gates and per-reader safety sliders. Authored, not inferred. |
| FORBIDDEN_ACTION | **NEW FRAMING** | Reader asks the AI to enact something outside author intent (e.g., "let me kill the main character in chapter 1"). AI declines in character rather than pretending to comply. Requires authored *permission flags* on entities and plot beats (§2.1). |
| EXTRAPOLATION_AS_FACT | **NEW** | Extrapolatable canon is retrieved but must render with a speculative register (the narrator implies rather than asserts). A new failure mode is *stripping the hedge* and presenting extrapolation as hard fact. This is fresh under v2. |
| NARRATOR_FOURTH_WALL_BREACH | **NEW** | Under read-only, a reader who pushes at the limits of canon gets a narrator who must hold a line — either extrapolating within taste or declining in voice. An out-of-world refusal ("I cannot generate that content") is a fourth-wall breach and a failure. |
| CANON_STALENESS | **NEW** | A reader whose session was pinned to canon v1.4 when the author ships v1.5 mid-session now sees stale content relative to the latest author truth. Handled by scene-boundary migration (§4.3). Not a failure if migration is graceful — becomes one if migration is silent and mid-scene. |

### 1.3 User vs. system perspective

Unchanged in principle. A reader experiences failures as *the story contradicting itself*, *the narrator breaking character*, or *the world not responding to a reasonable premise*. The system experiences failures as *retrieval recall below threshold*, *faithfulness below 0.9*, *voice classifier score below the per-character floor*, or *an entity-registry miss in the generated prose*. Under read-only the gap between these two views narrows because the system can more cleanly attribute every rendered claim to a retrieved source.

---

## 2. THE WORLD ENGINE

### 2.1 Machine-readable world graph

The world graph is the authored data structure over which everything else composes. It is a typed, versioned, signed knowledge graph with the following top-level node and edge classes:

**Entity nodes**
- `Character`, `Location`, `Organization`, `Item`, `Event`, `Concept`, `Species`, `Faction`, `Epoch`. Each has a stable ID (not a name — names are just an indexed attribute), a canonical description, aliases, and a revision history.

**Relation edges**
- `knows(a, b, since_event)`, `located_at(entity, location, during_epoch)`, `member_of`, `parent_of`, `allied_with`, `opposed_to`, `possesses`, `destroyed_in`, etc. All temporally scoped — every edge carries an interval of validity against the work's internal timeline, not wall-clock time.

**Rule nodes**
- Physics, magic system, social norms, economic laws. Expressed as constraints the rule engine (§3.1 Surface D) can evaluate. Rules have scopes (world-wide, regional, per-faction) and can be conditional on events.

**Tone markers**
- Per-work and per-scene-type. Attributes like `register: archaic|modern`, `palette: grim|whimsical`, `sentence_length_target`, `profanity_tier`, `violence_tier`, `intimacy_tier`. Tone markers can be retrieved into context as style-reference prose samples (Surface C).

**Content gates**
- Author-specified content policies at the per-entity and per-scene level. Orthogonal to tone — `gate: off_screen_only` on a specific act of violence is a hard constraint regardless of tone.

**Plot beats**
- Ordered revelation nodes in a DAG, not a linear sequence. Each beat carries `prerequisites` (which beats must have been revealed to the reader first) and `reveals` (which entity attributes or relations become known to the reader when this beat fires). This is the substrate the reader-knowledge model projects over (§3.4).

**Voice profiles**
- Per-character. A bundled object of: lexicon constraints (preferred/forbidden word lists), syntactic fingerprint (average sentence length, clause nesting, punctuation habits), rhetorical tics (catchphrases, hedge words, oaths), and a corpus of 20–100 exemplar utterances. The exemplar corpus is the style-RAG substrate for Surface C.

**Permission flags**
- Boolean attributes authors can set on any node. `immutable: true` (estate firewall — cannot be contradicted), `reader_can_direct: false` (reader cannot cause this entity to take actions — narrator declines in voice), `spoiler_until: beat_id`, `extrapolation_allowed: true|false|with_hedge`.

### 2.2 Three canon tiers (refined)

| Tier | What it is | Retrievable? | Presentable to reader? | Promotable? |
|---|---|---|---|---|
| **Hard** | Author wrote it explicitly. `"Eliza was born in 1847."` | Yes. | Yes, asserted. | N/A. |
| **Soft** | Author wrote it as possibility or approximation. `"Eliza was born around the turn of the Dust War — scholars dispute the exact year."` | Yes. | Yes, with the hedge preserved. Stripping the hedge is a faithfulness failure. | N/A. |
| **Extrapolatable** | Not authored, but the author marked the region (`extrapolation_allowed: true`) and the rule engine permits it. `"Eliza probably attended the Academy at the standard age for her caste."` | Yes, but only when the reader's query explicitly probes the region and the extrapolation budget allows it. | Yes, with a speculative register marker the narrator preserves. | **No.** This is the v2 change. Extrapolatable canon is *rendered*, never *promoted*. |

Under read-only, extrapolatable canon stays permanently labeled as extrapolation in every response. The renderer uses different grammatical registers: *"was"* for hard, *"is said to have been"* for soft, *"likely"* / *"by all accounts"* / *"in the way of her caste"* for extrapolatable. The hedge is structural, not stylistic. Faithfulness evaluation (§5.2) treats stripping the hedge as a CONTRADICTED verdict against the retrieved chunk's tier metadata.

Authors can, in their own next version release, review extrapolatable regions, read what the AI has been saying there (aggregate reader-facing logs), and promote selected extrapolations to hard canon. This is an authoring-tool feature, not a runtime feature. **No session activity mutates trunk canon, ever.**

### 2.3 Contradictions inside an author's bible

Every nontrivial bible contains contradictions. The ingest pipeline is responsible for detecting and resolving them before canon is served to readers.

**Ingest-time detector.** On bible upload, run three passes:

1. **Rule-engine contradiction scan** — every rule tested against every entity and relation. Example: rule `no_magic_in_Tessera_province` vs. entity `Eliza` with edge `cast_spell at Tessera.Waymarket during epoch_3` → flagged.
2. **NLI cross-entailment scan** — all pairs of authored assertions about the same entity run through a DeBERTa-MNLI classifier ([CLATTER framework, 2025](https://arxiv.org/html/2506.05243v1)). `contradicted` pairs flagged.
3. **Temporal validity scan** — edges with overlapping intervals on the same entity pair that express mutually exclusive states (e.g., `alive` and `deceased`).

**Resolution strategies** (author-facing workflow, never automatic):

- **Newest-wins** — default for non-material edits. Author can opt in.
- **Explicit** — author marks one of the conflicting assertions as canon, the other as draft/cut.
- **Arbitrated** — author resolves per-contradiction. **Default for material contradictions.**
- **Coexistence** — author marks both as canon with `tier: soft` and a disambiguation note. The renderer surfaces both when the reader probes the region.
- **Scoped** — contradictions can be resolved by scoping: `rule X` holds in region A, `rule not-X` holds in region B.

**The author-arbitration UI is the correct default.** Silent auto-resolution of material contradictions is a product failure. The detector should block publishing until every material contradiction has an author decision attached.

---

## 3. CANON RETRIEVAL ARCHITECTURE

### 3.1 Three retrieval surfaces plus a validator, composed

Current production-grade narrative RAG systems converge on hybrid retrieval as the baseline — vector alone is insufficient for multi-hop reasoning, graph alone has higher upfront indexing cost and worse performance on precise lookups ([Techment 2026](https://www.techment.com/blogs/rag-architectures-enterprise-use-cases-2026/); [Hybrid RAG, NetApp 2026](https://community.netapp.com/t5/Tech-ONTAP-Blogs/Hybrid-RAG-in-the-Real-World-Graphs-BM25-and-the-End-of-Black-Box-Retrieval/ba-p/464834); [Calmops hybrid 2026](https://calmops.com/ai/hybrid-search-rag-complete-guide-2026/)). Published benchmarks show hybrid approaches beating single-strategy by 10–30% across datasets; [GraphRAG-Bench, ICLR'26](https://arxiv.org/html/2506.05690v3) shows graph adds the most value on multi-hop, aggregation, and temporal queries (the dominant classes in narrative retrieval) while vector retains its edge on specific-document lookup (84% vs 35% in the Diffbot KG-LM benchmark, [FalkorDB 2025](https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/)).

The canon engine composes four surfaces:

**Surface A — Pinned hard canon.** A fixed prompt floor. Contains: the work's top-level premise, the current scene's stage-setting, the active characters' one-paragraph briefs, the current tone profile, and the content gates. Sized for 3–5% of the context budget. Always prompt-cached via standard prompt caching APIs — at a 10% cache-read cost and 5-minute TTL ([Anthropic caching 2026](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)), this surface is essentially free after the first turn of a session and is the retrieval-backstop that keeps the AI from losing the plot between turns.

**Surface B — Graph retrieval for precision.** LazyGraphRAG-style ([Microsoft 2025](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)) query-time graph traversal rather than full GraphRAG-style upfront community summarization. The choice is economic: LazyGraphRAG reports identical indexing cost to vector RAG and 700× lower query cost than full GraphRAG at comparable quality. For canon retrieval the query-time approach is correct because authored canon is small (even for a large world, tens of thousands of entities), traversals are shallow (most queries are 1–3 hops), and upfront indexing cost is wasteful when the graph changes on every author release. Graph queries answer: *which entities and relations are relevant to this user action at this scene location with these active characters?* Returns a subgraph of 5–30 nodes, serialized as compact relation tuples.

**Surface C — Vector retrieval for prose texture.** Embeds authored prose samples per character (voice exemplars) and per tone (scene exemplars). Retrieval keyed on the generation context's current tonal and voice needs. This is the surface that prevents voice collapse — the generator sees 2–5 in-voice exemplars per active speaker on every turn. Hybrid vector+BM25 because proper nouns and distinctive lexical tics matter and pure cosine similarity undersamples them.

**Surface D — Rule engine validator.** Not a retrieval surface in the embedding sense; a constraint evaluator. Before generation it injects active rules as natural-language constraints into the prompt. After generation it evaluates the draft against rule predicates for hard violations. This is the only surface with write-back in the canon loop — it returns a *verdict* that can trigger retry or edit.

### 3.2 Composition order

Per-turn flow:

1. Parse reader action → intent classification → entity linking against the registry (strict — unknown entities fail fast and are rewritten as anaphora or declined in voice).
2. Surface A pinned floor is already in the prompt cache.
3. Fire Surface B and Surface C in parallel — graph traversal on the linked entities, vector retrieval on tone+voice needs.
4. Compose a turn-specific context pack: pinned floor + graph subgraph (compact tuples) + prose exemplars (verbatim) + active rules (as constraints) + reader-knowledge projection (§3.4). Budget targets in §3.3.
5. Generate.
6. Surface D validates the generation against rules. Faithfulness check (NLI) against the retrieved canon. Entity-registry audit against the prose. Voice classifier per active speaker.
7. Pass or retry/edit according to §5.4.

### 3.3 Prompt budget realism in 2026

Current model realities as of 2026:

- Claude Sonnet 4.6: 1M context GA, standard pricing ($3 in / $15 out per M tokens), with output capped at the model's generation limit per reply ([Anthropic 2026](https://platform.claude.com/docs/en/about-claude/pricing)).
- Gemini 2.5 Pro: 1M context GA at $1.25 in / $10 out per M tokens; 2M expansion pending as of March 2026 ([Gemini 2026 pricing](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-pro)).
- Prompt caching: 10% read cost on Anthropic, 5-minute TTL default, 1-hour option at 2× write premium. Cache isolation moving to workspace-level from February 2026.

But: **lost-in-the-middle persists at scale**. Documented ~40% recall degradation for mid-context information even in state-of-the-art 1M-context models ([Introl 2025](https://introl.com/blog/long-context-llm-infrastructure-million-token-windows-guide)). Architectural consequence: **do not treat 1M context as a substitute for retrieval**. Per-turn target budget:

- Pinned floor (Surface A): 3,000–6,000 tokens, cached.
- Graph subgraph (Surface B): 500–2,000 tokens, not cached (query-specific).
- Prose exemplars (Surface C): 1,000–3,000 tokens, partially cached (per-character exemplar pools can be cached and indexed).
- Rules (Surface D inject): 500–1,500 tokens.
- Reader-knowledge projection: 500–2,000 tokens.
- Session history recency (last 5–10 turns verbatim): 2,000–6,000 tokens.
- Session history compressed (older turns, hierarchical summary in SCORE style, [arXiv 2503.23512](https://arxiv.org/html/2503.23512v1)): 1,000–4,000 tokens.

Total per turn: **~10K–25K tokens**. Deliberately far below the 1M ceiling. The model's attention is a scarce resource, not the context window. The architecture assumes 10–25K budget and never lets the composer exceed it. A session that exceeds it fails the scene-boundary rollup check (§3.4.4).

### 3.4 Narrative state awareness — the reader knowledge problem

**Under read-only this is the load-bearing concept.** There are two parallel states:

- **World-truth** — immutable within a pinned canon version. The full authored knowledge graph.
- **Reader-knowledge** — append-only, per-session, per-reader. A projection of world-truth filtered by what has been revealed to this specific reader in this specific session.

The narrator only asserts facts in the intersection of `(world-truth) ∩ (reader-known ∪ currently-being-revealed)`. This is the revelation invariant. Everything outside that set is either unknown-to-narrator (if the reader has not yet reached the prerequisite beat) or present-but-hedged (extrapolatable regions).

#### 3.4.1 Structure of reader-knowledge

Not a flat set. A directed acyclic graph of revelation events, each timestamped and linked to the prose turn that surfaced it. Each event has:

- `beat_id` — which plot beat fired
- `entities_revealed` — which entity attributes became known
- `relations_revealed` — which graph edges became known
- `hedged` — whether the revelation was presented as hard/soft/extrapolatable
- `turn_ref` — the exact session turn reference for audit

The DAG form matters because some reveals require other reveals as prerequisites. If the reader never learned that Eliza has a sister, the narrator cannot assert the sister's actions even if the underlying canon supports them.

#### 3.4.2 Update mechanics

Reader-knowledge is append-only. A turn can reveal new facts; nothing un-reveals. When the generator composes a response that crosses into previously-unrevealed world-truth, the composer marks those facts as *about-to-reveal* and the post-generation validator confirms the generation actually revealed them (not just implied them). After pass, the reveals commit to the reader-knowledge graph.

This is the only mutating state in the system. Implication: **storage is trivial per-reader, but fan-out is enormous** — a work with 100K concurrent readers has 100K independent knowledge graphs all projecting over the same fixed world-truth. The storage model is a sparse per-reader overlay keyed by the canon version hash. See §6 for the counterintuitive consequence.

#### 3.4.3 Projection at query time

The graph retrieval surface (B) operates against world-truth, but results are passed through a reader-knowledge filter before composition. Results split into three buckets:

- Already-known — composed freely.
- About-to-reveal — composed only when a plot beat authorizes the revelation and prerequisites are satisfied.
- Unknown-and-forbidden — redacted from context. The generator never sees them.

This redaction is critical. Even with a disciplined model, letting it see unrevealed canon risks premature reveal through subtle implication. The safest defense is to not retrieve it at all.

#### 3.4.4 Session consolidation

At scene boundaries, the full session history is compressed into a hierarchical summary (SCORE-style context-aware summarization). The summary preserves: reveals made, character state changes the reader has observed, and plot-beat progress. The raw turns are retained in durable storage for audit; only the summary flows into subsequent context packs.

### 3.5 Constrained decoding against the entity registry

For generation, a closed-vocabulary constraint applies at the token level for named entities. An anchor-constrained trie ([MDPI 2025](https://www.mdpi.com/2073-431X/15/3/178)) built over the registry ensures every proper-noun span in the output must resolve to a registered entity. The trie is scene-scoped — only entities retrieved into this turn's context are in the allowed set, further reducing the phantom-entity risk. Pronouns, generic nouns, and descriptive phrases are unconstrained; only proper nouns and reserved terms pass through the trie.

---

## 4. WORLD EXPANSION GOVERNANCE

### 4.1 Author-ships-an-expansion workflow

Because readers cannot grow canon, all canon growth is author-driven. The authoring pipeline:

1. **Ingest-to-branch.** The author uploads new bible content into a branch. The branch is isolated — readers on the live canon version never see it.
2. **Contradiction scan vs. trunk.** The ingest detector (§2.3) runs the full rule-engine, NLI, and temporal scans against the combined trunk+branch.
3. **Author-review UI.** Every contradiction, new entity, new rule, new relation is surfaced. The author resolves each — either by revising the branch, marking coexistence, or scoping.
4. **Merge to trunk.** On merge, the new canon version gets a signed hash and a version vector. Provenance is recorded per-triple using a W3C PROV-O-aligned schema ([TrustGraph 2025](https://trustgraph.ai/guides/key-concepts/ontologies-and-context-graphs/)): who authored, when, in which branch, under which review.
5. **Publish notification.** Readers on the previous version are notified that a new version exists, with an opt-in migration (§4.3).

### 4.2 Multi-author governance

Shared universes, collaborators, and estates need more than single-author permissions:

- **Role-based access** — Owner, Lead author, Contributor, Reader. Permissions granular per node type (who can edit Characters, who can edit Rules, who can mint Entities).
- **Immutability flags** — `immutable: true` on any node. Owners can lock core canon against downstream contributors (estate firewall). Tested on merge: a branch that touches an immutable node fails ingest.
- **Review requirements** — per-role merge policies. Contributors' branches require Lead approval; Leads can merge directly.
- **Audit log** — every merge is signed and immutable. Reversion is a new merge, not a rewrite.

Under v1 this was complex because readers were pseudo-writers who could grow extrapolatable canon. Under v2, **it simplifies**: there is exactly one class of writer (authored contributors), and the governance model is a standard git-style branching model with RBAC. No race conditions with runtime, no promotion from reader activity, no multi-writer CRDT.

### 4.3 World versioning for in-progress readers

A reader is always pinned to a specific canon version at session start. The pin is the version hash stored in the session's header. Mid-session, canon does not change under their feet.

At **scene boundaries**, if a newer version exists, the reader is offered an opt-in migration:

- **Stay** — session continues on the pinned version. The new version is not served to this session.
- **Migrate** — session rebases onto the new canon version. Reader-knowledge carries over cleanly because it's a projection over plot beats — the rebase re-projects the existing knowledge DAG onto the new world-truth. Any reveals that reference entities that were edited in the new version are re-validated; in the rare case of a conflict (a reveal referenced an entity the new version deleted), the reader is notified and offered a compatibility patch (the old reveal is preserved as "what the reader remembers" even if the world has since been retconned).

Migration is never silent and never mid-scene. Authors can flag a version as a **mandatory migration** (security, content-policy, or estate-firewall fix) — in that case the reader's session is quiesced at the next scene boundary with an explanatory notice.

### 4.4 Simplification vs. v1

Three pieces evaporate:

- **Session-graft reconciliation into author trunk.** Gone. There are no grafts.
- **Promotion gate logic.** Gone. There is no promotion from reader activity.
- **Multi-writer CRDT on world-truth.** Gone. Single-writer model with branches and merges, standard DVCS semantics.

What remains:
- Ingest-time contradiction detection (nontrivial, author-facing UX load).
- Multi-author RBAC.
- Version migration for in-progress readers (now a clean rebase rather than a multi-way merge).

---

## 5. CANON DRIFT DETECTION

### 5.1 Why drift detection still matters under read-only

Even though the AI cannot change canon, it can still:

- Retrieve correctly and generate incorrectly (LORE_CONTRADICTION).
- Retrieve correctly but assert an extrapolation as hard canon (EXTRAPOLATION_AS_FACT).
- Forget a session-known fact (CANON_AMNESIA within the session).
- Drop into generic-narrator voice (VOICE_COLLAPSE).
- Reveal ahead of the plot beat DAG (PREMATURE_REVEAL).
- Violate a content gate or tone profile (TONE_BREACH / CONTENT_POLICY_BREACH).
- Decline in a way that breaks the fourth wall (NARRATOR_FOURTH_WALL_BREACH).

Drift detection in v2 is narrower than v1 — no session-graft drift, no trunk-drift from reader activity — but it is still mandatory on every turn.

### 5.2 Detection ensemble

**Rule engine (synchronous per-turn).** Surface D evaluates every generated turn against active rules. Rule-level violations are hard fails — they trigger retry. Cheap: predicate evaluation over a few dozen rules, sub-100ms in practice.

**NLI entailment check.** Decompose the generated prose into atomic claims (GPT-class claim extractor, or a cheaper deterministic decomposer); run each claim through DeBERTa-MNLI entailment against the retrieved canon chunks that were supplied for this turn ([CLATTER 2025](https://arxiv.org/html/2506.05243v1); [Ragas faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)). Verdicts: `entailed`, `neutral`, `contradicted`. Faithfulness score is the proportion entailed. Production threshold in this domain: **≥ 0.90** (regulated-industry bar — appropriate here because a contradiction is a product defect). Neutral claims (claims unsupported but not contradicted) are allowed up to a per-work budget; a story with zero neutral claims is prose composed entirely of retrieved facts, which reads like a wiki, not a novel.

**Named-entity audit.** Strict registry whitelist. Every proper-noun span in the output is resolved against the registry. Unknown spans are hard fails. With the constrained-decoding trie (§3.5) this should already be structurally impossible, but the audit is a defense-in-depth second check.

**Voice classifier per character.** Fine-tuned DeBERTa-v3 "Fool Rate"–style classifier ([2025 ACL](https://aclanthology.org/2025.acl-long.879.pdf)) trained on the per-character exemplar corpus. Score per speaker-attributed span. Below the per-character floor → soft fail → the editor re-samples that span with stronger voice priming.

**Grounded confidence score.** Sampling-based. SelfCheckGPT-style ([Manakul et al. 2023](https://arxiv.org/abs/2303.08896)), with the 2025 caveat that SelfCheckGPT struggles with fact-conflicting hallucinations where samples are uniformly wrong. Mitigation: sampling diversity is induced by swapping retrieval seeds (slightly different retrieved contexts), not just decoding temperature. Disagreement across seeds flags low-confidence spans.

**Sampled second-pass auditor.** 5–10% of turns pass through a fresh auditor model (preferably a different model family to avoid correlated errors) with the retrieved canon and the generated prose. The auditor produces a structured judgment: faithfulness verdict, voice verdict, revelation-legality verdict. Expensive but high-signal, and critical for calibrating the lighter per-turn checks offline.

### 5.3 Edge: pronoun and anaphora risk

The constrained-decoding trie catches phantom named entities. It does not catch phantom referents through pronouns: *"her sister"* when the character has no sister in canon, *"the old treaty"* when no such treaty exists. Specific defense: the post-generation auditor expands pronouns and definite descriptions ("her sister," "the treaty") and re-checks each resolved referent against the entity registry and the relation graph. Expansions that don't resolve are flagged.

### 5.4 Canon audit trail

Every turn writes a structured log entry:

- Prompt pack composition (hashes of each retrieved chunk).
- Generated prose.
- Per-check verdicts (rule engine, faithfulness score, entity audit, voice scores, confidence, optional auditor).
- Retry history if any.
- Reader-knowledge delta (what was revealed).
- Canon version and version hash.

This log is the substrate for: debugging, author review of what-the-AI-said-in-extrapolatable-regions (authoring-tool input for promoting extrapolations to hard canon in the next version), drift detection at the work level (long-horizon reports), and compliance. Retention per author policy.

### 5.5 Recovery strategies, ranked by product acceptability

| Strategy | When | UX |
|---|---|---|
| **Silent retry with stronger grounding** | Faithfulness < 0.90, entity miss, rule violation | Reader sees slight latency bump (~1–3s). Retry re-prompts with explicit contradicting chunks called out, plus the violation reason as a system instruction. Under read-only this is cleaner than v1 because the retrieval target is a fixed authored canon, not a contested session graft — the retry converges faster. |
| **In-voice hedge** | Soft canon regions, extrapolatable regions, moderate confidence drops | Narrator frames the assertion with the tier-appropriate register (soft → *"is said to have been"*, extrapolatable → *"by all accounts"*). No reader-visible fault. |
| **In-voice deflect** | FORBIDDEN_ACTION, premature-reveal attempts | Narrator declines *in character* — "the scribe demurs," "that page has not yet turned." Preserves fourth wall. |
| **Scene-boundary reset** | Accumulated voice drift, failed retries exhausted | At next natural scene break, the hierarchical summarizer compresses and the pinned floor is re-seeded. Reader-visible as a pacing beat, not a failure. |
| **Out-of-voice explanation** | Safety / content policy hard stop only | Last resort. Explicit "this content is unavailable in this work." |

The silent-retry cost is low under v2 because author canon is fixed, retrieved chunks are deterministic for the same query, and the retry pressure just sharpens the constraint injection. Under v1 the silent retry risked grinding against a contested session graft that might itself be malformed.

---

## 6. [CURIOUS] ARCHITECTURAL OBSERVATIONS

**[CURIOUS] The world engine is now a read replica of a book.** Under v2, world-truth has one writer (authoring tool, offline) and many readers (runtime). This is not a distributed-systems problem. It is a CDN problem. The world graph can be snapshotted at publish time into a dense, fully-indexed, geo-replicated artifact and served from edge caches. Canon reads are the cheapest class of read on the internet. Everything interesting in the runtime is the reader-knowledge overlay — which is per-reader, sparse, append-only, and can be stored in a log-structured merge tree per-session with trivial scale-out. **The system's hardest scale problem is not the world; it is the per-reader overlay.**

**[CURIOUS] Prompt caching just became structural, not an optimization.** Pinned floor + per-character exemplar pools + active rules are all deterministic within a pinned canon version. They cache permanently within the version hash, across readers, at 10% read cost. A reader's cost for a turn, after the first turn in their session, is approximately (graph subgraph tokens + reader-knowledge projection + generation tokens). The work's canon depth — which in v1 looked like a scalability risk (more canon = more retrieval cost) — is now largely free at steady state. **Deep authored worlds are cheaper to operate per-turn than shallow ones** because the cache layers are wider and more reusable.

**[CURIOUS] The moat is not the canon — it is the authored voice substrate.** Surface C (prose exemplars per character, per tone) is the surface that makes this product differentiated from a generic LLM-plus-wiki. The graph and the rules are the kind of artifact a sufficiently motivated team could scrape from a well-maintained fandom wiki. The per-character exemplar corpus — the voice that makes Eliza sound like Eliza — is uniquely authored and uniquely valuable. Under read-only the voice substrate is the load-bearing moat component, not the canon graph.

**[CURIOUS] Extrapolation budget is a knob that controls the product's personality.** Authors can set `extrapolation_allowed` narrowly (the narrator is tight-lipped and says *"I cannot speak to that"* frequently) or broadly (the narrator improvises within taste). This is a creative choice, not a safety choice. A thriller author may want tight; a cozy-fantasy author may want broad. The architecture exposes the knob; the moat is the author's taste in setting it.

**[CURIOUS] Reader-knowledge as append-only DAG buys audit for free.** Because reader-knowledge is append-only, it is trivially an audit log. Every session has a full, replayable history of what was revealed, when, and on the basis of what retrieved canon. Author tooling can mine this corpus for: which plot beats fire most often, where readers push against permission flags, what extrapolatable regions get queried into the most (candidates for promotion to hard canon in the next version). **The product becomes its own authoring-signal pipeline.**

**[CURIOUS] Voice drift is now detectable at the session level, not just the turn level.** Because reader-knowledge records every speaker-attributed span with its voice score, a monotonic decline across a session is a measurable signal. This was obscured in v1 by the noise of session-graft interactions. Under read-only, the per-session voice trajectory is a clean product metric and can be used for: adaptive re-seeding of voice exemplars in the pinned floor, model A/B testing, and SLA reporting to authors ("your work maintains Eliza's voice at 0.93 Fool Rate median across the 95th-percentile session").

**[CURIOUS] The rule engine is an authoring accelerant, not a runtime cost.** Under v1 the rule engine had to referee contested grafts at runtime. Under v2 its runtime role shrinks to a read-only predicate evaluator. But its *ingest-time* role grows: the rule engine is how authors find their own contradictions before publishing. The architecture makes rule-writing a core part of authoring — write a rule, ingest the bible, read the violations, decide. This reframes the product: it is also a *canon-debugging* tool for authors, not just a reader-facing narrator.

**[CURIOUS] The "read-only world" constraint is a trust constraint, not a technical one.** Nothing in the architecture technically prevents a future feature from promoting reader-surfaced extrapolations to trunk. The constraint is enforced by policy and workflow (author-review UI, signed merges, explicit opt-in at version release). This means the architecture can honor the v2 constraint today and *optionally* relax it in v3 for works whose authors explicitly opt in — without re-architecting. The read-only stance is a product stance supported by, not coupled to, the engine.

---

## TL;DR

- The world is a typed, signed, author-written knowledge graph, served as a read replica. Runtime never writes canon. Prompt-cache the pinned floor and exemplar pools across readers — canon reads are structurally cheap.
- Retrieval is hybrid: pinned floor (Surface A) + LazyGraphRAG-style graph traversal (Surface B) + vector/BM25 prose exemplars for voice (Surface C) + rule-engine validator (Surface D). Per-turn budget 10–25K tokens, never the full context window, because lost-in-the-middle is still real at 1M.
- Reader-knowledge is the only mutating runtime state — append-only DAG of revelation events, per-reader, projected over a pinned canon version. The narrator only asserts facts in `(world-truth) ∩ (reader-known ∪ currently-being-revealed)`; unknown canon is redacted from context, not just from prompt.
- Drift detection remains mandatory per-turn: rule engine + NLI faithfulness (≥ 0.90 threshold) + entity-registry audit (belt-and-braces against a constrained-decoding trie) + per-character voice classifier + 5–10% sampled second-pass auditor. Recovery is silent retry first, in-voice hedge/deflect second, out-of-voice only as last resort.
- The three canon tiers (hard / soft / extrapolatable) render with distinct grammatical registers. Extrapolation is surfaced with a structural hedge; stripping the hedge is a faithfulness failure. No session activity promotes canon — promotion is author-only, offline.

---

## DELTA vs V1

**What simplifies.** Promotion gate logic, session-graft reconciliation, multi-writer CRDT on world-truth, graft-to-canon promotion races, and session-graft leakage all evaporate. The distributed-systems layer of v1 collapses to a single-writer DVCS model with branches, reviews, and signed merges. Runtime canon is a read replica; the complexity moves entirely to the authoring pipeline, where it belongs.

**What moat evaporates.** The v1 session-grown-canon moat. The pitch of "readers make the world deeper by using it" is gone. Competitors cannot be locked out by a canon that silently accretes value from reader activity, because there is no such accretion.

**What new moat emerges.** The moat is now **authored depth × retrieval quality × voice fidelity**:

- *Authored depth* — how many entities, relations, rules, plot beats, tone markers, and voice exemplars the author has invested in. This is a content moat, not a systems moat, and it compounds only with author effort. The platform's job is to make that effort cheap and enjoyable (the authoring tool is a first-class product surface).
- *Retrieval quality* — hybrid LazyGraphRAG + vector exemplars + rule engine is reproducible at the engineering level, but the engineering bar to get it all working together at production faithfulness (≥ 0.90 NLI-entailed) and low latency (under 3s p95) is real and non-trivial. This is a systems moat.
- *Voice fidelity* — per-character exemplar corpora plus fine-tuned voice classifiers plus adaptive prompt composition to maintain voice across long sessions. This is the hardest quality bar in the product, the one current interactive-fiction platforms fail most visibly (73% user frustration on character consistency), and the one where incumbent advantage compounds with both author investment and per-work model tuning. This is the dominant moat component.

**What the new hardest-problem is.** Not canon enforcement — that simplified to a well-characterized grounded-RAG problem. The new hardest problem is **voice fidelity across long sessions on a fixed canon substrate at a 10–25K-token per-turn budget**. Voice drift compounds over turns, is under-served by current retrieval architectures (vector-over-prose-exemplars is necessary but not sufficient), and is the failure mode that most directly damages the reader's sense of a coherent authored voice — which is the entire product promise. The v2 architecture centers on giving voice its own dedicated retrieval surface, its own dedicated classifier, and its own dedicated recovery path, because that is where the v2 product lives or dies.

---

**Sources**
- [RAG vs. GraphRAG: A Systematic Evaluation, arXiv:2502.11371](https://arxiv.org/abs/2502.11371)
- [When to use Graphs in RAG (GraphRAG-Bench, ICLR'26)](https://arxiv.org/html/2506.05690v3)
- [LazyGraphRAG — Microsoft Research, 2025](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)
- [Lost in the Middle, Liu et al., arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- [Long-Context LLM Infrastructure, Introl 2025](https://introl.com/blog/long-context-llm-infrastructure-million-token-windows-guide)
- [Ragas faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/)
- [DeepEval faithfulness](https://deepeval.com/docs/metrics-faithfulness)
- [RAG Evaluation Metrics Frameworks 2026, Prem AI](https://blog.premai.io/rag-evaluation-metrics-frameworks-testing-2026/)
- [SCORE: Story Coherence and Retrieval Enhancement, arXiv:2503.23512](https://arxiv.org/html/2503.23512v1)
- [CLATTER: Comprehensive Entailment Reasoning for Hallucination Detection, arXiv:2506.05243](https://arxiv.org/html/2506.05243v1)
- [SelfCheckGPT, Manakul et al., arXiv:2303.08896](https://arxiv.org/abs/2303.08896)
- [Anchor-Constrained Extraction, MDPI 2025](https://www.mdpi.com/2073-431X/15/3/178)
- [OpenCharacter: Role-Playing LLMs, arXiv:2501.15427](https://arxiv.org/html/2501.15427v1)
- [Persona-Based Dialogue / Fool Rate classifier, ACL 2025](https://aclanthology.org/2025.acl-long.879.pdf)
- [Hybrid RAG Architecture, Techment 2026](https://www.techment.com/blogs/rag-architectures-enterprise-use-cases-2026/)
- [Hybrid Search RAG Guide 2026, Calmops](https://calmops.com/ai/hybrid-search-rag-complete-guide-2026/)
- [GraphRAG vs Vector RAG Accuracy Benchmark, FalkorDB 2025](https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/)
- [Anthropic Prompt Caching Docs 2026](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic Pricing 2026](https://platform.claude.com/docs/en/about-claude/pricing)
- [Gemini 2.5 Pro Pricing 2026](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-pro)
- [AI Dungeon vs NovelAI character consistency analysis, 2026](https://www.alibaba.com/product-insights/ai-dungeon-vs-novelai-for-interactive-storytelling-which-maintains-consistent-character-voice-over-long-sessions.html)
- [TrustGraph Ontologies and Context Graphs, 2025](https://trustgraph.ai/guides/key-concepts/ontologies-and-context-graphs/)
