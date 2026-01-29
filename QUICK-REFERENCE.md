# Quick Reference
## EV Pulse NC - Daily Commands

---

## Daily Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push
```

---

## Useful Commands

```bash
# View recent commits
git log --oneline -5

# See what changed
git diff

# Verify LFS files
git lfs ls-files

# Pull latest changes
git pull
```

---

## File Locations

```
data/raw/          <- Raw datasets (CSV, XLSX)
data/processed/    <- Cleaned data
code/python/       <- Python scripts
docs/              <- Documentation
output/figures/    <- Generated visualizations
paper/             <- Research paper
```

---

## Remember

- Commit often with descriptive messages
- Push daily during active work
- Don't commit *.log or *.lst files
- Large files (CSV, XLSX) are tracked by Git LFS automatically

---

**First-time setup?** See [INSTALLATION.md](INSTALLATION.md)
