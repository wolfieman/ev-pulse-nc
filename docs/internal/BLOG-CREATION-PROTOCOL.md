# EV Research Blog Creation Protocol

**A Complete Guide for Creating Publication-Quality Blog Posts**

Author: Wolfgang Sanyer
LinkedIn: https://www.linkedin.com/in/wolfgangsanyer/
Project: EV Pulse NC
Created: February 2026

---

## Table of Contents

1. [Python Libraries for Blog Graphics](#1-python-libraries-for-blog-graphics)
2. [Writing Style Guide - Avoiding AI Tells](#2-writing-style-guide---avoiding-ai-tells)
3. [Workflow Protocol](#3-workflow-protocol)
4. [BRIDGE Prompt Template](#4-bridge-prompt-template)
5. [Complete Step-by-Step Protocol](#5-complete-step-by-step-protocol)
6. [Tool Recommendations](#6-tool-recommendations)
7. [Ready-to-Use Templates](#7-ready-to-use-templates)

---

## 1. Python Libraries for Blog Graphics

### 1.1 What You Already Have (Leverage First)

Your `publication_style.py` is excellent for academic figures. For blog graphics, you need to add:

| Library | Purpose | Install |
|---------|---------|---------|
| **plotly** | Interactive charts, embed in web posts | `pip install plotly` |
| **altair** | Declarative visualization, clean aesthetics | `pip install altair` |
| **pygal** | SVG charts with hover effects | `pip install pygal` |
| **pillow** | Image manipulation, social previews | `pip install pillow` |
| **matplotlib** | Already installed - use for static exports | - |

### 1.2 Recommended Libraries by Use Case

#### For Data Visualizations (Charts, Graphs)

```python
# PLOTLY - Best for interactive web embeds
import plotly.express as px
import plotly.graph_objects as go

fig = px.line(df, x='date', y='bev_count',
              title='NC BEV Registrations Over Time',
              template='plotly_white')
fig.write_html('chart.html')  # Embed in Substack
fig.write_image('chart.png', scale=2)  # Static export
```

```python
# ALTAIR - Best for clean, publication-style web graphics
import altair as alt

chart = alt.Chart(df).mark_line().encode(
    x='date:T',
    y='bev_count:Q',
    color='county:N'
).properties(
    title='BEV Growth by County',
    width=600,
    height=400
)
chart.save('chart.png', scale_factor=2)
```

#### For Infographic-Style Visuals

```python
# MATPLOTLIB with custom styling (extend your publication_style.py)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patheffects import withStroke

def create_stat_card(stat_value, stat_label, color='#2ecc71'):
    """Create a single statistic card for infographics."""
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background card
    card = patches.FancyBboxPatch(
        (0.05, 0.05), 0.9, 0.9,
        boxstyle="round,pad=0.05,rounding_size=0.1",
        facecolor=color, alpha=0.15,
        edgecolor=color, linewidth=2
    )
    ax.add_patch(card)

    # Large stat number
    ax.text(0.5, 0.6, stat_value, fontsize=36, fontweight='bold',
            ha='center', va='center', color=color)

    # Label below
    ax.text(0.5, 0.25, stat_label, fontsize=12,
            ha='center', va='center', color='#333333')

    return fig

# Usage
fig = create_stat_card('1,727%', 'BEV Growth\n(2018-2025)')
fig.savefig('stat_card.png', dpi=300, bbox_inches='tight',
            facecolor='white', transparent=False)
```

#### For Social Media Preview Images (LinkedIn/Substack)

```python
# PILLOW for social preview images
from PIL import Image, ImageDraw, ImageFont

def create_social_preview(title, subtitle, output_path,
                          size=(1200, 628)):  # LinkedIn optimal
    """Create a social media preview image."""
    # Create image
    img = Image.new('RGB', size, color='#1a365d')  # Dark blue
    draw = ImageDraw.Draw(img)

    # Load fonts (use system fonts or download)
    try:
        title_font = ImageFont.truetype('arial.ttf', 48)
        subtitle_font = ImageFont.truetype('arial.ttf', 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Add gradient overlay (visual interest)
    for i in range(size[1]):
        alpha = int(255 * (1 - i / size[1]) * 0.3)
        draw.line([(0, i), (size[0], i)],
                  fill=(255, 255, 255, alpha))

    # Title text
    draw.text((60, size[1]//2 - 60), title,
              font=title_font, fill='white')

    # Subtitle
    draw.text((60, size[1]//2 + 20), subtitle,
              font=subtitle_font, fill='#a0aec0')

    # Add branding bar at bottom
    draw.rectangle([(0, size[1]-8), (size[0], size[1])],
                   fill='#2ecc71')

    img.save(output_path, quality=95)
    return img

# Usage
create_social_preview(
    "NC's EV Revolution: 1,727% Growth",
    "How 94,000 electric vehicles are reshaping infrastructure needs",
    "linkedin_preview.png"
)
```

### 1.3 Advanced: Multi-Panel Infographic Generator

```python
def create_blog_infographic(stats_dict, title, output_path):
    """
    Create a multi-panel infographic for blog posts.

    Args:
        stats_dict: {'label': value, ...}
        title: Main title
        output_path: Where to save
    """
    n_stats = len(stats_dict)
    fig, axes = plt.subplots(1, n_stats, figsize=(n_stats * 3, 3.5))

    if n_stats == 1:
        axes = [axes]

    colors = ['#2ecc71', '#3498db', '#9b59b6', '#f39c12', '#e74c3c']

    for ax, (label, value), color in zip(axes, stats_dict.items(), colors):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Circular background
        circle = plt.Circle((0.5, 0.55), 0.35, color=color, alpha=0.15)
        ax.add_patch(circle)
        circle_border = plt.Circle((0.5, 0.55), 0.35,
                                    fill=False, color=color, linewidth=3)
        ax.add_patch(circle_border)

        # Value
        ax.text(0.5, 0.55, str(value), fontsize=28, fontweight='bold',
                ha='center', va='center', color=color)

        # Label
        ax.text(0.5, 0.08, label, fontsize=10, ha='center',
                va='center', color='#333', wrap=True)

    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    fig.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', pad_inches=0.3)
    plt.close(fig)

# Usage
create_blog_infographic(
    {
        'BEV Growth': '1,727%',
        'Total BEVs': '94,371',
        'BEVs/Port': '16.9',
        'NEVI Funding': '$109M'
    },
    'North Carolina EV Infrastructure at a Glance',
    'infographic.png'
)
```

### 1.4 Libraries NOT Recommended for Your Use Case

| Library | Why to Avoid |
|---------|--------------|
| **infographic** (PyPI) | Abandoned, poor quality |
| **pycairo** | Steep learning curve, overkill |
| **reportlab** | For PDFs, not web graphics |
| **bokeh** | Heavier than Plotly, less LinkedIn-friendly |

---

## 2. Writing Style Guide - Avoiding AI Tells

### 2.1 Words and Phrases to AVOID

These are statistical markers that flag AI-generated text:

#### Overused Transitional Phrases
| AVOID | USE INSTEAD |
|-------|-------------|
| "delve into" | examine, look at, explore |
| "tapestry of" | mix of, combination of |
| "landscape" (metaphorical) | situation, environment, market |
| "in the realm of" | in, within, regarding |
| "it's important to note that" | (delete entirely, just state the fact) |
| "at the end of the day" | ultimately, in practice |
| "paradigm shift" | major change, transformation |
| "leverage" (as verb) | use, apply, employ |
| "synergy" | cooperation, combined effect |
| "game-changer" | significant development |

#### Overused Sentence Starters
| AVOID | USE INSTEAD |
|-------|-------------|
| "In today's world..." | (start with the specific topic) |
| "It goes without saying..." | (if it goes without saying, don't say it) |
| "When it comes to..." | "For...", "Regarding...", or just start |
| "There's no denying that..." | (state the fact directly) |
| "This begs the question..." | "This raises a question:" |

#### Punctuation Tells
| AVOID | USE INSTEAD |
|-------|-------------|
| Em-dash overuse (--) | Use sparingly; prefer commas or periods |
| Exclamation points! | Reserve for genuine excitement |
| Semicolons; everywhere | Break into shorter sentences |
| Ellipsis... for drama | (avoid entirely in professional writing) |

### 2.2 Structural Patterns to Avoid

**The "List of Three" Pattern**
```
AVOID: "This approach offers efficiency, scalability, and sustainability."
BETTER: "This approach is efficient. More importantly, it scales to handle
        the state's growth without requiring proportional infrastructure
        investment."
```

**The Hedge-Then-Assert Pattern**
```
AVOID: "While some may argue otherwise, the data clearly shows..."
BETTER: "The data shows X. Here's why: [specific evidence]"
```

**The False Balance Pattern**
```
AVOID: "There are pros and cons to every approach. On one hand...
        On the other hand..."
BETTER: "Three factors favor this approach: [specific]. The main
        drawback is [specific], which we address by [solution]."
```

### 2.3 Humanizing Techniques

#### Add Specificity
```
GENERIC: "EV adoption has grown significantly in recent years."
SPECIFIC: "Wake County added 847 BEVs in October 2025 alone--more than
          the entire state had in September 2018."
```

#### Include Your Perspective
```
DETACHED: "The data suggests infrastructure gaps exist."
PERSONAL: "When I mapped the charging stations against BEV registrations,
          the gaps jumped out: 16.9 BEVs competing for each public port."
```

#### Use Concrete Examples
```
ABSTRACT: "Rural areas face unique challenges."
CONCRETE: "Graham County has 47 BEVs and zero public chargers. The nearest
          fast charger is a 45-minute drive to Cherokee."
```

#### Vary Sentence Length
```
Short sentences punch. They create emphasis.

Longer sentences work well for explaining complex relationships, like how
the 53.8% compound annual growth rate in BEV registrations has outpaced
the infrastructure deployment rate by roughly 2:1, creating the current
16.9 BEV-per-port ratio.

Mix them.
```

### 2.4 Pre-Publication Checklist

Before publishing, run through this checklist:

- [ ] **Read aloud**: Does it sound like you talking to a colleague?
- [ ] **First-person audit**: Did you use "I" or "we" at least 2-3 times?
- [ ] **Specificity check**: Every claim has a specific number or example?
- [ ] **Em-dash count**: More than 2 per 500 words? Cut some.
- [ ] **"Delve/tapestry/landscape" check**: Find and replace all.
- [ ] **Opening line**: Does it start with data, story, or question (not "In today's...")?
- [ ] **Conclusion**: Does it end with action or insight (not "In conclusion...")?

### 2.5 Tools for Detecting AI Patterns

| Tool | Purpose | Link |
|------|---------|------|
| **GPTZero** | AI detection (use to test your own work) | gptzero.me |
| **Hemingway Editor** | Readability, passive voice | hemingwayapp.com |
| **Grammarly** | General writing quality | grammarly.com |
| **ProWritingAid** | Style analysis, overused words | prowritingaid.com |

**Self-test workflow:**
1. Write draft with AI assistance
2. Run through Hemingway Editor
3. Test with GPTZero (aim for <30% AI probability)
4. Read aloud and edit
5. Re-test with GPTZero

---

## 3. Workflow Protocol

### 3.1 Can This Be Done Entirely in Python/Claude Code?

**Short answer: Partially, but not optimally.**

| Task | Python/Claude | External Tool Better |
|------|---------------|---------------------|
| Data analysis | Yes | - |
| Statistical charts | Yes | - |
| Basic infographics | Yes (limited) | Canva |
| Social preview images | Yes (basic) | Canva/Figma |
| Writing first draft | Yes | - |
| Humanizing text | Partial | Human editing |
| Final layout | No | Substack/LinkedIn |
| Audio/podcast | No | NotebookLM |

### 3.2 Optimal Hybrid Workflow

```
[Research/Data]     [Writing]          [Graphics]         [Publishing]
     |                  |                  |                   |
     v                  v                  v                   v
  Python           Claude Code         Python            Substack/
  Analysis      +  + NotebookLM    +   + Canva       +   LinkedIn

  (Your code)      (Draft text)       (Charts +           (Final
                   (Audio summary)    Infographics)        publish)
```

### 3.3 NotebookLM's Strengths

NotebookLM excels at:
- **Audio Overviews**: Turn your research into podcast-style summaries
- **Source Grounding**: Answers tied to your uploaded documents
- **Cross-Document Synthesis**: Combine multiple papers/datasets
- **Conversational Exploration**: Q&A with your own research

**Best Use for Your Project:**
1. Upload your PROJECT-BRIEF.md and key analysis outputs
2. Generate Audio Overview for podcast content
3. Ask specific questions to extract blog angles
4. Use generated insights as blog post starting points

### 3.4 Tool Integration Map

```
                    +-------------------+
                    |   Your Research   |
                    |  (ev-pulse-nc/)   |
                    +--------+----------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
     +--------+--------+           +--------+--------+
     |  NotebookLM     |           |  Python/Claude  |
     |  - Audio        |           |  - Analysis     |
     |  - Q&A          |           |  - Charts       |
     |  - Synthesis    |           |  - Basic        |
     +--------+--------+           |    infographics |
              |                    +--------+--------+
              |                             |
              +-------------+---------------+
                            |
                            v
                   +--------+--------+
                   |  Draft Content  |
                   |  (Markdown)     |
                   +--------+--------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
     +--------+--------+         +--------+--------+
     |  Canva/Figma    |         |  Human Review   |
     |  - Infographics |         |  - AI tells     |
     |  - Social cards |         |  - Voice/tone   |
     +--------+--------+         +--------+--------+
              |                           |
              +-------------+-------------+
                            |
                            v
                   +--------+--------+
                   |  Substack /     |
                   |  LinkedIn       |
                   +--------+--------+
```

---

## 4. BRIDGE Prompt Template

### 4.1 The BRIDGE Framework

| Letter | Element | Purpose |
|--------|---------|---------|
| **B** | Background | Who YOU are, context, AND what PERSONA the AI should adopt |
| **R** | Request | What you want created - specific deliverables |
| **I** | Inputs | Source material being used |
| **D** | Deliverable | Detailed structure of what you want created |
| **G** | Guardrails | Do's and Don'ts, boundaries, constraints |
| **E** | Evaluation | Checklist to verify output is complete/correct |

### 4.2 BRIDGE Template for EV Research Blog Posts

```markdown
## BRIDGE Prompt: EV Research Blog Post

### BACKGROUND

**Who I Am:**
I'm Wolfgang Sanyer, a data analyst and BIDA 670 (Applied Business
Intelligence & Data Analytics) graduate student at Fayetteville State
University. I'm completing my MBA with a concentration in data analytics.
My project (EV Pulse NC) uses Python, statistical modeling, and geographic
analysis to study North Carolina's electric vehicle infrastructure gap.

**Who My Audience Is:**
- LinkedIn professionals in energy, transportation, and public policy
- Data enthusiasts who appreciate methodology transparency
- North Carolina policy makers and infrastructure planners
- Business leaders evaluating EV market opportunities
- Fellow graduate students and academics in applied analytics

**Your Role (AI Persona):**
Act as a technical writer who specializes in translating data analytics
research for business and policy audiences. Write as if you ARE Wolfgang
Sanyer: a practitioner who bridges data science and business strategy.

You embody:
- **Data Translator**: You convert statistical findings into plain-language
  insights without dumbing them down
- **Policy Interpreter**: You understand how research connects to real
  infrastructure decisions
- **Engagement Strategist**: You know what makes LinkedIn and Substack
  audiences stop scrolling
- **Credibility Builder**: You establish authority through specificity,
  not jargon

Your voice is:
- Analytical but accessible (you explain the "so what" behind every number)
- Confident but not arrogant (you show your work, acknowledge limitations)
- Curious and conversational (you ask questions, invite discussion)
- Grounded in specifics (you cite exact figures, name specific counties)
- Direct and concise (you respect readers' time)

You are NOT: an academic writing for peer review, a journalist chasing
clicks, a consultant selling services, or a generic content writer.
You are a graduate student sharing genuine insights from hands-on research.

---

### REQUEST

**Primary Deliverable:**
Write a blog post for LinkedIn (600-800 words) or Substack (1,200-1,500 words)
that translates EV Pulse NC research findings into accessible, engaging content.

**Specific Components:**
1. Hook (1-2 sentences): Surprising statistic, concrete comparison, or
   provocative question
2. Context (2-3 sentences): Ground the reader in NC's specific situation
3. Key Finding (1-2 paragraphs): Main insight with supporting data
4. So What (1-2 paragraphs): Implications for specific audiences
5. Methodology Note (1-2 sentences): Brief credibility statement
6. Call to Action (1-2 sentences): Engagement prompt or question

---

### INPUTS

**Key Research Findings to Draw From:**
- 53.8% CAGR in BEV registrations (Sept 2018 - June 2025)
- 94,371 total BEVs, 1,727% growth since 2018
- 16.9 BEVs per public charging port (vs 10-15 national benchmark)
- Gini coefficient of 0.805 (extreme geographic concentration)
- Top 10 counties hold 72% of all BEVs
- Bottom 50 counties hold only 4.8% of BEVs
- Forecast validation MAPE: 4.34% (strong accuracy)
- Systematic underprediction: 69.00% of forecasts below actuals
- $109 million NEVI funding allocation decision pending

**Source Material:**
- PROJECT-BRIEF.md
- Analysis outputs from Python notebooks
- NCDMV registration data
- AFDC charging station data

---

### DELIVERABLE

**Structure:**

## Part 1: The Hook
- 1-2 sentences maximum
- Open with a surprising statistic, a concrete comparison, or provocative question
- Never open with "In today's..." or abstract scene-setting

## Part 2: Context
- 2-3 sentences grounding the reader
- What's happening in NC? Why does this matter now?

## Part 3: Key Finding
- 1-2 paragraphs presenting the main insight with supporting data
- Use "compared to" or "that means" constructions to make numbers meaningful

## Part 4: So What
- 1-2 paragraphs on implications for specific audiences
- Name counties, cite dollar amounts, reference actual decisions

## Part 5: Methodology Note
- 1-2 sentences on data sources and analysis approach
- Keep it conversational (not academic)

## Part 6: Call to Action
- 1-2 sentences prompting engagement
- End with a question or invitation to comment

**Format Requirements:**
- Length: 600-800 words (LinkedIn) or 1,200-1,500 words (Substack)
- Paragraphs: 2-3 sentences each (scannable)
- Bullet points: Use sparingly for lists of 3+ items
- Headers: Use for Substack; omit for LinkedIn short-form
- First person: Use "I" at least 2-3 times

---

### GUARDRAILS

**Do:**
- Use specific numbers and county names
- Explain the "so what" behind every statistic
- Vary sentence length (mix short punchy with longer explanatory)
- Include personal perspective ("When I mapped..." or "I found...")
- Sound like Wolfgang talking to a colleague over coffee

**Don't - CRITICAL AI Tells to AVOID:**

| BANNED | USE INSTEAD |
|--------|-------------|
| "delve into" | examine, look at, explore |
| "tapestry" | mix, combination |
| "landscape" (metaphor) | situation, market, environment |
| "paradigm shift" | major change, shift |
| "leverage" (verb) | use, apply |
| "synergy" | combined effect |
| "game-changer" | significant development |
| "in the realm of" | in, within |
| "it's important to note" | (delete; just state the fact) |
| "In today's world..." | (start with specifics) |
| "at the end of the day" | ultimately |
| "there's no denying that" | (state the fact directly) |
| "when it comes to" | "For...", "Regarding...", or just start |
| "it goes without saying" | (if it goes without saying, don't say it) |

**Punctuation Constraints:**
- Em-dashes: Maximum 2 per 500 words
- Exclamation points: Only for genuine surprise (rare)
- Semicolons: Prefer shorter sentences instead
- Ellipsis: Avoid entirely

**Structural Patterns to Avoid:**
- "List of Three" pattern ("efficiency, scalability, and sustainability")
- Hedge-Then-Assert ("While some may argue..., the data clearly shows...")
- False Balance ("On one hand... On the other hand...")

---

### EVALUATION

**Completeness Check:**
- [ ] Hook opens with data, story, or question (not "In today's...")
- [ ] Context grounds reader in NC's specific situation
- [ ] Key finding includes 2-3 specific statistics with meaningful context
- [ ] At least one specific county or dollar figure named
- [ ] Methodology briefly mentioned for credibility
- [ ] Ends with question or invitation that prompts comments

**Quality Check:**
- [ ] Pass the "read aloud" test (sounds like Wolfgang talking to a colleague)
- [ ] Score <30% on GPTZero (reads as human-written)
- [ ] "I" or "we" used at least 2-3 times
- [ ] No banned words/phrases from the AVOID list
- [ ] Em-dash count: 2 or fewer per 500 words
- [ ] Sentence length varies (short punchy + longer explanatory)

**Audience Check:**
- [ ] Professional but conversational tone
- [ ] Data-driven but not dry
- [ ] Confident but humble about limitations
- [ ] Builds toward BIDA 670 final presentation by establishing credibility

---

### SUPPLEMENTARY: Examples

**Strong Opening Examples:**
- "Wake County added 847 BEVs in October 2025. The county added 3 public
  chargers. Something has to give."
- "What does 16.9 look like? That's how many EVs compete for each public
  charging port in North Carolina. The national benchmark is 10-15."
- "Graham County has 47 electric vehicles and zero public chargers. The
  nearest fast charger is a 45-minute drive to Cherokee."

**Weak Opening to AVOID:**
- "In today's rapidly evolving transportation landscape, electric vehicles
  are becoming increasingly important..."
- "As we delve into the complex tapestry of EV infrastructure..."
- "It goes without saying that the future of transportation is electric..."

**Strong Closing Example:**
- "The $109 million question isn't whether NC needs more chargers. It's
  where. What would you prioritize: filling gaps in rural counties or
  meeting demand in Wake and Mecklenburg?"

**Weak Closing to AVOID:**
- "In conclusion, EV infrastructure is a multifaceted challenge that
  requires collaborative solutions from all stakeholders."
```

### 4.3 NotebookLM-Specific BRIDGE Adaptation

When using NotebookLM, upload your sources first, then use this prompt:

```markdown
## NotebookLM Source Exploration Prompt

Based on the uploaded EV Pulse NC research documents, I need to create
a LinkedIn blog post. Please help me:

1. Identify the 3 most surprising statistics from the research
2. Find a "contrast pair" (two numbers that together tell a story)
3. Suggest a hook question that would grab a business audience
4. Extract any quotes or specific findings about Wake/Mecklenburg counties
5. Summarize the methodology in one sentence for credibility

After exploring, generate an Audio Overview focused on:
- The infrastructure gap problem
- Why the 16.9 BEV-per-port ratio matters
- What the $109M NEVI funding decision means for NC
```

---

## 5. Complete Step-by-Step Protocol

### Phase 1: Research Synthesis (30 minutes)

| Step | Tool | Action |
|------|------|--------|
| 1.1 | Python | Run analysis, export key statistics |
| 1.2 | NotebookLM | Upload findings, generate Audio Overview |
| 1.3 | NotebookLM | Ask targeted questions for blog angles |
| 1.4 | Notion/Notes | Collect 5-7 key statistics with context |

**Output:** Statistics document with:
- 5-7 key numbers
- Context for each (what does it mean?)
- 2-3 potential hooks
- Target audience notes

### Phase 2: Draft Creation (45 minutes)

| Step | Tool | Action |
|------|------|--------|
| 2.1 | Claude Code | Use BRIDGE prompt to generate draft |
| 2.2 | Claude Code | Request 3 alternative openings |
| 2.3 | Self | Choose best opening, combine strongest elements |
| 2.4 | Hemingway | Paste draft, fix readability issues |

**Output:** Draft blog post (Markdown file)

### Phase 3: AI-Tell Removal (20 minutes)

| Step | Tool | Action |
|------|------|--------|
| 3.1 | GPTZero | Test draft, note AI probability |
| 3.2 | Self | Apply humanizing techniques from Section 2 |
| 3.3 | Self | Read aloud, mark awkward phrases |
| 3.4 | GPTZero | Re-test, aim for <30% AI probability |

**Output:** Humanized draft

### Phase 4: Graphics Creation (30-45 minutes)

| Step | Tool | Action |
|------|------|--------|
| 4.1 | Python | Generate data charts (use publication_style.py) |
| 4.2 | Python | Create stat cards/basic infographics |
| 4.3 | Canva | Create polished infographic (if needed) |
| 4.4 | Python/Canva | Create social preview image |

**Output:**
- 2-3 charts (PNG, 300+ DPI)
- 1 infographic or stat card grid
- 1 social preview image (1200x628)

### Phase 5: Final Review & Publish (20 minutes)

| Step | Tool | Action |
|------|------|--------|
| 5.1 | Grammarly | Final grammar/style check |
| 5.2 | Self | Final read-through with checklist |
| 5.3 | Substack/LinkedIn | Upload, format, add images |
| 5.4 | Self | Write post description/teaser |
| 5.5 | Publish | Schedule or publish immediately |

**Output:** Published blog post

### Total Time: ~2.5-3 hours per post

---

## 6. Tool Recommendations

### 6.1 Essential Tools (Use These)

| Tool | Purpose | Cost | Priority |
|------|---------|------|----------|
| **Python + matplotlib** | Data charts | Free | Must-have |
| **Claude Code** | Drafting, analysis | Subscription | Must-have |
| **NotebookLM** | Audio, synthesis | Free | Must-have |
| **Hemingway Editor** | Readability | Free | Must-have |
| **GPTZero** | AI detection self-test | Free tier | Must-have |
| **Canva** | Infographics, social cards | Free tier | Recommended |

### 6.2 Nice-to-Have Tools

| Tool | Purpose | Cost | When to Use |
|------|---------|------|-------------|
| **Figma** | Advanced design | Free tier | Complex infographics |
| **Plotly** | Interactive charts | Free | Substack embeds |
| **Grammarly Premium** | Advanced style | $12/mo | High-volume writing |
| **Descript** | Audio/video editing | Free tier | Podcast from NotebookLM |

### 6.3 Tool Comparison: Canva vs Python for Infographics

| Factor | Canva | Python |
|--------|-------|--------|
| **Speed** | Faster for one-offs | Faster for templates |
| **Consistency** | Manual | Programmatic |
| **Data integration** | Manual entry | Automatic |
| **Design quality** | Higher ceiling | Lower ceiling |
| **Reproducibility** | Low | High |
| **Learning curve** | Low | Medium |

**Recommendation:** Use Python for data-driven graphics (charts, stat cards with your actual numbers). Use Canva for design-heavy pieces (hero images, complex infographics with icons).

---

## 7. Ready-to-Use Templates

### 7.1 Blog Post Template (Markdown)

```markdown
# [Compelling Title with Number or Question]

*[One-sentence hook that creates tension or curiosity]*

---

[2-3 sentence context paragraph. What's the situation? Why now?]

## The Key Finding

[State your main insight clearly. Include the primary statistic.]

[Expand with supporting data. Use a "compared to" or "that means"
construction to make numbers meaningful.]

> [Optional: Pull quote or key statistic in blockquote format]

## Why This Matters

[2-3 sentences on implications. Who does this affect? What decisions
does this inform?]

[Specific example: "For Wake County, this means..."]

## What I Found

[Brief methodology credibility statement. One sentence on data source,
one on analysis approach.]

The data covers [scope]. I analyzed [method] to find [result].

## What's Next

[Call to action or forward-looking statement. What should readers
think about, do, or watch for?]

---

*[Your sign-off. Keep it consistent across posts.]*

*Wolfgang Sanyer researches EV infrastructure at Fayetteville State
University. This analysis is part of the EV Pulse NC project.*
```

### 7.2 LinkedIn Post Template (Short Form)

```markdown
[Hook statistic or question - max 2 lines]

Here's what the data shows:

[Bullet point 1 - key finding]
[Bullet point 2 - supporting data]
[Bullet point 3 - implication]

The bottom line: [One sentence takeaway]

[Question to drive engagement: "What's your take on...?" or
"Have you noticed this in your area?"]

#ElectricVehicles #EVInfrastructure #NorthCarolina #DataAnalytics

---
[Link to full Substack post if applicable]
```

### 7.3 Social Preview Image Specifications

| Platform | Size (px) | Aspect Ratio | Notes |
|----------|-----------|--------------|-------|
| LinkedIn | 1200 x 628 | 1.91:1 | Most important |
| Substack | 1456 x 180 | ~8:1 | Banner/header |
| Twitter/X | 1200 x 675 | 16:9 | If cross-posting |

### 7.4 Quick Statistics Reference (Your Data)

Use these in your posts:

| Statistic | Value | Context |
|-----------|-------|---------|
| BEV Growth | 1,727% | Sept 2018 to June 2025 |
| Current BEVs | 94,371 | June 2025 |
| CAGR | 53.8% | Compound annual growth rate |
| BEVs per Port | 16.9 | vs 10-15 national benchmark |
| Gini Coefficient | 0.805 | Extreme geographic concentration |
| Top 10 Counties | 72% | Share of all BEVs |
| Top 5 Counties | 57.4% | Share of all BEVs |
| Bottom 50 Counties | 4.8% | Share of all BEVs |
| Charging Connectors | 6,145 | Individual units (all levels L1/L2/DCFC, Feb 2026) |
| Charging Stations | 1,985 | Physical locations (Feb 2026 AFDC API) |
| NEVI Funding | $109M | Federal allocation for NC |
| Forecast MAPE | 4.34% | Validation accuracy |
| Underprediction Rate | 69.00% | Forecasts below actuals |

---

## Appendix: Quick Reference Checklist

### Pre-Writing
- [ ] Key statistics identified (5-7)
- [ ] Target audience defined
- [ ] Hook drafted (3 options)
- [ ] BRIDGE prompt prepared

### Writing
- [ ] Opening avoids "In today's..."
- [ ] First person used (I/we)
- [ ] Specific numbers included
- [ ] No "delve/tapestry/landscape"
- [ ] Em-dashes limited (<3)

### Review
- [ ] Hemingway score: Grade 9 or lower
- [ ] GPTZero: <30% AI probability
- [ ] Read aloud test passed
- [ ] Graphics match text claims

### Publishing
- [ ] Social preview image created
- [ ] Alt text for images
- [ ] Tags/hashtags added
- [ ] Cross-post scheduled

---

*Last updated: April 2026*
*Document version: 1.0*
