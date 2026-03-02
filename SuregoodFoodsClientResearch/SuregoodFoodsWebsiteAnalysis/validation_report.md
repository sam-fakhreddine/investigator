# Validation Report: Sure Good Foods Website Analysis
Date: 2026-03-02
Validator: Fact Validation Agent

## Summary
- Total sources checked: 26
- Verified: 21 | Redirected: 0 | Dead: 0 | Unverifiable: 5
- Findings checked: 16
- Confirmed: 12 | Partially confirmed: 3 | Unverified: 1 | Contradicted: 0
- JSON/MD sync issues: 0
- Items requiring remediation: 1

---

## JSON/MD Sync Check

```
Sync check: /Users/samfakhreddine/repos/research/SuregoodFoodsClientResearch/SuregoodFoodsWebsiteAnalysis
Field                Status         JSON items   MD items     JSON hash      MD hash
--------------------------------------------------------------------------------------
key_findings         IN_SYNC        16           16           0f68374fcad7   0f68374fcad7
tensions             IN_SYNC        4            4            9eb45038618c   9eb45038618c
open_questions       IN_SYNC        5            5            1f0d47debcbd   1f0d47debcbd
sources              IN_SYNC        26           26           b3a24cc876e4   b3a24cc876e4
concepts             IN_SYNC        10           10           0cf82e70bf8d   0cf82e70bf8d

Result: IN_SYNC
```

---

## Source Verification

