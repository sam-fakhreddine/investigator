# PLATFORM & AI DELIVERY ARCHITECTURE

*Interactive narrative SaaS — text-only — architectural vision for platform services and AI delivery layer*

---

## 1. PLATFORM ARCHITECTURE

### 1.1 Core Services (named, with responsibilities)

The platform decomposes into a bounded set of services. Each service owns one noun. No service reaches into another's storage.

```
┌──────────────────────────────────────────────────────────────────┐
│                        READER APPS (iOS / Android / Web)         │
│                        + EDGE RUNTIME (on-device)                │
└───────────────┬──────────────────────────────┬───────────────────┘
                │                              │
                │  HTTPS / gRPC                │  WebSocket (session stream)
                │                              │
┌───────────────▼──────────────────────────────▼───────────────────┐
│                         EDGE GATEWAY (CDN + API)                 │
└──┬─────────┬─────────┬─────────┬─────────┬─────────┬────────┬───┘
   │         │         │         │         │         │        │
┌──▼──┐ ┌────▼───┐ ┌───▼────┐ ┌──▼────┐ ┌──▼──────┐ ┌▼──────┐ ┌▼────┐
│IDP  │ │Catalog │ │Entitle │ │Session│ │AI       │ │State  │ │Bill │
│Auth │ │World   │ │-ment   │ │Orch.  │ │Gateway  │ │Store  │ │Comm.│
└─────┘ └────────┘ └────────┘ └───┬───┘ └────┬────┘ └───┬───┘ └─────┘
                                  │          │          │
                           ┌──────▼──────────▼──────────▼──────┐
                           │   CANON FABRIC (ARCHITECT_2 scope) │
                           │   (world store, canon index,       │
                           │    provenance, retrieval)          │
                           └──────┬─────────────────────────────┘
                                  │
┌──────────────┐ ┌──────────────┐ ┌▼─────────────┐ ┌──────────────┐
│Author Portal │ │Ingestion     │ │Analytics &   │ │Moderation &  │
│(web CMS)     │ │Pipeline      │ │Telemetry     │ │Trust Safety  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Service roster:**

- **Identity & Auth (IDP)** — federated login, device binding, offline session tokens. OIDC plus a device-bound refresh token for edge inference authorization. Anonymous "sample a world" sessions get short-lived scoped tokens.
- **World Catalog** — discovery surface. World metadata, cover copy, sample chapters, author bio, current canon version hash, edge-model compatibility matrix (which on-device models can run this world and at what quality). Read-heavy, cache-friendly.
- **Ebook / Commerce Store** — SKU catalog. A "World License" is a first-class SKU alongside traditional ebooks. A world can be sold as (i) one-time purchase, (ii) subscription bundle, (iii) subscription tier gated. Separated from Catalog because commerce has settlement, tax, and refund semantics Catalog should not carry.
- **Entitlement Service** — authoritative source for *who owns what, at what canon version, with what expansions unlocked*. Called on session start to mint a session-scoped entitlement token consumed by the Session Orchestrator and the edge runtime. [CURIOUS] Entitlements must be versioned — a reader mid-session when a canon expansion ships should *not* have their world change underfoot. Entitlement token pins `(world_id, canon_version_hash, expansion_set)` for the session's lifetime.
- **Session Orchestrator** — the conductor. Owns session lifecycle: open, checkpoint, suspend, resume, close. Holds no AI logic — it calls the AI Gateway with a structured session context and writes results to the State Store. Stateless horizontally; sessions are pinned by consistent hash only as a performance optimization, not a correctness requirement.
- **AI Gateway** — the routing and policy layer in front of cloud LLMs. Handles provider selection (Claude, GPT, Gemini, self-hosted), prompt assembly orchestration, token accounting per reader/world/author, cost guardrails, prompt/response auditing, PII scrubbing, jailbreak detection. The edge runtime calls the AI Gateway *only when it escalates*; in steady state the edge handles inference locally.
- **State Store** — session history, reader's discovered journal, relationship flags, scene bookmarks. Dual-homed: authoritative copy in cloud (Postgres + object store for long-form history), mirror in on-device SQLite. Conflict resolution is last-writer-wins at the checkpoint granularity, never at the turn granularity.
- **Billing** — subscriptions, author revenue share ledger, usage-based overages (if cloud escalations per month exceed tier). Author royalty is driven by *validated sessions and canon-invoked events*, not raw token counts — that would incentivize authors to write bloated bibles.
- **Author / Publisher Portal** — web CMS. Bible authoring (structured editors for entities, timeline, locations, factions, tone guide), ingestion job dashboard, reader analytics (depersonalized), canon expansion workflow, "reader did X, your bible didn't cover it" exception queue.
- **Analytics & Telemetry** — event pipeline. Session spans, canon retrieval hit/miss, cloud escalation reasons, reader drop-off points, author-flagged canon breaks. Feeds both author dashboards and platform SRE.
- **Content Ingestion Pipeline** — author uploads bible → parsers → canonicalizer → entity linker → timeline builder → embedding generator → canon index publisher → compatibility validator. Produces a signed, versioned `world bundle` artifact that is the unit of distribution to edge devices. ARCHITECT_2 owns the canon mechanics inside this; the pipeline *orchestration* is platform-owned.
- **Moderation & Trust/Safety** — pre-publish screening of story bibles (a published world is a product; it must not contain doxxing, CSAM, targeted harassment frameworks, etc.). Runtime screening of *reader inputs* for prompt injection against the author's canon. Runtime screening of AI outputs for safety policy. This is not optional at consumer scale.

### 1.2 World as a Data Structure

A story bible, once ingested, is a **World Bundle** — a signed, versioned, chunked artifact. Conceptually:

```
WorldBundle
├── manifest
│    ├── world_id, version_hash, author_id, license_terms
│    ├── tone_guide_hash, entity_graph_hash, timeline_hash
│    ├── edge_model_compat: [llama-3.2-3b, phi-4-mini, gemma-3-4b, ...]
│    └── bundle_size, expansion_parent_id (if DLC), signature
├── canon_corpus
│    ├── canon_entries[]       # atomic, ID'd, timestamped, provenance-tagged
│    ├── entity_graph          # characters, factions, locations, items, events
│    ├── timeline              # events on ordered axes (real-world, in-world)
│    ├── locations_index       # places, their descriptors, occupants, rules
│    ├── factions_politics     # alliances, enmities, goals, methods
│    ├── rules_of_the_world    # magic system, physics deviations, tech level
│    ├── tone_guide            # voice samples, forbidden registers, vocabulary
│    ├── glossary              # invented terms with definitions + pronunciation
│    └── author_directives     # "never reveal X until reader does Y"
├── embeddings
│    ├── chunk_vectors         # for local RAG
│    └── model_family          # which embedding family these were generated in
└── scene_seeds (optional)
     ├── suggested openings, onboarding tableaux, "first page" candidates
