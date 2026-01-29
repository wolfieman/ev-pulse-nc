#!/bin/bash

# EV Pulse NC - Repository Structure Builder
# Run this script to create the complete folder structure locally
# Usage: bash setup-repo-structure.sh

echo "🚀 Creating EV Pulse NC repository structure..."
echo ""

# Create main directory
# mkdir -p ev-pulse-nc
# cd ev-pulse-nc

# ============================================================================
# DATA DIRECTORIES
# ============================================================================
echo "📁 Creating data directories..."
mkdir -p data/raw
mkdir -p data/processed

# Create data README
cat > data/README.md << 'EOF'
# Data Directory

## Raw Data (`raw/`)

### NC_EV_PHEV_TS.csv (520 MB)
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Description:** Monthly electric vehicle (BEV) and plug-in hybrid (PHEV) registrations
- **Structure:** 8,200 observations (100 counties × 82 months)
- **Period:** September 2018 - June 2025
- **Variables:**
  - `Month`: YYYY-MM format
  - `County`: NC county name
  - `Electric`: Battery electric vehicle count (BEV) - **PRIMARY FOCUS**
  - `PlugInHybrid`: Plug-in hybrid count (PHEV) - excluded from analysis
  - `MonthDate`: Numeric month (YYYYMM)

### alt_fuel_stations_ev_charging_units.csv (695 MB)
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Description:** Connector-level EV charging infrastructure data
- **Structure:** 1,725 charging unit records from 355 unique stations
- **Coverage:** 135 cities across North Carolina, deployed 2011-2025
- **Key Variables:**
  - Station identification, network provider, location (lat/long)
  - Connector types: NACS (J3400), CCS (J1772COMBO), CHAdeMO, J1772
  - Power output (kW) per connector
  - Facility type, access type, operational status

## Processed Data (`processed/`)

Cleaned and transformed datasets generated from SAS processing scripts.

**Note:** Use Git LFS for all CSV files >100MB
EOF

# ============================================================================
# CODE DIRECTORIES
# ============================================================================
echo "💻 Creating code directories..."
mkdir -p code/sas/01-data-import
mkdir -p code/sas/02-data-prep/nc-regs
mkdir -p code/sas/02-data-prep/supply
mkdir -p code/sas/02-data-prep/shapefiles
mkdir -p code/sas/03-eda
mkdir -p code/sas/04-forecasting
mkdir -p code/sas/05-gap-analysis
mkdir -p code/sas/06-visualization
mkdir -p code/python

# Create code README
cat > code/README.md << 'EOF'
# Code Directory

## SAS Scripts (`sas/`)

Execute in numerical order:

### 01-data-import/
Data import scripts (.ctl files) for loading datasets into SAS libraries

**TODO:** Export your SAS import scripts here
- `alt-fuel-stations-import.ctl`
- `ev_charging_units-import.ctl`
- `nc_ev_phev_ts-import.ctl`

### 02-data-prep/
Data cleaning, validation, and transformation

- `nc-regs/` - BEV registration data processing
- `supply/` - Charging infrastructure processing
- `shapefiles/` - Geographic data handling (if used)

**TODO:** Export your data prep .sas scripts here

### 03-eda/
Exploratory data analysis scripts

**TODO:** Export your EDA .sas scripts here

### 04-forecasting/
Time series forecasting models (ARIMA, Exponential Smoothing)

**TODO:** Export your forecasting .sas scripts here

### 05-gap-analysis/
Diagnostic gap metrics and county classification

**TODO:** Export your gap analysis .sas scripts here

### 06-visualization/
Chart and map generation code

**TODO:** Export your visualization .sas scripts here

## Python Scripts (`python/`)

**Status:** Future development
EOF

# Create placeholder files
touch code/sas/01-data-import/PLACEHOLDER-import-scripts.txt
touch code/sas/02-data-prep/PLACEHOLDER-prep-scripts.txt
touch code/sas/03-eda/PLACEHOLDER-eda-scripts.txt
touch code/sas/04-forecasting/PLACEHOLDER-forecast-scripts.txt
touch code/sas/05-gap-analysis/PLACEHOLDER-gap-analysis-scripts.txt
touch code/sas/06-visualization/PLACEHOLDER-viz-scripts.txt

# ============================================================================
# DOCS DIRECTORIES
# ============================================================================
echo "📝 Creating documentation directories..."
mkdir -p docs/planning
mkdir -p docs/eda-reports
mkdir -p docs/research

# ============================================================================
# OUTPUT DIRECTORIES
# ============================================================================
echo "📊 Creating output directories..."
mkdir -p output/figures
mkdir -p output/tables
mkdir -p output/models

# Create output README
cat > output/README.md << 'EOF'
# Output Directory

## Figures (`figures/`)
Visualizations for paper appendix (max 2 pages)

**TODO:** Export your generated figures here
- BEV growth trajectory charts
- County-level gap severity maps
- Forecasted scenario ribbon charts
- Network provider comparisons

## Tables (`tables/`)
Summary statistics and results tables

**TODO:** Export your generated tables here

## Models (`models/`)
Saved forecasting model artifacts and evaluation metrics

**TODO:** Save your model outputs here
EOF

touch output/figures/PLACEHOLDER-figures-here.txt
touch output/tables/PLACEHOLDER-tables-here.txt

# ============================================================================
# PAPER DIRECTORY
# ============================================================================
echo "📄 Creating paper directory..."
mkdir -p paper