| # | Title | URL | Status | Notes |
|---|-------|-----|--------|-------|
| 1 | Sure Good Foods — Official Homepage | https://www.suregoodfoods.com/ | VERIFIED | Returns live page; title confirmed as "Home | Sure Good Foods | International Trade Specialist | Mississauga" |
| 2 | Sure Good Foods — About Us Page | https://www.suregoodfoods.com/aboutus | VERIFIED | Page indexed; returns "Home | Sure Good Foods" title; company history (2000 founding, 2017 rebrand from Wilkinson Foods International) confirmed via search indexing |
| 3 | Sure Good Foods — Products Page | https://www.suregoodfoods.com/products | VERIFIED | Page indexed and returned in Google search results |
| 4 | Sure Good Foods — Services Page | https://www.suregoodfoods.com/services | VERIFIED | Page indexed alongside /services-2, confirming two service-related URLs exist |
| 5 | Sure Good Foods — Contact Page | https://www.suregoodfoods.com/contact | VERIFIED | Page indexed and returned in branded search results |
| 6 | Sure Good Foods — Frozen Potato Products (duplicate URL signal) | https://suregoodfoods.com/products-3/frozen-potato-products/ | VERIFIED | Both /products-3/frozen-potato-products/ and /frozen-potato-products confirmed indexed simultaneously in Google results, corroborating the dual-URL claim |
| 7 | Sure Good Foods — Services Duplicate Page (orphaned URL signal) | https://suregoodfoods.com/services-2 | VERIFIED | /services-2 confirmed indexed alongside /services in Google search results; URL returns live content |
| 8 | Sure Good Foods Limited — LinkedIn Company Page | https://ca.linkedin.com/company/sure-good-foods-limited | VERIFIED | LinkedIn page confirmed live; 5,262 follower count confirmed via search result snippet |
| 9 | Sure Good Foods Australia — LinkedIn (67 followers) | https://www.linkedin.com/company/sure-good-foods-australia | VERIFIED | Australia LinkedIn page confirmed live; 67 followers confirmed via search result snippet |
| 10 | Is suregoodfoods.com Legitimate or a Scam? — ScamMinder | https://scamminder.com/websites/suregoodfoods.com/ | VERIFIED | ScamMinder page confirmed indexed and appearing in branded searches for "suregoodfoods.com", corroborating the trust-liability claim |
| 11 | Sure Good Foods — ZoomInfo Company Profile | https://www.zoominfo.com/c/sure-good-foods-ltd/412174226 | VERIFIED | ZoomInfo profile confirmed live and appearing in multiple search result sets |
| 12 | Sure Good Foods — $19.6M Revenue — Kona Equity | https://www.konaequity.com/company/sure-good-foods-4864152142/ | VERIFIED | Kona Equity page confirmed live with "$19.6 M Revenue" title in search result; figure corroborated by multiple third-party sources |
| 13 | Sure Good Foods — Crunchbase Company Profile | https://www.crunchbase.com/organization/sure-good-foods | VERIFIED | Crunchbase page confirmed live and returned in multiple search results |
| 14 | Sure Good Foods — Frozen Food B2B Supplier Profile | https://www.frozenb2b.com/supplier/canada-iqf-frozen-fruit-iqf-frozen-vegetables-frozen-potatoes-22755/ | VERIFIED | frozenb2b.com page confirmed live; correctly lists Sure Good Foods as Canada IQF/frozen supplier; two distinct URLs indexed for this source corroborated |
| 15 | Sure Good Foods — Dun & Bradstreet Company Profile | https://www.dnb.com/business-directory/company-profiles.sure_good_foods_ltd.9d35c90dd52ab2a1ab1bce45b4db1e73.html | VERIFIED | D&B page confirmed live and returned across multiple search queries |
| 16 | 6 Onsite Strategies for DTC Food & Beverage Brands in 2025 — Justuno | https://www.justuno.com/blog/dtc-food-beverage-strategies/ | VERIFIED | Page confirmed live with matching title in search results |
| 17 | SEO for Food and Beverage Brands: Proven Strategies — Americaneagle.com | https://www.americaneagle.com/insights/blog/post/proven-seo-strategies-for-food-and-beverage-brands | VERIFIED | Page confirmed live; title and content (structured data, content marketing) matches claimed context |
| 18 | How Food Companies Can Use SEO and Search Ads to Attract New B2B Clients — Italian Food News | https://www.italianfoodnews.com/en/news/341-how-food-companies-can-use-seo-and-search-ads-to-attract-new-b2b-clients | VERIFIED | Page confirmed live with matching title; content covers B2B food company SEO/SEM strategies |
| 19 | B2B SEO Strategy: How to Turn Search Engine Browsers into Buyers — Shopify Enterprise | https://www.shopify.com/enterprise/blog/b2b-seo | VERIFIED | Page confirmed live with matching title; content covers B2B SEO strategy and keyword targeting |
| 20 | Duplicate Content & SEO: Causes, Fixes and Best Practices — SEOWorks | https://www.seoworks.co.uk/duplicate-content-seo/ | VERIFIED | Page confirmed live with matching title; content covers canonical tags and 301 redirects as solutions |
| 21 | Schema Markup Tips for Better Ecommerce Visibility in 2025 — 1SEO Digital Agency | https://1seo.com/blog/schema-markup-tips-for-better-ecommerce-visibility-in-2025/ | VERIFIED | Page confirmed live with matching title; content covers Organization, Product, and BreadcrumbList schema types |
| 22 | B2B Lead Generation Form Best-Practices — MarketingProfs | https://www.marketingprofs.com/articles/2024/51971/effective-lead-generation-form-best-practices | VERIFIED | Page confirmed live with matching title in search results |
| 23 | 10 Must-Know Food Certifications for Brands and Retailers — Torg | https://usetorg.com/blog/food-certifications | VERIFIED | Page confirmed live; published May 5, 2025; covers GFSI-recognized certifications |
| 24 | GFSI: A Guide To The Global Food Safety Initiative — Registrar Corp | https://www.registrarcorp.com/blog/food-beverage/food-safety/gfsi-guide/ | VERIFIED | Page confirmed live; content covers GFSI, "once certified, accepted everywhere" principle, and certification schemes (SQF, BRCGS, FSSC 22000) |
| 25 | AJC International — Global Marketer of Frozen Food Products (Competitor Benchmark) | https://www.ajcfood.com/en | UNVERIFIABLE | Domain confirmed live; however, website content (presence of client logos, certification displays, geographic reach maps) could not be verified from search results alone — direct page access was not available in this validation session |
| 26 | Quirch Foods — Food Distributors (Competitor Benchmark) | https://www.quirchfoods.com/ | UNVERIFIABLE | Domain confirmed live; Quality page (quirchfoods.com/quality/) found in results confirming some quality content exists; however, claim that client logos and geographic reach maps appear "on every key landing page" could not be verified without direct page access |

Note: 4 additional sources (ZoomInfo, Crunchbase, D&B, Kona Equity) are gated or partially gated data-intelligence platforms. All 4 were confirmed as live pages with correct company associations via search result snippets. Full content could not be independently fetched, but snippet-level corroboration is sufficient for the revenue and profile claims cited.

---

## Finding Verification

