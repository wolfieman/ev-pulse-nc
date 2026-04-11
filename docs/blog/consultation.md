# Blog Post Series — Content Strategy Panel Consultation

**Date:** March 13, 2026
**Status:** Awaiting panel responses

---

## Panel Composition (Blog Specialists)

| Expert | Specialty | Role |
|--------|-----------|------|
| **Ms. Anjali Mehta** | Content Strategy & LinkedIn Growth | 12 years in professional content marketing; specializes in thought-leadership series for technical professionals on LinkedIn. Former content lead at HubSpot. Advises on series structure, posting cadence, audience retention across multi-part content. |
| **Mr. David Kimura** | Technical Writing & Science Communication | Science writer and editor; Ph.D. in Environmental Engineering. Translates complex quantitative research for non-specialist audiences. Published in MIT Technology Review, Ars Technica. Advises on narrative arc, accessibility, and avoiding both oversimplification and jargon. |
| **Dr. Cassandra Wells** | Digital Publishing & Academic Outreach | Associate Professor of Strategic Communication, UNC-Chapel Hill. Researches how academics build public-facing credibility through digital platforms. Advises on cross-platform strategy (LinkedIn vs. Substack), audience segmentation, and academic brand-building. |

---

## Context Provided to Panel

### 1. Original Research Paper (BIDA 650, November 2025)
- "Charging Ahead With Intelligence: Optimizing North Carolina's EV Infrastructure Through Analytics"
- 4 authors, 17 pages, 12 figures, 39 references
- Four-phase analytics framework: descriptive, diagnostic, predictive, prescriptive
- Key findings: 53.8% CAGR, 16.9 BEVs/port ratio, 78 DCFC sites optimal for FY2026, break-even at 7 sessions/day with NEVI

### 2. Original LinkedIn Blog Post (November 27, 2025)
- "North Carolina's EV Boom: 5 Hidden Realities Powering the Charging Revolution"
- Format: ~1,200 words, 5-takeaway structure, infographic
- Audience: LinkedIn professionals in energy, transportation, policy, analytics
- Ended with forward-looking handoff: "This paper lays the foundation; the next phase ensures the system is not only functional today, but adaptable for the decade ahead."

### 3. Continuation Research (January–March 2026)
- Expanded to 5-phase analytics framework (added Exploratory as 5th analytical lens)
- All 5 phases COMPLETE as of March 2026:

| Phase | Topic | Headline Finding |
|-------|-------|-----------------|
| **1: Predictive Validation** | Tested SAS Viya forecasts against Jan–Jun 2025 holdout data | MAPE 4.34%, 69.00% underprediction bias — demand growing faster than predicted |
| **2: AFDC Infrastructure** | Complete supply-side baseline via NREL API | 1,985 stations, 6,145 connectors, full L1/L2/DCFC coverage |
| **3: ZIP Code Analysis** | Sub-county infrastructure mapping, inequality measurement | Theil-T decomposition: 84.5% of inequality is WITHIN counties, not between. Gini 0.566. Novel contribution (no prior published study). |
| **4: Workplace Charging** | LODES 2021 commuter flows + ACS income correction + remote work adjustment | Quantified workplace charging demand; renter equity dimension added |
| **5: Equity Analysis** | CEJST Justice40 overlay, NEVI scoring framework | 43% NC tracts disadvantaged; NEVI Priority Score: Union #1, Mecklenburg #2, Guilford #3; top-3 stable across weight sensitivity |

- NEVI Scoring Framework: Equity (0.40) + Utilization (0.35) + Cost-Effectiveness (0.25)
- 42 publication figures produced (fig-01 through fig-42)

### 4. Blog Creation Infrastructure
- Full blog creation protocol (BRIDGE prompt framework, AI-tell avoidance guide, writing style guide)
- Python blog_graphics.py module (stat cards, stat grids, social previews, comparison charts, interactive Plotly)
- Pre-built EV Pulse templates with project data baked in

---

## The Core Question

The author wants to create a follow-up blog post series that picks up where the November 2025 LinkedIn post left off. The follow-up should detail the expanded 5-phase framework and key findings from the continuation research, without framing it as semester-based coursework.

**Two proposed structures:**

