# SSH & Git Remote Setup Guide - ryze CMS v2

## ✅ Completed: SSH Key Generation

Your SSH key has been successfully generated on this machine.

### SSH Key Details

- **Key Type**: ED25519 (Modern, Secure)
- **Private Key Location**: `~/.ssh/id_ed25519`
- **Public Key Location**: `~/.ssh/id_ed25519.pub`
- **Email Associated**: educ1.eoex@gmail.com
- **Key Fingerprint**: SHA256:JRERbvH+5hX9soXTJnDgBeyOEtm3gf7x5MYMsyuH9Ec

### SSH Configuration

SSH config file created at `~/.ssh/config` with proper GitHub settings:

```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    AddKeysToAgent yes
    IdentitiesOnly yes
    PreferredAuthentications publickey
    StrictHostKeyChecking accept-new
```

All permissions set correctly (600).

---

## 📋 NEXT STEPS: Add SSH Key to GitHub

### Step 1: Copy Your Public Key

Your public SSH key (the one to share with GitHub):

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILp5b3kjD8uy1cB9wCO0wrJuTYcjFsZ05jpN/778hRZ2 educ1.eoex@gmail.com
```

Or retrieve it anytime with:
```bash
cat ~/.ssh/id_ed25519.pub
```

### Step 2: Add Key to GitHub Account

1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. **Title**: ryze CMS v2 Local Dev (or your preference)
4. **Key type**: Authentication Key
5. **Key**: Paste the entire public key from above
6. Click "Add SSH key"

### Step 3: Verify SSH Connection

Once the key is added to GitHub, test the connection:

```bash
ssh -T git@github.com
```

You should see:
```
Hi eoextrainer! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 🔗 Git Remote Configuration

### Current Setup

Your repository has been configured with:

```
origin   → git@github.com:eoextrainer/ryze.git  (Downstream/Main)
upstream → git@github.com:eoextrainer/ryze.git  (Upstream/Integration)
```

### Ready Branch Configuration

The `ready` branch is configured with:

- **Push Remote**: `origin` (downstream)
- **Merge Remote**: `upstream` (upstream/int)
- **Purpose**: Syncs with upstream/int (pulls) and pushes to origin/main

### After GitHub SSH Key Setup

Once you've added the SSH key to GitHub, initialize the remote tracking:

```bash
cd /media/eoex/DOJO/CONSULTING/PROJECTS/ryze/cms-v2

# Fetch all remote branches
git fetch --all

# Configure ready branch to track upstream/int
git checkout ready
git branch -u upstream/int ready

# Verify configuration
git branch -vv
```

---

## 🔄 Ready Branch Sync Workflow

### Pull Latest from Upstream (int branch)

```bash
git checkout ready
git pull upstream int
```

This pulls from `git@github.com:eoextrainer/ryze.git` on branch `int`

### Push to Origin (main branch)

```bash
git checkout ready
git push origin ready:main
```

This pushes local `ready` to remote `main` on `origin`

### Combined Sync Operation

```bash
# Pull from upstream int
git checkout ready
git pull upstream int

# Push to origin main
git push origin ready:main
```

Or as a single command:

```bash
git fetch upstream int && git push origin ready:main
```

---

## 📊 Branch Mapping

```
Local           Upstream Remote    Origin Remote
─────           ──────────────     ──────────────
ready           ← upstream/int     → origin/main
                (pull/merge from)  (push to)
```

### Complete Sync Pipeline

```
Local Workflow:
feature → develop → ready

Remote Upstream (Integration):
ready → [git pull upstream int]

Remote Origin (Main):
[git push origin ready:main]

GitHub Remote Structure:
git@github.com:eoextrainer/ryze.git
  ├─ main       (Downstream - receives from ready)
  └─ int        (Upstream - provides to ready)
```

---

## 🔑 SSH Key Management

### Verify SSH Key is Working

```bash
# Test connection
ssh -T git@github.com

# You should see:
# Hi eoextrainer! You've successfully authenticated...
```

### View Your SSH Keys