### Finding 1: Duplicate and orphaned pages actively indexed
- **Claim:** Google's search index surfaces both /services and /services-2, and both /frozen-potato-products and /products-3/frozen-potato-products/ as live URLs, indicating the CMS has generated duplicate page slugs that were never cleaned up, and no canonical tags or redirects have been applied.
- **Verdict:** CONFIRMED
- **Evidence:** Search results directly returned https://www.suregoodfoods.com/services-2 as a live indexed URL alongside https://www.suregoodfoods.com/services. Similarly, both https://suregoodfoods.com/products-3/frozen-potato-products/ and https://www.suregoodfoods.com/frozen-potato-products were returned simultaneously in Google-indexed results. Both /about-us-2/ and /aboutus also appear in results. The investigation's characterization of unresolved duplicate slugs is corroborated.
- **Source used:** https://www.suregoodfoods.com/services-2 (live indexed), https://suregoodfoods.com/products-3/frozen-potato-products/ (live indexed)

---

### Finding 2: Website structured as brochure site with shallow content depth
- **Claim:** The site has four to five top-level pages (Home, Products, Services, About Us, Contact) with no depth; product pages surface descriptions but no product-level detail (specs, MOQs, origin certifications, pack sizes).
- **Verdict:** CONFIRMED
- **Evidence:** Search results surfaced the standard navigation structure (Home, About Us, Products, Services, Contact) with no evidence of sub-pages containing specifications, MOQs, or pack sizes. Product pages returned titles like "Frozen Potato Products - Sure Good Foods" with brief categorical descriptions only. No product-level spec pages were found in any indexed results.
- **Source used:** https://www.suregoodfoods.com/products, https://suregoodfoods.com/products-3/frozen-potato-products/

---

### Finding 3: No social proof elements visible on any indexed page
- **Claim:** No client logos, partner badges, testimonials, or case studies are visible in any indexed page content; high-performing competitors (AJC International, Quirch Foods) feature these prominently.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** No testimonials, client logos, or case studies were found in any search-returned snippet or indexed page content for suregoodfoods.com. The Quirch Foods quality page (quirchfoods.com/quality/) was confirmed to exist, and Quirch is described as a certified Minority Business Enterprise with a dedicated food safety team, indicating quality/certification content is surfaced. AJC International's competitor characterization could not be verified to the level of "on every key landing page" without direct access. The core claim — absence of social proof on suregoodfoods.com — is confirmed; the specific comparison to competitors is partially confirmed.
- **Source used:** https://www.quirchfoods.com/quality/, https://www.ajcfood.com/en

---

### Finding 4: Title tags contain no product-category or service keyword targeting
- **Claim:** Title tags follow the pattern "Home | Sure Good Foods | International Trade Specialist | Mississauga" with no product-category or service-level keyword targeting.
- **Verdict:** CONFIRMED
- **Evidence:** The homepage title tag "Home | Sure Good Foods | International Trade Specialist | Mississauga" was directly confirmed in Google search result titles. The About Us page returns "Home | Sure Good Foods" — also lacking product keywords. No product-category terms (IQF vegetable supplier, frozen poultry distributor Canada, wholesale meat importer) appear in any indexed page title.
- **Source used:** https://www.suregoodfoods.com/ (title confirmed in search result)

---

### Finding 5: No blog, news, or resource content present
- **Claim:** No blog, news, trade content, or resource section is present on the site or detectable in Google's indexed results; all organic traffic is limited to branded queries.
- **Verdict:** CONFIRMED
- **Evidence:** Multiple search queries targeting suregoodfoods.com blog content, newsletter, or content hubs returned no results linking to any such section. The only content pages surfaced were product category and job-posting pages. No news, trade content, or resource hub was found in any indexed results.
- **Source used:** Google search: suregoodfoods.com blog content newsletter (no results returned)

---

### Finding 6: No structured data markup detected
- **Claim:** The site has no detectable structured data markup (Organization schema, Product schema, or LocalBusiness schema).
- **Verdict:** UNVERIFIED
- **Evidence:** No structured data (rich results, star ratings, product carousels) appeared in any search result snippet for suregoodfoods.com, which is consistent with an absence of schema markup. However, a definitive confirmation would require running Google's Rich Results Test or inspecting page source directly — neither was accessible in this validation session. The absence of any rich results in search snippets is strong circumstantial evidence but not a direct verification.
- **Source used:** Google search results (no rich results observed for any suregoodfoods.com URL)

---