cat > paper/README.md << 'EOF'
# Research Paper

## Requirements
- **Main Text:** 2-5 pages (target: 4 pages)
- **Appendix:** Optional, up to 2 pages for visualizations
- **Format:** Word document (.docx) or PDF

## Structure
1. Introduction (½ page)
2. Problem Statement (½ page)
3. Data (½ page)
4. Data Cleaning & Validation (½ page)
5. Analysis (1½-2 pages) ⭐ CORE SECTION
6. Visualization (brief text reference)
7. Impact & Implications (½ page)
8. Suggestions for Future Study (¼-½ page)
9. Conclusion (¼-½ page)

**Appendix A:** Supporting visualizations (1-2 pages max)
EOF

# ============================================================================
# REFERENCES DIRECTORY
# ============================================================================
echo "📚 Creating references directory..."
cat > references/data-sources.md << 'EOF'
# Data Sources & References

## Primary Data Sources

### 1. North Carolina Electric Vehicle Registrations
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Dataset:** NC_EV_PHEV_TS.csv
- **URL:** https://ncdot.gov/data (verify actual source)
- **Coverage:** September 2018 - June 2025 (82 months)
- **Granularity:** County-month panel data (100 counties × 82 months = 8,200 observations)

### 2. Alternative Fuel Stations - Electric Vehicle Charging
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Dataset:** alt_fuel_stations_ev_charging_units.csv
- **URL:** https://afdc.energy.gov/stations
- **Coverage:** 355 stations, 1,725 connector records
- **Updated:** 2025

## Supporting Research

- Anyer et al. - EV adoption modeling methodologies
- McKinsey & Company - Public EV charging station profitability analysis
- NREL - 2030 National Charging Network projections
- NEVI Formula Program guidelines - Federal infrastructure funding
EOF

# ============================================================================
# ROOT FILES
# ============================================================================
echo "📋 Creating root configuration files..."

# Create .gitattributes for Git LFS
cat > .gitattributes << 'EOF'
# Git LFS tracking rules for large data files
# Install Git LFS before committing: git lfs install

# Track all CSV files with Git LFS
*.csv filter=lfs diff=lfs merge=lfs -text

# Track Excel files with Git LFS
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xls filter=lfs diff=lfs merge=lfs -text

# Track SAS data files with Git LFS
*.sas7bdat filter=lfs diff=lfs merge=lfs -text
*.sas7bcat filter=lfs diff=lfs merge=lfs -text
EOF

# Create initial commit checklist
cat > SETUP-CHECKLIST.md << 'EOF'
# Setup Checklist for ev-pulse-nc

## ✅ Pre-Commit Checklist

- [ ] Install Git LFS: `git lfs install`
- [ ] Copy dataset files to `data/raw/`
  - [ ] NC_EV_PHEV_TS.csv (520 MB)
  - [ ] alt_fuel_stations_ev_charging_units.csv (695 MB)
- [ ] Copy project documents to `docs/`
  - [ ] planning/ (execution plan, outline)
  - [ ] eda-reports/ (3 EDA PDFs)
  - [ ] research/ (supporting papers)
- [ ] Export SAS code scripts to `code/sas/`
- [ ] Verify `.gitignore` and `.gitattributes` in place
- [ ] Update README.md with your GitHub username in URLs

## 🚀 Git Setup Commands

```bash
# Initialize repository
git init

# Install Git LFS
git lfs install

# Track large files
git lfs track "*.csv"
git lfs track "*.xlsx"

# Stage all files
git add .

# Initial commit
git commit -m "Initial commit: EV Pulse NC research project structure"

# Create GitHub repo (via web or gh CLI)
gh repo create ev-pulse-nc --public --source=. --remote=origin

# Or manually add remote
git remote add origin https://github.com/yourusername/ev-pulse-nc.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 📦 What Gets Committed

### ✅ INCLUDE (committed to Git)
- All code (.sas, .ctl, .py)
- Documentation (.md, .docx, .pdf in docs/)
- README, LICENSE, .gitignore, .gitattributes
- Folder structure and placeholder files
- Paper drafts

### ⚠️ LARGE FILES (committed via Git LFS)
- data/raw/*.csv (tracked by LFS)
- data/raw/*.xlsx (tracked by LFS)

### ❌ EXCLUDE (ignored by .gitignore)
- SAS temporary files (*.log, *.lst)
- Python cache (__pycache__)
- OS files (.DS_Store, Thumbs.db)
- Scratch/temp folders

## 📊 Verify Git LFS

After first commit, verify LFS is working:

```bash
git lfs ls-files
# Should show your CSV files

git lfs env
# Verify LFS is installed and configured
```
EOF

echo ""
echo "✅ Repository structure created successfully!"
echo ""
echo "📂 Directory tree:"
tree -L 2 -a

echo ""
echo "🎯 NEXT STEPS:"
echo "1. Review SETUP-CHECKLIST.md"
echo "2. Copy your data files to data/raw/"
echo "3. Copy your documents to docs/"
echo "4. Export SAS scripts to code/sas/"
echo "5. Install Git LFS: git lfs install"
echo "6. Initialize Git: git init"
echo "7. Stage and commit: git add . && git commit -m 'Initial commit'"
echo ""
echo "📖 See SETUP-CHECKLIST.md for detailed Git setup commands"
echo ""
