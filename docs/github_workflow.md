# GitHub Workflow for JedgeBot

## **Branching Strategy**
- **`main`** → Stable production-ready code.
- **`dev`** → Active development branch.
- **Feature branches (`feature/xyz`)** → For individual tasks.

---

## **GitHub Development Workflow**

### ✅ 1. Create a New Repository
```bash
git init
git remote add origin https://github.com/512jay/jedgebot.git
```

### ✅ 2. Create a Development Branch
```bash
git checkout -b dev
```

### ✅ 3. Work on a Feature
```bash
git checkout -b feature/tastytrade-api
```
After coding, commit changes:
```bash
git add .
git commit -m "Added TastyTrade API integration"
```
Push to GitHub:
```bash
git push origin feature/tastytrade-api
```

### ✅ 4. Merge Back to `dev`
After testing, merge it back:
```bash
git checkout dev
git merge feature/tastytrade-api
git push origin dev
```
Once stable, merge to `main`:
```bash
git checkout main
git merge dev
git push origin main
```

---

## **Best Practices**
✅ **Use Issues & Project Board** – Track features, bugs, and improvements.
✅ **Write Clear Commit Messages** – Describe changes concisely.
✅ **Pull Requests (PRs) for Merges** – Keep `main` and `dev` stable.
✅ **Use `.gitignore`** – Ignore `venv/`, `.env`, `__pycache__/`.
✅ **Automate with GitHub Actions** – For CI/CD pipelines (later).

---
