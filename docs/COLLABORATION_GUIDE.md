# InfoFlow Simulator Team Collaboration Guide

---

## 1. The Three Repositories

| Repository | Who Uses It | Purpose |
| :--- | :--- | :--- |
| **Upstream (Main Repo)** | Everyone | `https://github.com/yc-eagle/infoflow-simulator` — The "official version" where all code ultimately merges |
| **Origin (Your Fork)** | Each individual | `https://github.com/[your-username]/infoflow-simulator` — Your personal copy under your own GitHub account |
| **Local** | Each individual | The project folder on your own computer |

---

## 2. First-Time Setup (One Time Only)

**Step 1: Fork the main repository**

Go to `https://github.com/yc-eagle/infoflow-simulator` and click the **Fork** button in the top-right corner. Wait a few seconds — you will see a copy of the repository under your own GitHub account.

**Step 2: Clone to your local computer**

```bash
git clone https://github.com/[your-github-username]/infoflow-simulator.git
cd infoflow-simulator
```

**Step 3: Add the main repository as "upstream"**

```bash
git remote add upstream https://github.com/yc-eagle/infoflow-simulator.git
```

**Step 4: Verify the configuration**

```bash
git remote -v
```

You should see output like this:

```
origin    https://github.com/your-username/infoflow-simulator.git (fetch)
origin    https://github.com/your-username/infoflow-simulator.git (push)
upstream  https://github.com/yc-eagle/infoflow-simulator.git (fetch)
upstream  https://github.com/yc-eagle/infoflow-simulator.git (push)
```

---

## 3. Daily Workflow (The Golden Rule)

**Core principle: NEVER write code directly on the local `main` branch!**

### Every day before starting work (15 seconds)

```bash
git checkout main           # Switch to main branch
git pull upstream main      # Pull the latest code from the main repo
git push origin main        # Sync your own fork
```

### Every time you start a new task (e.g., "write SQL queries")

```bash
git checkout -b feature/your-task-name   # e.g., feature/sql-queries
```

This creates an independent branch. All your changes stay in this branch and will not affect anyone else.

### After writing code, save and commit

```bash
git add .                          # Stage all changes
git commit -m "feat: describe what you did in English"
```

**Commit message conventions:**

| Prefix | Use Case |
| :--- | :--- |
| `feat: add simulation engine logic` | New feature |
| `fix: resolve dashboard data loading issue` | Bug fix |
| `docs: update README with setup instructions` | Documentation |
| `style: adjust chart color scheme` | Formatting/style |

### Push your changes to your GitHub fork

```bash
git push origin feature/your-task-name
```

### Finally, open a Pull Request on GitHub

1. Go to the main repository page (`https://github.com/yc-eagle/infoflow-simulator`)
2. Click **Pull Requests → New Pull Request**
3. Click **"compare across forks"**
4. **base** repository: `yc-eagle/infoflow-simulator` with branch `main`
5. **head** repository: your fork with your branch name
6. Fill in the PR description (see template below)
7. Click **Create Pull Request**

**PR description template:**

```
## What I did
- [x] Completed XXX module
- [x] Generated XXX data/charts

## What to review
- Please check if the SQL query logic is correct
- Review the chart color scheme

## Additional notes
- None
```

### After your PR is reviewed and merged by the team lead

Your local branch is no longer needed. You can delete it:

```bash
git checkout main
git pull upstream main
git branch -d feature/your-task-name        # Delete local branch
git push origin --delete feature/your-task-name   # Delete remote branch
```

---

## 4. Common Problems & Solutions

| Problem | Solution |
| :--- | :--- |
| Accidentally changed code on `main` but haven't committed yet | `git stash` → switch to new branch → `git stash pop` |
| Accidentally changed code on `main` and already committed | `git checkout -b feature/new-branch` → go back to main → `git reset --hard upstream/main` |
| `git pull upstream main` reports a "conflict" | VSCode highlights conflicted files. Manually choose which code to keep, save, then `git add . && git commit` |
| Need to merge upstream changes into your current branch | `git fetch upstream` → `git rebase upstream/main` |
| Push fails with "rejected" | Your branch is behind remote. Run `git pull origin your-branch-name` and push again |
| Want to undo the last commit (not pushed yet) | `git reset --soft HEAD~1` |
| Want to undo the last commit (already pushed) | `git revert HEAD` |

---

## 5. Team Members & Branch Assignments

| Member | GitHub Username | Recommended Branch Name | Core Task |
| :--- | :--- | :--- | :--- |
| Yicheng Jiang (Team Lead) | yc-eagle | `feature/simulation-engine` | Simulation engine, data schema, final presentation, overall integration |
| Shuoyang Jin | — | `feature/sql-model` | SQL queries, pandas cleaning, regression/classification models |
| Jiaxin Wang | — | `feature/dashboard` | Streamlit dashboard development, deployment configuration |
| Quanquan Lu | — | `feature/narrative` | Report writing, README, PPT, theoretical framing, AI usage disclosure |

**Everyone works independently on their own branch, no interference.**

---

## 6. Daily Rhythm (One Sentence Summary)

> **Before coding:** `git pull upstream main` to sync
>
> **While coding:** Work on your `feature/xxx` branch
>
> **After coding:** `git add . && git commit -m "feat: description"` + `git push origin feature/xxx`
>
> **To merge:** Open a Pull Request on GitHub, wait for the team lead to review

---

## 7. Emergency Recovery

If things go wrong and you just want to start fresh:

**Option A: Reset to the latest upstream state (discard all local changes)**

```bash
git fetch upstream
git reset --hard upstream/main
```

**Option B: Copy your changed files to a desktop backup → delete the entire project folder → clone again → paste the backup files back**

Both options work. Pick whichever makes you more comfortable.

---

**Happy collaborating! 🚀**

*Team: Yicheng Jiang, Shuoyang Jin, Jiaxin Wang, Quanquan Lu*

