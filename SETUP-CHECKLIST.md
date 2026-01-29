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
