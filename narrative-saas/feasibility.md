# FEASIBILITY RESEARCH

## 1. MARKET SIZE

### Adjacent Markets (2025, sourced)

| Market | 2025 Size | Source |
|---|---|---|
| Global ebooks | $14.9B (Statista) to ~$18–26B (others) | [Statista](https://www.statista.com/forecasts/1294207/ebook-market-revenue-worldwide), [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/e-book-market) |
| Interactive fiction games | $4.3B projected → $7.8B by 2032 (CAGR 12%) | [Intel Market Research](https://www.intelmarketresearch.com/interactive-fiction-game-market-21560) |
| Tabletop RPG (TTRPG) | ~$2.15B → $6.59B by 2035 (CAGR 11.84%) | [Industry Research](https://www.industryresearch.biz/market-reports/tabletop-role-playing-game-ttrpg-market-105312) |
| AI companion apps (revenue) | $82M H1 2025, on track for $120M+ full year (+64% YoY) | [RoboRhythms](https://www.roborhythms.com/ai-companion-app-market-2026/) |
| AI companion / emotional AI market | $37.1B in 2025 [UNVERIFIED — wide variance across reports] | [Precedence Research](https://www.precedenceresearch.com/ai-companion-market) |
| Creator economy (total) | $178B–$254B in 2025 (sources vary widely) | [Market.us](https://market.us/report/creator-economy-market/), [Precedence Research](https://www.precedenceresearch.com/creator-economy-market) |

### Venn Placement

The proposed concept sits at the intersection of **ebook publishing × interactive fiction × AI companion/chatbot**. None of those markets individually is the right TAM. The most honest framing:

- **Realistic SAM**: The overlap of ebook readers who already pay for narrative subscription experiences (Kindle Unlimited, Audible, Scribd/Everand) AND who have tolerance for AI-mediated interaction. Kindle Unlimited has an estimated 3–5M subscribers globally [UNVERIFIED — Amazon does not disclose]; Audible has ~5M paying members in the U.S. [UNVERIFIED precise number]. A reasonable realistic initial target is the crossover of "literary fiction reader" + "paid for an AI app in 2024–25," likely in the **1–3M addressable user range in English-speaking markets**.
- **Realistic TAM (mature)**: If the category matures to ~10% of AI companion app revenue plus ~2% of ebook revenue, that's ~$300–500M/year globally by 2030 [UNVERIFIED — projection].
- [CURIOUS] **AI companion revenue is growing at 64% YoY while ebook revenue is flat-to-declining in the U.S.** That growth differential is the structural tailwind the concept rides — but the concept has to actually convert *book readers* (a flat market) into *AI-using readers* (a growing one). That crossover is the entire thesis.

### Growth Trajectory

- LLM inference costs are **declining ~10× per year** — GPT-4-class performance went from $20 per 1M tokens (late 2022) to ~$0.40 per 1M tokens by 2025. [Silicon Data](https://www.silicondata.com/blog/llm-cost-per-token)
- This trend favors the unit economics of long-session narrative experiences that were unaffordable at 2022 prices. [CURIOUS]
- Offsetting: **KV cache scaling is the hidden cost**. One concurrent user with a 32K-token context has a cache "approaching the size of the model weights themselves," and doubling context halves concurrent user density. [Silicon Data](https://www.silicondata.com/blog/llm-cost-per-token) This is directly adverse to long-canon narrative sessions — the exact thing this product needs to do well.

---

## 2. COMPETITIVE LANDSCAPE

### Direct Competitors — AI + Narrative

| Company | Scale (2025) | Model | Gap vs. proposed concept |
|---|---|---|---|
| **AI Dungeon (Latitude)** | Peaked at 1.5M MAU in Feb 2021; removed from Steam March 2024; only $3.3M in disclosed funding (2021 seed, NFX) | User-generated scenarios, GPT-family models | **No licensed author IP, no canon governance, no royalty layer.** Content moderation meltdown of 2021 damaged trust permanently. [TechCrunch](https://techcrunch.com/2021/02/04/latitude-seed-funding/), [Wikipedia](https://en.wikipedia.org/wiki/AI_Dungeon) |
| **Character.AI** | Peak 28M MAU mid-2024, ~20M in 2025; $50M revenue 2025 (+66% YoY); Google paid $2.7B in Aug 2024 for license + acqui-hire of founders | User-created character chatbots | **No narrative arc, no ebook, no canon ownership model.** Now under severe legal/safety pressure (see §5). [Business of Apps](https://www.businessofapps.com/data/character-ai-statistics/), [Deep Learning AI](https://www.deeplearning.ai/the-batch/google-acquires-character-ai-talent-and-tech-in-strategic-move/) |
| **NovelAI** | Self-funded since 2021; $10–25/mo tiers; user counts undisclosed | AI-assisted authorship + anime image gen | **Tool for writers, not a consumer reading experience. No licensed IP.** [Crunchbase](https://www.crunchbase.com/organization/novelai) |
| **Inworld AI** | $125.7M raised through June 2025, $500M valuation; Xbox + Ubisoft partnerships | B2B AI NPC infrastructure | **B2B infrastructure, not a direct-to-reader product. Doesn't license author IP.** [Inworld](https://inworld.ai/blog/inworld-valued-at-500-million), [GamesBeat](https://gamesbeat.com/inworld-ai-raises-new-round-at-500m-valuation-for-ai-game-characters/) |
| **Replika (Luka Inc.)** | 30M+ users (Aug 2024); $24M revenue 2024; fined €5M in Italy 2025 | AI companion / relationship sim | **Not narrative. Hit hard by EU enforcement; shows regulatory ceiling for this category.** [Library of Congress](https://www.loc.gov/item/global-legal-monitor/2025-09-04/italy-italian-authorities-sanction-maker-of-replika-chatbot-for-inadequate-protections), [EDPB](https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en) |
| **Sudowrite** | "Advanced" tier at $499/mo; Story Engine product | Author-facing tool | **Producer-side. Not a reader product.** [Sudowrite](https://sudowrite.com/pricing) |

### Adjacent Competitors — Interactive Fiction / Narrative Games

| Company | Scale / Model | Why they're not the same thing |
|---|---|---|
| **Choice of Games / Hosted Games** | 25% royalty to authors on Hosted titles; $10K–15K advances on CoG flagship titles | Deterministic branching script (ChoiceScript), not LLM. Pre-authored; no emergent canon defense. [Choice of Games](https://www.choiceofgames.com/looking-for-writers/write-a-hosted-game/) |
| **inkle Studios** (80 Days, Heaven's Vault) | 80 Days: TIME GotY 2014; Heaven's Vault estimated ~$391K gross on Steam [third-party data — [SteamRevenueCalculator](https://steam-revenue-calculator.com/app/774201/heaven's-vault)] | Scripted narrative + `ink` scripting language. No LLM; no licensed-world marketplace. |
| **Failbetter Games** (Fallen London) | Independent, self-funded; new Mandrake title announced June 2025 | Single-studio IP, no platform model. [Failbetter](https://www.failbettergames.com/) |
| **Roll20** | ~$16.4M earnings bracket [UNVERIFIED precise], 70% creator royalty | Tabletop VTT; human GM still required. No AI delivery of canon. [Roll20 Partners](https://pages.roll20.net/partners) |

### Where Every Competitor Stops Short

No existing player has assembled the **four-way combination** the proposed concept requires:
1. **Licensed, professionally-authored story bibles** (Character.AI has user-gen; Choice of Games is authored but scripted, not LLM)
2. **LLM-delivered interactive experience** (AI Dungeon has LLM, but no canon)
3. **Canon governance / narrative arc enforcement** (nobody solves this — it's the hardest open problem in the category)
4. **Ebook-plus-subscription commerce with ongoing author royalties** (Kindle Unlimited has the commerce, but no interactivity)

The defensible differentiator, if the product can be built, is **canon governance** — the "AI holds the canon, reader meanders freely but is guided back." No LLM product in market does this well today.

---

## 3. ANALOGUES AND PRECEDENTS

### Kindle Unlimited (KU) — "platform monetizes reading, pays authors per page"

- **Payout model**: KENP rate in Sept 2025 = **$0.004521 per page read**. A 300-page book read fully pays the author ~$1.36. [BookBloom](https://www.bookbloom.io/tools/kenp-calculator), [Written Word Media](https://www.writtenwordmedia.com/kdp-global-fund-payouts/)
- **Global fund structure**: Amazon allocates a monthly fund (typically $30–40M) divided by total KENP reads — rate fluctuates monthly. [Kindle Unlimited Payout](https://www.automateed.com/kindle-unlimited-payout)
- **What held**: Authors tolerate the model because of Amazon's scale. Pay-per-unit-consumed model is now a default consumer expectation for bundled content.
- **What broke**: Perpetually erodes per-page rate as supply grows. Strong incentive to game the system (bonus chapters, fake page counts) requiring ongoing policy policing. Authors routinely complain the rate is below sustenance.
- **Lesson for proposed concept**: A "pay-per-play-session" or "pay-per-scene" model will replicate KU's dynamic — worlds that attract whale readers dominate; the long tail of authors earns near-zero. **Budget for a rate-fluctuation war.**

### Spotify — "platform licenses content, pays per stream"

- **Music per-stream**: $0.003–$0.005 per stream (2025). [Vocal Media](https://vocal.media/beat/how-much-spotify-pays-per-stream-in-2025-real-numbers-explained)
- **Podcast creator payouts**: $100M in Q1 2025 alone; Partner Program pays 50% of ad revenue to creators. [Spotify Newsroom](https://newsroom.spotify.com/2025-04-28/from-audio-to-video-spotifys-100-million-payout-fuels-creator-success-stories/)
- **What held**: Spotify made subscription audio default. A flat-fee, unlimited-access model was viable at scale.
- **What broke**: Artist revolt over per-stream rates; Rogan and podcasting shifted to revenue-share instead. [CURIOUS] **Podcasts moved from flat-license (Spotify paid $200M+ for Rogan) to 50% ad share — the market *converged* on revenue share once scale was known.** Proposed concept starts with revenue share — that's correct positioning.

### Audible Originals / ACX

- **Exclusive rate**: 40% (recently raised to 50%). Non-exclusive: 25% (recently 30%). [ACX blog](https://www.acx.com/mp/blog/audibles-new-royalty-model-early-access-successes), [Audible](https://www.audible.com/about/newsroom/audibles-new-royalty-model-more-opportunities-for-authors-and-publishers)
- **Lesson**: Exclusivity premium is ~20 percentage points. The proposed concept will face the same tradeoff — authors will demand non-exclusive rights to publish ebooks elsewhere, and the platform will have to choose.

### Roll20 Marketplace

- **70% creator royalty** — notably high. [Roll20 Partners](https://pages.roll20.net/partners)
- **Reality for creators**: One forum thread cites a creator who'd need ~574 customers with "$100 over 3 years" buying habits to hit a living wage. One creator reportedly quit their day job Aug 2025 to do Roll20 maps full-time. [Roll20 Forum](https://app.roll20.net/forum/post/3921772/marketplace-creators-what-has-your-experience-been)
- **Lesson**: Even at 70%, narrow niche plus long tail means few creators reach sustenance. The proposed concept's author-royalty promise needs to model top-1% / top-10% / median earnings *before* pitching to established authors.

### Wattpad → Naver / Webtoon

- **$600M acquisition (2021)** of Wattpad by Naver; combined audience ~166M MAU. [Variety](https://variety.com/2021/digital/asia/wattpad-acquired-600-million-naver-webtoon-1234888216/)
- **$2.8B paid to creators 2021–2025** across fees, IP licensing, advertising. [Korea Herald](https://www.koreaherald.com/article/10696220)
- **[CURIOUS]** Webtoon Q4 reported a **363.2B KRW (~$260M) impairment charge on Wattpad** — indicating the parent believes significant value has been destroyed post-acquisition. The UGC-to-IP-factory thesis has under-delivered financially even at massive scale.
- **Lesson**: UGC-at-the-front, licensed-IP-at-the-back is a two-sided market with painful economics. Platform's proposed model is more similar to **already-licensed IP at the front**, which is closer to Audible Originals than Wattpad — but misses the free user-acquisition flywheel UGC provides.

### Quibi — what failure looks like

- **$1.75B raised**, shut down 6 months post-launch. **92% of users left** after free trial. [Failory](https://www.failory.com/cemetery/quibi), [How They Grow](https://www.howtheygrow.co/p/why-quibi-died-the-2b-dumpster-fire)
- **Applicable lesson**: Format-forward, premium-priced, celebrity-stacked content bet failed because the *use case wasn't real*. The proposed concept needs to answer: **what specifically is the book reader doing differently than just reading the book?** If the answer is "same thing but slower and more expensive," this fails the Quibi test.

### AI Dungeon — near-miss precedent for the model itself

- **93% decline in downloads** April–July 2021 over content moderation policy. 177K Reddit posts/comments of backlash in a 3-month window. [Toolify](https://www.toolify.ai/ai-news/the-controversy-surrounding-ai-dungeon-unveiling-the-drama-2487420)
- **[CURIOUS]** AI Dungeon was the closest commercial product to this concept, and its near-extinction event was entirely regulatory/platform-policy-driven, not technical. **The content moderation question is existential, not operational.**

---

## 4. RISK ASSESSMENT

### Top 5 Business Risks (ranked)

1. **Content moderation creates binary platform risk.** AI Dungeon lost 93% of downloads in 3 months over this; Character.AI faces active wrongful-death litigation and a settlement with Google in Jan 2026. [CNN](https://www.cnn.com/2026/01/07/business/character-ai-google-settle-teen-suicide-lawsuit) A licensed-IP platform has *amplified* liability because content is authored-world + AI-improvised + consumer-input; the chain of responsibility is a plaintiff's dream.
2. **Unit economics don't close at long context.** KV cache costs scale per user per session; a 32K-token narrative context for a "long novel" interactive session makes concurrent user density collapse. [Silicon Data](https://www.silicondata.com/blog/llm-cost-per-token) Subscription pricing has to absorb inference cost while still leaving enough for author royalty splits. At $10/mo subscription, author share X%, LLM share Y%, payment processing Z%, marketing W% — the margin is very thin even with falling token prices.
3. **Two-sided market cold start.** Need readers to justify author licensing; need authors to justify reader acquisition. Audible and KU succeeded because Amazon had pre-existing reader scale. A standalone startup does not.
4. **Author IP holders will not move early.** Estates (Tolkien, Herbert) have historically refused restrictive licensing; the Tolkien Estate forbids all derivative fanworks and has enforced aggressively. [Silmarillion Writers' Guild](https://www.silmarillionwritersguild.org/node/5391) Estates with brand risk to protect will say no at first. Early-career or mid-list authors become the only realistic supply side for launch — which means the platform's library starts weak.
5. **Book-reader willingness-to-pay for AI experiences is unproven.** Character.AI converted ~20M MAU to only $50M annual revenue — that's ~$2.50 per user per year, and those are already AI-native users. [Sacra](https://sacra.com/c/character-ai/) Book readers tend to skew older and more skeptical of AI. Conversion rates may underperform the AI-companion baseline.

### Top 3 Technical Risks

1. **Canon integrity over long sessions.** LLMs "forget previous rooms" as context fills; hallucination rate increases with session length. [Cuckoo AI Network](https://cuckoo.network/blog/2025/04/17/negative-feedback-on-llm-powered-storytelling-and-roleplay-apps) Retrieval-augmented canon works for encyclopedic facts but not for "did this character already meet this person in this session." Narrative arc enforcement is an unsolved research problem.
2. **Arc-guidance vs. freedom tension.** Readers either feel railroaded (bad) or drift into incoherence (also bad). The "meanders freely but is guided back" promise has no production-proven implementation.
3. **Adversarial user testing.** Users will attempt jailbreaks to produce content outside canon (explicit, impersonation, violence involving licensed characters). Every mitigation degrades the creative-freedom value prop. [AI Dungeon content moderation history](https://help.aidungeon.com/faq/how-does-content-moderation-work)

### The Single Hardest Problem (one sentence)

**Defending the canon of a licensed world against an LLM's own drift and a determined user's adversarial prompting — simultaneously — over a multi-hour session, while keeping per-session inference costs below a subscription price that book readers will actually pay.**

---

## 5. REGULATORY AND IP CONSIDERATIONS

### Copyright Status of AI-Generated Derivative Content

- **Prompts alone do not confer copyright** on AI output (U.S. Copyright Office, 2025 Part 2 report). [Copyright.gov](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)
- Copyright attaches to AI output only where a **human author has determined sufficient expressive elements** or a human-authored work is perceptible in the output. [McGuireWoods](https://www.mcguirewoods.com/client-resources/alerts/2025/9/copyright-and-generative-ai-recent-developments-on-the-use-of-copyrighted-works-in-ai/)
- **Implication for proposed concept**: The "AI-delivered session" is a derivative work of the licensed bible. Whether the *session transcript itself* is copyrightable is unclear — and whether the *reader* or *platform* or *author* holds rights to it is even less clear. **This needs to be contracted explicitly**; the default is legal ambiguity.

### Bartz v. Anthropic and the Training-Data Question

- **June 2025 ruling**: Training an LLM on copyrighted books was **fair use** (transformative purpose). However, **downloading pirated books was not fair use**. [Mid-Year Review: Copyright Alliance](https://copyrightalliance.org/ai-copyright-case-developments-2025/)
- **September 2025**: Anthropic agreed to pay **$1.5 billion** to settle the pirated-books claim — the largest copyright settlement in U.S. history. [Authors Guild](https://authorsguild.org/advocacy/artificial-intelligence/what-authors-need-to-know-about-the-anthropic-settlement/)
- **Implication**: Using a third-party LLM (Anthropic, OpenAI) to deliver licensed narrative content creates a **supply-chain provenance question**. If the platform's underlying LLM was trained on pirated material, does licensing the specific author's bible "cleanse" it? **No existing case law resolves this.** Licensed authors will want indemnification — which platform probably cannot fully provide.

### Liability When AI Goes Off-Canon / Harmful Content

- **Character.AI precedent is severe**: Sewell Setzer III, 14, died by suicide in Feb 2024 after extended interaction with a Character.AI chatbot modeled on a *Game of Thrones* character. The mother's October 2024 lawsuit alleged the platform failed to implement proper safety measures. [CNN](https://www.cnn.com/2024/10/30/tech/teen-suicide-character-ai-lawsuit)
- **January 2026**: Google and Character.AI settled that lawsuit. [JURIST](https://www.jurist.org/news/2026/01/google-and-character-ai-agree-to-settle-lawsuit-linked-to-teen-suicide/)
- **Additional suits**: Texas families (Dec 2024) alleged chatbots encouraged self-harm; Colorado suit (Sept 2025) from 13-year-old's family. [Social Media Victims Law Center](https://socialmediavictims.org/character-ai-lawsuits/)
- **Who is on the hook in the proposed model**? **All three** (platform, author, LLM provider) — plaintiffs will sue every deep-pocket defendant. The author who licensed the world is now co-defendant for any harmful session. **This alone may kill author supply from established names.** [CURIOUS]

### Replika / EU Enforcement Precedent

- **Italian DPA fined Replika €5M in April 2025** for unlawful processing, transparency failures, inadequate age verification. [EDPB](https://www.edpb.europa.eu/news/national-news/2025/ai-italian-supervisory-authority-fines-company-behind-chatbot-replika_en)
- Initial block imposed Feb 2023; 2.5-year enforcement cycle. [IAPP](https://iapp.org/news/a/italy-s-dpa-reaffirms-ban-on-replika-over-ai-and-children-s-privacy-concerns)
- **Implication**: EU market entry requires robust age-gating, GDPR-compliant data processing, and proactive minor protection. The fine amount (~$5.5M) is "cost of doing business" for a well-funded platform but catastrophic for a startup.

### Content Moderation Landscape for AI-Generated Fiction

- **No consensus exists**. AI Dungeon's 2021 moderation policy destroyed 93% of its user base; its 2022 reversal to "unpublished single-player content is never moderated" solved trust but amplifies liability when a bad case reaches court. [AI Dungeon Help](https://help.aidungeon.com/faq/how-does-content-moderation-work)
- **Sexually explicit content**: OpenAI/Anthropic APIs reject it; running uncensored models requires self-hosted infrastructure (cost explosion). Many AI Dungeon defectors moved to NovelAI and local-model alternatives specifically for this — adult-fiction demand is real, unmet, and legally hazardous.
- **Impersonation of real persons in licensed worlds**: If the licensed bible references real historical figures (common in historical fiction), every such reference becomes a defamation/right-of-publicity exposure surface.

### Estate-Managed IP

- **Tolkien Estate**: Publicly opposed to fanworks. "Publishing fan-fiction for personal or commercial purposes, even online, is absolutely not authorized." [Tolkien Estate](https://www.tolkienestate.com/frequently-asked-questions-and-links/)
- **Middle-earth Enterprises** (separate entity, owns film/derivative rights) licenses extensively — so there is a precedent for structured licensing distinct from the author's estate. [Wikipedia](https://en.wikipedia.org/wiki/Middle-earth_Enterprises)
- **Implication**: The proposed concept is effectively **impossible to launch with estate-held legacy IP**. Supply side must be **living authors with unencumbered IP** — which means the platform must either recruit mid-list / emerging authors, or become a publisher of new worlds built for the platform (which is what the "new-author publishing program" in the brief implies). That's the structurally correct move.

---

## TL;DR

- **Structural tailwind is real**: AI companion app revenue +64% YoY, LLM inference cost declining 10× annually, interactive fiction market $4.3B and growing 12% CAGR — but the concept has to convert *book readers* (flat market) into *AI-using readers* (growing market), and that crossover is unproven.
- **No competitor combines all four pillars** (licensed bible + LLM delivery + canon governance + ebook-plus-subscription commerce). Defensibility comes from canon governance, which is also the hardest unsolved technical problem in the category.
- **Regulatory/liability exposure is existential, not incidental**: Character.AI's wrongful-death settlement (Jan 2026), Replika's €5M Italian fine (April 2025), AI Dungeon's 93% download collapse (2021), Anthropic's $1.5B copyright settlement (Sept 2025) — this product's legal surface stacks *all* of these risk categories on top of each other, with the licensed author now as co-defendant.
- **Author supply starts weak**: Estates (Tolkien-class) will refuse; only path to launch is living mid-list authors and a new-author publishing arm. Plan for Kindle-Unlimited-style long-tail economics — top 1% of worlds earn most of the royalties, the median licensor earns very little.
- **Single hardest problem**: Defending the canon against LLM drift and adversarial prompting over multi-hour sessions while keeping per-session inference cost below a subscription price book readers will pay. Everything else is tractable. This one is not yet solved in any production system.