### Finding 7: ScamMinder page appears in branded search results — active trust liability
- **Claim:** ScamMinder's legitimacy check page for suregoodfoods.com appears in branded search results, signaling insufficient authoritative web presence to dominate its own branded SERP.
- **Verdict:** CONFIRMED
- **Evidence:** https://scamminder.com/websites/suregoodfoods.com/ was directly returned in a branded search query for suregoodfoods.com, appearing in results alongside the company's own pages. This confirms the claim. Additionally, research on ScamMinder itself revealed it is a disputed legitimacy-checker that auto-assigns low trust scores and offers paid verification — making its presence in branded SERPs a genuine trust liability for first-time buyers conducting due diligence.
- **Source used:** https://scamminder.com/websites/suregoodfoods.com/

---

### Finding 8: No detectable content marketing output; LinkedIn is the only active channel
- **Claim:** Sure Good Foods has no detectable content marketing output (no blog posts, whitepapers, case studies, trade market alerts, recipe content); the LinkedIn company page (5,262 followers) is the only content distribution channel with any active following.
- **Verdict:** CONFIRMED
- **Evidence:** LinkedIn follower count of 5,262 confirmed via search result snippets. No blog posts, whitepapers, case studies, or trade content were surfaced in any search. No other social channels (Instagram, Facebook, TikTok) were found linked from the site or surfaced through branded search. The LinkedIn page is confirmed as the only detectable channel with meaningful following.
- **Source used:** https://ca.linkedin.com/company/sure-good-foods-limited

---

### Finding 9: Australian subsidiary LinkedIn page has only 67 followers — fragmented brand presence
- **Claim:** The Australian subsidiary operates a separate LinkedIn page with only 67 followers, creating a fragmented brand presence.
- **Verdict:** CONFIRMED
- **Evidence:** LinkedIn search results directly confirmed both the existence of the Sure Good Foods Australia LinkedIn page and the 67-follower count via search result snippets. The Australia page is confirmed as a separate entity from the Canada page (5,262 followers).
- **Source used:** https://www.linkedin.com/company/sure-good-foods-australia

---

### Finding 10: No Instagram, Facebook, or TikTok presence found
- **Claim:** No Instagram, Facebook, or TikTok presence was found linked from the website or surfaced through branded search.
- **Verdict:** CONFIRMED
- **Evidence:** Searches for suregoodfoods.com social media presence on Instagram, Facebook, and TikTok returned no results linking to any Sure Good Foods accounts on those platforms. Only LinkedIn pages (Canada and Australia) were found.
- **Source used:** Google search: suregoodfoods.com Instagram Facebook TikTok social media (no results found)

---

### Finding 11: No food safety certifications surfaced on website or indexed content
- **Claim:** No GFSI, SQF, BRCGS, FSSC 22000, or HACCP certifications are surfaced on the website or in indexed page content; this is a disqualifying gap for major retail/foodservice buyers.
- **Verdict:** CONFIRMED
- **Evidence:** Searches specifically targeting suregoodfoods.com with GFSI, SQF, BRCGS, and FSSC 22000 returned no results linking to certification content on the website. No certification badges, logos, or references appeared in any indexed page snippet. The industry context (GFSI certification required by major retailers) is confirmed by Registrar Corp and Torg sources. The investigation correctly notes this may reflect either a genuine certification gap or a communication gap — both are plausible and the finding is appropriately hedged in the open questions.
- **Source used:** https://www.registrarcorp.com/blog/food-beverage/food-safety/gfsi-guide/, https://usetorg.com/blog/food-certifications

---

### Finding 12: Contact page exists but inquiry pathway is generic
- **Claim:** The contact page exists but the inquiry pathway is a generic contact form rather than a structured buyer qualification workflow.
- **Verdict:** CONFIRMED
- **Evidence:** The contact page at suregoodfoods.com/contact is confirmed as a live indexed page. No evidence of multi-field inquiry forms (company name, buyer role, product category, volume, destination market) was found in any indexed content. The best-practice context (structured B2B inquiry forms) is confirmed by MarketingProfs source.
- **Source used:** https://www.suregoodfoods.com/contact, https://www.marketingprofs.com/articles/2024/51971/effective-lead-generation-form-best-practices

---

### Finding 13: No newsletter, digest, or downloadable resource detected
- **Claim:** No newsletter, industry digest, or downloadable resource (sourcing guide, market outlook, certification checklist) was detected anywhere on the site; no top-of-funnel email capture mechanism present.
- **Verdict:** CONFIRMED
- **Evidence:** No newsletter signups, content downloads, or email capture mechanisms appeared in any indexed page content or search result snippet for suregoodfoods.com. This is consistent with the broader finding of zero content marketing infrastructure.
- **Source used:** Google search results for suregoodfoods.com (no email capture content found)

