# Upstream Sync Guide — zmr-skills

This repo is a fork of [mattpocock/skills](https://github.com/mattpocock/skills) with custom skills added on top.

**Custom skills** (owned by this fork, never synced from upstream):
- `skills/engineering/anatomy/` — codebase architecture tracer

**Upstream skills** — everything else. Sync regularly to get bug fixes and new skills.

---

## When upstream updates

### Step 1 — Verify upstream remote is set

```bash
cd ~/Documents/zaob-dev/zmr-skills
git remote -v
```

Expected output should include:
```
upstream  git@github.com:mattpocock/skills.git (fetch)
upstream  git@github.com:mattpocock/skills.git (push)
```

If `upstream` is missing, add it once:
```bash
git remote add upstream git@github.com:mattpocock/skills.git
```

### Step 2 — Fetch and inspect

```bash
git fetch upstream
git log --oneline HEAD..upstream/main
```

Read what changed. Pay attention to commits that touch:
- `skills/engineering/` — could affect skills you depend on
- `scripts/` — the `skills` CLI itself
- `CHANGELOG.md` — summary of intentional changes

### Step 3 — Merge

```bash
git merge upstream/main
```

**If there are conflicts** on your custom skill files (`skills/engineering/anatomy/**`), always keep **your** version:

```bash
git checkout HEAD -- skills/engineering/anatomy/
git add skills/engineering/anatomy/
git merge --continue
```

### Step 4 — Verify custom skills are intact

```bash
ls skills/engineering/anatomy/
# Should list: SKILL.md  references/  scripts/
```

### Step 5 — Push

```bash
git push origin main
```

### Step 6 — Update consumer repos

In every repo that has `maemreyo/zmr-skills` in its `skills-lock.json` (e.g. `oh-my-class`):

```bash
npx skills@latest update
```

This re-fetches updated skill files and recomputes hashes in `skills-lock.json`.

---

## Adding a new custom skill

1. Create `skills/engineering/<name>/SKILL.md` (or the appropriate category folder).
2. Write YAML frontmatter (`name`, `description`) and instructions.
3. Add `references/` or `scripts/` subdirectories as needed.
4. Commit and push to `origin main`.
5. In consumer repos: `npx skills@latest update`.
6. Add the new skill name to the **Custom skills** list at the top of this file.

---

## Removing or shadowing an upstream skill

```bash
# Option A: Delete it (consumers won't install it)
rm -rf skills/engineering/<name>/
git add -A && git commit -m "chore: remove upstream skill <name>"

# Option B: Override in place with a stub
echo '---\nname: <name>\ndescription: Disabled.\n---\n# Disabled' \
  > skills/engineering/<name>/SKILL.md
git add skills/engineering/<name>/SKILL.md
git commit -m "chore: stub out upstream skill <name>"
```

---

## Checking for upstream changes (manual)

```bash
git fetch upstream && git log --oneline HEAD..upstream/main | head -20
```

Empty output = you're up to date.
