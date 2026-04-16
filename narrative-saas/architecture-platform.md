# PLATFORM & AI DELIVERY ARCHITECTURE

*Architect_1 — Platform & AI Delivery Layer. v2 refinement: world is read-only, queryable-but-immutable. No session grafts. No record_session_graft interface. No graft promotion service. No author-graft-review workflow inside the AI delivery path.*

---

## 1. PLATFORM ARCHITECTURE (refined)

### 1.1 What Survives, What Deletes

The read-only refinement removes an entire class of machinery. The deletions are larger than they look on paper — they reduce not only code but the hardest operational problems in the v1 design.

**Deletes under read-only:**

- **Graft Promotion Service** — gone. There is nothing to promote.
- **Author Graft Review Workflow** — gone. Authors never see a queue of reader-generated canon extensions because none are generated.
- **Graft-to-canon diffing / merge tooling** — gone.
- **Session-graft lifecycle states** (draft / pending-author / promoted / rejected / abandoned) — gone. The most complex state machine in v1 is removed.
- **Graft-aware canon retrieval** (querying canon-plus-my-session's-accepted-grafts, which was the hardest correctness problem in v1) — gone. Retrieval now hits a single immutable bundle.
- **Cross-session contamination protection** for graft leakage — gone. Two readers in the same world cannot see each other's grafts because there are no grafts.
- **Versioned graft conflict resolution** when an author releases world v2 and a reader has pending v1 grafts — gone.

**Survives:**

- World Bundle registry (immutable artifacts)
- Canon Retrieval Service (now strictly read-only)
- Session State Service (now a pure projection, never a mutator)
- Reading Surface (companion panes, typography, input)
- Author Studio (upload, validate, publish — unchanged)
- Versioning & reader-opt-in migration (pin-to-v1, migrate at scene boundary)
- LLM Gateway (routing, caching, escalation)
- Arbiter (canon-bound refusal logic)
- Billing, auth, sync, telemetry

[CURIOUS] The v1 design had roughly 40% of its service surface dedicated to graft handling. v2 deletes that 40% cleanly. The simplification is not cosmetic; it is the biggest architectural win in the refinement.

### 1.2 Service Topology (v2)

```
┌──────────────────────────────────────────────────────────────────────┐
│                         READER EDGE CLIENT                           │
│  (React/React Native/Swift — text surface + companion panes)         │
└──────────────────┬───────────────────────────────────┬───────────────┘
                   │ session turns                      │ bundle sync
                   ▼                                    ▼
┌──────────────────────────────────┐    ┌───────────────────────────────┐
│    AI DELIVERY GATEWAY           │    │   BUNDLE DISTRIBUTION CDN     │
│  - prompt assembly               │    │  - signed World Bundles       │
│  - retrieval orchestration       │    │  - version pinning            │
│  - cache management              │    │  - static assets              │
│  - escalation router             │    │    (SVG maps, char cards)     │
└──────┬──────────┬────────────────┘    └───────────────────────────────┘
       │          │
       │          ▼
       │   ┌──────────────────────────────┐
       │   │  CANON RETRIEVAL SERVICE     │
       │   │  - vector + keyword + graph  │
       │   │  - READ-ONLY                 │
       │   │  - no mutation path exists   │
       │   └──────────────┬───────────────┘
       │                  │
       ▼                  ▼
┌────────────────┐   ┌────────────────────┐
│ LLM PROVIDERS  │   │  WORLD BUNDLE      │
│ (multi-vendor) │   │  STORE             │
│ - Claude Haiku │   │  (immutable        │
│ - Claude Sonnet│   │   content-addressed│
│ - DeepSeek V3.2│   │   artifacts)       │
│ - Gemini Flash │   │                    │
│ - edge-local   │   └────────────────────┘
└────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                       SESSION STATE SERVICE                          │
│  - event-sourced discovery log (per reader × world × session)        │
│  - projections: journal, glossary-learned, scenes-entered,           │
│    characters-met, relationships-encountered                         │
│  - NEVER writes to canon, NEVER writes to bundle                     │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                         AUTHOR STUDIO                                │
│  (bundle upload, validate, publish, version → produces immutable    │
│   artifacts; no path from reader activity to this studio)            │
└──────────────────────────────────────────────────────────────────────┘
```

The diagram is worth studying because the **read-only arrow direction is architecturally enforced**: Session State never calls into Bundle Store or Author Studio. The compiler / container boundary (separate service, separate DB, no shared write credential) makes it impossible to violate canon.

### 1.3 World Bundle — the Immutable Manifest

A World Bundle is a content-addressed artifact: manifest JSON + canon docs + embeddings + static assets, hashed, signed by the author's key, served immutable.

```
WorldBundle v2 manifest
├── bundle_id         (content hash — world_<hash>)
├── author_id
├── version           (semver; v1.3.2, v2.0.0)
├── published_at
├── canon/
│   ├── world_rules.md        (rules, physics, magic, tech)
│   ├── characters/           (one file per character)
│   ├── locations/
│   ├── timeline.md
│   ├── factions.md
│   └── lore_glossary.md
├── tone_guide.md             (author's voice anchors)
├── scene_graph.json          (discoverable scenes, gating conditions)
├── assets/                   (SVG maps, static cards)
├── embeddings/               (pre-computed — author-side cost, not reader-side)
└── signature
```

Under read-only the bundle is truly immutable post-publish. The **only** modification path is the author publishing a new version. No in-session mutation. No delta. No patch. This is the simplification that makes everything downstream cheap.

ARCHITECT_2 owns the internal structure of canon docs and the scene-graph gating logic. My interface contract to them: **the bundle is a read-oracle; give me a `query_canon` endpoint and a `validate_response` endpoint; I do not need anything else.**

### 1.4 Concurrency Isolation — Trivially Easy Now

Multi-user concurrent access to the same world is **embarrassingly simple** in v2 because there is no shared mutable state. The canon is read-only; two readers in the same world are both hitting the same immutable bundle. Session state is per-reader-per-world-per-session — fully isolated by session_id.

The classic concurrency headaches (serializable isolation on graft writes, two readers discovering the same region of canon simultaneously and both trying to add a graft, etc.) do not exist. A thousand readers can be in the same world at once; the canon retrieval layer is pure read, cacheable, horizontally scalable.

[CURIOUS] v1's concurrency design needed pessimistic locking on graft insertion paths and optimistic reconciliation on graft-aware reads. v2 collapses this to stateless read caching with per-reader session isolation. This is the kind of simplification where the *absence* of complexity is the architectural point.

### 1.5 Session State — a Projection, Never a Mutation Layer

This is the most important conceptual shift in v2.

Session state is **entirely a record of what the reader has uncovered from an unchanging world**. It is not a record of how the world changed; the world does not change. Event-sourced discovery log, with derived views:

```
DiscoveryLog (append-only per session)
├── turn_001: reader_entered_scene(scene_id="mercer_lane")
├── turn_001: character_revealed(char_id="elias_thorne")
├── turn_002: reader_queried(topic="the_compact")
├── turn_002: glossary_entry_unlocked(term="the_compact")
├── turn_003: relationship_observed(char_id="elias_thorne", toward="mercer")
└── ...

Projections (materialized on demand, cacheable, deterministic):
  - Journal (summarized narrative of reader's path)
  - Characters Met (with what the reader knows about each)
  - Glossary Learned (only terms reader has encountered)
  - Scene Map (fog-of-war — revealed regions only)
  - Relationships Observed (per reader's knowledge, not ground-truth)
```

Every projection is derived from the discovery log; the log is derived from canon-grounded turns. No projection mutates canon. No projection mutates any other projection. No session writes to any other session.

The reader's experience of the world is a **lens**, not an edit. This is the core simplification.

---

## 2. AI DELIVERY LAYER (refined)

### 2.1 What the LLM Is Doing (and Not Doing) Per Turn

In v1, the LLM had three roles: narrator, character actor, game-master-with-stakes. The "game master" role is the one that forced the generative-canon-extension pathway. Under v2, **the game-master role largely evaporates**.

The LLM per turn is doing one of these:

| Role | Description | Still alive in v2? |
|------|-------------|--------------------|
| **Narrator** | Describe the scene, pacing, observation, atmosphere using only canon material | Yes — primary |
| **Character Actor** | Voice an NPC in-character, constrained by their canon-defined knowledge and personality | Yes — primary |
| **Oracle / Surface-Canon** | Answer a reader's question or reveal information the reader earned | Yes — core loop |
| **Arbiter** | Refuse or redirect an action that violates world rules, in-character and gracefully | Yes — critical |
| **Game-Master-with-Stakes** | Resolve reader actions that have consequences on the world | **Mostly gone** |
| **Canon Generator** | Invent new world material when reader goes off-map | **Deleted** |

The "mostly gone" on game-master-with-stakes deserves a note: there is still *local* stakes resolution — did the reader successfully persuade a merchant? Did they hear the footsteps? — but these resolve against canon-defined character disposition and world rules, not against an evolving world. The *result* is narrated; the *world* is unchanged.

This means the per-turn work is dominated by **retrieval + narration**, not by generation of new world content. That is a smaller, more bounded task, and the cost model reflects that.

### 2.2 Layered Prompt Architecture

Every turn assembles a layered prompt. Each layer is versioned independently. The version of each layer is logged with the turn for audit and reproducibility.

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 0 — PLATFORM BEHAVIOR                                 │
│ (safety, format, narrator etiquette, refusal posture,       │
│  session-isolation promises, out-of-world handling)         │
│ Version: platform_v3.1.2                                    │
│ CACHE: long-TTL, universal prefix — shared across all       │
│  readers and all worlds. Prompt-cache hit rate ~99%         │
├─────────────────────────────────────────────────────────────┤
│ LAYER 1 — AUTHOR CANON RETRIEVAL                            │
│ (scene-scoped canon slice: relevant characters, locations,  │
│  rules retrieved via vector + keyword + scene-graph)        │
│ Version: bundle_<hash>/scene_<id>                           │
│ CACHE: per-scene, per-bundle — very high reuse across       │
│  readers in the same scene                                  │
├─────────────────────────────────────────────────────────────┤
│ LAYER 2 — AUTHOR TONE GUIDE                                 │
│ (author voice anchors, rhythm, style, forbidden phrases)    │
│ Version: bundle_<hash>/tone                                 │
│ CACHE: per-bundle — high reuse across all readers of this   │
│  world                                                      │
├─────────────────────────────────────────────────────────────┤
│ LAYER 3 — SESSION KNOWLEDGE PROJECTION                      │
│ (what THIS reader has uncovered: journal summary,           │
│  characters met, glossary learned, current scene position)  │
│ Version: session_<id>/turn_<n>                              │
│ CACHE: per-session, short-TTL — changes each turn but       │
│  slowly                                                     │
├─────────────────────────────────────────────────────────────┤
│ LAYER 4 — READER TURN                                       │
│ (the raw user input for this turn)                          │
│ Version: user input, uncached                               │
└─────────────────────────────────────────────────────────────┘
```

The layer ordering is deliberate and aligns with prompt caching economics. Claude prompt-cache reads cost 10% of base input [1]. Gemini cached reads cost 75% of base input [2]. OpenAI cache hits cost 50% of base input [3]. **The layering puts stable content at the top so most of the prompt is a cache hit on every turn.** Only layers 3 and 4 miss cache routinely, and layer 3 is small (a knowledge projection, not raw canon).

Under v2 this caching is *more* effective than v1 because canon never mutates — a scene's retrieved canon at turn 1 is identical to turn 100. In v1, graft-aware retrieval broke cache more often.

### 2.3 Interface Contract to ARCHITECT_2 (Canon Enforcement)

Under read-only, the contract is far smaller. ARCHITECT_2 owns the internal data shape and retrieval semantics. The contract my AI delivery layer consumes:

**`query_canon(bundle_id, session_context, scene_id, query_text, k) → RetrievalSlice`**
- Returns ranked canon excerpts (docs, character sheets, location cards, rules) relevant to the query
- Caller passes session_context so the retrieval layer knows what the reader has already observed (for scope) but the retrieval is read-only
- Deterministic: same inputs → same slice. Required for cacheability.

**`validate_response(bundle_id, scene_id, proposed_narration) → ValidationVerdict`**
- ARCHITECT_2's canon-consistency check on the LLM's output before the reader sees it
- Returns `APPROVED` | `CONTRADICTS_CANON(which, where)` | `UNGROUNDED(claim_without_source)`
- On non-APPROVED, my gateway re-prompts or surfaces the arbiter refusal

**`record_session_graft(...)` → DELETED**. This interface does not exist in v2. No path from reader turn to bundle mutation.

**`promote_graft(...)` → DELETED.**

**`author_graft_queue(...)` → DELETED.**

The simplification of the contract alone buys us faster prototyping, smaller agreement surface, and lower coupling between my layer and ARCHITECT_2's.

### 2.4 Handling Unanticipated Reader Actions (Decision Framework)

The hardest design question in v2. When a reader does something the author didn't anticipate, under v1 the AI could extend canon gracefully. Under v2, it cannot. The AI must respond within canon bounds. Ranked decision framework, applied in order:

**Rank 1 — Surface Relevant Canon**
If the retrieval layer finds canon material that addresses the action, narrate using it. Most "unanticipated" reader turns are actually canon-adjacent and are covered by material the author already wrote but the reader hasn't reached.
*Example: reader asks a character about a topic the author covered in a lore doc the reader hasn't unlocked. AI narrates the character's answer drawing on that doc, and the session log records a glossary/knowledge unlock.*

**Rank 2 — Narrate Observation Within Authored Material**
If no direct canon addresses the action but the action is a benign observation (looking around, picking up a described object, asking a general question), narrate using only already-authored material. Never invent new facts. If the reader looks at a wall the author didn't describe, the narration describes what *is* described — perhaps the room's lighting, the ambient sound — without fabricating wall details.

**Rank 3 — Arbiter In-Character Refusal**
If the action violates world rules (breaks magic constraints, defies established physics, contradicts a character's known personality), the Arbiter surfaces an in-character refusal. *"The talisman resists your touch; nothing the Compact has bound can be undone so casually."* This is always canon-grounded — the refusal references the specific rule.

**Rank 4 — Explicit "The Text Does Not Record This" Response**
When nothing in canon touches the question and invention would be required, the AI says so — gently, in the author's narrator voice. *"The chronicles do not say what Mercer ate for breakfast on that morning. Some things remain the author's silence."* This is a key v2 design decision: **we prefer honest silence over hallucinated canon**. A reader who wants to play in a fully plastic world is playing AI Dungeon, not this.

The decision is made by the Arbiter Layer evaluating the retrieval slice + the reader's turn + the scene context. If retrieval returns strong matches → Rank 1. Weak matches but action benign → Rank 2. Rule-violation detected → Rank 3. Empty retrieval + invention required → Rank 4.

**Tuning knob:** authors choose how strict the Rank 4 threshold is. Some authors want tight silence. Others allow Rank 2 to stretch further. Both are configurations of the same immutable-world architecture — there is no author path that re-enables generative canon extension.

### 2.5 Which Model for Which Turn

Model routing is driven by turn complexity. Current 2026 pricing makes this a clean three-tier decision:

| Turn type | Model | Rationale | Cost signal |
|---|---|---|---|
| Glossary lookup, scene transition narration, simple oracle answer | **Claude Haiku 4.5** ($1/$5 per M) [4] OR **DeepSeek V3.2** ($0.28/$0.42 per M) [5] | Bounded retrieval + short narration; small model sufficient | Floor |
| Character dialog, atmosphere narration, multi-turn persona continuity | **Claude Sonnet 4.5/4.6** ($3/$15 per M) [1] OR **Gemini 2.5 Flash** ($0.30/$2.50 per M) [6] | Needs voice coherence and longer-form narration | Mid |
| Multi-character scenes, complex canon synthesis, arbitrated refusals with long justification, world-rule resolution | **Claude Sonnet 4.5** with 1M context [1] OR **Gemini 2.5 Pro** ($1.25/$10 per M under 200K) [7] | Needs reasoning + retrieval quality (Claude 78% vs Gemini 25% retrieval accuracy at 1M [8]) | Oracle |

The per-turn routing decision is itself deterministic code (not LLM judgment) — classifier on the reader turn + retrieval complexity + scene metadata.

---

## 3. SURFACE AREA — TEXT FIRST, ALWAYS

### 3.1 Reading Surface Specification

Text-only by constraint, text-beautiful by intent. The read-only refinement makes this *more* important, not less — discovery is the core loop, so the companion panes that reflect discovery carry a higher percentage of reader attention.

```
┌──────────────────────────────────────────────────────────────┐
│  [≡]  Whisperwood  /  Chapter: The Compact          [⚙] [?] │
├───────────────────────────────────────┬──────────────────────┤
│                                       │  JOURNAL             │
│  The lane narrowed. Mercer's sign    │  • Met Elias Thorne  │
│  hung loose on one iron hook, the    │  • Learned of the    │
│  paint blistered. You had seen the   │    Compact           │
│  same blistering on the boats down   │  • Heard rumor of    │
│  at the quay. The same hand had      │    the blistering    │
│  been at work, then — or the same    │                      │
│  weather.                             ├──────────────────────┤
│                                       │  WHO                 │
│  Elias stepped from the doorway. He   │  Elias Thorne        │
│  did not smile.                       │  — mercer, cautious  │
│                                       │  — knows of Compact  │
│  > what do you want to do             │                      │
│                                       ├──────────────────────┤
│                                       │  GLOSSARY            │
│                                       │  the Compact         │
│                                       │  mercer's lane       │
│                                       │  (3 entries)         │
│                                       ├──────────────────────┤
│                                       │  MAP  (SVG, static)  │
│                                       │                      │
└───────────────────────────────────────┴──────────────────────┘
```

**Typography:** serif body (~19–21px on desktop, fluid on mobile), generous line-height, narrow measure (~65 char), typographic quote/dash handling, fade-in of newly revealed prose. The reading surface is deliberately paced; prose animates in at a slower rhythm than the LLM emits.

**Pagination vs scroll:** scrolling with scene breaks marking chapter-like transitions. Scene transitions are persistent anchors — readers can return.

**Input affordance:** a single text field at the bottom. Free-form. The reader can also invoke quick-actions from companion panes (ask Elias about the Compact → populates input).

**Companion panes:** journal, characters, glossary, scene map, relationships. Each pane is a projection of session state. Each entry is marked with how the reader learned it (which scene, which turn). Discovery is not just the narrative experience; it's visible accretion in the panes.

### 3.2 Text-Native Features Reassessed Under Read-Only

| Feature | Leverage under v2 |
|---|---|
| Companion panes as discovery mirror | **Higher** — discovery is the core loop; panes are the primary feedback loop |
| Fog-of-war scene map | **Higher** — reader-visible uncovering of a fixed territory is satisfying in a way that emergent territory isn't |
| Journal-as-recap | **Higher** — deterministic to regenerate because canon is stable |
| Glossary-on-encounter | **Higher** — predictable, author-curated definitions |
| Relationship web | **Stable** — shows what the reader has observed, not what is true |
| Scene re-entry / bookmarking | **New leverage** — readers returning to prior scenes is coherent in v2 because those scenes are still on canon |
| Multiple playthrough branches | **New leverage** — a reader can start a second session in the same world and discover it differently; fully isolated |
| Author's director commentary | **Possible** — author-authored meta-annotations shown optionally, like a DVD commentary track |

### 3.3 Author-Provided Static Assets

Still permitted, still author-authored. SVG maps, character portraits (hand-drawn or author-licensed), cover art. **No AI image generation on the reader side and no AI image generation in the author pipeline.** Authors upload what they have; the platform renders it.

This preserves authorial craft and avoids the uncanny-valley drift of mid-session image generation. [CURIOUS] There is a commercial temptation to add AI illustration; resisting it is a strategic, not just an aesthetic, decision — it keeps the product in a category where canon integrity is the product.

### 3.4 Forbidden

- AI image generation
- AI voice synthesis / TTS of LLM output
- AI video
- Avatars, animated characters
- Chat-app gamification: notifications, streaks, daily-read quests, friend leaderboards, engagement loops. This is a reading product. Reading products that gamify engagement cease to be reading products.

---

## 4. SCALE — EDGE / CLOUD SPLIT (cost critical, live pricing)

### 4.1 Current 2026 Price Surface (Verified Live)

| Model | Input $/M | Output $/M | Cache read $/M | Notes | Source |
|---|---|---|---|---|---|
| Claude Sonnet 4.5 | $3.00 | $15.00 | $0.30 | 1M context; 78% retrieval accuracy at 1M | [1] |
| Claude Haiku 4.5 | $1.00 | $5.00 | $0.10 | 200K context, 4–5× faster than Sonnet | [4] |
| GPT-4.1 | $2.00 | $8.00 | ~$1.00 | 128K context | [3] |
| GPT-4o-mini | $0.15 | $0.60 | $0.075 | 128K context | [9] |
| Gemini 2.5 Pro | $1.25 | $10.00 | $0.9375 | 1M context; retrieval weaker than Claude at depth | [7] |
| Gemini 2.5 Flash | $0.30 | $2.50 | ~$0.075 | Fast, cheap | [6] |
| Gemini 2.5 Flash Lite | $0.10 | $0.40 | — | Cheapest first-party | [6] |
| DeepSeek V3.2 | $0.28 | $0.42 | $0.028 | 90% cache discount | [5] |
| Groq Llama 3.1 8B | $0.05 | ~$0.08 | — | Speed-optimized, open-weight | [10] |
| Fireworks Llama 70B batch | ~$0.45 blended | — | — | Large-batch economics | [10] |

Open-weight models on-device (2026):
- Gemma 4 E2B: 2.3B effective, 5GB RAM, 4-bit Q, 128K ctx [11]
- Phi-4-mini: 3.8B, strong instruction following [11]
- Qwen 3.5 2B/4B: 262K native context [11]
- iPhone 15 Pro / 16 Pro: 20–30 tok/s on 3B-class models via MLX [12][13]
- Snapdragon 8 Elite Hexagon NPU: 5–11k tok/s prefill, 100+ tok/s decode on mobile-tuned stacks [14]
- ExecuTorch (Meta) GA Oct 2025 — production mobile runtime [15]

### 4.2 Session Definition Reassessed

Under v2 a "session" is more oracle-like than game-like. Turns are shorter — more "what do I see? who is this? what does she know?" and less "I attempt to overthrow the baron by raising an army, resolve turn after turn with rolls and consequences." Revised session profile:

| Metric | v1 estimate | v2 estimate | Rationale |
|---|---|---|---|
| Avg turns per session | 40 | 30 | More oracle-like; satisfying discovery in fewer turns |
| Avg input per turn (tokens) | 80 | 60 | Reader prompts are shorter; less narrative authorship |
| Avg output per turn (tokens) | 400 | 280 | Narration is tighter; less generative filler |
| Retrieval tokens per turn (cached, via layer 1) | 1800 | 1800 | Roughly unchanged — canon slice still needed |
| Cache hit rate (prompt prefix) | ~70% | ~88% | Higher, because canon is immutable |

### 4.3 Escalation Rate Reassessed

v1 assumed 15–25% of turns escalate from edge/cheap model to cloud/premium (Sonnet/Pro) because generative canon extension is hard. Under v2 this is materially lower. Most turns are retrieval + narration within tight canon bounds — a bounded task that small models handle competently. Estimated v2 escalation rate: **6–10%**. Triggers:

- Multi-character scene with >3 NPCs
- Long-context synthesis (reader asks something requiring multiple canon slices)
- Arbiter refusal with long in-character justification
- First-encounter character reveal (needs the premium voice establishment)

Under v2 the bulk of turns look like *oracle calls*: short input, canon-grounded narration, stable tone. These fit comfortably in Haiku-class or on-device.

### 4.4 Three Cost Configurations

Let one session = 30 turns × (60 in + 280 out) per turn, plus layered prompt overhead. The layered prompt is ~3000 tokens prefix (platform + tone + canon slice), which caches almost entirely after turn 1.

**Per-session token accounting:**

- Reader input (uncached): 30 × 60 = 1,800 tokens
- Output: 30 × 280 = 8,400 tokens
- Prompt prefix, first turn (cache write): 3,000 tokens at 1.25× write rate
- Prompt prefix, turns 2–30 (cache read, 88% hit): 29 × 3,000 × 0.88 = 76,560 cached-read tokens; 9,000 × 0.12 = 1,080 uncached miss tokens
- Session projection (layer 3), grows ~100 tok/turn cumulative, average 1,500 per turn: 45,000 tokens uncached-ish (short TTL cache within session, ~50% reuse → ~22,500 miss)

**Config A — 100% Cloud (Claude Sonnet 4.5):**
- Uncached input: (1,800 + 1,080 + 22,500) = 25,380 tokens × $3/M = $0.0761
- Cached read: 76,560 tokens × $0.30/M = $0.0230
- Cache write (first turn): 3,000 × 1.25 × $3/M = $0.0113
- Output: 8,400 × $15/M = $0.1260
- **Per-session: ~$0.236** before any optimization

**Config A' — 100% Cloud but routed (Haiku for 92%, Sonnet for 8%):**
- 92% at Haiku 4.5 rates ($1/$5): ~$0.042 per session
- 8% at Sonnet 4.5 rates: ~$0.019 per session
- **Blended per-session: ~$0.061**

**Config B — Edge 80% + Cloud 20% (escalation + oracle):**
- 80% of turns handled on-device (Gemma 4 E2B or Phi-4-mini via ExecuTorch/MLX) — $0 marginal per turn
- 20% of turns go cloud: mix of Haiku (70% of the cloud portion) + Sonnet (30%)
- 30 turns × 20% = 6 cloud turns
- Haiku cost per turn (60 in + 280 out + cached layers at Haiku rates): ~$0.0018
- Sonnet cost per turn (with cached layers): ~$0.009
- Per session: 4.2 × $0.0018 + 1.8 × $0.009 = $0.0076 + $0.0162 = **~$0.024**
- Plus one-time bundle sync + embedding download (amortized per reader-month, not per session)

**Config C — Self-hosted at scale (open-weight on rented GPUs):**
- A100 80GB at $0.78–$1.49/hr [16]
- A Llama 3.1 70B at batched-mode concurrency can serve ~30–60 concurrent sessions per GPU at quality acceptable for narration
- Amortized cost per session: **~$0.008–$0.015** at steady-state utilization
- Break-even vs Config A' ($0.061/session cloud): at ~2,000 concurrent sessions = **~30,000–50,000 DAU** depending on session frequency and retention

### 4.5 Per-Session Cost Under v2

**Per-session target: $0.02–$0.03 at the architecture we're describing (Config B), without going self-hosted.**

That's a ~60% reduction from v1's $0.07/session estimate. The reduction comes from:

1. Shorter sessions (30 vs 40 turns)
2. Smaller outputs (280 vs 400 avg)
3. Higher cache hit rate (88% vs 70%)
4. Lower escalation rate (8% vs 20%)
5. Better on-device performance availability than v1 assumed (ExecuTorch GA, Gemma 4 E2B, MLX maturity)

At $8/mo consumer price and generous 30 sessions/month per active reader (high), COGS is $0.60/user/month. At $0.02/session and heavier 60 sessions/month, COGS is $1.20/user. Both sit comfortably under a $8–15/mo pricing band with room for infra, storage, CDN, author revenue share, and margin.

### 4.6 Self-Hosting Crossover

Config C becomes compelling around 30–50k DAU assuming 1 session/day/active-user. Below that, pay-per-token cloud is cheaper than GPU fleet capacity. Above that, Config C's 2–5× lower marginal cost pays for the ops burden.

Realistic path: launch on Config A' (pure cloud, routed), migrate to Config B (edge + cloud hybrid) at ~5k DAU when on-device model quality is validated with real readers, evaluate Config C at ~30–50k DAU.

### 4.7 What Syncs vs What Stays Local

| Artifact | Location | Notes |
|---|---|---|
| World Bundle (canon + assets + embeddings) | CDN → device cache | Pinned version; ~20–200 MB per world typical |
| Canon embeddings | Device-local (for edge retrieval) | Enables fully local retrieval when edge model is used |
| Session discovery log | Both (cloud of record + device shadow) | Cross-device sync via event stream |
| Projections (journal, glossary, map) | Derived both places | Deterministic, no canonicalization conflict |
| LLM inference | Mixed | Edge for routine; cloud for escalation |
| Reader preferences | Cloud of record | Settings, accessibility |

The only thing that *must* be cloud-side is the billing, auth, and cross-device sync log. Everything else can degrade gracefully to offline-read if a reader is on a plane — they can continue a session on-device against the cached bundle, using the edge model.

### 4.8 Canon Update Flow Under Read-Only

Author publishes v2 of their world. The new bundle is content-addressed, so it's a new bundle_id. Downstream effects:

1. Readers currently mid-session remain pinned to v1 — their session_state holds `bundle_id=v1_hash`.
2. When they reach a scene boundary, they see an opt-in prompt: *"The author has published a new version of Whisperwood. Continue in v1, or migrate to v2 at the next scene? (Migration may change what you discover next.)"*
3. On opt-in, the session's bundle_id updates; future turns retrieve against v2. The discovery log is unchanged (reader still remembers what they learned), but canon beneath them has shifted.
4. Readers who decline stay on v1 indefinitely. v1 bundles are immutable and live on the CDN forever.

Under v1 this flow had a painful edge case: mid-session grafts pending author review at the moment v2 publishes. Under v2 that edge case does not exist. Nothing is pending.

---

## 5. THE HOLODECK FRAMING — WHERE IT HOLDS, WHERE IT FAILS

The Star Trek holodeck runs user-selected "programs" with "safeties" that prevent the program from harming the user or escaping its bounds. Under v2 read-only, the mapping is much closer:

### Where the metaphor is strengthened by read-only

- **"You can't rewrite the program."** In TNG canon, a user enters a program and plays *within* it. The program is what the author of the program wrote. Our v2 world is exactly that: author-authored, reader-playable, reader-unmodifiable. The "Sherlock Holmes program" does not become a different Sherlock Holmes program because a user rearranged the furniture. Our v2 worlds don't either. This was *not* true in v1 — grafts were an escape hatch from the metaphor.

- **Safeties are in-character.** When a holodeck character refuses to violate their program, the refusal is diegetic ("I don't understand your query, sir"). Our Arbiter refusal is the same — in-character, canon-grounded. Not a popup, not an error.

- **Multiple users can run the same program.** In TNG this is implicit; in our system it's per-session projection over shared immutable canon.

- **Programs can be versioned without corrupting active users.** Picard can keep playing his Dixon Hill program from season 2 even if someone releases a Dixon Hill season-4 update; our v1/v2 bundle pinning does the same.

### Where the metaphor still fails

- **Holodeck programs are experiential, not authorial.** They don't hold a canonical *text*. There is no "Dixon Hill novel" underlying the program. Ours is text-first and the canon is the text. The reader's experience is a *projection of reading*, not a simulation.

- **Holodeck users interact physically.** Ours interact textually. Holodeck metaphor over-promises embodiment.

- **Holodeck safeties fail dramatically.** Our Arbiter doesn't. We do not want the holodeck's "what if the program malfunctions?" plot device.

- **Holodeck programs generate adaptive drama.** Ours narrate a fixed world. Readers who want adaptive drama are in a different product category (AI Dungeon, NovelAI) [17].

[CURIOUS] **The v2 refinement pulls the concept *closer* to a canonical holodeck, not further.** v1's graft mechanism was the part of the design that was *unlike* a holodeck — a user rewriting the program as they played. Removing it makes the metaphor cleaner and the product identity sharper. The concept becomes: "a holodeck of books."

---

## TL;DR

- **Read-only is the killer simplification.** It deletes the graft pipeline, the author review queue, the session-to-canon mutation path, the cross-session graft contamination problem, and versioned graft conflict resolution — roughly 40% of the v1 architectural mass. Do not let it creep back.
- **The AI's job is retrieval + narration + arbitration, not world-extension.** Game-master-with-stakes role mostly evaporates. This makes per-turn work bounded, cacheable, and cheap — small models handle ~80–92% of turns competently.
- **Layered prompt + immutable canon = 88% cache hit rate.** Cost per session drops to ~$0.024 in Config B (edge + cloud hybrid) versus v1's ~$0.07, well inside an $8–15/mo consumer pricing band.
- **Handling off-map reader actions ranks surface-canon → narrate-observation → arbiter-refusal → honest silence.** We prefer "the chronicles do not say" over hallucinated canon. This is an identity choice.
- **The holodeck metaphor is now *more* apt, not less.** v2 is "a holodeck of books": author-written programs, reader-playable, reader-unmodifiable, with diegetic safeties. Lean into it.

---

## DELTA vs V1

**Deleted (architectural mass removed):**
- Graft Promotion Service — gone entirely
- Author Graft Review Workflow — gone entirely
- Graft state machine (5 states, cross-session contamination guards) — gone
- `record_session_graft` contract — deleted; the path from reader turn → bundle mutation no longer exists
- `promote_graft`, `reject_graft`, `author_graft_queue` — deleted
- Graft-aware canon retrieval (the hardest correctness problem in v1) — gone; retrieval now hits a single immutable bundle
- Versioned graft migration at bundle upgrade time — unnecessary; nothing pending to migrate
- Pessimistic locking on graft-insertion paths — gone
- Generative canon extension pathway in the LLM layer — gone; replaced by the 4-rank decision framework
- "Mid-session reader has pending graft when v2 publishes" edge case — doesn't exist

**Simplified (still present but cheaper/cleaner):**
- Session State Service — reduced from log-plus-mutation-layer to pure projection; probably half the code
- Canon Retrieval Service — now strictly read-only; horizontally scalable stateless cache
- Concurrency model — embarrassingly simple; no shared mutable state across sessions
- Interface contract to ARCHITECT_2 — two endpoints (`query_canon`, `validate_response`) instead of six
- LLM role taxonomy — 3 primary roles (narrator, character actor, arbiter) instead of 6
- Canon update flow — reader opt-in at scene boundary, no pending-graft conflict resolution
- Per-session cost model — ~60% cheaper (~$0.024 vs $0.07)
- Escalation rate — 6–10% vs v1's 15–25% (bounded task is easier)
- Cache hit rate — 88% vs 70% (canon never mutates)
- Prompt layering — stable-top ordering works better because layers 0–2 are truly immutable

**Stays (unchanged):**
- World Bundle format and versioning
- Author Studio upload/validate/publish pipeline
- Reading surface specification (typography, companion panes, input)
- Static asset handling (SVG maps, character cards, author-authored)
- Forbidden list (no AI image/audio/video, no chat-app gamification)
- Text-first product identity
- Multi-vendor LLM gateway with routing
- Billing, auth, cross-device sync
- Three-tier cost configuration (cloud / hybrid / self-hosted) with roughly same crossover logic
- Holodeck framing — strengthened, not weakened

**Reframed (same concept, different emphasis):**
- Discovery is now explicitly the core reader loop; companion panes carry more of the experience than prose-pacing alone
- The product identity moves from "living story" (v1's implicit generative premise) to "holodeck of books" (v2's explicit canonical premise)

The simplification is not cosmetic. It is a real, measurable reduction in the service surface area, the correctness surface area, and the cost surface area. v2 is a smaller, sharper product. Do not smuggle back the removed machinery under a different name.

---

## Sources

- [1] [Claude API Pricing — Anthropic](https://platform.claude.com/docs/en/about-claude/pricing)
- [2] [Gemini Context Caching Pricing 2026](https://www.geminipricing.com/context-caching)
- [3] [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing)
- [4] [Claude Haiku 4.5 Pricing 2026 — pricepertoken](https://pricepertoken.com/pricing-page/model/anthropic-claude-haiku-4.5)
- [5] [DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing-details-usd)
- [6] [Gemini 2.5 Flash Pricing 2026](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-flash)
- [7] [Gemini 2.5 Pro Pricing 2026](https://pricepertoken.com/pricing-page/model/google-gemini-2.5-pro)
- [8] [Claude 1M Context Window — Retrieval Accuracy 2026](https://claude5.com/news/context-window-race-2026-how-200k-to-1m-tokens-transform-ai)
- [9] [GPT-4o-mini Pricing 2026 — PE Collective](https://pecollective.com/tools/gpt-4o-mini-pricing/)
- [10] [Token Arbitrage: Groq / Fireworks / Together 2026](https://blog.gopenai.com/the-token-arbitrage-groq-vs-deepinfra-vs-cerebras-vs-fireworks-vs-hyperbolic-2025-benchmark-ccd3c2720cc8)
- [11] [Small Language Models 2026: Phi-4, Gemma 4, Qwen 3.5](https://localaimaster.com/blog/small-language-models-guide-2026)
- [12] [On-Device LLMs: State of the Union 2026](https://v-chandra.github.io/on-device-llms/)
- [13] [MLX for Apple Silicon LLM Inference](https://github.com/ml-explore/mlx)
- [14] [Qualcomm Snapdragon 8 Elite NPU LLM Performance](https://grapeup.com/blog/running-llms-on-device-with-qualcomm-snapdragon-8-elite)
- [15] [ExecuTorch Mobile LLM Inference — PyTorch](https://pytorch.org/blog/unleashing-ai-mobile/)
- [16] [H100 / A100 Rental Pricing 2026 — Thunder Compute](https://www.thundercompute.com/blog/nvidia-h100-pricing)
- [17] [AI Dungeon vs NovelAI Architecture Comparison 2026](https://slashdot.org/software/comparison/AI-Dungeon-vs-NovelAI/)
- [Anthropic Prompt Caching Guide 2026](https://markaicode.com/anthropic-prompt-caching-reduce-api-costs/)
- [RAG Cost Breakdown 2026](https://leanopstech.com/blog/rag-vector-database-cloud-cost-optimization/)
- [Cloudflare Workers AI Edge Inference Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [OpenAI Embeddings Pricing 2026](https://tokenmix.ai/blog/openai-embedding-pricing)
- [Pinecone Serverless Pricing 2026](https://pecollective.com/tools/pinecone-pricing/)
