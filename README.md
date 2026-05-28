# tripmind-agentic-travel-ai

# Git Workflow Rules

Every team member must follow the same GitHub workflow to avoid conflicts and maintain clean project structure.

---

# IMPORTANT RULES

## DO NOT:

* push directly to main
* work on another member’s branch
* rewrite unrelated files
* upload broken code
* change architecture randomly

---

# ALWAYS:

* work only on your assigned branch
* pull latest changes before starting work
* commit properly
* test locally before pushing
* keep commits clean and meaningful

---

# BRANCH ASSIGNMENTS

## frontend-ui

Frontend developer branch.

Handles:

* Next.js
* Tailwind CSS
* UI implementation
* animations
* dashboard
* responsive design

---

## backend-api

Backend developer branch.

Handles:

* FastAPI
* APIs
* middleware
* Supabase integration
* backend services

---

## ai-agents

AI developer branch.

Handles:

* CrewAI
* prompts
* agents
* workflows
* orchestration
* recommendation systems

---

## integration-testing

Integration engineer branch.

Handles:

* frontend/backend integration
* API debugging
* CrewAI integration
* Supabase connection
* full testing
* deployment preparation

---

# DAILY DEVELOPMENT WORKFLOW

## STEP 1 — Switch to Your Branch

Example:

```bash id="u7fk2m"
git checkout frontend-ui
```

OR

```bash id="p8v1zr"
git checkout backend-api
```

OR

```bash id="x5m2ka"
git checkout ai-agents
```

---

# STEP 2 — Pull Latest Changes

Before starting work ALWAYS run:

```bash id="r4n9yw"
git pull origin <your-branch-name>
```

Example:

```bash id="k2f8we"
git pull origin frontend-ui
```

This prevents conflicts.

---

# STEP 3 — Start Working

Generate code using:

* master PDF
* initialization prompt
* Figma design
* uploaded files/assets

Work ONLY on your assigned module.

---

# STEP 4 — Test Locally

Before pushing:

* run project locally
* check for errors
* verify UI
* verify APIs
* verify integrations

Never push broken code.

---

# STEP 5 — Add Changes

```bash id="m6t2pl"
git add .
```

---

# STEP 6 — Commit Changes

Write clean commit messages.

Examples:

```bash id="q3x7fa"
git commit -m "Added itinerary dashboard cards"
```

```bash id="d1v8kp"
git commit -m "Integrated Supabase auth middleware"
```

```bash id="n5r4yt"
git commit -m "Created CrewAI recommendation workflow"
```

Avoid bad commits like:

* update
* fix
* changes

---

# STEP 7 — Push to Your Branch

```bash id="w8m3zx"
git push origin <your-branch-name>
```

Example:

```bash id="j4k9vr"
git push origin frontend-ui
```

---

# INTEGRATION WORKFLOW

After all developers push code:

The Integration Engineer will:

1. Go to:

```bash id="b9t2wl"
integration-testing
```

2. Pull all branches.

3. Connect:

* frontend ↔ backend
* backend ↔ CrewAI
* backend ↔ Supabase

4. Fix:

* API mismatches
* response errors
* environment issues
* CORS issues
* integration bugs

5. Test the full workflow.

6. Prepare stable build.

---

# FINAL MERGE WORKFLOW

ONLY after:

* full testing
* successful integration
* bug fixing
* stable build

The integration engineer should merge everything into:

```bash id="c5r8mx"
main
```

Main branch should always remain:

* stable
* clean
* deployment-ready

---

# IMPORTANT ENVIRONMENT RULES

Never push:

* .env
* API keys
* secrets
* tokens

Instead use:

```bash id="z7k4qp"
.env.example
```

---

# TEAM COMMUNICATION RULES

Before changing:

* APIs
* folder structure
* architecture
* database schema

Inform the team first.

Do NOT create unexpected breaking changes.

---

# FINAL GOAL

Maintain:

* clean architecture
* scalable workflow
* modular code
* startup-grade quality
* easy integration
* consistent design system
* smooth collaboration