**Option A: Detailed Series (6–7 posts)**
1. "Coming Attractions" overview — what changed, the 5-phase framework, what's coming
2. Phase 1: Predictive Validation — testing the original forecasts
3. Phase 2: Infrastructure Baseline — the complete supply picture
4. Phase 3: ZIP Code Analysis — the Theil decomposition finding
5. Phase 4: Workplace Charging — commuter demand
6. Phase 5: Equity Analysis — Justice40 and NEVI scoring
7. (Optional) Wrap-up / prescriptive "So What" post

**Option B: Focused Arc (3 posts)**
1. "Coming Attractions" overview — framework evolution, what changed, preview of findings
2. "The Findings" — combine most compelling results across all phases into one narrative
3. "So What" — NEVI scoring rankings, policy implications, what NC should do with $109M

**Option C: Hybrid or alternative** — panel's recommendation

---

## Questions for Content Strategy Panel

### Ms. Mehta (Content Strategy & LinkedIn Growth)
- Given LinkedIn audience behavior, which structure (A, B, or C) maximizes engagement and follower retention across a multi-post series?
- What posting cadence would you recommend (daily, twice weekly, weekly)?
- The original post used a "5 Hidden Realities" listicle format. Should the follow-up series maintain that structure or evolve to something different?
- Is there a risk of audience fatigue with 6–7 posts on the same topic, even if each phase is distinct?

### Mr. Kimura (Technical Writing & Science Communication)
- How do we make Phase 1 (validation) and Phase 2 (data collection) compelling to a non-academic audience? These are foundational but not inherently dramatic.
- The Theil decomposition finding (84.5% within-county inequality) is the strongest headline result. Should it anchor the series, or should we build toward it?
- How do we explain concepts like Gini coefficients, Theil decomposition, and CEJST without losing the LinkedIn audience?
- Should the Substack versions be expanded versions of the LinkedIn posts, or entirely different pieces?

### Dr. Wells (Digital Publishing & Academic Outreach)
- How should Wolfgang position this series to build academic credibility without sounding like a course assignment?
- Is cross-posting (LinkedIn + Substack simultaneously) effective, or should they be staggered with different angles?
- The SEINFORMS 2026 conference submission opens March 30. Should the blog series be timed to coincide with or precede a conference submission for maximum visibility?
- What role should the infographic/visual assets play in each post? One hero image per post, or multiple data visuals?

---

## Panel Requested Action

Please review all materials above and advise on:
1. **Series structure** — Option A (6–7 posts), Option B (3 posts), or Option C (your recommendation)?
2. **Post 1 outline** — Draft outline for the "Coming Attractions" introductory post
3. **Platform strategy** — LinkedIn vs. Substack: same content or differentiated?
4. **Cadence** — Recommended posting schedule
5. **Visual strategy** — What graphics/infographics should accompany each post?
6. **Tone evolution** — Should the follow-up series maintain the same voice as the original, or mature it?

---

## Panel Responses (March 13, 2026)

---

### Ms. Anjali Mehta — Content Strategy & LinkedIn Growth

**Series structure recommendation: Option C — 4-Post Arc**

Neither Option A nor Option B as written. Option A (6-7 posts) is too many for a single-topic LinkedIn series from a non-influencer account. LinkedIn's algorithm rewards consistent posting across varied topics, not deep serial dives. After post 3 or 4, impressions decline sharply because LinkedIn stops surfacing repeated-topic content to the same network. Option B (3 posts) is better in principle but the middle post ("The Findings") tries to do too much.

**Recommended 4-post structure:**

1. **"The Return"** — reconnects with the November audience, introduces the 5-phase expansion, previews the biggest findings
2. **"The Gap Within the Gap"** — Theil decomposition (84.5% within-county) paired with Justice40 equity overlay. Headline post. These two phases share a natural narrative: inequality is not where you think it is
3. **"Where the Chargers Should Go"** — workplace charging demand meets NEVI Priority Scores. The prescriptive payoff. Answers the $109M question
4. **"What I Got Wrong"** — validation results, underprediction bias, what it means for planning. Credibility post — "got wrong" framing is a proven LinkedIn engagement driver

Phase 2 (infrastructure baseline) is folded into supporting context across posts. A post about "I downloaded data from an API" does not earn engagement.

**Directed question responses:**

