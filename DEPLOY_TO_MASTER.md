# Deploying the Website from `master`

This site builds on Netlify when `master` gets a new commit pushed.

## Important idea

If you only push your feature branch, the website does **not** update.
You must get those changes onto `master` and then push `master`.

## Exact steps

### 1. Open the `master` worktree

```powershell
cd "C:\Users\MSI Sword\.windsurf\worktrees\C00lnerd Tutoring Website\master"
```

### 2. Make sure you are really on `master`

```powershell
git status
```

You should see:

```text
On branch master
```

### 3. Pull the latest `master`

```powershell
git pull origin master
```

### 4. Merge your feature branch into `master`

```powershell
git merge cascade/this-was-from-my-session-on-the-98c246
```

If it says `Already up to date`, you are probably running the command in the wrong worktree or the branch was already merged.

### 5. Push `master`

```powershell
git push origin master
```

This is the step that should trigger the Netlify build.

## Quick version

```powershell
cd "C:\Users\MSI Sword\.windsurf\worktrees\C00lnerd Tutoring Website\master"
git pull origin master
git merge cascade/this-was-from-my-session-on-the-98c246
git push origin master
```

## If you changed files directly in the `master` worktree

Only do this if you actually edited files in `master`:

```powershell
git add .
git commit -m "Describe the change"
git push origin master
```

## Why `git add .` did nothing earlier

Because `master` had no changed files yet.
Your astrophotography work was still on the feature branch, not in the `master` worktree.

## How to confirm the website should build

After `git push origin master`, Git should show that something new was pushed.
If it says:

```text
Everything up-to-date
```

then Netlify usually has nothing new to build.

## Optional local build check

```powershell
npm run build
```

This checks whether Astro builds successfully on your machine.
