# Installation Guide
## EV Pulse NC

**START HERE** for first-time setup.

---

## Prerequisites

- Python 3.14+ installed
- Git installed
- Git LFS installed ([download](https://git-lfs.github.com/))
- GitHub account
- Terminal access

---

## Quick Start (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/wolfieman/ev-pulse-nc.git
cd ev-pulse-nc

# 2. Install Git LFS and pull large files
git lfs install
git lfs pull

# 3. Verify data files exist
ls -lh data/raw/
```

```bash
# 4. Set up Python environment with uv
#    (Install uv first if needed: https://docs.astral.sh/uv/)
uv sync

# 5. Verify
uv run python -c "import pandas; print('Ready')"
```

**Done!** You now have the full project with all data files and dependencies.

---

## Setup From Scratch

If creating a new repository (not cloning):

### Step 1: Install Git LFS

```bash
# macOS
brew install git-lfs

# Windows
# Download from https://git-lfs.github.com/

# Linux
sudo apt-get install git-lfs

# Verify
git lfs version
```

### Step 2: Create Directory Structure

```bash
mkdir -p ev-pulse-nc && cd ev-pulse-nc
mkdir -p data/{raw,processed,reference-forecasts}
mkdir -p code/python/{data-acquisition,analysis,blog}
mkdir -p docs/{eda-reports,research,internal,figures,blog}
mkdir -p frameworks scripts references
mkdir -p output/{figures,models,validation}
mkdir -p paper
```

For the authoritative tree, see the **Repository Structure** section of [`README.md`](README.md).

### Step 3: Initialize Git

```bash
git init
git lfs install
git lfs track "*.csv"
git lfs track "*.xlsx"
```

### Step 4: Add Files and Commit

```bash
git add .
git commit -m "Initial commit"
```

### Step 5: Push to GitHub

```bash
git remote add origin https://github.com/USERNAME/ev-pulse-nc.git
git branch -M main
git lfs push --all origin main
git push -u origin main
```

---

## Storage Overview

| Location | Contents |
|----------|----------|
| **Git LFS** | CSV, XLSX files (data) |
| **Regular Git** | Code (.py), docs (.md, .pdf, .docx) |
| **Ignored** | *.log, *.lst, __pycache__, .DS_Store |

---

## Troubleshooting

### "File too large" error
```bash
git lfs install
git rm --cached data/raw/*.csv
git add data/raw/*.csv
git commit -m "Fix: Track with LFS"
```

### LFS push fails
```bash
git lfs push --all origin main
git push
```

### Verify LFS is working
```bash
git lfs ls-files
```

---

## Daily Workflow

See [QUICK-REFERENCE.md](QUICK-REFERENCE.md) for daily commands.

---

**Last Updated:** May 2026
