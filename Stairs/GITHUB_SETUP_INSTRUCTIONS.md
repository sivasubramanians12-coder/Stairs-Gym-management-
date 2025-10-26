# GitHub Repository Setup Instructions

Follow these steps to create the "stairs-gym" repository and push your code:

---

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in the details:
   - **Repository name:** `stairs-gym`
   - **Description:** `AI-Powered Gym Management System with conversational workout logging, standardized assessments, and hallucination-free reports`
   - **Visibility:** Choose Public or Private (your preference)
   - **DO NOT** check "Initialize this repository with a README" (we already have one)
   - **DO NOT** add .gitignore or license (we already have them)
3. Click **"Create repository"**

---

## Step 2: Update Git Remote (Run these commands)

After creating the repository on GitHub, run these commands:

```bash
cd "C:\Users\siva.s\AI Experiments\Stairs"

# Remove the old remote
git remote remove origin

# Add the new remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/stairs-gym.git

# Verify the new remote
git remote -v

# Push to the new repository
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Alternative: If you get authentication errors

If you get a password prompt or authentication error when pushing, you need to use a Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Stairs Gym Project"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

Then when pushing, use:
```bash
git push -u origin main
```

When prompted for password, paste your Personal Access Token (not your GitHub password).

---

## Step 3: Verify Upload

After pushing, go to your repository URL:
`https://github.com/YOUR_USERNAME/stairs-gym`

You should see:
- ✅ README.md displayed
- ✅ 52 files in the repository
- ✅ All documentation files visible
- ✅ Python scripts present
- ✅ .env file is NOT uploaded (excluded by .gitignore)

---

## Quick Commands Summary

```bash
# 1. Navigate to project
cd "C:\Users\siva.s\AI Experiments\Stairs"

# 2. Remove old remote
git remote remove origin

# 3. Add new remote (UPDATE YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/stairs-gym.git

# 4. Push to GitHub
git push -u origin main
```

---

**Note:** Your .env file with API keys is automatically excluded by .gitignore and will NOT be uploaded to GitHub. This is correct for security!
