# LOCAL Repository Setup Guide
## EV Pulse NC - `ev-pulse-nc`

**For macOS/Linux/Windows users**

---

## 🎯 OVERVIEW

You will create this repository **locally** on your computer, then push to GitHub.

**Critical Requirements:**
- ✅ Git installed
- ✅ Git LFS installed (for 1.2GB+ datasets)
- ✅ GitHub account
- ✅ Terminal/command line access

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### STEP 1: Install Git LFS

Your datasets are **too large** for regular Git (520MB + 695MB = 1.2GB+).

**macOS (Homebrew):**
```bash
brew install git-lfs
```

**macOS (Manual):**
Download from https://git-lfs.github.com/

**Windows:**
Download installer from https://git-lfs.github.com/

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install git-lfs
```

**Verify installation:**
```bash
git lfs version
# Should show: git-lfs/3.x.x
```

---

### STEP 2: Download Repository Files

I've created 4 key files for you:

1. `.gitignore` - Ignores temporary files, keeps repo clean
2. `README.md` - Professional project documentation
3. `LICENSE` - Your Polyform Noncommercial License (unchanged)
4. `NOTICE.md` - Copyright notice (updated for this project)

**Download these files from this conversation** and save them locally.

---

### STEP 3: Run the Setup Script

**Option A: Automatic (Recommended)**

1. Download `setup-repo-structure.sh` from this conversation
2. Make it executable and run:

```bash
chmod +x setup-repo-structure.sh
bash setup-repo-structure.sh
```

This creates the entire folder structure automatically.

**Option B: Manual**

If the script doesn't work, create folders manually:

```bash
mkdir -p ev-pulse-nc
cd ev-pulse-nc

# Create all directories
mkdir -p data/{raw,processed}
mkdir -p code/sas/{01-data-import,02-data-prep/{nc-regs,supply,shapefiles},03-eda,04-forecasting,05-gap-analysis,06-visualization}
mkdir -p code/python
mkdir -p docs/{planning,eda-reports,competition-guidelines/reference-papers,research}
mkdir -p output/{figures,tables,models}
mkdir -p paper
mkdir -p references/competitor-analyses
```

Then copy the 4 downloaded files (`.gitignore`, `README.md`, `LICENSE`, `NOTICE.md`) into `ev-pulse-nc/`

---

### STEP 4: Copy Your Project Files

**Copy datasets to `data/raw/`:**
```bash
cd ev-pulse-nc
cp /path/to/NC_EV_PHEV_TS.csv data/raw/
cp /path/to/alt_fuel_stations_ev_charging_units.csv data/raw/
```

**Copy documents to `docs/`:**
```bash
# Planning documents
cp /path/to/execution-plan-v01.docx docs/planning/
cp /path/to/outline-v03.docx docs/planning/
cp /path/to/curiosity-cup-2026-paper-outline.md docs/planning/

# EDA reports
cp /path/to/ncevregistrationseda.pdf docs/eda-reports/
cp /path/to/altfuelstationseda.pdf docs/eda-reports/
cp /path/to/enhancedchargingunitseda.pdf docs/eda-reports/

# Competition materials
cp /path/to/curiosity_cup2026finalcompetitionguidelines.pdf docs/competition-guidelines/

# Reference papers
cp /path/to/teamdatamindcuriositycup2025.pdf docs/competition-guidelines/reference-papers/
cp /path/to/teammachinelearningdynamite_curiositycup2025.pdf docs/competition-guidelines/reference-papers/
cp /path/to/teamdataacescuriositycup2025.pdf docs/competition-guidelines/reference-papers/

# Research papers
cp /path/to/evpapersanyeretal.pdf docs/research/
```

**Export SAS code** (when ready):
- Export your `.ctl` files to `code/sas/01-data-import/`
- Export your `.sas` scripts to appropriate subdirectories in `code/sas/`

---

### STEP 5: Initialize Git with LFS

**From inside `ev-pulse-nc/` directory:**

```bash
# Initialize Git repository
git init

# Initialize Git LFS
git lfs install

# Verify .gitattributes exists (should be created by setup script)
cat .gitattributes
# Should show:
# *.csv filter=lfs diff=lfs merge=lfs -text
# *.xlsx filter=lfs diff=lfs merge=lfs -text

# If .gitattributes is missing, create it:
cat > .gitattributes << 'EOF'
*.csv filter=lfs diff=lfs merge=lfs -text
*.xlsx filter=lfs diff=lfs merge=lfs -text
*.xls filter=lfs diff=lfs merge=lfs -text
*.sas7bdat filter=lfs diff=lfs merge=lfs -text
*.sas7bcat filter=lfs diff=lfs merge=lfs -text
EOF