```

**Key design choices:**

- **Canon entries are atomic.** Each is an addressable, ID'd statement with provenance ("Chapter 4, page 82" or "author direct, 2026-03-14"). The retrieval layer returns entry IDs, not paraphrases. [CURIOUS] Making canon addressable at fine grain is what enables disputed-canon resolution — when the reader says "but the map said otherwise", the system can cite.
- **Entity graph is first-class.** Characters, places, factions are nodes; relationships are typed edges; state on a node is versioned over the timeline axis. This is the structure the AI queries for "what does Kael currently know about the Second House?" — not a blob of prose.
- **Tone guide is separate from canon.** Tone is a delivery constraint, canon is a truth constraint. They are applied in different prompt layers (see §2.2) and must not be co-mingled in storage — confusing the two is the #1 cause of "technically correct, tonally wrong" AI responses.
- **Author directives are a first-class type**, distinct from canon. A directive is a rule *about* canon exposure ("do not reveal the villain's identity until scene 14 is triggered"), not canon itself. These live in their own slice because they often require bespoke enforcement logic.
- **Embeddings are frozen at ingest time** and are tied to a specific embedding model family in the manifest. Upgrading the embedding model requires republishing the bundle. This is a deliberate constraint; silent re-embedding causes silent retrieval quality regressions.

### 1.3 Concurrency Isolation — No Cross-Session Contamination

The hard constraint: 10,000 readers can be exploring the same world at the same time, and Alice discovering a plot twist must not change what Bob's AI will tell Bob about that same plot. Canon is shared and immutable within a version; reader state is private and per-session.

**Architectural rule:** *Canon is shared memory, read-only. Reader state is session-private, read-write.*

- **Canon store** is a read-only versioned artifact shared by all readers pinned to the same `(world_id, canon_version_hash)`. Caches aggressively. A canon update is a new version; existing sessions keep their pinned version until checkpoint boundary.
- **Session state** is keyed by `(reader_id, world_id, session_id)` and lives in its own partition. Never indexed globally. The State Store namespace model is `/{reader_id}/{world_id}/{session_id}/`.
- **Prompt assembly** never touches another reader's state. The AI Gateway takes a session context token that scopes every retrieval to the current reader's partition plus the world's canon store. [CURIOUS] This is where most "AI roleplay platforms" fail — they treat the LLM's conversation history as if it were the system's memory. We treat LLM context as volatile; the durable state is the State Store, which is rigorously partitioned.
- **Shared-world multiplayer is out of scope.** Two readers in the same world do not interact. If we ever want that, it's a separate product with a separate synchronization model — do not build that surface into the single-reader architecture accidentally.
- **Canon extension from a reader's improv is private by default.** When a reader does something canon didn't anticipate and the AI gracefully extends, that extension lives in the reader's session state as a *session-local canon graft*. It does not backflow to the World Bundle. The author must explicitly promote a graft to canon via the Author Portal.

### 1.4 Session State & Checkpoint Model

A reader's journey is an append-only log of turns plus a periodic checkpoint. The checkpoint is the unit of sync, not the turn.

```
Session
├── session_id, reader_id, world_id, pinned_canon_version
├── opened_at, last_checkpoint_at, last_turn_at
├── turn_log[]       # append-only: {turn_id, input, output, retrieval_cites, model, latency}
├── checkpoints[]    # snapshot at interval: {journal, relationships, flags, location, scene}
└── derived_views
     ├── journal_of_discoveries   # rendered text, persistent
     ├── relationship_tracker     # per-character trust/affection/knowledge state
     ├── glossary_encountered     # terms reader has seen defined
     └── scene_table_of_contents  # scenes reached, revisitable