```bash
# List all SSH keys
ls -la ~/.ssh/

# View public key
cat ~/.ssh/id_ed25519.pub

# View key fingerprint
ssh-keygen -l -f ~/.ssh/id_ed25519
```

### Add Key to SSH Agent (Optional, for convenience)

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## 🚀 First Push After SSH Setup

Once SSH key is added to GitHub:

### Option 1: Push All Branches

```bash
cd /media/eoex/DOJO/CONSULTING/PROJECTS/ryze/cms-v2
git push -u origin --all
```

### Option 2: Push Ready Branch Specifically

```bash
git checkout ready
git push -u origin ready
```

### Option 3: Push Ready → Main (As Per Workflow)

```bash
git checkout ready
git push origin ready:main
```

---

## 🔗 Complete Remote Commands Reference

### Fetch Operations

```bash
# Fetch from upstream
git fetch upstream

# Fetch from origin
git fetch origin

# Fetch from both
git fetch --all
```

### Pull Operations

```bash
# Pull from upstream int to ready
git checkout ready
git pull upstream int

# Pull with rebase (cleaner history)
git pull --rebase upstream int
```

### Push Operations

```bash
# Push ready to origin main
git push origin ready:main

# Push ready to origin ready
git push origin ready

# Push all branches
git push origin --all

# Push with tags
git push origin --all --tags
```

### View Remotes

```bash
# List remotes
git remote -v

# Show remote info
git remote show origin
git remote show upstream

# Show branch tracking
git branch -vv
```

---

## 📝 Troubleshooting SSH

### "Permission denied (publickey)"

**Problem**: SSH key not added to GitHub

**Solution**:
1. Go to https://github.com/settings/keys
2. Add your public key (from `cat ~/.ssh/id_ed25519.pub`)
3. Wait a moment for GitHub to process
4. Test with `ssh -T git@github.com`

### "Could not open a connection to your authentication agent"

**Problem**: SSH agent not running

**Solution**:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### "Host key verification failed"

**Problem**: GitHub host key not recognized

**Solution**: 
```bash
# Manually accept GitHub's host key
ssh -T git@github.com
# Type 'yes' when prompted
```

### "No more authentication methods to try"

**Problem**: SSH key permissions incorrect

**Solution**:
```bash
# Fix permissions
chmod 600 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/config
chmod 700 ~/.ssh
```

---

## ✅ Verification Checklist

Before proceeding with git operations:

- [ ] SSH key generated at `~/.ssh/id_ed25519`
- [ ] SSH config file at `~/.ssh/config` with correct permissions
- [ ] Public key added to GitHub (https://github.com/settings/keys)
- [ ] SSH connection tested: `ssh -T git@github.com`
- [ ] Git remotes configured: `git remote -v` shows origin and upstream
- [ ] Remote branches fetched: `git fetch --all` succeeds
- [ ] Ready branch tracking configured: `git branch -vv` shows ready tracking upstream/int

---

## 📞 Quick Reference Commands

```bash
# Test SSH
ssh -T git@github.com

# Fetch all remotes
git fetch --all

# Check ready branch setup
git checkout ready && git branch -vv

# Pull latest from upstream int
git pull upstream int

# Push to origin main
git push origin ready:main

# View all remotes
git remote -v
```

---

## 🔐 Security Notes

- **Never share** your private key (`~/.ssh/id_ed25519`)
- **Only share** your public key (`~/.ssh/id_ed25519.pub`)
- SSH keys have proper permissions: 600 for files, 700 for directory
- SSH config restricts authentication to publickey only
- Keys are tied to your email: educ1.eoex@gmail.com

---

## 📚 Additional Resources

- GitHub SSH Setup: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- Git Branching: https://git-scm.com/book/en/v2/Git-Branching-Branch-Management
- SSH Config: https://linux.die.net/man/5/ssh_config

---

**Status**: SSH configured, ready for GitHub integration  
**Last Updated**: December 9, 2024  
**Author**: GitHub Copilot  
**For**: Sosthene Grosset-janin