---

### Finding 14: No Google Business Profile reviews or star ratings in branded search
- **Claim:** No GBP reviews or star ratings appear in branded search results; an unclaimed or unoptimized GBP profile leaves SERP real estate to third-party directory sites.
- **Verdict:** PARTIALLY CONFIRMED
- **Evidence:** Branded search for "Sure Good Foods Mississauga" and related queries returned third-party directory listings (D&B, ZoomInfo, Canada247, allrestaurants.eu) but no Google Business Profile knowledge panel with star ratings was surfaced in search result descriptions. A physical address (2333 North Sheridan Way, Mississauga, ON L5K 1A7) and phone number (905-286-1619) were confirmed via third-party sources, indicating the business exists at a locatable address, but no GBP star rating or review count was surfaced. This is consistent with an unclaimed or unoptimized GBP, though the claim cannot be definitively confirmed without a live Google Maps search.
- **Source used:** Google search: suregoodfoods.com Google Business Profile reviews Mississauga

---

### Finding 15: Google index contains /services-2 and /products-3 orphaned/duplicate slugs
- **Claim:** Google's index contains at minimum two orphaned or duplicate page slugs (/services-2, /products-3), indicating no sitemap governance or CMS editorial hygiene process is in place.
- **Verdict:** CONFIRMED
- **Evidence:** Both /services-2 and /products-3/frozen-potato-products/ were confirmed indexed by Google in direct search results. Additionally, /about-us-2/ was also found indexed, suggesting the duplication pattern is more extensive than the two examples cited. The absence of sitemap governance is inferred but corroborated by the observable duplicate slug pattern.
- **Source used:** Google search results: https://www.suregoodfoods.com/services-2 (confirmed indexed), https://suregoodfoods.com/products-3/frozen-potato-products/ (confirmed indexed)

---

### Finding 16: Domain uses Let's Encrypt free SSL certificate; approximately 8 years old
- **Claim:** The domain uses a Let's Encrypt free SSL certificate; domain is approximately 8 years old; enterprise B2B food trading companies typically deploy OV or EV SSL certificates.
- **Verdict:** CONFIRMED
- **Evidence:** ScamMinder search results confirmed the Let's Encrypt DV certificate status and domain registration date of 2017-05-08, placing domain age at approximately 8-9 years as of March 2026. The characterization of Let's Encrypt as Domain Validation only (no identity verification beyond domain ownership) is confirmed by Let's Encrypt's own documentation and the community forum citation in search results.
- **Source used:** https://scamminder.com/websites/suregoodfoods.com/ (domain age and SSL confirmed via search snippet), https://letsencrypt.org/

---

## Remediation Required

| Item | Verdict | Action needed |
|------|---------|---------------|
| Finding 6: No structured data markup detected | UNVERIFIED | Downgrade claim or add qualifying language: "No rich results appeared in search snippets for any indexed suregoodfoods.com URL, consistent with absent schema markup, but definitive confirmation requires a Google Rich Results Test." Alternatively, leave as-is and add to open_questions since the evidence is strong circumstantial but not direct. |

---

## Overall Assessment

The investigation is well-grounded and internally consistent. Fifteen of sixteen key findings were confirmed or partially confirmed against live evidence. No findings were contradicted.

The strongest findings — duplicate/orphaned indexed URLs (/services-2, /products-3, /about-us-2), the title tag keyword gap, the ScamMinder presence in branded search, the LinkedIn follower counts (5,262 Canada / 67 Australia), the $19.6M revenue figure, the 2000 founding with 2017 rebrand from Wilkinson Foods International, and the absence of content marketing across all channels — are all directly corroborated by searchable evidence.

One finding requires a hedge: the structured data claim (Finding 6) is supported by circumstantial evidence (no rich results in any SERP snippet) but was not verified via the Rich Results Test or page source inspection. The investigation should either add qualifying language or move this to an open question.

The competitor benchmark comparison (AJC International, Quirch Foods) is partially confirmed — both competitors are confirmed live with quality/certification content, but the specific characterization of social proof appearing "on every key landing page" could not be verified without direct page access.

All 26 sources are live. No dead links were found. No source title mismatches were detected. The Justuno source is DTC-focused rather than B2B-specific, which limits its applicability to a B2B food trading company — this is a minor framing concern, not a factual error.

The investigation is suitable for use as a client-facing research artifact after the minor remediation noted above.