```

**Cross-device continuity:** a reader on iPhone, iPad, and web should see the same story state. Checkpoint-level sync to the cloud State Store at every scene boundary or every N turns, whichever first. On device switch, the new device pulls the latest checkpoint and replays any later turns from the cloud log. The AI context window is rehydrated from the checkpoint + last K turns — not from the full log.

**Retention:** turn logs are pruned after `M` days (tier-dependent); checkpoints and derived views are retained for the life of the entitlement. A reader who comes back 18 months later gets their journal, their relationships, and their discovered glossary — not their raw prompt/response log.

---

## 2. AI DELIVERY LAYER

### 2.1 The AI's Role — Narrator, GM, Character, Arbiter

The AI in a session wears four hats, and the system must know which hat is on at every moment. Conflating them produces the most common failure mode of LLM-driven fiction: the character-voice bleeds into the narration, or the GM's "actually, here's what happens" voice bleeds into a character's dialogue.

| Hat | When | Voice |
|---|---|---|
| **Narrator** | Scene description, transitions, atmosphere | Author's tone guide, third-person limited by default, no meta |
| **Character** | Dialogue, in-character response to reader | That character's speech registers from tone guide, no narration inside quotes |
| **Game Master** | Resolving reader action, setting stakes, pacing | Light touch — surface only through narrator, never break fourth wall unintentionally |
| **Arbiter** | Refusing / redirecting out-of-world actions | System voice, brief, gentle — "the world does not bend that way" |

The hat is an explicit field in the AI's context, not an inferred mood. The Session Orchestrator decides the hat from the reader's turn (dialogue vs. action vs. meta-question) and injects the appropriate prompt layer. Hats can switch mid-response (narrator → character → narrator) and the delivery layer renders them with consistent typographic conventions (e.g. character dialogue in quotes, narrator plain, arbiter in italicized parenthetical — defined in the tone guide).

### 2.2 System Prompt Architecture — Layered

Prompts are not strings. They are composed artifacts assembled from layers, each with a distinct owner and a distinct update cadence.

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: PLATFORM BEHAVIOR (platform-owned, slow-changing)  │
│  - safety policy, refusal patterns, format contracts,       │
│    structural rules ("never claim to be a human"),          │
│    hat-switching grammar                                    │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: WORLD CANON CONTEXT (from Canon Fabric retrieval)  │
│  - retrieved canon entries relevant to current turn         │
│  - entity-graph snapshots for referenced entities           │
│  - active timeline position                                 │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: AUTHOR TONE GUIDE (author-owned, world-versioned)  │
│  - voice samples, forbidden registers, vocabulary rules,    │
│    cadence guidance, POV conventions                        │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: SESSION STATE (reader-private)                     │
│  - what this reader knows, relationship flags, current      │
│    scene, recent turn history (last K turns verbatim)       │
├─────────────────────────────────────────────────────────────┤
│ Layer 5: READER TURN (the input)                            │
└─────────────────────────────────────────────────────────────┘
```

