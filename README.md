# EV Pulse NC: North Carolina Electric Vehicle Analytics

📊 **Focus:** Data-driven analysis of North Carolina's electric vehicle adoption and charging infrastructure
🎯 **Objective:** Quantify the alignment between North Carolina's electric vehicle adoption growth and public charging infrastructure deployment

---

## 🚗 Project Overview

North Carolina's battery electric vehicle (BEV) fleet has experienced explosive growth, expanding from 5,165 vehicles in September 2018 to 94,371 in June 2025—a **1,727% increase** with a **53.8% compound annual growth rate (CAGR)**. However, public charging infrastructure has not kept pace, creating a widening gap that threatens the equitable transition to electric mobility.

This project applies a comprehensive **5-phase analytics framework**—exploratory, descriptive, diagnostic, predictive, and prescriptive analysis—to:

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
- **Python** - Primary analytics platform
  - pandas - Data manipulation and cleaning
  - statsmodels - Time series forecasting (ARIMA/Exponential Smoothing)
  - matplotlib/seaborn - Statistical visualization
  - geopandas - Geographic analysis
  - requests, openpyxl - Data acquisition
- **Excel** - Initial data profiling and validation

### Analytical Framework
1. **Exploratory Analysis** - Data profiling, quality assessment, initial patterns
2. **Descriptive Analysis** - Historical trends, distributions, geographic patterns
3. **Diagnostic Analysis** - Gap identification, county classification, equity assessment
4. **Predictive Analysis** - County-level BEV forecasting (Sept 2018 - June 2028)
5. **Prescriptive Analysis** - Investment optimization, deployment prioritization

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
ev-pulse-nc/
├── README.md                     # This file
├── INSTALLATION.md               # Setup guide
├── QUICK-REFERENCE.md            # Daily workflow commands
├── LICENSE                       # Polyform Noncommercial License 1.0.0
├── NOTICE.md                     # Copyright notice
├── .gitignore                    # Git ignore patterns
├── .gitattributes                # Git LFS tracking rules
│
├── data/                         # Dataset directory (Git LFS)
│   ├── raw/                      # Original datasets
│   ├── processed/                # Cleaned/transformed data
│   ├── generated/                # Analysis outputs
│   └── README.md                 # Data dictionary & sources
│
├── code/                         # Analysis code
│   ├── python/                   # Python scripts
│   │   ├── data-acquisition/     # Data download scripts
│   │   └── data-cleaning/        # Data consolidation scripts
│   └── README.md                 # Code execution guide
│
├── docs/                         # Project documentation
│   ├── planning/                 # Project plans and outlines
│   ├── eda-reports/              # Exploratory data analysis reports
│   └── research/                 # Supporting research papers
│
├── output/                       # Generated outputs
│   ├── figures/                  # Visualizations for paper
│   ├── tables/                   # Summary statistics tables
│   └── models/                   # Saved forecasting artifacts
│
├── paper/                        # Research paper
│
└── references/                   # Supporting materials
    └── data-sources.md           # Citations & links
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git with Git LFS extension

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/wolfieman/ev-pulse-nc.git
   cd ev-pulse-nc
   ```

2. **Install Git LFS and pull data**
   ```bash
   git lfs install
   git lfs pull
   ```

3. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install pandas statsmodels matplotlib seaborn geopandas
   ```

4. **Verify data files**
   ```bash
   ls -lh data/raw/
   ```

---

## 📊 Analytical Workflow

### Phase 1: Exploratory Analysis
- **Objective:** Profile data quality, identify patterns, and assess completeness
- **Outputs:**
  - Data quality reports
  - Missing value analysis
  - Initial visualizations and distributions

### Phase 2: Descriptive Analysis
- **Objective:** Characterize historical BEV adoption and infrastructure deployment
- **Outputs:** 
  - Time series trends (statewide and county-level)
  - Geographic distribution maps
  - Summary statistics by urban/rural classification

### Phase 3: Diagnostic Analysis
- **Objective:** Identify where infrastructure gaps exist and their severity
- **Key Metrics:**
  - BEVs per charging station (accessibility metric)
  - BEVs per kW capacity (utilization pressure metric)
  - County classification: Well-Aligned, Emerging Strain, High Strain
- **Outputs:**
  - County-level gap severity rankings
  - Urban vs. rural disparity analysis
  - Zero-infrastructure county identification

### Phase 4: Predictive Analysis
- **Objective:** Forecast future BEV adoption to anticipate infrastructure needs
- **Methods:**
  - County-level ARIMA time series forecasting
  - Weighted MAPE: 2.73% (high accuracy)
  - Horizon: Through June 2028
- **Outputs:**
  - Forecasted BEV registrations by county-month
  - Confidence intervals (±2σ)
  - Projected infrastructure gap scenarios

### Phase 5: Prescriptive Analysis
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

## 📄 Report Structure

### Analysis Report Organization
1. **Introduction** - Problem framing, stakes, preview
2. **Problem Statement** - Research questions, significance
3. **Data** - Sources, structure, scope
4. **Data Cleaning & Validation** - Quality assessment, processing
5. **Analysis** - Five-phase framework execution
6. **Visualization** - Figures in appendix
7. **Impact & Implications** - Policy relevance, stakeholder value
8. **Suggestions for Future Study** - Extensions, limitations
9. **Conclusion** - Key messages, call to action

**Appendix** - Essential visualizations

---

## 🎯 Key Differentiators

This analysis stands out through:

1. **Sophisticated Gap Metrics** - Capacity-weighted analysis (BEVs per kW) vs. simple station counts
2. **County-Level Granularity** - 100 counties × 82 months = 8,200 observations
3. **Connector-Level Detail** - 1,725 individual charging units analyzed (4.85x more granular than station-level)
4. **Equity Focus** - Urban-rural disparity analysis with Gini coefficient quantification
5. **5-Phase Completeness** - Full exploratory → descriptive → diagnostic → predictive → prescriptive workflow

---

## 👥 Team

**Wolfgang Sanyer**<br>
MBA Candidate, Business & Data Analytics Concentration<br>
Fayetteville State University<br>
Background: Computer Science, 15+ years data analytics experience

**Braeden Baker**<br>
MBA Candidate, Business & Data Analytics Concentration<br>
Fayetteville State University<br>
Background: Finance

**Faculty Advisor:** Dr. Majed Al-Ghandour<br>
**Course:** BIDA-670

---

## 📚 References & Acknowledgments

### Data Sources
- North Carolina Department of Transportation (NCDOT) - Vehicle Registration Database
- U.S. Department of Energy, Alternative Fuels Data Center (AFDC) - Charging Infrastructure Database

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
Copyright © 2025 Wolfgang Sanyer
Licensed under the Polyform Noncommercial License 1.0.0
https://polyformproject.org/licenses/noncommercial/1.0.0
```

---

## 🔗 Links

- **NCDOT Open Data:** https://ncdot.gov/data
- **AFDC Station Locator:** https://afdc.energy.gov/stations

---

## 📧 Contact

For questions about this analysis or collaboration opportunities:
- **GitHub Issues:** [Open an issue](https://github.com/wolfieman/ev-pulse-nc/issues)

---

**Status:** 🚧 Active Development
**Last Updated:** January 2026
