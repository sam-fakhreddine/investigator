# FEASIBILITY RESEARCH

## 1. MARKET SIZE (grounded, 2025–2026)

### 1.1 Interactive Fiction — the nearest-adjacent market

The interactive-fiction category — which spans Choice of Games-style branching prose, visual novels, and the broader "narrative games" segment — is the canonical TAM anchor for a read-only canonical-world reading product. 2025–2026 sizings vary by definition:

- Dataintelo pegs interactive fiction at **$6.4B in 2025**, projected to **$14.8B by 2034 at 9.8% CAGR** ([Dataintelo](https://dataintelo.com/report/interactive-fiction-market))
- IntelMarketResearch has the narrower "interactive fiction game" slice at **$3.84B (2024) → $7.8B (2032), 12.0% CAGR**, with 2025 at $4.30B ([IntelMarketResearch](https://www.intelmarketresearch.com/interactive-fiction-game-market-21560))
- Mobile is ~41% of the interactive fiction market in 2025, and Asia-Pacific projected >35% of global revenue by 2030 ([Dataintelo](https://dataintelo.com/report/interactive-fiction-market))

**[CURIOUS]** The category grew through the AI hype cycle *without* AI being a prominent feature. Choice of Games, inkle, Failbetter — all pre-LLM architectures — continue to be the named market leaders in 2025 research reports, suggesting readers value curated branching prose on its own merits. This is a tailwind for the v2 concept because the read-only world narrows the product toward that same reader psychology rather than toward the gamer/chatbot psychology.

### 1.2 AI Companion / Character Chatbot — the noisy adjacent category

Definitions here are wildly inconsistent. The tightest consumer-app slice is the most relevant:

- Consumer AI companion apps crossed **$120M in annual revenue in 2025** with the 2026 trajectory on path to $200M+ ([RoboRhythms](https://www.roborhythms.com/ai-companion-app-market-2026/))
- Broader "AI companion market" sized at **$24B–$50B in 2026** depending on scope, with CAGRs of 30%+ ([Fortune Business Insights](https://www.fortunebusinessinsights.com/ai-companion-market-113258); [Grand View Research](https://www.grandviewresearch.com/industry-analysis/ai-companion-market-report))
- Character.AI: **$50M revenue in 2025** (66% YoY), 20M MAUs (down from 28M mid-2024), valuation fell from $2.5B to ~$1B ([Sacra](https://sacra.com/c/character-ai/); [Business of Apps](https://www.businessofapps.com/data/character-ai-statistics/)). Traffic: 223M visits peak Feb 2025 → 153M Dec 2025 → 194M Jan 2026

**[CURIOUS]** Character.AI's *monetary* efficiency is staggeringly low per user — $50M / 20M MAU = **$2.50 ARPU annualized**. The v2 concept targets a reader population whose book-buying ARPU is already 10–20x that through Kindle/Audible patterns; the subscription-gated interactive layer is monetizing a population with *already-revealed willingness to pay for narrative*.

### 1.3 Ebook Subscription — the revenue-model anchor

- Global ebook market: **$23.5B (2025) → $34.5B (2033) at 4.9% CAGR**; subscription services took **55.72% of ebook market share in 2025** ([SkyQuest](https://www.skyquestt.com/report/ebook-market))
- Kindle Unlimited: **~10M subscribers early 2026** (up 15% YoY); 2025 author payouts **$711.3M** (avg $59.3M/month); total KU payouts since 2020: **$2.58B** ([The New Publishing Standard](https://thenewpublishingstandard.com/2026/03/19/kindle-unlimited-payout-2026-four-million-books-ebook-growth/))
- KENP rate Sept 2025: **$0.004521 per page read** ([Written Word Media](https://www.writtenwordmedia.com/kdp-global-fund-payouts/))

### 1.4 Creator Economy IP Licensing

- Creator economy **$214B–$234B in 2026**, projected **$528B by 2030 at 22.5% CAGR** ([Market.us](https://market.us/report/creator-economy-market/); [Coherent Market Insights](https://www.coherentmarketinsights.com/industry-reports/europe-and-us-creator-economy-market))
- IP licensing deal volume: 600K+ cross-border agreements annually ([Market.us](https://market.us/report/creator-economy-market/))
- Author fiction AI licensing deals fall into the **$1,500–$3,000 per book** range, with exceptional storytelling going higher ([The AI Optimist](https://www.theaioptimist.com/p/ai-pays-authors-3000-per-book-2025))

### 1.5 TAM / SAM / Initial Target

- **TAM (ceiling, interactive reading + canonical-world subscription combined):** ~$8–10B in 2026, assuming a convergence at the intersection of interactive fiction ($4.3–6.4B), ebook subscription ($12B+ subscription segment), and the licensing-to-reader bridge
- **SAM (English-speaking, premium book reader cohort willing to pay $10–15/mo for interactive access):** ~$500M–$1B. Anchored against Kindle Unlimited's 10M subs × conservative 5% conversion to interactive tier at $15/mo = ~$90M subscription-only; plus ebook unlock-gate pricing layered on top
- **Realistic initial target (Year 1–2, 1–2 anchor worlds with existing readership):** $10–30M ARR. One mid-famous fantasy world with 500K–1M readers × 5–10% conversion to $15/mo interactive sub

### 1.6 Cost Curve Tailwind

LLM inference costs have fallen **~10x annually 2022–2025**, with Epoch AI showing **40x/year price decline for GPT-4-equivalent performance on hard tasks** ([Epoch AI](https://epoch.ai/data-insights/llm-inference-price-trends/)). Current 2026 pricing:
- Claude Opus 4.5: $5/$25 per M tokens (down from $15/$75) ([Anthropic](https://platform.claude.com/docs/en/about-claude/pricing))
- Gemini 2.0 Flash-Lite: $0.075/$0.30 per M tokens ([TLDL](https://www.tldl.io/resources/llm-api-pricing-2026))
- DeepSeek V3.2: $0.28/$0.42 per M tokens ([TLDL](https://www.tldl.io/resources/llm-api-pricing-2026))

On-device: Snapdragon 8 Gen 3+ supports 3B–7B param models at 15–30 tok/s; Qualcomm's next gen is targeting 200 tok/s ([On-Device LLMs State of Union 2026](https://v-chandra.github.io/on-device-llms/)). Implication: by 2027–2028, a portion of canon-retrieval + constrained generation could plausibly run locally, collapsing per-reader marginal cost toward zero.

## 2. COMPETITIVE LANDSCAPE (2026 current state)

### 2.1 Direct AI-Narrative Platforms

**AI Dungeon / Latitude**
Post-2021 content-filter disaster (users banned for stories they didn't write; "8-year-old laptop" flagged as CSAM) drove most users off. Delisted from Steam March 2024 ([Wikipedia](https://en.wikipedia.org/wiki/AI_Dungeon); [aidungeon.com help](https://help.aidungeon.com/faq/openai-and-filters)). 2025–2026 consensus: three simultaneous failures killed trajectory — (1) OpenAI-mandated filter rollout was rushed and false-positive-saturated; (2) no canon/bounded-world system meant the AI generated whatever; (3) reactive moderation without author involvement. The v2 read-only design pre-empts all three.

**Character.AI (post-Google licensing, post-settlement)**
- Google paid **$2.7B in Aug 2024** for a non-exclusive technology license + Shazeer/de Freitas rehire; DOJ examined the structure as a potential acqui-hire end-run ([Bloomberg](https://www.bloomberg.com/news/articles/2024-08-02/character-ai-co-founders-hired-by-google-in-licensing-deal); [PYMNTS](https://www.pymnts.com/artificial-intelligence-2/2024/google-reportedly-spent-2-7-billion-to-rehire-character-ai-founder/))
- Abandoned own LLM development post-deal ([EM360Tech](https://em360tech.com/tech-articles/character-ai-scraps-building-llms-after-google-deal))
- **Jan 7, 2026: Character.AI + Google agreed to settle wrongful-death suits** in FL, NY, CO, TX — including Sewell Setzer III (Megan Garcia) and Juliana Peralta cases. Terms not disclosed, monetary damages expected but no liability admitted ([CNN](https://www.cnn.com/2026/01/07/business/character-ai-google-settle-teen-suicide-lawsuit); [CNBC](https://www.cnbc.com/2026/01/07/google-characterai-to-settle-suits-involving-suicides-ai-chatbots.html); [Washington Post](https://www.washingtonpost.com/technology/2026/01/07/google-character-settle-lawsuits-suicide/))
- Banned under-18 open-ended chat Nov 2025; rolling out age assurance ([NBC News](https://www.nbcnews.com/tech/tech-news/characterai-bans-minors-response-megan-garcia-parent-suing-company-rcna240985))
- April 2026: added ads to website version — classic late-stage monetization desperation signal ([RoboRhythms](https://www.roborhythms.com/character-ai-ads-april-2026/))

**NovelAI**
Unfunded, private, Kayra-XL + Anime V4 diffusion stack. $10/$15/$25/mo tiers. Subscriber count undisclosed ([G2](https://www.g2.com/products/novelai/reviews); [AI Tools DevPro](https://aitoolsdevpro.com/ai-tools/novelai-guide/)). Differentiator: uncensored + writer-focused. Text-only lineage is closest to v2, but no author/canon licensing layer.

**Inworld AI**
$500M valuation (2023), $125M+ total raised from Lightspeed/Kleiner/Founders Fund/Microsoft M12. Pivoted toward enterprise NPC/agent infrastructure, servicing companion apps, devtools, interactive media ([PitchBook](https://pitchbook.com/profiles/company/483614-92); [Crunchbase](https://news.crunchbase.com/ai-robotics/inworld-ai-funding-video-game-ai-character-generation/)). Not a direct competitor — they'd potentially be *infrastructure* a v2 platform might use.

**Replika / Luka Inc**
Hit with **€5M Italian DPA fine May 19, 2025** for GDPR violations — no legal basis for processing, no age verification despite claimed 18+ policy ([EDPB](https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en); [Captain Compliance](https://captaincompliance.com/education/replikas-e5-million-gdpr-fine-key-takeaways-for-ai-developers/)). Separate training-data investigation opened same day. Relevant precedent because v2 collects subscriber behavioral/emotional data from book readers.

**PolyBuzz / Janitor AI / Chub**
NSFW-adjacent roleplay hubs. Chub ($20/mo Mars sub) is losing traffic to Sakura.fm/Kindroid due to scaling issues in 2026 ([RoboRhythms](https://www.roborhythms.com/ai-companion-app-market-2026/); [All About AI](https://www.allaboutai.com/resources/best-chub-ai-alternatives/)). These are the UX anti-pattern v2 is defined against — no canon, no licensing, no professional authorship.

**Fable / Showrunner**
Amazon Alexa Fund invest July 2025, in talks to license **Disney IP** (Star Wars, Marvel) for AI-generated animated TV ([Variety](https://variety.com/2025/digital/news/netflix-of-ai-amazon-invests-fable-showrunner-launch-1236471989/); [Fiction Horizon](https://fictionhorizon.com/disney-in-talks-to-license-characters-for-ai-generated-streaming-platform-showrunner-fans-already-hate-it/)). Sub pricing $10–$40/mo credits. **[CURIOUS]** Fable is explicitly the *multimodal* opposite of v2 (animation generation, not text), but the IP-licensing-to-fans structure is the same wedge — validating that the licensing pattern is commercially live with Disney-tier estates in 2025–2026.

### 2.2 Adjacent / Gate-keepers

**Choice of Games / Hosted Games**: 25% author royalty with $10K–$15K advance. Proven branching-prose publisher model at scale but no AI element ([Choice of Games](https://www.choiceofgames.com/looking-for-writers/)).

**inkle, Failbetter**: Respected but small. Fallen London is the browser-subscription proof point. No 2025 revenue disclosures ([MCV/Develop](https://mcvuk.com/development-news/want-your-story-to-drive-your-game-rather-than-vice-versa-inkle-and-failbetter-discuss-the-storytelling-potential-of-the-open-source-ink/)).

**Roll20**: 70% creator revenue share on marketplace; $4.99 minimum price point; payment on 7th of each month ([Roll20 Partners](https://pages.roll20.net/partners)). Demonstrates that a durable creator-economy marketplace for narrative content can hold a 70/30 split.

**Sudowrite**: $3M raised, 300K+ fiction-writer users, $10–$44/mo ([PitchBook](https://pitchbook.com/profiles/company/482793-13); [Inkfluence](https://www.inkfluenceai.com/blog/sudowrite-review-pricing-2026)). Adjacent author-side tool; suggests author-side utility can stand alone as a business.

**Webtoon Entertainment (WBTN)**: FY2025 revenue $1.4B, net loss **$373.4M driven by goodwill impairments**; Q4 2025 revenue down 6.3% ([Webtoon IR](https://ir.webtoon.com/news-releases/news-release-details/webtoon-entertainment-inc-reports-fourth-quarter-and-full-year-0); [Stock Analysis](https://stockanalysis.com/stocks/wbtn/revenue/)). Stock $9.21 on March 13, 2026. The UGC-narrative-at-scale model is under real financial stress.

**Microsoft Publisher Content Marketplace (launched Feb 2026)**: 2-sided AI licensing marketplace. Launch partners: Business Insider, Condé Nast, Hearst, AP, USA TODAY, Vox Media. **[CURIOUS] Zero trade book publishers. Zero academic presses.** ([The New Publishing Standard](https://thenewpublishingstandard.com/2026/02/11/microsoft-publisher-content-marketplace-ai-licensing-fiction-book-publishers/); [Microsoft Ads](https://about.ads.microsoft.com/en/blog/post/february-2026/building-toward-a-sustainable-content-economy-for-the-agentic-web)). This is a material gap in the landscape — the trade-fiction rights holders are not yet in any general AI licensing marketplace as of Q1 2026.

### 2.3 Where each stops short, and what read-only changes

| Competitor | Where they stop | What read-only opens |
|---|---|---|
| AI Dungeon | No canon layer; AI invents uncontrollably | No adversarial story generation; canon corpus is finite |
| Character.AI | Characters without authored world; user-generated bots have no IP | Licensed canon = real IP value, no co-defendant exposure on invented canon |
| NovelAI | Writer tool, not reader tool; no IP relationship to canon owners | Reader-facing + licensed-canon is a different business |
| Fable/Showrunner | Multimodal, TV-show generation, IP-heavy but generative | Text-only + read-only = lower generation liability & lower inference cost |
| Inworld | Infra for game-makers | Could be infrastructure, not competition |

**The gap the v2 concept opens and existing players cannot close without breaking their model**: A licensed, canon-read-only reader-subscription product *cannot* be bolted onto Character.AI (their value prop is user-generated bots in any imagined IP, which is the exact liability surface they just settled over), nor onto AI Dungeon (their value prop is emergent AI-authored story, not curated authored canon), nor onto NovelAI (they're writer-side, not reader-side). Fable/Showrunner is multimodal and generative — they could in theory pivot, but doing so would cannibalize their animation-generation value prop. The closest existing player to potentially close the gap is a new entrant built by a major publisher or estate — which is the real competitive threat, not any of the current AI-narrative startups.

## 3. ANALOGUES AND PRECEDENTS (2025–2026)

### 3.1 Kindle Unlimited KENP — the per-page payout anchor

- **Sept 2025 rate: $0.004521/page**. Historical band $0.0041–$0.0046 ([Written Word Media](https://www.writtenwordmedia.com/kdp-global-fund-payouts/); [BookBloom](https://www.bookbloom.io/tools/kenp-calculator))
- Monthly KDP Select Global Fund: typically $25–$35M
- 2025 total KU payouts: **$711.3M** (+11.2% YoY) ([TNPS](https://thenewpublishingstandard.com/2026/03/19/kindle-unlimited-payout-2026-four-million-books-ebook-growth/))

**Implication for v2 royalty structure**: If a canonical-world interactive session averages 30–60 minutes of reader engagement, the "equivalent KENP" model would pay an author ~$0.05–$0.15 per session. For a platform to deliver material per-reader author royalty (≥$0.25/session), the subscription price must be high enough to clear LLM inference cost + platform margin + author share. At current Claude Opus 4.5 pricing ($5/$25 per M) and a 30-minute session generating ~20K output tokens, inference alone is ~$0.50/session — already higher than KENP equivalent. **Gemini 2.0 Flash-Lite class models ($0.075/$0.30 per M) drop this to ~$0.006/session, making the unit economics workable.**

### 3.2 Spotify — the streaming-rate reality check

- **$0.003–$0.005 per stream in 2026**; avg ~$0.004 US. 1M streams = $3–4K ([Ditto Music](https://dittomusic.com/en/blog/how-much-does-spotify-pay-per-stream); [Chartlex](https://www.chartlex.com/blog/money/how-much-does-spotify-pay-per-stream-2026))
- **Total 2025 payouts: record $11B** (70% of annual revenue); lifetime $70B ([Relix](https://relix.com/news/detail/spotify-announce-record-royalty-payouts-in-2026-loud-clear-report/))

**Warning signal**: Streaming aggregation pressure per-unit rates toward the floor. Any v2 platform that admits too many worlds creates the same pool-dilution dynamic. The defense: limit catalog depth in Year 1–2, keep author royalty per-session directly calculable not pool-split.

### 3.3 Audible / ACX 50% exclusive — the "creator-favorable" ceiling

- **New royalty model: 50% exclusive / 30% non-exclusive** — early-access creators seeing ~45% earnings uplift vs. old 40%/25% ([ACX](https://www.acx.com/mp/blog/audibles-new-royalty-model-early-access-successes); [Jane Friedman](https://janefriedman.com/audibles-royalty-shake-up-what-it-means-for-authors/))

This is the current north-star for "fair-feeling" creator split on a platform model. A v2 structure of 50% to author/publisher post-infrastructure-costs is defensible in the public narrative; anything below 35% will invite Authors-Guild-class pushback.

### 3.4 Roll20 — 70/30 creator marketplace

- 70% to creator, 30% to platform; $4.99 price floor ([Roll20 Partners](https://pages.roll20.net/partners))

The "narrative content for a subscription-gated platform" analog closest to the v2 read-only-world model. Demonstrates the 70% creator share is market-viable when platform doesn't bear LLM costs.

### 3.5 Wattpad / Naver / Webtoon — UGC narrative at scale, stressed

- Naver acquired Wattpad May 2021 for **$754M CAD / ~$600M USD**; now in Naver's entertainment division
- Webtoon Entertainment 2025: revenue $1.4B (+2.5%), net loss $373.4M, **goodwill impairments** ([Webtoon IR](https://ir.webtoon.com/news-releases/news-release-details/webtoon-entertainment-inc-reports-fourth-quarter-and-full-year-0))
- Q1 2026 guidance: $317–$327M revenue, $0–$5M adj. EBITDA — a flatlining top line

**[CURIOUS]** The strongest single cautionary signal in the whole landscape: a mature, IP-rich, narrative-at-scale platform with ~$1.4B revenue, a massive Korean parent, and recognizable global brand is booking hundreds of millions in impairments and guiding flat. Narrative content platforms do not compound easily even at scale.

### 3.6 Quibi retrospective — the "engineered market you don't have" warning

2025 consensus ([Babson](https://entrepreneurship.babson.edu/lessons-from-billion-dollar-failure/); [StartupWired](https://startupwired.com/2025/05/10/quibi-2-billion-and-a-6-month-shutdown/); [WBS](https://www.wbs.ac.uk/news/three-lessons-for-start-ups-from-quibi-s-failure/)): Quibi failed because (1) no problem existed (stuck between TikTok free and Netflix premium); (2) three founding assumptions were all wrong (10-min videos, A-list stars, marketing-driven momentum); (3) no social sharing crippled organic growth; (4) traditional-corporate operational rigidity vs. tech startup iteration. **Relevance to v2**: "Text-only interactive reading for book readers" is a narrower, more clearly-stated reader-behavior hypothesis than Quibi's "premium short video for in-between moments." The risk is still real — book readers may not want an interactive layer. This must be validated with a real anchor author + real reader base before burning more than seed capital.

### 3.7 AI Dungeon retrospective — the "don't let the platform author the canon" warning

2025–2026 consensus: AI Dungeon was strategically dead by mid-2021 after (a) OpenAI-mandated rushed CSAM filter, (b) 400+ false-positive rate on benign phrasings, (c) no author/canon discipline so the AI generated whatever users pushed it toward, (d) user backlash → review bombing → migration to NovelAI and downstream NSFW platforms ([Toolify](https://www.toolify.ai/ai-news/the-rise-and-fall-of-ai-dungeon-1683581); [aidungeon.com help](https://help.aidungeon.com/faq/openai-and-filters); [Wikipedia](https://en.wikipedia.org/wiki/AI_Dungeon)). **[CURIOUS]** The hand the v2 concept is designed to play is exactly the one AI Dungeon refused: restrict generation to author-sanctioned canon and externalize moderation risk onto the author's pre-approved corpus.

## 4. RISK ASSESSMENT (v2-refined)

### 4.1 Top 5 Business Risks (re-ranked for v2)

1. **Author-acquisition cost and quality curve.** To monetize at the KU-like scale, the platform needs ~50–500 authored worlds with 100K+ readership each. First 3–5 anchor authors will take 6–18 months of BD per signature. Without an IP-famous anchor (e.g., a Sanderson, a Scalzi, a Riordan), initial launch has no gravity. **[CURIOUS]** This is a *deeper* risk under v2 than v1 because the read-only constraint makes the *quality* of the canon the entire product. A 2K-page bible is meaningfully more expensive and slower to produce than a "stub world + AI fills it in" design.

2. **Subscription conversion from ebook-buying readers.** No proven conversion rate exists for "book reader → interactive reader subscriber." The Kindle Unlimited comparable (10M subs out of Amazon's ~300M Prime base = ~3%) is at best a distant proxy. Below 2% conversion at $15/mo, per-author economics break.

3. **Aggregation / disintermediation risk from Amazon/Microsoft.** Microsoft's Publisher Content Marketplace (Feb 2026) contains zero trade-book publishers today — but once it includes them, any independent "licensed-canon + AI delivery" play gets flanked. Amazon's "Ask This Book" launched Dec 11, 2025 as an *unlicensed* feature over books in your library ([Authors Guild](https://authorsguild.org/news/statement-on-amazon-kindle-ask-this-book-ai-feature/)) — Amazon is positioning toward exactly this space with its existing ebook rights contracts. **This risk is structurally higher under v2 than v1** because the read-only constraint makes Amazon's asset base (owned ebook corpus) more directly competitive.

4. **Platform-bans contagion from regulatory tightening on AI-minor interactions.** Even with read-only canon, California SB 243 (eff. Jan 1, 2026) requires every AI companion chatbot to disclose non-human identity at start of first conversation with a minor, block sexually inappropriate content, and surface mental-health crisis resources ([HeyOtto](https://www.heyotto.app/resources/ai-laws-protecting-kids-2026)). A federal bipartisan Senate bill would prohibit AI companion chatbots from being accessible to minors entirely ([HeyOtto](https://www.heyotto.app/resources/ai-laws-protecting-kids-2026)). If SB 243 interpretation extends to narrative reading experiences — not yet settled — the YA-fiction subsegment is unreachable.

5. **Consumer-perception blast radius from any child-safety incident in the category.** Even if the v2 platform has zero incidents, one Character.AI-style tragedy in the broader AI-narrative-chat category in 2026–2027 will re-trigger press, VC, and partner anxiety. The category has three settled/settling lawsuits as of Jan 2026 ([CNN](https://www.cnn.com/2026/01/07/business/character-ai-google-settle-teen-suicide-lawsuit)).

### 4.2 Risks that shrink materially under v2

- **Canon-generation liability (HUGE shrinkage).** Under v1 the AI could invent canon, creating content the author/estate never approved — prime litigation surface. Under v2, nothing leaves the author-approved corpus. Character.AI-class co-defendant exposure on invented in-world content is materially lower.
- **Content-moderation from AI-invented content (LARGE shrinkage).** Moderation collapses from "monitor unbounded AI generation" to "validate narration respects canon retrieval + safety policy." The AI Dungeon failure mode is structurally pre-empted.
- **Author IP-drift lawsuits (LARGE shrinkage).** Bartz v. Anthropic's $1.5B settlement (Sept 2025, ~$3K/book, ~500K works, four payment installments through Sept 2027 with final fairness hearing May 14, 2026 — [Susman Godfrey](https://www.susmangodfrey.com/wins/susman-godfrey-secures-1-5-billion-settlement-in-landmark-ai-piracy-case/); [Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)) establishes that training on unlicensed books is legally radioactive at the $3K/book floor. Under v2, the platform only uses author-licensed canon → the Bartz precedent *helps* the platform (because the platform is doing the opposite of Anthropic's Books3/LibGen ingestion).
- **Regulatory exposure on AI-generated harmful content (MEDIUM shrinkage).** EU AI Act GPAI enforcement begins Aug 2, 2026 with fines up to €15M or 3% global revenue ([Latham](https://www.lw.com/en/insights/eu-ai-act-gpai-model-obligations-in-force-and-final-gpai-code-of-practice-in-place); [Arnold & Porter](https://www.arnoldporter.com/en/perspectives/advisories/2025/08/does-your-company-have-eu-ai-act-compliance-obligations)). But the v2 platform is a downstream deployer, not a GPAI provider — the primary obligation lands on the model provider (Anthropic/OpenAI/Google). Downstream transparency obligations remain but are lower than generative obligations.

### 4.3 Risks that stay the same or grow

- **Minor-access regulation** (Replika €5M/GDPR precedent; Character.AI settlements; CA SB 243; federal Senate bill) — unchanged. Read-only vs. generative does not help here if reader is a minor, because the risk is attachment formation and emotional impact regardless of whether the canon was invented.
- **PII / behavioral-data GDPR exposure** — unchanged. Italian DPA hit Replika for processing basis + age verification independently of what the bot said.

### 4.4 Risks that are new or shifted under v2

- **Retrieval-truth risk.** Under v2, readers *expect* canonical accuracy. A hallucinated claim about Gondor's political structure is now a *product defect* — not a whimsical side-effect. The product's only value proposition becomes canonicity; losing it is existential.
- **Session-depletion risk.** Because the reader cannot mutate canon, there's a long-tail question of whether a finite world runs out of "new to uncover" for high-engagement subscribers. Retention curve analysis for mature readers is an unknown.
- **Author-side UX risk.** A read-only-world promise requires a *structured* canon — not just a manuscript. Authors must produce world-bibles with discrete retrievable facts. This is a ~10x heavier authoring workflow than handing over an ebook. Authors may balk.

### 4.5 Top 3 Technical Risks

1. **Canon-grounded generation accuracy at session scale.** RAG with graph overlay (GraphRAG-style) is the 2025–2026 state of art for canon fidelity ([Chitika](https://www.chitika.com/retrieval-augmented-generation-rag-the-definitive-guide-2025/); [Techment](https://www.techment.com/blogs/rag-in-2026/)). Million-token context windows (e.g., Gemini 2.5, Claude 200K+) reduce the need for retrieval on small bibles but don't eliminate drift on long multi-session arcs.
2. **Adversarial prompt injection for canon exfil or policy bypass.** OWASP Top 10 for LLMs 2025 ranks prompt injection as #1 threat; roleplay-exploit attacks hit 89.6% success rate against common guardrails; character-injection and AML evasion hit up to 100% success against Azure Prompt Shield and Meta Prompt Guard ([Astra](https://www.getastra.com/blog/ai-security/prompt-injection-attacks/); [ArXiv 2504.11168](https://arxiv.org/abs/2504.11168); [OWASP](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). A determined adversary *will* extract canon text verbatim, which becomes a copyright/licensing breach to the author.
3. **Cost stability at scale.** Inference costs are declining 10x/year on average but the variance is huge (9x–900x per benchmark — [Epoch AI](https://epoch.ai/data-insights/llm-inference-price-trends/)). A Year-1 unit-economics model that assumes 2026 Gemini Flash-Lite pricing and then sees capacity-constrained pricing (during model launches, NVIDIA supply issues, etc.) will have volatile margins.

### 4.6 The single hardest problem

**v1 position**: "Defend canon against drift + adversarial prompting at viable cost."

**v2 position — revised**: The hardest problem is no longer canon defense (read-only architecture removes most of it) — **the hardest problem is now author acquisition and canon-production UX.** Without 3–5 anchor-IP authors who can produce retrieval-ready structured world bibles, the platform has nothing to sell. Character.AI had 18M user-created bots because users made them for free; v2 has no equivalent zero-cost content supply. This is a cold-start problem that inference cost declines do not solve.

One sentence: **"Can we get three A-list authors or one major estate to produce retrieval-structured, read-only licensed canon within 12 months, at terms they'll publicly defend?"**

## 5. REGULATORY AND IP (2026 live state)

### 5.1 Character.AI × Google Settlement (Jan 7, 2026)

- Families and companies agreed to negotiate settlements in four states (FL, NY, CO, TX) for wrongful-death suits tied to teen suicides linked to chatbot use
- Specific terms not disclosed; monetary damages expected; no liability admitted in filings
- Platform concessions already made independently: Nov 2025 under-18 open-ended chat ban; "age assurance" functionality being deployed
- Google's role as licensor of tech + Character.AI co-founder rehire under the $2.7B Aug 2024 deal created the joint-defendant structure
- Sources: [CNN](https://www.cnn.com/2026/01/07/business/character-ai-google-settle-teen-suicide-lawsuit), [CNBC](https://www.cnbc.com/2026/01/07/google-characterai-to-settle-suits-involving-suicides-ai-chatbots.html), [TechCrunch](https://techcrunch.com/2026/01/07/google-and-character-ai-negotiate-first-major-settlements-in-teen-chatbot-death-cases/), [Washington Post](https://www.washingtonpost.com/technology/2026/01/07/google-character-settle-lawsuits-suicide/), [Axios](https://www.axios.com/2026/01/07/google-character-ai-lawsuits-teen-suicides)

**What the settlement actually changes**: Because it was settled rather than litigated to judgment, no binding precedent was created. But it establishes (a) AI chatbot companies *and their model-licensor tech partners* can both be named as co-defendants, (b) "age assurance" features are effectively table stakes now, (c) reference fact pattern for future plaintiffs will be Sewell Setzer / Juliana Peralta. **[CURIOUS]** The non-adjudication means the "AI platform immunity under Section 230" question remains legally open — no victory for either side.

### 5.2 Bartz v. Anthropic $1.5B Settlement (prelim approval Sept 25, 2025; final fairness hearing May 14, 2026)

- **~$3,000 per class work** × ~500,000 pirated works (LibGen + PiLiMi datasets)
- Four installments: Oct 2, 2025; April 30, 2026; Sept 25, 2026; Sept 25, 2027
- Releases Anthropic only from *past* liability for pre-Aug 25, 2025 conduct; no forward license
- Largest copyright settlement in US history
- Sources: [Susman Godfrey](https://www.susmangodfrey.com/wins/susman-godfrey-secures-1-5-billion-settlement-in-landmark-ai-piracy-case/), [Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/), [Authors Alliance](https://www.authorsalliance.org/2025/09/28/bartz-v-anthropic-settlement-gets-preliminary-approval-key-takeaways/), [Ropes & Gray](https://www.ropesgray.com/en/insights/alerts/2025/09/anthropics-landmark-copyright-settlement-implications-for-ai-developers-and-enterprise-users), [Copyright Alliance](https://copyrightalliance.org/participating-bartz-v-anthropic-settlement/)

**Current state of doctrine for derivative content**: Training on books without license is the predicate for the $3K/book floor. This is a *pro-v2* precedent because the v2 model is license-only. It *undermines* any competitor that would silently use an IP holder's catalog to power interactive experiences.

### 5.3 EU AI Act — 2026 Enforcement Posture

- GPAI obligations in force **Aug 2, 2025**; full enforcement powers at AI Office from **Aug 2, 2026**
- Pre-Aug-2025 legacy models: comply by **Aug 2, 2027**
- Fines: **up to €15M or 3% global revenue**, whichever higher
- 2026 Commission priorities: systemic-risk GPAI mitigation, procedural rule streamlining
- Sources: [Latham & Watkins](https://www.lw.com/en/insights/eu-ai-act-gpai-model-obligations-in-force-and-final-gpai-code-of-practice-in-place), [Arnold & Porter](https://www.arnoldporter.com/en/perspectives/advisories/2025/08/does-your-company-have-eu-ai-act-compliance-obligations), [DLA Piper](https://www.dlapiper.com/en-us/insights/publications/2025/08/latest-wave-of-obligations-under-the-eu-ai-act-take-effect), [EU Commission](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)

**Applicable to a text-only interactive narrative platform**: The platform is a downstream *deployer*, not a GPAI provider. Primary obligations (training-data summaries, copyright-compliance policy, risk mitigation) lie with the foundation-model provider. Deployer obligations under Art. 50 cover AI-interaction transparency — the user must know they're talking to AI. For a text-only canon-read-only product this is trivially satisfied by platform design. **Lower regulatory weight than competitors who train their own models.**

### 5.4 Replika / Italian DPA — Precedent Fallout

- €5M GDPR fine, May 19, 2025 ([EDPB](https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en); [IAPP](https://iapp.org/news/a/italy-s-dpa-reaffirms-ban-on-replika-over-ai-and-children-s-privacy-concerns))
- Separate training-data investigation opened same day
- Two main violations: no valid legal basis for processing user conversations; no meaningful age verification despite 18+ claim
- 2025–2026 follow-on enforcement: no *additional* individual fines yet on other AI-companion operators, but Italian Garante is now aggressively baseline-testing age-gating across the category

**Implication for v2**: The ebook-purchase-first funnel is an age-verification advantage. Every paying adult enters with a payment method and (for Amazon/Apple gateway flows) pre-verified account status. This materially *narrows* Replika's precedent exposure because the platform isn't a free-signup chatbot.

### 5.5 Content Moderation Landscape 2026

Post-AI-Dungeon, post-Character.AI, the category has converged on four table-stakes controls:
1. **Minor age assurance** at account level (Character.AI's Nov 2025 ban + age-assurance rollout as reference)
2. **Crisis-keyword interrupt** surfacing mental-health resources (CA SB 243 mandate)
3. **Author-approved canon** as the provenance claim (this is what v2 uniquely offers)
4. **Explicit AI disclosure** at session start (CA SB 243 for minors; EU AI Act Art. 50 for all)

California SB 243 (eff. Jan 1, 2026) — first US law specifically on AI companion chatbots for minors. Federal bipartisan Senate bill on minor-prohibition (unpassed but tracked). COPPA updates: Senate passed unanimously March 2026 raising coverage from under-13 to under-17 + targeted-ad prohibition + "eraser button" ([HeyOtto](https://www.heyotto.app/resources/ai-laws-protecting-kids-2026); [FTC Policy Statement Feb 25, 2026](https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-issues-coppa-policy-statement-incentivize-use-age-verification-technologies-protect-children)).

### 5.6 Estate IP Access Under Read-Only — Does the Door Open?

This is the single most consequential finding for v2 strategy. Under v1 (AI invents in-world content), no major estate will license. Under v2 (AI narrates only author-approved canon), the posture is materially different.

**Agatha Christie Estate (Agatha Christie Limited) — 2025 precedent**
BBC Maestro AI-Christie writing course launched April–May 2025 in partnership with the estate (head: James Prichard, great-grandson). Key structural terms the estate *insisted* on: **"all of the words spoken in the video had to come from Christie"** — authenticated by scholars from archival interviews, letters, writings ([Deadline](https://deadline.com/2025/04/bbc-making-ai-agatha-christie-1236381034/); [Hollywood Reporter](https://www.hollywoodreporter.com/business/digital/agatha-christie-writing-course-ai-bbc-maestro-1236204003/); [LitHub](https://lithub.com/an-unsettling-ai-agatha-christie-is-here-to-teach-you-how-to-write/)). **This is exactly the read-only principle.** Prichard: "skeptical at first," his prerequisites were "enough footage and authentic look," and the script "blew my brain away." The Christie estate has *operationally validated* the read-only pattern as acceptable.

**Tolkien Estate**
Appointed Curtis Brown Heritage Sept 2025 to handle all commercial partnerships/licensing/permissions ([The Tolkien Society](https://www.tolkiensociety.org/2025/09/tolkien-estate-appoints-curtis-brown-heritage/); [Wikipedia](https://en.wikipedia.org/wiki/Tolkien_Estate)). No public 2025–2026 statement specifically on AI. Historically most protective estate in fiction — but Curtis Brown Heritage appointment suggests structured licensing is now centrally managed. [UNVERIFIED] whether they'd entertain a read-only interactive offer; the appointment is a pro-commerce signal but silent on AI specifically.

**Frank Herbert Estate (Herbert Properties LLC)**
Legendary holds film/TV; Gale Force Nine holds tabletop; historically litigious on unofficial uses (Trident's enforcement against Second Life Dune RP, late-2000s; [New World Notes](https://nwn.blogs.com/nwn/2009/04/enforcers-of-dune.html)). No 2025–2026 AI statement located. [UNVERIFIED] — the estate's historical posture suggests it would require (a) pre-existing film/TV partner sign-off, (b) extremely tight canon definition, (c) likely exclusive-type terms.

**Ursula K. Le Guin Estate**
2026 Le Guin Prize for Fiction disqualifies undisclosed use of LLMs/"AI" in submitted works ([Ursula K. Le Guin](https://www.ursulakleguin.com/prize26)). Their *prize* policy is explicitly skeptical of AI in human works. This is a signal of estate-level reluctance to grant AI licenses over Le Guin canon — read-only probably does not open this door in the near term.

**Terry Pratchett Estate**
Active in canon management (controlled Good Omens Kickstarter post-Gaiman allegations — [For Reading Addicts](https://forreadingaddicts.co.uk/terry-pratchett-estate-issues-statement-regarding-the-future-of-good-omens/)) but no AI-specific public statement in 2025–2026 search results.

**Authors Guild 2025–2026 position**
AG actively working with AI companies on **licensed in-book chatbot and AI-enabled fan-fiction applications** where authors opt-in and receive additional income ([Authors Guild](https://authorsguild.org/news/statement-on-amazon-kindle-ask-this-book-ai-feature/); [AG AI Licensing](https://authorsguild.org/advocacy/artificial-intelligence/ai-licensing-what-authors-should-know/)). Explicitly critical of Amazon's "Ask This Book" (Dec 11, 2025) for being unlicensed and lacking opt-in. **[CURIOUS]** The Authors Guild is publicly pushing *toward* exactly the pattern v2 describes: opt-in, licensed, author-compensated interactive book experiences. They are a natural coalition partner for a v2 launch.

**Net assessment on estate IP access under read-only**
- Christie-class estates: **door is materially open** post-BBC Maestro precedent
- Tolkien-class estates: door is *probably unlocked but not yet open* — depends on specific partnership terms and Curtis Brown Heritage's posture
- Le Guin-class estates: door remains mostly closed short-term; these estates equate AI with inauthenticity
- Living authors (Sanderson, Scalzi, Riordan, Kingfisher, Novik): highest-probability Year-1 signatories because they can speak for themselves without estate committee overhead; Authors Guild advocacy gives them political cover

## TL;DR

- **The read-only refinement is architecturally different, not a branding tweak.** Risks that shrink massively: canon-generation liability, AI-invented-content moderation, author-IP-drift lawsuits (Bartz-class exposure). Risks that stay or grow: aggregation from Amazon/Microsoft, author acquisition cost, session-depletion for mature readers, minor-access regulation, retrieval-truth becomes a product defect not a side effect.
- **The Agatha Christie × BBC Maestro 2025 partnership is the single most important precedent.** The estate's operational insistence that "every word spoken must be Christie's own" is the read-only principle validated by a real estate in a real licensed production. A v2 platform with this structural constraint has a credible estate-pitch path that v1 did not.
- **Unit economics work on 2026 Gemini Flash-Lite / DeepSeek V3.2 class inference (~$0.006/session), break on Claude Opus class ($0.50/session).** The platform must be architected against the cheap-model tier from day one, not retrofit. The LLM cost curve is 9x–900x/year favorable depending on task.
- **Competitive gap is real and structurally hard for incumbents to close.** Character.AI can't pivot (UGC bots are their liability surface), AI Dungeon can't pivot (generative emergence is their value prop), Fable/Showrunner is multimodal, NovelAI is writer-side. The real competitive threat is a major publisher launching their own version — Amazon's Dec 2025 "Ask This Book" is the warning flare. Microsoft's Feb 2026 Publisher Content Marketplace *has zero trade-book publishers today* — this is a time-boxed opportunity.
- **The hardest problem is no longer canon defense — it is getting three A-list authors or one major estate signed to a retrieval-ready read-only license within 12 months.** This is a cold-start/BD problem that LLM cost declines do not solve and that no amount of engineering excellence resolves.

## DELTA vs V1

The read-only refinement is not a cosmetic tweak — it **materially changes the risk stack and the estate/author access conversation**, while leaving the business-side challenges largely intact.

Risks that **shrink** (meaningful): canon-invention liability, AI-Dungeon-style moderation disasters, Character.AI-class co-defendant exposure on invented in-world content, and Bartz v. Anthropic-class IP training exposure — because the platform now uses only licensed author corpora and never invents canon. The Agatha Christie × BBC Maestro precedent (estate insisted every word be Christie's own) is a direct operational match for the v2 architecture and flips the estate-licensing conversation from "almost impossible" to "precedented and defensible."

Risks that **stay or grow**: author acquisition cost (now *higher* because the 2K-page retrieval-structured canon is a heavier authoring lift than an ebook), aggregation risk from Amazon/Microsoft (possibly *higher* because the read-only scope maps more directly onto their owned ebook corpus), and retrieval-accuracy-as-product-defect (new category — under v1 drift was a quirk, under v2 it is the only thing the product promises).

Risks that are **new**: session-depletion for high-engagement readers (a finite canon can be exhausted in a way an unbounded-generative world cannot), prompt-injection canon-exfil (a targeted adversary extracts licensed canon verbatim, creating a copyright breach on the author's behalf), and the author-side UX problem of producing retrieval-ready structured bibles at scale.

**The v1 hardest problem ("defend canon against drift + adversarial prompting at viable cost") is no longer the hardest problem.** Under v2 the hardest problem shifts to **author/estate acquisition and canon-production UX** — a cold-start BD problem with a 6–18 month lead time that neither inference-cost declines nor retrieval-architecture advances resolve.

**Conclusion that flips vs v1**: Estate-licensed canon (Tolkien, Christie, Herbert-class) goes from "almost impossible in the AI era" in v1 to "demonstrably possible with the right architectural constraint" in v2. The Christie estate's BBC Maestro terms are the key unlock that a reader, a regulator, and an estate committee can all point to as a precedent that isn't Character.AI and isn't Anthropic. That is a materially different go-to-market than v1.
