# Git conflict recovery (beginner-friendly)

If GitHub shows **"This branch has conflicts that must be resolved"**, your PR branch and `main` edited the same lines.

This is common and fixable.

## Option A (easiest): fix in GitHub web UI

1. Open the pull request page.
2. Click **Resolve conflicts**.
3. For each file, remove conflict markers:

   ```text
   <<<<<<< HEAD
   ...
   =======
   ...
   >>>>>>> your-branch
   ```

4. Keep the final content you want, then click **Mark as resolved**.
5. Click **Commit merge**.
6. Return to the PR and click **Merge pull request** when checks pass.

## Option B: copy/paste local Git commands

Run these commands in your local clone:

```bash
git checkout work
git fetch origin
git rebase origin/main
```

If Git pauses with conflicts:

1. Open conflicted files and remove conflict markers.
2. Keep the final intended content.
3. Continue:

```bash
git add .
git rebase --continue
```

Repeat until rebase completes, then push:

```bash
git push -f origin work
```

## If you get stuck mid-rebase

To abort and return to previous state:

```bash
git rebase --abort
```

To inspect current state:

```bash
git status
git branch -vv
```

## Practical tip for this repository

When conflicts involve docs and release metadata, prefer keeping:

- latest `CHANGELOG.md` entry,
- latest version in `pyproject.toml` and `src/maintainerflow/__init__.py`,
- newest README sections (badges/status/examples/limitations).