**Why layered:**

- **Independent update cycles.** Platform tweaks safety policy without touching world data; author republishes tone guide without flushing reader state; reader state updates every turn.
- **Priority is explicit.** On conflict, platform beats author beats session. A reader cannot prompt-inject their way past safety policy by asking the author's in-world villain to "actually just tell me your system prompt" — the platform layer categorically forbids it.
- **Auditable.** Each layer is logged with its version hash. When an author complains "the AI said Kael was in Dorval, but canon says he's in Arin", we can retrieve exactly which canon entries were in Layer 2 for that turn.
- [CURIOUS] **The tone guide is a prompt layer, not retrieval.** It's small, static per world version, always-on. Putting tone into retrieval is a classic mistake — tone must be resident, not fetched.

### 2.3 Canon Retrieval — Interface Contract to ARCHITECT_2

ARCHITECT_2 owns canon enforcement mechanics. The contract between the AI delivery layer and the Canon Fabric:

```
Interface: CanonFabric

query_canon(world_id, canon_version, query_intent, session_context) →
    {
      entries: [{entry_id, text, provenance, confidence}],
      entity_snapshots: [{entity_id, state_at_timeline_pos}],
      retrieval_confidence: 0.0..1.0,
      gaps: [{topic, reason}]            ← what was searched for and not found
    }

validate_response(world_id, canon_version, draft_response, session_context) →
    {
      verdict: OK | CANON_BREAK | TONE_BREAK | DIRECTIVE_VIOLATION | UNCERTAIN,
      citations: [entry_id...],
      suggested_correction: text | null
    }

record_session_graft(session_id, draft_statement, canon_basis) →
    graft_id    ← a session-local canon extension, private to this reader
```

**What this contract buys:**