# Track large files with LFS
git lfs track "*.csv"
git lfs track "*.xlsx"

# Verify LFS tracking
git lfs track
# Should show:
# Listing tracked patterns
#     *.csv (.gitattributes)
#     *.xlsx (.gitattributes)
```

---

### STEP 6: Create GitHub Repository

**Option A: GitHub Web Interface**

1. Go to https://github.com/new
2. Repository name: **`ev-pulse-nc`**
3. Description: *SAS Curiosity Cup 2026: North Carolina EV Infrastructure Gap Analysis*
4. **Public** repository (you said no payment)
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

**Option B: GitHub CLI** (if installed)

```bash
gh repo create ev-pulse-nc \
  --public \
  --description "SAS Curiosity Cup 2026: North Carolina EV Infrastructure Gap Analysis" \
  --source=. \
  --remote=origin
```

---

### STEP 7: Stage and Commit

```bash
# Verify what will be committed
git status

# Add all files
git add .

# Verify LFS is tracking large files
git lfs ls-files
# Should show your CSV files (after git add)

# Create initial commit
git commit -m "Initial commit: SAS Curiosity Cup 2026 project structure

- Complete folder structure for 4-phase analytics workflow
- Project documentation and planning materials
- EDA reports and competition guidelines
- Large datasets tracked with Git LFS (1.2GB+)
- SAS code structure ready for script export"
```

---

### STEP 8: Push to GitHub

**If you created repo via web interface:**

```bash
# Add remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/ev-pulse-nc.git

# Verify remote
git remote -v

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you used GitHub CLI:**

```bash
# Already configured, just push
git push -u origin main
```

**⚠️ IMPORTANT:** First push with LFS may take 5-10 minutes due to large files.

---

### STEP 9: Verify on GitHub

1. Go to https://github.com/yourusername/ev-pulse-nc
2. Verify folder structure visible
3. Check that CSV files show LFS badge (small "LFS" indicator)
4. Click on `data/raw/NC_EV_PHEV_TS.csv` - should say "Stored with Git LFS"

---

## 🔍 TROUBLESHOOTING

### Problem: "File too large" error

**Solution:**
```bash
# Make sure Git LFS is installed
git lfs install

# Verify .gitattributes exists
cat .gitattributes

# If files were already committed without LFS:
git rm --cached data/raw/*.csv
git add data/raw/*.csv
git commit -m "Fix: Track CSV files with Git LFS"
```

### Problem: LFS bandwidth exceeded (GitHub free tier)

**Solution 1:** Use Git LFS bandwidth pack (costs money)

**Solution 2:** Store large files elsewhere and provide download links in README

**Solution 3:** Use alternative hosting like AWS S3, Dropbox, or Google Drive with links

### Problem: Can't find downloaded files

Check your browser's Downloads folder. Files are:
- `.gitignore` (no extension, hidden file)
- `README.md`
- `LICENSE`
- `NOTICE.md`
- `setup-repo-structure.sh`

---

## 📊 WHAT GETS STORED WHERE

### Git LFS (Large File Storage) - ~1.2GB
- `data/raw/NC_EV_PHEV_TS.csv` (520 MB)
- `data/raw/alt_fuel_stations_ev_charging_units.csv` (695 MB)

### Regular Git - ~50-100MB
- All code files (.sas, .ctl, .py)
- Documentation (.md, .docx, .pdf)
- Folder structure
- Configuration files

### Not Stored (in .gitignore)
- SAS temporary files (*.log, *.lst)
- Python cache
- OS files (.DS_Store)

---

## 🚀 ONGOING WORKFLOW

After initial setup, your workflow is:

```bash
# Make changes to code/docs
# ...

# Stage changes
git add .

# Commit
git commit -m "Descriptive message about what changed"

# Push to GitHub
git push
```

---

## 🎯 NEXT STEPS

1. ✅ Verify repository on GitHub
2. ✅ Update README.md line 165 with your GitHub username
3. ✅ Export SAS code to `code/sas/` subdirectories
4. ✅ Generate visualizations to `output/figures/`
5. ✅ Write competition paper in `paper/`
6. ✅ Commit and push changes as you work

---

## 📞 NEED HELP?

- Git LFS docs: https://git-lfs.github.com/
- GitHub docs: https://docs.github.com/
- SAS Curiosity Cup: https://www.sas.com/curiositycup

---

**Created:** December 30, 2025  
**Project Deadline:** February 22, 2026
