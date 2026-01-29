# Quick Reference Card
## ev-pulse-nc - Essential Commands

---

## 🚀 ONE-TIME SETUP (First Time)

```bash
# 1. Install Git LFS
brew install git-lfs              # macOS
# OR download from https://git-lfs.github.com/

# 2. Run setup script
chmod +x setup-repo-structure.sh
bash setup-repo-structure.sh

# 3. Copy your files
cp /path/to/NC_EV_PHEV_TS.csv data/raw/
cp /path/to/alt_fuel_stations_ev_charging_units.csv data/raw/
cp /path/to/*.docx docs/planning/
cp /path/to/*.pdf docs/eda-reports/
# ... (see LOCAL-SETUP-GUIDE.md for complete list)

# 4. Initialize Git + LFS
git init
git lfs install
git lfs track "*.csv"

# 5. Create GitHub repo (via web: github.com/new)
# Name: ev-pulse-nc
# Public, no README

# 6. Initial commit and push
git add .
git commit -m "Initial commit: EV Pulse NC research project"
git remote add origin https://github.com/YOUR_USERNAME/ev-pulse-nc.git
git branch -M main
git push -u origin main
```

---

## 📝 DAILY WORKFLOW (After Setup)

```bash
# Check status
git status

# Add changes
git add .
# OR add specific files:
git add code/sas/04-forecasting/arima-model.sas

# Commit with message
git commit -m "Add county-level ARIMA forecasting model"

# Push to GitHub
git push
```

---

## 🔍 VERIFICATION COMMANDS

```bash
# Verify Git LFS is working
git lfs ls-files
# Should show: data/raw/NC_EV_PHEV_TS.csv
#              data/raw/alt_fuel_stations_ev_charging_units.csv

# Verify LFS tracking rules
git lfs track
# Should show: *.csv, *.xlsx

# Check repository status
git status

# View commit history
git log --oneline
```

---

## 🆘 TROUBLESHOOTING

### LFS file not tracked
```bash
git rm --cached data/raw/*.csv
git add data/raw/*.csv
git commit -m "Fix: Track CSV with LFS"
```

### Wrong remote URL
```bash
git remote -v  # Check current
git remote set-url origin https://github.com/YOUR_USERNAME/ev-pulse-nc.git
```

### Undo last commit (not pushed yet)
```bash
git reset --soft HEAD~1
```

---

## 📂 FILE LOCATIONS REMINDER

```
data/raw/          ← Your 2 CSV files (1.2GB)
docs/planning/     ← execution-plan, outline
docs/eda-reports/  ← 3 EDA PDFs
code/sas/          ← Export your .sas and .ctl files here
output/figures/    ← Save generated visualizations here
paper/             ← Write final paper here
```

---

## ⚡ ESSENTIAL GIT CONCEPTS

- **`git add`** - Stage changes (prepare for commit)
- **`git commit`** - Save changes locally
- **`git push`** - Upload to GitHub
- **Git LFS** - Handles files >100MB
- **`.gitignore`** - Files to exclude (temp files, logs)

---

## 🎯 REMEMBER

✅ Commit often (after each meaningful change)  
✅ Use descriptive commit messages  
✅ Push regularly (daily during sprint)  
✅ Verify LFS is tracking large files  
❌ Don't commit passwords/API keys  
❌ Don't commit *.log or *.lst files  

---

**Full Instructions:** See LOCAL-SETUP-GUIDE.md
