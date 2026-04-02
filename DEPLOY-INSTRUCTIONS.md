# Velocity AI - Deploy to Vercel

## Step 1: Fix the corrupted .git directory and initialize fresh

Open PowerShell/Terminal in `C:\Users\mitch\Projects\velocity-ai\` and run:

```powershell
# Remove the corrupted .git directory
Remove-Item -Recurse -Force .git

# Initialize fresh
git init -b main
git config user.email "mitchpearce94@gmail.com"
git config user.name "Mitchell Pearce"

# Stage everything
git add -A

# Commit
git commit -m "Initial commit: Velocity AI full project"
```

## Step 2: Push to GitHub

```powershell
git remote add origin https://github.com/mitchpearce94-afk/Velocity-AI.git
git push -u origin main
```

If the repo already has content and you get a rejection, use:
```powershell
git push -u origin main --force
```

## Step 3: Deploy to Vercel

### Option A: Vercel Dashboard (Easiest)
1. Go to https://vercel.com/dashboard
2. Click "Add New..." > "Project"
3. Import the `mitchpearce94-afk/Velocity-AI` GitHub repo
4. Configure:
   - Framework Preset: **Other**
   - Root Directory: **./** (leave default)
   - Build Command: leave empty
   - Output Directory: **website**
5. Click "Deploy"

The `vercel.json` in the repo will handle the rest automatically.

### Option B: Vercel CLI
```powershell
npm install -g vercel
cd C:\Users\mitch\Projects\velocity-ai
vercel login
vercel --prod
```

## What's Deployed

The website is a self-contained React landing page (`website/index.html`) that loads:
- React 18 via CDN
- Tailwind CSS via CDN
- Lucide React icons via CDN
- Babel standalone for JSX transformation
- Google Fonts (Inter)

No build step required - it's a static HTML file with inline JSX.

## Files Added for Deployment
- `website/index.html` - Copy of preview.html (entry point for Vercel)
- `vercel.json` - Vercel deployment config (static site, website/ as output dir)
- `.gitignore` - Standard ignores (node_modules, .env, .vercel, logs)