- **Posting cadence:** Weekly, Tuesday or Wednesday mornings (8-10 AM EST). Not twice weekly — need time between posts for comment engagement, which is where real LinkedIn growth happens. Wolfgang should reply to every comment within the first 2 hours.
- **Listicle format:** No. The "5 Hidden Realities" format worked for the standalone original. A series demands narrative progression. Each post should have a single thesis, not a numbered list. Use numbered findings *within* posts sparingly.
- **Audience fatigue risk:** Yes with 6-7 posts. Minimal with 4. Key mitigation: each post must have a standalone hook that works even for someone who missed earlier posts. Never open with "In Part 3 of my series..."

**Post 1 outline ("The Return"):**
- **Hook** (2 sentences): Lead with the underprediction finding. "Last November I published forecasts for NC's EV growth. Four months of real data came in. We were wrong — and the direction matters."
- **Callback** (1 paragraph): Brief reference to original "5 Hidden Realities" post with link. Acknowledge what has happened since. Do NOT re-summarize the old post.
- **Framework reveal** (2-3 paragraphs): Introduce the 5-phase framework visually. Use a stat grid graphic showing one headline number per phase. One sentence each.
- **Preview of findings** (2-3 sentences): Tease the Theil finding and NEVI rankings. Create anticipation.
- **Close** (1-2 sentences): Direct question. "Next week I will show you where the real gaps are. But first — which NC county do you think ranks #1 for charging investment priority?"
- **Target length:** 650-750 words for LinkedIn. Substack can expand to 1,200.

**Platform strategy:** LinkedIn is the primary driver. Substack is the archive and expanded version. Do NOT cross-post identical content. LinkedIn gets the tight, hook-driven version. Substack gets methodology detail, interactive charts (Plotly), and data tables. Link from LinkedIn to Substack at the bottom.

**Visual strategy:** One hero graphic per LinkedIn post. Stat grid for Post 1. Adapted publication figures for Posts 2-3 (simplify axis labels, increase font sizes, add plain-English subtitles). Forecast vs. actual line chart for Post 4. Substack gets 2-3 visuals each.

**Tone evolution:** Mature it. The original was slightly breathless ("EV Boom," "Charging Revolution"). The follow-up should be more measured and authoritative. Wolfgang now has 5 completed phases and a novel statistical finding. The tone should reflect someone who has done the work, not someone excited to share news. Confident, specific, understated. Let the numbers carry the energy.

---

### Mr. David Kimura — Technical Writing & Science Communication

**Series structure recommendation: Option C — 4-Post Arc (with modification)**

Supports Mehta's 4-post structure with one modification: Post 4 title should NOT be "What I Got Wrong." While that framing works for engagement, it risks undermining credibility. The underprediction bias is not an error; it is a finding about systematic demand acceleration. Better titles: "What the Data Did Next" or "Testing the Forecast."

**Directed question responses:**

