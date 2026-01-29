#!/bin/bash

# EV Pulse NC - Repository Structure Builder
# Run this script to create the complete folder structure locally
# Usage: bash setup-repo-structure.sh

echo "🚀 Creating EV Pulse NC repository structure..."
echo ""

# ============================================================================
# DATA DIRECTORIES
# ============================================================================
echo "📁 Creating data directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/generated

# Create data README
cat > data/README.md << 'EOF'
# Data Directory

## Raw Data (`raw/`)

### NC_EV_PHEV_TS.csv
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Description:** Monthly electric vehicle (BEV) and plug-in hybrid (PHEV) registrations
- **Structure:** 8,200 observations (100 counties × 82 months)
- **Period:** September 2018 - June 2025

### alt_fuel_stations_ev_charging_units.csv
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Description:** Connector-level EV charging infrastructure data
- **Structure:** 1,725 charging unit records from 355 unique stations

## Processed Data (`processed/`)

Cleaned and transformed datasets.

## Generated Data (`generated/`)

Analysis outputs and derived datasets.

**Note:** CSV and XLSX files are tracked by Git LFS.
EOF

# ============================================================================
# CODE DIRECTORIES
# ============================================================================
echo "💻 Creating code directories..."
mkdir -p code/python/data-acquisition
mkdir -p code/python/data-cleaning
mkdir -p code/python/analysis
mkdir -p code/python/visualization

# Create code README
cat > code/README.md << 'EOF'
# Code Directory

## Python Scripts (`python/`)

### data-acquisition/
Scripts for downloading and fetching data from sources.

### data-cleaning/
Data cleaning, validation, and transformation scripts.

### analysis/
Core analysis scripts:
- Exploratory data analysis
- Descriptive statistics
- Diagnostic gap analysis
- Predictive modeling (ARIMA forecasting)
- Prescriptive recommendations

### visualization/
Chart and map generation code.

## Running the Analysis

```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Run scripts in order
python code/python/data-cleaning/consolidate_zev_monthly.py
# ... additional scripts
```
EOF

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
Visualizations for paper appendix.

## Tables (`tables/`)
Summary statistics and results tables.

## Models (`models/`)
Saved forecasting model artifacts and evaluation metrics.
EOF

# ============================================================================
# PAPER DIRECTORY
# ============================================================================
echo "📄 Creating paper directory..."
mkdir -p paper

cat > paper/README.md << 'EOF'
# Research Paper

## Structure
1. Introduction
2. Problem Statement
3. Data
4. Data Cleaning & Validation
5. Analysis (5-phase framework)
6. Visualization
7. Impact & Implications
8. Suggestions for Future Study
9. Conclusion

**Appendix:** Supporting visualizations
EOF

# ============================================================================
# REFERENCES DIRECTORY
# ============================================================================
echo "📚 Creating references directory..."
mkdir -p references

cat > references/data-sources.md << 'EOF'
# Data Sources & References

## Primary Data Sources

### 1. North Carolina Electric Vehicle Registrations
- **Source:** North Carolina Department of Transportation (NCDOT)
- **Coverage:** September 2018 - June 2025 (82 months)
- **Granularity:** County-month panel data

### 2. Alternative Fuel Stations - Electric Vehicle Charging
- **Source:** U.S. Department of Energy, Alternative Fuels Data Center (AFDC)
- **Coverage:** 355 stations, 1,725 connector records

## Supporting Research
- McKinsey & Company - Public EV charging station profitability analysis
- NREL - 2030 National Charging Network projections
- NEVI Formula Program guidelines
EOF

# ============================================================================
# ROOT FILES
# ============================================================================
echo "📋 Creating root configuration files..."

# Create .gitattributes for Git LFS
cat > .gitattributes << 'EOF'
# Git LFS tracking rules for large data files
*.csv filter=lfs diff=lfs merge=lfs -text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xls filter=lfs diff=lfs merge=lfs -text
*.shp filter=lfs diff=lfs merge=lfs -text
*.shx filter=lfs diff=lfs merge=lfs -text
*.dbf filter=lfs diff=lfs merge=lfs -text
*.prj filter=lfs diff=lfs merge=lfs -text
*.cpg filter=lfs diff=lfs merge=lfs -text
EOF

echo ""
echo "✅ Repository structure created successfully!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Copy your data files to data/raw/"
echo "2. Copy your documents to docs/"
echo "3. Set up Python: python -m venv .venv && pip install -r requirements.txt"
echo "4. Initialize Git: git init && git lfs install"
echo "5. Stage and commit: git add . && git commit -m 'Initial commit'"
echo ""
echo "📖 See INSTALLATION.md for detailed setup instructions"
echo ""