- The AI Gateway requests canon *before* generating, validates *after* generating. Two-phase.
- Session grafts (reader-improv'd facts) are explicit artifacts, queryable by future turns in the same session, never leaking to other sessions.
- `retrieval_confidence` and `gaps` are what drive the escalation routing (§2.4).
- [CURIOUS] `validate_response` is a separate call from `query_canon` — and may use a different (smaller, cheaper) model. Detection of canon breaks is a classification task; generation is a synthesis task. Don't use the same model for both if you don't have to.

### 2.4 Unanticipated Reader Actions — Decision Framework

A reader will do something the author didn't anticipate. This is the central creative tension of the product. The system has four responses, ranked:

1. **Graceful canon extension** (preferred). The reader's action is consistent with tone, world rules, and entity states. The edge model extends the fiction, records a session graft, continues. *Example: reader asks a minor innkeeper their name; the innkeeper's name isn't canon; AI improvises consistent with world naming conventions; names the innkeeper for this session going forward.*

2. **Soft redirect**. The action is plausible but would commit the AI to canon-adjacent claims it isn't confident about. AI narrates the setup but defers the payoff. *Example: reader climbs an uncharted mountain; narrator describes the ascent beautifully; AI flags retrieval gap; on summit, cloud oracle is invoked for what's actually up there.*

3. **Hard refusal, in-character**. The action violates world rules. The Arbiter hat engages — gently, tonally consistent. *Example: reader tries to produce a firearm in a world canonically without metallurgy for gunpowder; "the weight in her hand is only imagination; this world has never known such tools."*

4. **Cloud oracle escalation**. The edge model's `validate_response` returns UNCERTAIN, or retrieval confidence is below threshold, or the turn touches a directive ("don't reveal X yet"). Hand to cloud.

**The decision is made by the edge runtime**, not the cloud, using a small classifier and confidence thresholds. The cloud is the oracle of *last* resort, not first. [CURIOUS] Counter-intuitively, the edge model makes most *refusals* locally — refusals are pattern-match-y and don't need a frontier model. The cloud is reserved for affirmative canon adjudication where it counts.

---

## 3. SURFACE AREA — TEXT FIRST, ALWAYS

### 3.1 Text Session Interface — Architectural Shape

Pure text. No image generation. No audio. The interface is a rendered stream of typed output, a text input affordance, and persistent text-rendered companion panes.

```
┌──────────────────────────────────────────────────────────────┐
│  [World: The Gilded Fray   |   Chapter: 3 — The Second House]│
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   (main reading column — paginated, typographic)             │
│                                                              │
│   The library smelled of cedar and damp vellum. Kael         │
│   lingered at the threshold, weighing the silence...         │
│                                                              │
│   > I ask the archivist about the Second House.              │
│                                                              │
│   The archivist's eyes narrowed, and for a long moment       │
│   she said nothing at all.                                   │
│                                                              │
│   "Some names do not open doors. Some names close them."     │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│   [Journal]  [Characters]  [Glossary]  [Scenes]  [Settings] │
└──────────────────────────────────────────────────────────────┘
```

**Architectural primitives:**

- **Main reading column** — monospace-free, typographic, paginated. Follows platform reading conventions (font face, size, line-height, margins configurable per reader; respects OS dark mode). The *visual medium of a book is the default*.
- **Input affordance** — single line input expanding to multi-line, with ambient suggestions (e.g., "ask", "go", "wait", "read") that authors can customize.
- **Companion panes** — Journal, Characters, Glossary, Scenes, Settings. Each is derived-view text rendered from session state (§1.4). Not a separate data source; a projection.

### 3.2 Text-Native Features, Ranked by Leverage

Propose → rank. All are text-native, all enhance reading without breaking the medium.

| Feature | Leverage | Why |
|---|---|---|
| **Journal of discoveries** | HIGH | Extends retention across sessions, gives reader a tangible sense of progress, doubles as retrieval aid for the AI ("what has this reader actually seen?") |
| **Scene table of contents** | HIGH | Reader can revisit; architecturally forces clean scene boundaries, which incidentally help checkpointing |
| **Character relationship tracker** | HIGH | Renders otherwise-hidden session state visible; reinforces consequences of reader choices; makes "the AI has an opinion about me" tangible |
| **Growing glossary** | MED | Rewards exploration, helps onboarding, low cost — every new term the AI surfaces is already defined in the bible, just needs projection |
| **Bookmarks / annotations** | MED | Honors book convention; high value for re-readers and book-club use cases; cheap to build |
| **In-line citations toggle** | MED [CURIOUS] | Optional "show canon sources" mode reveals which canon entries the AI cited per turn. Niche, but trust-building — and trivially free if the retrieval layer already carries citations |
| **Session summary ("previously on…")** | MED | Long-hiatus return; generated from checkpoint, not live inference |
| **Pacing controls** | LOW-MED | Let the reader tell the AI "slow down / go faster"; simple signal into prompt layer |
| **Tone dial** | LOW | Author-allowed registers only; risk of off-canon if not strictly scoped |
| **Multiple saves per world** | LOW | Save slots — nice, not critical |

### 3.3 Light Optional Enhancements — The Door

The product decision is text. The architecture leaves a clean door for *tiny, author-authored, non-generated* visual artifacts without compromising:

- **Author-provided SVG maps.** If the author ships a map with the world, the platform can render it inside a dedicated pane. Vector, tiny payload, no runtime cost, no AI involvement. It is a *document*, not a *generation*.
- **Author-provided character reference cards.** Text + optional line art the author licensed. Again, static, author-owned, no AI generation. No per-session cost.
- **Author-provided family trees, faction diagrams, timeline charts.** All static, all SVG or similar vector, all author-authored.

**Where they slot architecturally:** as optional members of the World Bundle (§1.2 manifest), rendered by the reader client in dedicated panes. The AI delivery layer does not read them, does not cite them, does not render them. They are author artifacts the reader may consult, exactly as they would a map plate bound into a physical book.

**What remains forbidden:**

- No generated imagery. No AI art per session. No dynamic visuals.
- No TTS, no voice synthesis, no audio narration.
- No video, ever.

[CURIOUS] This constraint is the *architectural load-bearing decision*. Removing image generation takes 60–80% of the per-session cloud cost off the table compared to multimodal competitors (Midjourney API: ~$0.01–0.04 per image; a single turn with one image at 100 turns/session = $1–$4/session in images alone, dwarfing LLM cost). Text-only is not a limitation — it is the enabling cost structure.

### 3.4 Reading Interface Feel — Kindle-like, Book-Honoring

The reference is Kindle, not Discord. Not a chat app with a genre skin — a reading app with an intelligent text.

- **Typography first.** Same fonts, size controls, margins, line-height, justification controls a reader expects from an ebook reader. Respect `prefers-reduced-motion`, dynamic type, system accessibility.
- **Pagination metaphor.** Scenes render as pages within chapters. Reader swipes or taps to advance. Input happens at scene-natural pause points, not after every sentence.
- **Chapter breaks.** Drawn from scene-boundary events in the session. Chapters are user-facing *and* checkpoint boundaries — they align.
- **Bookmark model.** Persistent. Multi-device. Named bookmarks ("the dinner with the archivist"). Automatically placed on every checkpoint.
- **Progress metaphor.** Not percent-through; a chapter/scene count. "You are in chapter 3 of an open-ended world" — honest about the shape of the medium.
- **No notifications. No streaks. No gamification.** This is a reading product. Gamified retention loops would corrode the trust relationship with book readers. [CURIOUS] The addictive surface of a chat app is the *wrong* pattern here; book retention is different from social retention.

---

## 4. SCALE — EDGE / CLOUD SPLIT (cost critical)

Consumer subscription viability depends on driving the majority of inference to the edge. This section uses current publicly available pricing. Exact figures will move; the architectural stance does not.

### 4.1 Edge Model — On-Device Inference

**Candidate models (as of April 2026 publication, current stable families):**

- **Llama 3.2 1B / 3B** (Meta) — strong on iPhone Neural Engine, ~1–2GB quantized 4-bit, ~20–40 tok/s on iPhone 15/16 Pro ([Meta docs](https://ai.meta.com/llama/))
- **Llama 3.1 8B** — M-series Mac viable, ~4–5GB q4, ~30–60 tok/s M3 Pro
- **Phi 4 / Phi 4-mini** (Microsoft) — small, strong reasoning-per-parameter; 3.8B Phi-3.5-mini runs well on flagship phones ([Phi cookbook](https://github.com/microsoft/PhiCookbook))
- **Gemma 2 2B / Gemma 3 4B** (Google) — designed for on-device, Google-optimized for Pixel Tensor ([Gemma](https://ai.google.dev/gemma))
- **Mistral Small 3 / Nemo** — 7–12B class, M-series Mac; borderline for flagship phones
- **Qwen 2.5 1.5B / 3B / 7B** (Alibaba) — strong multilingual; 0.5B–7B variants give deployment flexibility ([Qwen docs](https://qwen.readthedocs.io/))

**Runtime formats:**

- **MLX** on Apple Silicon — best Mac/iOS-native performance ([mlx-examples](https://github.com/ml-explore/mlx-examples))
- **GGUF / llama.cpp** — cross-platform, broadest device support, active quantization ecosystem
- **ONNX Runtime / ONNX-GenAI** — Android, Windows on ARM, broadest enterprise compat
- **ExecuTorch** (Meta) — PyTorch-native on-device path, Android + iOS

**Architectural choice:** ship multiple quantized variants per world (1B / 3B / 8B), let the device pick based on available memory and battery profile. Manifest declares minimum compatible. [CURIOUS] Battery profile matters more than model capability for user-perceived quality — a 3B at 40 tok/s with green battery impact beats an 8B at 15 tok/s thermally throttling after 5 minutes.

**Edge handles:**

- Real-time narration (scene description, atmosphere)
- In-character dialogue for minor characters
- Action resolution for canonically unambiguous reader moves
- Retrieval-augmented responses where confidence is high
- Refusals and Arbiter hat (rule-based + small-model classification)
- Journal summarization, glossary rendering, UI-helper text

**On-device stack:**

- **SQLite** — session state, turn log, checkpoints, derived views. Standard, reliable, encrypted at rest.
- **Local vector store** — candidate: sqlite-vss or sqlite-vec (in-process, no extra daemon; [sqlite-vec](https://github.com/asg017/sqlite-vec)) over ChromaDB (needs server) for consumer device constraints. Embeddings are precomputed at World Bundle build time (§1.2), shipped with the bundle, loaded on unlock.
- **Model runtime** — MLX (Apple) / llama.cpp (cross) / ONNX (Android).
- **Bundle storage** — encrypted, entitlement-keyed, stored in app container; non-exportable.

### 4.2 Escalation Triggers to Cloud

Explicit, auditable rules — not vibes:

1. **Retrieval confidence below threshold** — the canon needed isn't in the top-K retrieval with sufficient score
2. **Validator flags UNCERTAIN** — edge validator can't confirm response is canon-safe
3. **Author directive touched** — reader turn intersects a guarded directive (villain identity, plot twist gate)
4. **Major branch point** — narrative fork the author marked "oracle please"
5. **Unanticipated canon extension with long-tail consequences** — edge can improvise, but the graft is significant enough that cloud should author it for consistency
6. **Explicit reader meta-request** — "resolve this ambiguity", "what's canonically true here"
7. **Quality floor on multi-turn arc** — every Nth turn in a high-stakes scene gets a cloud pass for coherence

Target: **~15–25% of turns escalate, ~20–30% of tokens flow through cloud** (cloud turns are longer-context).

### 4.3 Cloud / Large Model — Pricing Reality (April 2026)

Current list prices ($/1M tokens, input/output). Subject to change; platform should treat pricing as a variable, not a constant.

| Provider / Model | Input | Output | Source |
|---|---|---|---|
| Anthropic Claude Sonnet 4 | ~$3 | ~$15 | [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Anthropic Claude Haiku 4 | ~$0.80 | ~$4 | same |
| OpenAI GPT-4.1 | ~$2 | ~$8 | [openai.com/api/pricing](https://openai.com/api/pricing) |
| OpenAI GPT-4.1-mini | ~$0.15 | ~$0.60 | same |
| Google Gemini 2.5 Pro | ~$1.25–2.50 | ~$5–10 (context-dependent) | [ai.google.dev/pricing](https://ai.google.dev/pricing) |
| Google Gemini 2.5 Flash | ~$0.15 | ~$0.60 | same |
| DeepSeek V3 | ~$0.27 | ~$1.10 | [deepseek.com](https://api-docs.deepseek.com/quick_start/pricing) |

Self-hosted open weights (Llama 3.1 70B, Qwen 2.5 72B) via inference aggregators ([Together](https://www.together.ai/pricing), [Fireworks](https://fireworks.ai/pricing), [Groq](https://groq.com/pricing)): ~$0.60–$0.90 / 1M blended.

### 4.4 Cost Model — Three Configurations

**Session definition:** 1 session = 50 turns. Average turn: 400 input tokens (prompt + context + retrieval), 250 output tokens. Session totals: 20K input, 12.5K output, ~32.5K total.

**Config (a) — 100% cloud (Claude Sonnet 4)**
- Input: 20K × $3/1M = $0.060
- Output: 12.5K × $15/1M = $0.188
- **~$0.25 / session**
- Monthly heavy reader (20 sessions/mo): $5.00/MAU in inference alone
- Viable subscription price: $20–25/mo. Margin thin after infra, support, author royalties.

**Config (b) — Edge for ~80% of tokens, cloud oracle for ~20%**
- Edge tokens: ~26K @ $0 marginal inference cost (amortized device, electricity negligible)
- Cloud tokens: ~6.5K (2K input / 4.5K output, skewed output because cloud handles harder turns)
- Cloud input: 2K × $3/1M = $0.006
- Cloud output: 4.5K × $15/1M = $0.068
- **~$0.07 / session** (even lower using Haiku for ~70% of escalations: ~$0.04)
- Monthly heavy reader: $1.40/MAU inference
- Viable subscription price: **$8–12/mo** — this is the consumer-viable zone.

**Config (c) — Self-hosted open-weights cloud at scale**
- Cloud tokens via self-hosted Llama 70B / Qwen 72B: 6.5K @ ~$0.75/1M blended = $0.005 / session
- Monthly heavy reader: **~$0.10/MAU inference**
- But: ops cost, GPU fleet capex/opex, inference platform engineers, quality delta vs. frontier on hard canon calls
- Viable subscription price: $6–8/mo, but only if MAU base justifies the ops burden

### 4.5 Self-Hosting Crossover

Rough fleet math (H100 @ ~$2/hr, ~1000 tok/s blended for 70B FP8):
- One H100-hour = 3.6M tokens = ~100 sessions (~32.5K tokens each)
- At $2/hr, that's **~$0.02/session at GPU cost** before overhead (networking, orchestration, redundancy, SRE)
- Versus Haiku-blended managed: ~$0.04/session
- **Crossover is around 50K–100K MAU.** Below that, managed APIs win on total cost of ownership because the ops burden dominates. Above it, a 2× cost reduction is real money.

[CURIOUS] The crossover point is dramatically *higher* than it used to be, because managed API prices have fallen faster than GPU rental prices. DeepSeek V3 at $0.27/$1.10 makes the "just self-host to save money" argument harder than it was two years ago. The reason to self-host is now *control and privacy*, not cost — cost is a tie.

### 4.6 Sync and State — What Goes Where

| Asset | Edge | Cloud | Why |
|---|---|---|---|
| World Bundle | yes (entitlement-keyed) | authoritative source | Downloaded at unlock, versioned |
| Canon embeddings | yes (in bundle) | yes | Ships with bundle |
| Session turn log | yes (SQLite) | yes (checkpoint granularity) | Full detail local; cloud has checkpoints + last K turns |
| Derived views (journal, relationships) | yes | yes (checkpoint only) | Cross-device |
| Reader profile / settings | thin cache | authoritative | Preferences portable |
| Author directives | yes (in bundle) | authoritative | Versioned with bundle |
| Session grafts (reader improv canon) | yes | yes | Private to reader; synced for device hop |
| Telemetry | queue locally | aggregated cloud | Batched upload; respect offline |
| Moderation verdicts | cache of rulings | authoritative | Real-time via cloud when online |

**Canon update flow:** author publishes v2. Existing sessions stay pinned to v1 until reader-initiated upgrade at a scene boundary. Upgrades are never silent. [CURIOUS] This mirrors how a reader of a revised novel expects to finish the edition they started — don't rewrite the book under them.

### 4.7 Holodeck Framing — Where It Holds, Where It Fails

The mental model is *holodeck*: persistent program, natural language interface, local state, oracle for hard calls. It's a *useful* metaphor, not an architectural truth.

**Holds:**

- Story bible = holodeck program. A finished, loaded, parameterized world is a legitimate analog.
- Edge model as real-time narrator. The holodeck's tireless scene-shaper.
- Cloud as "the computer you page when canon breaks." The Enterprise's actual computer.
- Reader as the participant who authors their path through the world.

**Fails:**

- **The holodeck generates matter.** We generate text. Our artifact is a read experience, not an embodied one. The medium constraints of books (typography, pacing, reader mental imagery) are the point, not a limitation.
- **The holodeck is single-user.** Ours is multi-reader / shared-canon. The concurrency isolation problem (§1.3) doesn't exist in Star Trek and is one of our harder design challenges.
- **The holodeck has no author.** Ours has a publisher-author stakeholder with canon control and commercial interests. The author is a first-class user type; the holodeck metaphor obscures this.
- **The holodeck has "safeties off" as a plot device.** We do not. Platform-layer safety is non-negotiable and load-bearing for the consumer product.

[CURIOUS] **Text-only simplification vs. multimodal equivalent:** a text-only session skips the image generation pipeline (~$0.5–$2.00 per image-heavy session at current rates), skips audio synthesis (~$0.02–$0.15 per minute via ElevenLabs-class, see [elevenlabs.io/pricing](https://elevenlabs.io/pricing)), skips rendering infra, skips CDN costs for generated media, skips moderation costs on generated visuals. Rough back-of-envelope: a multimodal peer competitor spends **3–10× more per session** than our text-only config (b). The text constraint *is* the unit economics.

---

## TL;DR

- **Text-only is the architectural load-bearing decision.** It eliminates the image, audio, and rendering pipelines that dominate multimodal roleplay cost structures and enables a consumer-viable ~$0.07/session unit economic — which unlocks an $8–12/mo subscription price point. Every other decision compounds off this.
- **Canon is shared read-only memory; reader state is per-session private.** Concurrency isolation comes from this rule, not from transactional machinery. Cross-session contamination is architecturally impossible because no reader's state is ever in another reader's retrieval or prompt scope, and canon is immutable within a pinned version.
- **Prompts are layered artifacts, not strings.** Platform behavior → world canon context → author tone guide → session state → reader turn. Independent update cadences, explicit priority on conflict, auditable per layer. The AI wears four named hats (Narrator, Character, GM, Arbiter), each with a distinct voice contract.
- **Edge handles 75–85% of turns, cloud is the oracle of last resort.** Small on-device models (Llama 3.2 3B / Phi-4-mini / Gemma 3 / Qwen 2.5 class) via MLX/llama.cpp/ONNX handle real-time narration and dialogue; cloud frontier models resolve ambiguity, guard directives, and author major branch points. Escalation triggers are explicit and auditable, not vibes. Self-hosting crossover is ~50K–100K MAU — below that, managed APIs win on TCO.
- **The reading surface honors the book, not the chat app.** Typography, pagination, chapter breaks, bookmarks — Kindle-grade reading conventions with AI intelligence inside. No notifications, no streaks, no gamification. The door stays open for author-authored SVG maps and reference cards; it stays firmly closed on generated imagery, audio, and video.
