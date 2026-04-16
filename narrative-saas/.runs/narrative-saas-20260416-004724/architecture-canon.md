# CANON ENFORCEMENT & WORLD ENGINE ARCHITECTURE

## 1. THE CANON ENFORCEMENT PROBLEM

### Why this is the hardest technical problem in the product

An interactive narrative SaaS built on authored canon is structurally hostile to the default behavior of a large language model. LLMs are statistical continuation engines — they are trained to produce the most *plausible* next token given everything they have ever read. The product requires something categorically different: the *correct* next token given a single author's private, often idiosyncratic, sometimes internally inconsistent story bible. Plausibility and canonicity are different objectives, and they diverge most at exactly the moments a reader finds most memorable — named characters, factional politics, physics/magic rules, emotional stakes, late-plot reveals. Every "generic fantasy tavern" cliché that leaks through is a product failure.

Three compounding factors make canon enforcement uniquely hard here:

- **The oracle is authored, not objective.** Unlike a code assistant (where a compiler is ground truth) or a medical assistant (where PubMed is ground truth), the story bible is the *only* source of truth, and it was written by a human who may have contradicted themselves on page 47. There is no external arbiter to appeal to.
- **The failure cost is symmetric and narrative.** A factual hallucination in a chatbot costs the user a correction. A canon violation in a narrative product breaks immersion, which is the product. Readers cannot "correct" a blue sun back to blue once the AI narrator called it yellow — the world has been ruptured, and the rupture is felt viscerally, not logically.
- **Canon is high-dimensional and partly implicit.** Hard facts are the easy part. Tone, voice, cadence, what a given character *would not* say, which verbs are anachronistic in this world — these are soft canon, and they are what readers grade the AI on. Research on long-session AI narrative products confirms this failure mode: "voice continuity drifts beyond 20–30 turns; pronouns drift, speech patterns flatten, backstory contradictions emerge" ([AI Dungeon vs NovelAI voice consistency](https://www.alibaba.com/product-insights/ai-dungeon-vs-novelai-for-interactive-storytelling-which-maintains-consistent-character-voice-over-long-sessions.html)).

### Concrete failure modes (named)

These are the specific, nameable ways the AI goes off-canon. Each needs a detector and a response in the engine.

1. **LORE_CONTRADICTION** — AI asserts a fact that contradicts hard canon ("The capital is Veranth" when the bible says "The capital is Tarn"). Detectable via entailment check against the structured world graph.
2. **PHANTOM_ENTITY** — AI introduces a named NPC, location, artifact, or faction not in the bible. Detectable via named-entity recognition cross-referenced against the entity registry. [CURIOUS] Some phantom entities are desirable (an innkeeper with no narrative weight), so the detector must distinguish *narratively load-bearing* phantoms from *set-dressing* phantoms — a tier boundary, not a binary.
3. **UNAUTHORIZED_RULE_INFERENCE** — AI invents a physics or magic rule the author never established ("The mage teleports" when teleportation was never sanctioned). The model extrapolates from genre priors instead of this world's rules. This is the most insidious failure because it *feels* plausible.
4. **VOICE_COLLAPSE** — A character speaks out of register. The stoic warlord becomes chatty; the formal court mage uses contemporary slang. Detectable via per-character style embeddings compared against output.
5. **PREMATURE_REVEAL** — AI spoils a plot beat the author has gated behind narrative conditions ("You notice the innkeeper is actually the lost prince" in chapter 2 when the reveal is scheduled for chapter 9). Requires a *narrative state* representation — see §3.
6. **FORBIDDEN_ACTION** — Reader attempts something the author has explicitly disallowed (e.g., "kill the protagonist's mentor in the prologue"), and the AI complies instead of deflecting in voice.
7. **TONE_BREACH** — Grim-dark war saga suddenly adopts a whimsical register, or a cozy mystery turns graphic. Detectable via tone classifier on the output versus the author's declared tone profile.
8. **CONTENT_POLICY_BREACH** — Output violates either platform-level or author-level content gates (e.g., "no on-page violence against children"). A hard safety check, not a stylistic one.
9. **TEMPORAL_INCOHERENCE** — AI places an event before its prerequisite ("The king dies" in a scene set before his coronation). Requires a timeline graph with Allen-interval relations.
10. **CANON_AMNESIA** — AI forgets an established session fact within the same session ("Your sword broke in chapter 3" but in chapter 5 the AI describes swinging the same sword). Detectable via session-state store, independent of the authored bible.

### User perspective vs system perspective

A reader experiences a canon violation as *wrongness* — a wrinkle in the world that breaks the dream. They rarely articulate which tier was violated; they just stop trusting the narrator. The system, by contrast, can only notice a violation if there is a rule or a fact to measure against. This is the asymmetry the architecture must close: **every reader-perceptible category of wrongness must have a machine-checkable analog**. Where the author has authored no analog, the system cannot detect the failure — which is why the bible ingestion pipeline (§2) must actively elicit canon that the author didn't think to write down.

---

## 2. THE WORLD ENGINE

### Story bible as machine-readable knowledge

The ingested bible is not a blob of prose with vector embeddings slapped on. It is a **World Graph** — a typed, versioned, queryable structure. The authoring UI can accept prose, tables, or structured forms; the ingestion pipeline (a background service, not the narrative runtime) extracts the graph. Prose never goes directly into the retrieval path without a structured shadow.

Core node types in the World Graph:

- **Entity** — Characters, locations, factions, items, concepts, deities. Each has identity, aliases, and canon tier per attribute.
- **Relation** — Typed edges between entities (`rules`, `allied_with`, `born_in`, `enemy_of`, `parent_of`, `member_of`). Relations are first-class and carry their own tier markers and temporal validity intervals.
- **Rule** — Declarative constraints on the world: "Magic requires a focus object", "Iron weapons cannot harm fae". These compile to validator predicates.
- **Tone Marker** — Author-declared style attributes: genre, register (formal/colloquial), prose density, sentence-length distribution, vocabulary exclusions, profanity posture.
- **Content Gate** — Hard yes/no rules on what the narrator will or will not depict. Child harm, on-page sex, graphic torture, slurs. Gates apply regardless of tier.
- **Plot Beat** — Narrative events gated by preconditions (reader must have done X, session must be in chapter Y, character Z must be present). The spine of premature-reveal prevention.
- **Voice Profile** — Per-character style embedding plus explicit directives: vocabulary whitelist/blacklist, sentence patterns, tics, topics of fixation, topics of aversion.
- **Permission Flag** — Per-node flags: `mutable_in_session`, `author_confirmed`, `derived_by_ingest`, `contested_by_validator`. These govern downstream behavior when canon needs to expand mid-session.

Edges and nodes alike carry: `tier` (hard/soft/extrapolatable), `source` (page/paragraph reference in the authored bible), `confidence` (how well the extractor was able to confirm it), `version` (world version it appeared in), and `valid_interval` (for temporally bounded facts).

### The three canon tiers

- **Hard canon** — Inviolable. Author-declared or author-confirmed. "Character X died in Chapter 7." "The sun is blue." Violations are **blocking**: output containing them is regenerated or rewritten. These facts are always in the prompt budget (§3).
- **Soft canon** — Author preferences, defaults, tendencies. Typical pacing, tone, default NPC behaviors, vocabulary register. Violations are **corrective**: the system prefers on-canon but may tolerate soft deviations if reader action warrants. Retrieved as needed.
- **Extrapolatable canon** — The logical closure of hard and soft canon. Not stated, but inferable within established rules. "If iron hurts fae and this NPC is fae, they flinch from iron." The system may generate into this space with **attribution tagging** — each extrapolated assertion is marked as derived so the author can later confirm it into hard canon or reject it.

### How the system knows which tier

A hybrid, not a pure author-declared or pure inferred system. Pure author-declaration is unrealistic (authors won't tag 10,000 facts); pure inference is unsafe (the model's guess at what's hard becomes a self-fulfilling prophecy). The tier pipeline:

1. **Ingest-time extraction** assigns a *provisional tier* using rules: explicit bible statements with modal certainty ("always", "never", "must") → hard; statements with hedges ("usually", "tends to") → soft; patterns present but unstated → extrapolatable.
2. **Author review UI** surfaces every hard-canon promotion for confirmation. The author sees a batch of extracted facts with a "Confirm / Downgrade / Edit" interaction. Batch size is capped to prevent review fatigue.
3. **Usage feedback** — when an extrapolation gets used in a session and the author doesn't flag it, its confidence increments. After N uncontested uses, it can be promoted to soft canon with author notification. [CURIOUS] This produces *session-grown canon* — the world quietly becomes more specified as readers inhabit it, subject to author veto.

### Handling contradictions inside a story bible

Authors contradict themselves. The detection/resolution pipeline:

- **Contradiction Detector** runs at ingest and on every bible edit. It executes a pass of pairwise NLI-style entailment checks on extracted propositions, scoped by entity. Modern faithfulness evaluation literature decomposes prose into atomic claims and classifies them as entailed/neutral/contradicted — the same pattern applies here ([Faithfulness as an LLM evaluation metric](https://deepeval.com/docs/metrics-faithfulness)).
- **Resolution Strategies (author-selectable defaults)**:
  - *Newest wins* — later bible revisions override earlier. Simple, works for continuity-patching authors.
  - *Explicit wins* — whichever assertion has higher modality/specificity wins. "The dragon is always red" beats "The dragon appeared pale."
  - *Author-arbitrated* — contradiction is queued to the author with both sources shown side-by-side. Default for hard-canon collisions.
  - *Coexistence* — both facts remain, tagged as *author_unresolved*. The narrative runtime avoids asserting either; the AI is instructed to narrate around the contradiction.
- **Contradiction as first-class world state** — Unresolved contradictions are visible to the narrative runtime, which can flag them to the author during any scene that would force disambiguation. This turns a bug (inconsistent bible) into a workflow (just-in-time canon resolution).

---

## 3. CANON RETRIEVAL ARCHITECTURE

### Why pure vector RAG fails this use case

Vector retrieval over embedded bible chunks is the default pattern. For canon enforcement it is *necessary but radically insufficient*. Three concrete failure modes:

- **Lossy on specific facts** — Embedding similarity rewards topical adjacency, not factual precision. "The capital is Tarn" and "The capital is Veranth" embed almost identically; both score high against "Where is the capital?" Retrieval alone cannot arbitrate.
- **Entity-count collapse** — Research on GraphRAG vs vector RAG shows vector accuracy drops toward zero as the number of entities per query grows past ~5 ([GraphRAG vs vector RAG accuracy](https://atlan.com/know/knowledge-graphs-vs-rag-for-ai/), [FalkorDB benchmark](https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/)). A scene with three characters in a faction dispute already has 5+ entities.
- **Relationship-blind** — Vector retrieval doesn't know that `ally_of` is the inverse of `ally_of` on the other node. Narrative reasoning is relational by nature.

Knowledge-graph-only retrieval has the inverse problem: precise on explicit facts, blind to the prose texture — voice, vibe, scene cadence — that readers actually grade on.

### The required pattern: Hybrid Retrieval with Layered Budget

Three retrieval surfaces, composed, with a deterministic budget policy.

**Surface A — Always-in-Prompt Canon (Pinned Layer):**
Hard canon facts relevant to the current scene, plus the active characters' voice profiles, plus active plot-beat gates, plus active content gates. This is the **non-negotiable prompt floor**. Compiled from the World Graph by a deterministic scene-resolver — no embedding similarity, no ranking, just graph walks from the scene's anchor entities.

**Surface B — Structured Graph Retrieval (Graph Layer):**
Relationship queries, multi-hop lookups (`who is X's rival's patron?`), faction trees, timeline positioning. Called by the orchestrator when the reader's action or the scene context references entities that aren't in Surface A. Sub-second graph queries, not LLM-in-the-loop.

**Surface C — Vector Retrieval over Canonical Prose (Texture Layer):**
Authored scene exemplars, descriptive passages, sample dialogue, tone samples. Used to inject *voice and texture* — not facts. Retrieved by semantic similarity to the current scene's emotional/situational vector. This is where the system learns *how the author writes this kind of moment*, not *what is true*.

**Optional Surface D — Rule Engine (Validator Layer):**
Not a retrieval surface per se, but a parallel execution path. The Rule nodes compile to predicates that run over proposed outputs before delivery. "Output mentions iron touching the fae character — does rule R_iron_fae apply? Check for flinch/damage markers." Rule violations trigger regeneration.

This is the "hybrid approaches are becoming a powerful pattern" conclusion from current RAG literature made concrete: vector for breadth and texture, graph for precision and relational reasoning, pinned facts for non-negotiable truth ([GraphRAG vs Vector RAG hybrid pattern](https://ninthpost.com/rag-vs-graph-rag/)).

### Narrative state awareness — the reader knowledge problem

The world engine must maintain **two parallel states**: *world-truth* (everything that is canonically the case) and *reader-knowledge* (the subset the reader has actually discovered this session). The AI narrator must only assert the intersection of (world-truth) and (reader-knowledge ∪ currently-being-revealed).

Architecturally:

- **Canonical Fact Store** — The immutable world graph: what is true.
- **Session Knowledge Store** — An append-only event log of every fact the reader has been exposed to in this session: what they have been shown, told, or plausibly deduced. Event-sourced; every reader turn is a sequence of events that may reveal facts. Martin Fowler's classic event-sourcing pattern applied to narrative exposure ([Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)).
- **Knowledge Projection** — At retrieval time, the narrative state is computed as `session.knowledge_projection(world_graph)` — a view of the world masked by what this reader knows. This directly maps to a fog-of-war model from game design, where information asymmetry between the true state and the player's belief state is the core mechanic ([Fog of War in games](https://www.designthegame.com/learning/tutorial/the-art-science-fog-war-systems-video-games)).
- **Plot Beat Gates** reference both surfaces: a reveal fires when `precondition(reader_knowledge) == true AND world_condition == true`.

[CURIOUS] The most subtle bug this architecture prevents is *narrator omniscience leakage*: the AI, because it sees the full world graph in retrieval, accidentally narrates something the reader couldn't know. The fix is not "tell the model to be careful" — it is a masked retrieval path where, in the reader-facing generation step, the model literally doesn't receive unrevealed facts. Two retrieval passes: one for pacing and plot-beat machinery (full world), one for the narrator's voice (masked world).

### Prompt budget

Current realistic context windows (April 2026): Claude Sonnet 4 with 1M-token beta tier, Gemini 3 Pro at 2M, GPT-5 at 400K ([LLM context windows 2026](https://claude5.com/news/context-window-race-2026-how-200k-to-1m-tokens-transform-ai)). These are *theoretical* windows. The empirical observation across current literature is that effective windows are ~60-70% of advertised, and middle-of-context recall drops to 76-82% vs 85-95% at edges — the "lost in the middle" effect persists ([Best LLMs for Extended Context Windows 2026](https://aimultiple.com/ai-context-window)).

Implication: **do not pack canon into a mega-context and hope**. A story bible for a substantial world runs 200K-2M tokens on its own. Even at 2M tokens, packing the whole bible destroys middle-recall and triples latency. Budget policy:

- **Edge placement for hard canon** — Hard canon facts go at the top and bottom of the prompt, not the middle. Exploits the U-shaped recall curve.
- **Tight bounds on Surface A** — Target <8K tokens of pinned canon per turn. Anything more means scene-resolver needs to aggressively scope.
- **Mid-range budget for Graph Surface** — 4-12K tokens of structured facts pulled on demand.
- **Aggressive compression of Texture Surface** — Vector-retrieved prose samples summarized by a small model to tone descriptors + 1-2 short exemplars, not full chunks.
- **Soft/extrapolatable canon never pinned** — Always retrieved on demand.

Total canon budget per turn: ~20-30K tokens, well within even modest context windows and aggressively below the middle-recall cliff.

---

## 4. WORLD EXPANSION GOVERNANCE

### Author-side expansion reconciliation

When an author ships an expansion, sequel, or retcon, they are proposing a diff against the current World Graph. The pipeline:

1. **Ingest to a branch** — New content enters a *world branch* (version in the graph layer), never the main world trunk.
2. **Contradiction Scan** runs the branch against trunk. Every new assertion is classified: *new fact* (no conflict), *additive fact* (elaborates an existing entity), *contradictory fact* (contradicts trunk), *retcon* (explicitly supersedes trunk).
3. **Author Review UI** surfaces all contradictory and retcon items with a merge workflow: confirm, reject, edit, or split (keep both as coexisting variants for separate narrative paths).
4. **Merge to trunk** produces a new world version with a full changelog and provenance trail: every altered fact carries `previous_value`, `new_value`, `reason`, `author`, `timestamp`, `version`.

This is conceptually git-for-canon. It is intentional, because the engineering patterns from version control — branches, merges, diffs, changelogs, provenance — map nearly 1:1 to canon expansion.

### Multi-author governance

Shared universes, estate IP (a deceased author's successor), collaborators, licensees. Each author-or-collaborator gets a **role** with scoped permissions:

- **Universe Owner** — Full rights. Can change hard canon. Merges land on trunk.
- **Co-Canoneer** — Can propose hard-canon changes via PR; requires owner approval. Full write on soft canon in their designated domain.
- **Domain Author** — Write access to a scoped slice (e.g., "the southern kingdoms only"). Cannot touch canon outside their slice. Their writes flow through a scoped merge workflow.
- **Fan/Community Contributor** (optional) — Proposes extrapolatable canon only; never hard. Owner promotes or rejects.

Permission is *per-entity* and *per-attribute*. Estate cases (successor author inherits a deceased author's universe) set specific entities as immutable even to the successor — the "things the original author would never have allowed" firewall. This is expressed via immutability flags on World Graph nodes, enforced at write time.

**Canon pull request review** is conceptually: a branch of the World Graph, a structured diff (what entities changed, what relations changed, what rules changed), a contradiction report against trunk, a reviewer UI showing the diff in both graph form and rendered-prose form, and a merge action gated by the required approvals.

### World versioning for in-progress readers

A canon update to a universe with readers mid-session is the hardest operational problem in this section.

- **World-version pin at session start** — Every reader session records `world_version = v_N` at start. By default, a session runs against its pinned version for its duration, even if the author ships v_N+1.
- **Author-choice on updates** — On merge, the author declares the update's *session policy*:
  - *Additive only* (new entities, no contradictions): safe; in-progress sessions can opt in to upgrade mid-session with no break.
  - *Contradictory* (retcons): in-progress sessions stay on old version to session-end, migrate on next session. The reader may get a "The world has been updated" notification at session-end.
  - *Critical* (content safety, author-requested takedown): forced migration mid-session. Rare, reserved for safety.
- **Session resumption handling** — On resuming an old session whose pinned version is deprecated, reader is offered: continue on snapshot, migrate to current (accepting possible inconsistencies), or branch off.
- **World Changelog** — A human-readable and machine-readable changelog per version. Readers can see "what changed in this world since my last session" to orient themselves.

---

## 5. CANON DRIFT DETECTION

The generation loop needs drift detection because prevention is not sufficient — even with hybrid retrieval and constrained prompting, the model will drift. Detection is the last line of defense.

### Detection approaches (ranked by product fit)

1. **Rule-Engine Validators (synchronous, per-turn)** — Compiled predicates from World Graph Rule nodes and Content Gates. Fast (<50ms for a typical ruleset), deterministic, explainable. Catches: LORE_CONTRADICTION on rule-encoded facts, UNAUTHORIZED_RULE_INFERENCE against declared rules, CONTENT_POLICY_BREACH. This is the floor — it always runs.
2. **Structured NLI/Entailment Check (synchronous, per-turn)** — Decompose the AI's output into atomic claims, check each against retrieved canon context via a small fine-tuned entailment model ([Faithfulness grounding via NLI](https://jumpcloud.com/it-index/what-is-a-faithfulness-grounding-score)). Catches: LORE_CONTRADICTION on facts, CANON_AMNESIA on session facts. Fast enough for per-turn use with a small model; too slow if you use a flagship LLM as the judge.
3. **Named Entity Audit (synchronous, per-turn)** — Extract every named entity from the output; cross-reference against the World Graph entity registry; flag unknown entities. Catches: PHANTOM_ENTITY.
4. **Voice Classifier (synchronous, per-turn)** — Compare output's per-character dialogue to the character's voice profile via style embedding distance. Catches: VOICE_COLLAPSE, TONE_BREACH.
5. **Second-Pass LLM Auditor (asynchronous, sampled)** — A larger model reviews a sampled % of turns for holistic drift. Not per-turn (too expensive, too slow), but as a quality signal and training feedback loop. Research shows reasoning models hallucinate more than base models on complex factual questions because "extended generation provides more surface area for factuality drift" ([LLM Hallucination Survey](https://arxiv.org/html/2510.06265v2)) — so the auditor uses a non-reasoning model tuned for fact-checking, not a chain-of-thought monster.
6. **Retrieval-Grounded Confidence Scoring (passive signal)** — Every AI claim is scored for how well it's grounded in retrieved canon context. Low-grounding claims are flagged. Cheap, continuous signal that feeds into the decision to regenerate.

The ensemble: 1-4 run every turn before delivery; 5 runs on sampled turns post-hoc; 6 is a continuous background signal.

### Canon audit trail

Every AI turn produces a structured record:

- `turn_id`, `session_id`, `world_version`, `reader_id`
- `reader_input` — what the reader did
- `retrieved_context` — every fact, rule, prose exemplar, voice profile, and plot gate pulled; with identity and version of each
- `model_output_raw` — before any corrective regeneration
- `drift_checks` — results from each validator (rule, NLI, entity, voice)
- `corrections_applied` — whether output was regenerated, what prompt changes triggered the regeneration, how many attempts
- `model_output_delivered` — what the reader actually saw
- `post_hoc_audit` — if sampled by the second-pass auditor, its verdict

This is both a debugging asset and a product asset: the author's dashboard can surface "these scenes produced the most regenerations" as a canon gap signal. Scenes with frequent regenerations mean the bible is underspecified in that region.

### Recovery when drift is detected mid-session (product-acceptability ranked)

1. **Silent retry with stronger grounding** (most acceptable) — Detected drift triggers a regeneration with an augmented prompt: the violated fact is injected as a hard pin, the violated rule is included in system prompt, temperature is lowered. Reader never sees the drift. First-line default.
2. **Narrator rewind in voice** — If regeneration fails 2-3 times, the narrator produces a diegetic rewind: "— no, that's wrong. Let me try again." This is an authorial narrator voice, not a system error. Used sparingly; works best in genres that already use meta-narration.
3. **Session pause for oracle query** — The AI pauses, surfaces a terse "consulting the world..." beat, and the system escalates to a larger model with full canon context for one turn. Acceptable in slow-paced genres, breaks immersion in fast ones.
4. **Explicit reader notification** (least acceptable) — "The AI made a canon error; here is a corrected version." Breaks the fiction completely. Reserved for catastrophic drift (content safety breach caught post-delivery) where reader notification is a feature, not a bug.

The ranking is intentional: the product's quality bar is that canon enforcement is *invisible*. The reader should feel the world is coherent without ever noticing the machinery. Explicit error messages are an architectural admission of failure.

---

## 6. [CURIOUS] ARCHITECTURAL OBSERVATIONS

- **The authoring surface dictates the enforcement ceiling.** You cannot enforce what the author did not author. The bible ingestion UX is load-bearing for canon enforcement quality — the thing that looks like a product surface (the author's editor) is actually the core of the canon engine.
- **Contradictions become features.** An internal-inconsistency detector that queues contradictions for just-in-time author resolution turns the most annoying authorial problem (self-contradiction) into a workflow benefit — the bible gets tighter the more it is used.
- **Session-grown canon is a moat.** The longer a world is inhabited by readers, the more its extrapolatable canon gets tested and promoted. The world literally becomes more specified over time. This is a data flywheel that generic LLM story products cannot replicate.
- **Constrained decoding has limited applicability here.** Grammar-constrained decoding works for structured outputs (JSON, regex, code) ([Constrained decoding guide](https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output)). Narrative prose is not a grammar; you cannot constrain it at the token level without killing voice. Constrained decoding is useful only at narrow checkpoints (e.g., dialogue turns where a character must use/not use a token list) and catastrophic elsewhere.
- **The narrator and the oracle are different models.** The generation model (writes prose, has voice) and the audit model (checks facts, has no voice) should not be the same prompt or even necessarily the same model family. They have different objectives and different failure modes.

---

## TL;DR

- **Canon enforcement is a hybrid retrieval + validation problem, not a prompting problem.** Pinned hard canon + graph-structured precision retrieval + vector texture retrieval + rule engine, composed, with a deterministic prompt budget that respects lost-in-the-middle.
- **The World Engine is a typed, versioned graph with three canon tiers.** Hard (inviolable, always pinned), soft (preferences, retrieved as needed), extrapolatable (logical closure, tagged on use for author promotion).
- **Reader knowledge is distinct from world truth and must be tracked separately.** Event-sourced session knowledge store; the narrator generates against a masked view, the plot-beat engine sees the full world. This prevents premature-reveal leakage architecturally, not through prompt hygiene.
- **Drift detection is an ensemble of synchronous cheap checks and sampled deep audits.** Rule engine + NLI entailment + entity audit + voice classifier run every turn; larger-model auditor runs on samples. Every turn produces a structured audit record that feeds both debugging and author-facing canon-gap signals.
- **World expansion is git-for-canon.** Branches, diffs, contradiction scans, merge workflow, changelogs, version pins on sessions. Multi-author governance is role-plus-scope permissions enforced at the graph node level, with immutability flags for estate/IP firewalls.

## Sources

- [GraphRAG vs Vector RAG Knowledge Graph — atlan.com](https://atlan.com/know/knowledge-graphs-vs-rag-for-ai/)
- [FalkorDB GraphRAG Accuracy Benchmark](https://www.falkordb.com/blog/graphrag-accuracy-diffbot-falkordb/)
- [RAG vs Graph-RAG Hybrid — Ninth Post](https://ninthpost.com/rag-vs-graph-rag/)
- [Best LLMs for Extended Context Windows 2026 — AIMultiple](https://aimultiple.com/ai-context-window)
- [AI Context Window Sizes 2026 — Claude5 Hub](https://claude5.com/news/context-window-race-2026-how-200k-to-1m-tokens-transform-ai)
- [LLM Hallucination Survey — arXiv 2510.06265](https://arxiv.org/html/2510.06265v2)
- [Consistency Is The Key: Detecting Hallucinations — arXiv 2511.12236](https://arxiv.org/html/2511.12236)
- [Faithfulness (Grounding) Score — JumpCloud](https://jumpcloud.com/it-index/what-is-a-faithfulness-grounding-score)
- [Faithfulness — DeepEval](https://deepeval.com/docs/metrics-faithfulness)
- [Benchmarking LLM Faithfulness in RAG — arXiv 2505.04847](https://arxiv.org/html/2505.04847)
- [Ontologies — Blueprints for Knowledge Graph Structures, FalkorDB](https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/)
- [Netflix Entertainment Knowledge Graph](https://netflixtechblog.medium.com/unlocking-entertainment-intelligence-with-knowledge-graph-da4b22090141)
- [Event Sourcing — Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Fog of War in Games — DesignTheGame](https://www.designthegame.com/learning/tutorial/the-art-science-fog-war-systems-video-games)
- [AI Dungeon vs NovelAI Voice Consistency](https://www.alibaba.com/product-insights/ai-dungeon-vs-novelai-for-interactive-storytelling-which-maintains-consistent-character-voice-over-long-sessions.html)
- [Constrained Decoding Guide — Michael Brenndoerfer](https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output)
- [Guiding LLMs The Right Way — arXiv 2403.06988](https://arxiv.org/html/2403.06988v1)