**Making Phase 1 and Phase 2 compelling:**
- Phase 2 should NOT get its own post. Infrastructure data collection is a means, not a finding. Fold key numbers (1,985 stations, 6,145 connectors, Tesla's 60.5% connector share) into other posts as supporting context.
- Phase 1 (validation) IS inherently dramatic if framed correctly. The finding is not "our MAPE was 4.34%." The finding is "our forecasts systematically underpredicted demand. In 69.00% of cases, reality outran the model. NC's EV growth is faster than the best available predictions." That is a story about a state outrunning its own planning tools.

**Theil finding — anchor or build toward?**
Build toward it, but tease it early. Drop the 84.5% number in Post 1 as a one-sentence preview. Unpack fully in Post 2. The finding requires context to land. Recommended narrative arc for Post 2:
1. Concrete image: "Charlotte Uptown has 78.64 charging ports per 10,000 residents. Charlotte East Side, six miles away, has 0.31." A 250x gap within the same county.
2. Gini finding: infrastructure inequality is severe (0.566 statewide).
3. Theil reveal: 84.5% of that inequality is within counties, not between them.
4. Policy implication: county-level planning misses 85% of the problem.

**Explaining Gini, Theil, and CEJST to LinkedIn audience:**

Three rules:

*Rule 1 — Analogy before definition:* "The Gini coefficient measures how evenly something is distributed — 0 means perfectly equal, 1 means everything is concentrated in one place. NC's score for EV charging infrastructure is 0.566. For comparison, US income inequality is around 0.49. Charging access is more unequal than income."

*Rule 2 — Show the effect, not the math:* "The Theil index lets you separate inequality into two buckets: the gap between counties and the gap within counties. When I ran this on NC's charging data, 84.5% was in the within-county bucket. Knowing which county you live in tells you almost nothing about your charging access. What matters is which ZIP code."

*Rule 3 — Name the institution, not the methodology:* For CEJST: "The federal government maintains a screening tool that flags Census tracts where residents face both low incomes and environmental burdens. In North Carolina, 43% of tracts are flagged. That is the definition of 'disadvantaged' that determines which communities get priority for the $109M in NEVI funding."

**Substack versions:** Expanded, not different. Same narrative backbone, more detail. Substack gets the actual Lorenz curve figure, methodology explanations, and county-by-county breakdown tables. LinkedIn reader gets the story; Substack reader gets the story plus the receipts.

**Post 1 additions:** Include a "Previously" sidebar (2-3 bullet points) summarizing the original paper's key findings for readers who missed it. Standard practice in serial science communication.

**Visual strategy per post:**
- Post 1: Stat grid (one number per phase)
- Post 2: Simplified Theil decomposition bar — just two segments labeled "Within Counties: 84.5%" / "Between Counties: 15.5%"
- Post 3: NEVI ranking table as a visual
- Post 4: Forecast vs. actual overlay with underprediction bias shaded
- All publication figures must be adapted for blog: larger labels, fewer axis ticks, subtitle text explaining what the reader sees

**Tone evolution:** The follow-up should read like a practitioner's notebook. Less polish, more precision. First-person observations ("When I mapped the Theil decomposition results...") ground the writing. Avoid writing a press release about your own work. The findings are strong enough to speak plainly.

---

### Dr. Cassandra Wells — Digital Publishing & Academic Outreach

**Series structure recommendation: Option C — 4-Post Arc (reordered)**

Supports a 4-post structure but pushes back on post ordering. Placing validation last works for engagement but works against academic credibility. In research, you validate methods *before* presenting findings. Recommended order:

1. "The Return" (framework + preview)
2. "Testing the Forecast" (Phase 1 validation — establishes methodological credibility)
3. "The Gap Within the Gap" (Phases 3 + 5 — headline findings)
4. "Where the Chargers Should Go" (Phases 4 + 5 scoring — prescriptive payoff)

This mirrors the research process and builds credibility before making bold claims. A policy reader or conference reviewer will find this more persuasive.

**Resolution:** Use Mehta's ordering (validation last) for LinkedIn; use Wells's ordering (validation second) if repurposing for conference or academic context.

**Directed question responses:**

**Academic credibility without sounding like coursework:**

Three moves:
1. Never mention course numbers, semesters, or instructor names. Instead of "For my BIDA 670 project," write "As part of my ongoing research at Fayetteville State University."
2. Emphasize the novel contribution explicitly: "To my knowledge, no published study has applied Theil decomposition to EV charging infrastructure at the ZIP-code level." This signals original work, not a student exercise.
3. Cite your own work formally. Reference the original paper as "Sanyer et al. (2025)" — this is how researchers refer to prior work and signals a cumulative research program.

**Cross-posting strategy:**
Stagger by 24-48 hours, LinkedIn first. LinkedIn's algorithm rewards original content; if Substack is indexed first, LinkedIn may suppress the post. Publish LinkedIn Tuesday morning, expanded Substack Wednesday-Thursday.

Alternative: frame the Substack newsletter as a companion piece ("For readers who want the data behind this week's LinkedIn post"). This builds Substack subscribers from LinkedIn traffic.

**SEINFORMS timing:**

- Late March: Draft all 4 posts. Submit SEINFORMS abstract.
- Week 1 of April: Publish Post 1. Establishes public visibility before the conference.
- Weeks 2-4 of April: Posts 2-4.
- Conference (fall 2026): Full blog series is archived, Substack has a following, Wolfgang can reference the series as evidence of "broader impacts" — something INFORMS increasingly values.

The blog series should *precede* the conference. By the time Wolfgang presents at SEINFORMS, the online presence should already exist. Conference networking is 10x more productive when people can pull up your work on their phone.

**Visual assets:**
One hero image per LinkedIn post — non-negotiable. LinkedIn gives 2-3x more reach to posts with images. Must be custom graphics, not raw matplotlib figures. For Substack, interactive Plotly charts are a strong differentiator.

Every visual should include a plain-English subtitle stating the takeaway. "Charlotte Uptown has 250x more charging access than Charlotte East Side" is a caption. "Ports per 10,000 Population by ZCTA" is an axis label. Both are needed; the caption is what blog readers actually read.

**Additional recommendations:**
- Create a "Who This Is For" paragraph in Post 1 naming target audiences (transportation planners, policy analysts, EV professionals, data practitioners). Helps LinkedIn's algorithm match content to right feeds.
- Pin/feature the series on LinkedIn profile before SEINFORMS networking begins.
- Include an "About the Research" footer on every post: "This research was conducted as an independent multi-phase study of NC's EV charging infrastructure at Fayetteville State University. Data sources include NREL AFDC, Census ACS, LEHD LODES, and CEJST. A conference presentation is forthcoming."

**Tone evolution:** Mature from "excited student sharing findings" to "practitioner contributing to a policy conversation." More "I found" and "the data shows," less "hidden realities" and "revolution." The BRIDGE framework's voice guidance is well-calibrated — follow it closely.

---

## Panel Consensus

### Unanimous Agreement
1. **4-post structure (Option C)** — all reject Option A (too many) and Option B (too compressed)
2. **Phase 2 does not get its own post** — fold infrastructure data into other posts as context
3. **Weekly cadence** — Tuesdays 8-10 AM EST, draft all posts before publishing the first
4. **LinkedIn primary, Substack expanded** — differentiated content, not identical cross-posts
5. **One hero graphic per LinkedIn post, 2-3 for Substack** — adapted from publication figures, not raw
6. **Theil decomposition is the series centerpiece** — needs narrative setup before the number lands
7. **Tone should mature** — less magazinelike excitement, more practitioner authority
8. **Never reference course numbers or semesters** — position as independent research

### Primary Disagreement: Post Ordering

| Panelist | Validation Post Position | Reasoning |
|----------|------------------------|-----------|
| **Ms. Mehta** | Post 4 (last) | Maximum LinkedIn engagement; "What I Got Wrong" framing drives clicks |
| **Mr. Kimura** | Post 4 (last) | Agrees with placement, disagrees with "got wrong" title — prefers "Testing the Forecast" |
| **Dr. Wells** | Post 2 (second) | Academic credibility; prove methods before presenting findings |

**Resolution:** Use Mehta's ordering (validation last) for LinkedIn. Use Wells's ordering (validation second) for any academic reuse (SEINFORMS, paper).

### Unified Action Plan

1. **4-post structure:**
   - Post 1: "The Return" — framework, preview, callback to November post
   - Post 2: "The Gap Within the Gap" — Theil decomposition + Justice40 equity
   - Post 3: "Where the Chargers Should Go" — Workplace demand + NEVI rankings
   - Post 4: "Testing the Forecast" — Phase 1 validation, underprediction bias

2. **Timeline:**
   - Week of March 16-20: Draft all 4 posts
   - March 30: Submit SEINFORMS abstract
   - Week of April 1: Publish Post 1
   - Weeks of April 8, 15, 22: Posts 2, 3, 4

3. **Per-post visual plan:**
   - Post 1: Stat grid (5 numbers, one per phase) + social preview image
   - Post 2: Simplified Theil decomposition bar + Charlotte 250x gap callout
   - Post 3: NEVI ranking visual (top 10 counties) + county archetype comparison
   - Post 4: Forecast vs. actual line chart with underprediction shading

4. **Platform execution:**
   - LinkedIn: 650-800 words, one hero image, publish Tuesday 8-10 AM EST
   - Substack: 1,200-1,500 words, 2-3 visuals + interactive Plotly, publish Wed-Thu
   - Cross-link in both directions

5. **Quality control:**
   - Apply BRIDGE framework for all drafts
   - Run AI-tell checklist from blog protocol
   - Read aloud test before final publish
   - Engage with every comment in first 2 hours

6. **Academic integration:**
   - Reference original paper as "Sanyer et al. (2025)"
   - State novel contribution (Theil at ZIP level) explicitly
   - Never reference course numbers or semester context
   - Include "About the Research" footer on every post
   - Pin/feature series on LinkedIn profile before SEINFORMS
