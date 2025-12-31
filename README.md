# SAS Curiosity Cup 2026: North Carolina EV Infrastructure Gap Analysis

🏆 **Competition:** [SAS Curiosity Cup 2026](https://www.sas.com/curiositycup) - Global Student Analytics Competition  
📊 **Category:** Business & Economy  
🎯 **Objective:** Quantify the alignment between North Carolina's electric vehicle adoption growth and public charging infrastructure deployment  
📅 **Competition Timeline:** December 2025 - February 2026

---

## 🚗 Project Overview

North Carolina's battery electric vehicle (BEV) fleet has experienced explosive growth, expanding from 5,165 vehicles in September 2018 to 94,371 in June 2025—a **1,727% increase** with a **53.8% compound annual growth rate (CAGR)**. However, public charging infrastructure has not kept pace, creating a widening gap that threatens the equitable transition to electric mobility.

This project applies a comprehensive **4-phase analytics framework**—descriptive, diagnostic, predictive, and prescriptive analysis—to:

1. **Quantify infrastructure gaps** at the county level across North Carolina
2. **Forecast future demand** using time series models
3. **Identify high-priority deployment zones** through gap severity analysis
4. **Optimize investment strategies** for the $109M NEVI Formula Program funding

---

## 📈 Key Findings

### Demand-Side Analysis
- **Explosive Growth:** 53.8% CAGR in BEV registrations (Sept 2018 - June 2025)
- **Geographic Inequality:** Gini coefficient of **0.805** (extreme concentration)
  - Top 10 counties: **72%** of all BEVs
  - Top 5 counties: **57.4%** of all BEVs
- **Urban Dominance:** 11 urban counties (11% of counties) account for **70%** of BEVs
- **Research Triangle Leadership:** Wake + Durham + Orange counties = **35.2%** of state total

### Supply-Side Analysis
- **Infrastructure Snapshot:** 355 charging stations, 1,725 individual charging units
- **Tesla Dominance:** **60.5%** of all charging connectors despite only **24.8%** of stations
- **High-Power Focus:** **80.5%** of units provide ≥150 kW charging capacity
- **Recent Deployment Surge:** **47.6%** of all infrastructure added in 2024-2025 alone

### Infrastructure Gap
- **Current Ratio:** ~16.9 BEVs per public charging port
- **National Benchmark:** 10-15 BEVs per port (industry standard)
- **Conclusion:** Infrastructure lagging demand by **13-40%** depending on county

---

## 🛠️ Tech Stack & Methodology

### Software & Tools
- **SAS Viya Workbench for Learners** - Primary analytics platform
  - Time series forecasting (ARIMA/Exponential Smoothing)
  - Data manipulation and cleaning
  - Statistical analysis and visualization
- **Python** - Exploratory data analysis, geospatial processing
  - pandas, matplotlib, seaborn
  - Geopy for geocoding
- **Excel** - Initial data profiling and validation

### Analytical Framework
1. **Descriptive Analysis** - Historical trends, distributions, geographic patterns
2. **Diagnostic Analysis** - Gap identification, county classification, equity assessment
3. **Predictive Analysis** - County-level BEV forecasting (Sept 2018 - June 2028)
4. **Prescriptive Analysis** - Investment optimization, deployment prioritization

### Data Sources
- **NC Department of Transportation (NCDOT)** - Vehicle registration time series
  - 8,200 observations (100 counties × 82 months)
  - September 2018 - June 2025
- **Alternative Fuels Data Center (AFDC)** - U.S. Department of Energy
  - 1,725 charging connector records across 355 stations
  - Detailed capacity and technology data

---

## 📁 Repository Structure

```
sas-cup-26/
├── README.md                     # This file
├── LICENSE                       # Polyform Noncommercial License 1.0.0
├── NOTICE.md                     # Copyright notice
├── .gitignore                    # Git ignore patterns
├── .gitattributes                # Git LFS tracking rules
│
├── data/                         # Dataset directory (Git LFS)
│   ├── raw/                      # Original datasets
│   │   ├── NC_EV_PHEV_TS.csv              # 520 MB - BEV registrations
│   │   └── alt_fuel_stations_ev_charging_units.csv  # 695 MB - Charging infrastructure
│   ├── processed/                # Cleaned/transformed data
│   └── README.md                 # Data dictionary & sources
│
├── code/                         # Analysis code
│   ├── sas/                      # SAS Studio/Viya code
│   │   ├── 01-data-import/       # Import scripts (.ctl files)
│   │   ├── 02-data-prep/         # Cleaning, validation, geocoding
│   │   ├── 03-eda/               # Exploratory data analysis
│   │   ├── 04-forecasting/       # Time series forecasting models
│   │   ├── 05-gap-analysis/      # Diagnostic gap metrics
│   │   └── 06-visualization/     # Chart and map generation
│   ├── python/                   # Python EDA scripts (future)
│   └── README.md                 # Code execution guide
│
├── docs/                         # Project documentation
│   ├── planning/
│   │   ├── execution-plan-v01.docx
│   │   ├── outline-v03.docx
│   │   └── curiosity-cup-2026-paper-outline.md
│   ├── eda-reports/              # Exploratory data analysis reports
│   │   ├── ncevregistrationseda.pdf
│   │   ├── altfuelstationseda.pdf
│   │   └── enhancedchargingunitseda.pdf
│   ├── competition-guidelines/
│   │   ├── curiosity_cup2026finalcompetitionguidelines.pdf
│   │   └── reference-papers/     # Winning papers from 2025
│   └── research/                 # Supporting research
│       └── evpapersanyeretal.pdf
│
├── output/                       # Generated outputs
│   ├── figures/                  # Visualizations for paper appendix
│   ├── tables/                   # Summary statistics tables
│   └── models/                   # Saved forecasting artifacts
│
├── paper/                        # Competition submission
│   ├── final-paper.docx          # 4-5 page main text
│   └── appendix-visualizations.docx  # 2-page appendix
│
└── references/                   # Supporting materials
    ├── competitor-analyses/      # 2025 winning papers
    └── data-sources.md           # Citations & links
```

---

## 🚀 Getting Started

### Prerequisites
- SAS Viya Workbench for Learners (free academic license)
- Git with Git LFS extension
- Python 3.8+ (optional, for EDA scripts)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sas-cup-26.git
   cd sas-cup-26
   ```

2. **Install Git LFS** (required for large datasets)
   ```bash
   git lfs install
   git lfs pull
   ```

3. **Verify data files**
   ```bash
   ls -lh data/raw/
   # Should show NC_EV_PHEV_TS.csv (520 MB)
   # Should show alt_fuel_stations_ev_charging_units.csv (695 MB)
   ```

4. **Import data into SAS Viya**
   - Use scripts in `code/sas/01-data-import/`
   - Follow instructions in `code/README.md`

5. **Run analyses**
   - Execute SAS scripts in numerical order (01 → 06)
   - Review outputs in `output/` directory

---

## 📊 Analytical Workflow

### Phase 1: Descriptive Analysis
- **Objective:** Characterize historical BEV adoption and infrastructure deployment
- **Outputs:** 
  - Time series trends (statewide and county-level)
  - Geographic distribution maps
  - Summary statistics by urban/rural classification

### Phase 2: Diagnostic Analysis
- **Objective:** Identify where infrastructure gaps exist and their severity
- **Key Metrics:**
  - BEVs per charging station (accessibility metric)
  - BEVs per kW capacity (utilization pressure metric)
  - County classification: Well-Aligned, Emerging Strain, High Strain
- **Outputs:**
  - County-level gap severity rankings
  - Urban vs. rural disparity analysis
  - Zero-infrastructure county identification

### Phase 3: Predictive Analysis
- **Objective:** Forecast future BEV adoption to anticipate infrastructure needs
- **Methods:**
  - County-level ARIMA time series forecasting
  - Weighted MAPE: 2.73% (high accuracy)
  - Horizon: Through June 2028
- **Outputs:**
  - Forecasted BEV registrations by county-month
  - Confidence intervals (±2σ)
  - Projected infrastructure gap scenarios

### Phase 4: Prescriptive Analysis
- **Objective:** Optimize infrastructure investment allocation
- **Framework:**
  - Composite scoring: Current gap + Forecasted growth + Equity considerations
  - Investment strategies by county type (urban densification, rural corridor coverage)
  - NEVI funding optimization (80/20 cost-share model)
- **Outputs:**
  - High-priority county rankings
  - Deployment strategy recommendations
  - Budget allocation scenarios

---

## 📄 Competition Deliverables

### Paper Structure (4-5 pages + 2-page appendix)
1. **Introduction** (½ page) - Problem framing, stakes, preview
2. **Problem Statement** (½ page) - Research questions, significance
3. **Data** (½ page) - Sources, structure, scope
4. **Data Cleaning & Validation** (½ page) - Quality assessment, processing
5. **Analysis** (1½-2 pages) - Four-phase framework execution ⭐ CORE
6. **Visualization** (brief reference) - Figures in appendix
7. **Impact & Implications** (½ page) - Policy relevance, stakeholder value
8. **Suggestions for Future Study** (¼-½ page) - Extensions, limitations
9. **Conclusion** (¼-½ page) - Key messages, call to action

**Appendix A** (1-2 pages) - Essential visualizations only

---

## 🎯 Key Differentiators

This analysis stands out through:

1. **Sophisticated Gap Metrics** - Capacity-weighted analysis (BEVs per kW) vs. simple station counts
2. **County-Level Granularity** - 100 counties × 82 months = 8,200 observations
3. **Connector-Level Detail** - 1,725 individual charging units analyzed (4.85x more granular than station-level)
4. **Equity Focus** - Urban-rural disparity analysis with Gini coefficient quantification
5. **4-Phase Completeness** - Full descriptive → diagnostic → predictive → prescriptive workflow

---

## 👥 Team

**Wolfie**  
MBA Candidate, Business & Data Analytics Concentration  
Fayetteville State University  
Background: Computer Science, 15+ years data analytics experience

**Faculty Advisor:** Dr. Xiaofeng Nie  
Course: BIDA 650 - Advanced Business Analytics

---

## 📚 References & Acknowledgments

### Data Sources
- North Carolina Department of Transportation (NCDOT) - Vehicle Registration Database
- U.S. Department of Energy, Alternative Fuels Data Center (AFDC) - Charging Infrastructure Database

### Competition Framework
- SAS Institute Inc. - Curiosity Cup 2026 Competition Guidelines
- Reference analyses from 2025 winning teams (see `docs/competition-guidelines/reference-papers/`)

### Research Support
- Anyer et al. - EV adoption modeling methodologies
- McKinsey & Company - Public EV charging station profitability analysis
- NREL - 2030 National Charging Network projections

---

## 📄 License

This project is licensed under the **Polyform Noncommercial License 1.0.0**.

You may use, copy, modify, and redistribute this software **only for non-commercial purposes**.

See the [LICENSE](LICENSE) file for full terms.

**Required Notice:**
```
Copyright © 2025 Wolfie
Licensed under the Polyform Noncommercial License 1.0.0
https://polyformproject.org/licenses/noncommercial/1.0.0
```

---

## 🔗 Links

- **SAS Curiosity Cup:** https://www.sas.com/curiositycup
- **Competition Guidelines:** [docs/competition-guidelines/curiosity_cup2026finalcompetitionguidelines.pdf]
- **NCDOT Open Data:** https://ncdot.gov/data
- **AFDC Station Locator:** https://afdc.energy.gov/stations

---

## 📧 Contact

For questions about this analysis or collaboration opportunities:
- **GitHub Issues:** [Open an issue](https://github.com/yourusername/sas-cup-26/issues)
- **Competition Timeline:** Submission deadline February 22, 2026

---

**Status:** 🚧 Active Development (Dec 2025 - Feb 2026)  
**Last Updated:** December 30, 2025
