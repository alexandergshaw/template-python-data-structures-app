# template-python-database-app

A best-practice Flask + Supabase **personal portfolio** template — designed for a single student to show off their own work.

## Personalization

Set the following environment variables (see `.env.example`) to make the site your own. They power the hero, about section, footer, and contact button across every page:

| Variable | Description |
|----------|-------------|
| `STUDENT_NAME` | Your name — shown in the nav, hero, footer, and page titles |
| `STUDENT_TAGLINE` | A one-line tagline shown in the hero section |
| `STUDENT_BIO` | A short paragraph shown in the "About me" section |
| `STUDENT_CONTACT_EMAIL` | The email address the "Email me" button opens |

## Architecture

```text
app/
  __init__.py                 # app factory, dependency wiring, logging
  config.py                   # environment-aware config objects
  extensions.py               # Supabase client initialization (retry, validation)
  domain/models.py            # domain entities (dataclasses)
  repositories/
    base.py                   # abstract repository interface
    portfolio_repository.py   # Supabase-backed implementation
  services/                   # business logic layer
  web/
    routes.py                 # Flask blueprint/routes
    health.py                 # /health endpoint for monitoring
app/templates/
  base.html
  portfolio/index.html
  portfolio/detail.html
app/static/css/style.css
supabase/migrations/          # SQL migrations with RLS policies
run.py                        # local entrypoint (loads .env)
api/index.py                  # Vercel serverless entrypoint
tests/test_app.py             # unit tests
```

## Key Design Decisions

| Concern | Approach |
|---------|----------|
| **Separation of concerns** | Abstract `PortfolioRepository` interface decouples services from Supabase |
| **Security** | Row Level Security (RLS) policies on all tables; anon key for reads only |
| **Resilience** | Retry logic with exponential backoff on client initialization |
| **Graceful degradation** | App serves placeholder content when Supabase is unreachable |
| **Observability** | Structured logging + `/health` endpoint for monitoring |
| **Config validation** | URL/key format checks at startup with clear warnings |

## Setup

This guide walks you through setting up the project with **Supabase** (database), **Vercel** (hosting), and **GitHub Classroom** (assignment distribution).

---

### Prerequisites

- Python 3.11+
- A GitHub account
- A [Supabase](https://supabase.com) account (free tier works)
- A [Vercel](https://vercel.com) account (free tier works)

---

## 1. Supabase Setup (Database)

### 1.1 Create a Supabase project

1. Go to [supabase.com](https://supabase.com) and sign in (or create an account).
2. Click **New Project**.
3. Choose an organization, enter a project name (e.g. `student-portfolio`), set a database password, and select a region close to you.
4. Click **Create new project** and wait for provisioning to complete.

### 1.2 Get your API credentials

1. In your Supabase project dashboard, navigate to **Settings → API**.
2. Copy the following values — you'll need them later:

   | Value | Where to find it |
   |-------|-----------------|
   | **Project URL** | Under "Project URL" (e.g. `https://abc123.supabase.co`) |
   | **anon (public) key** | Under "Project API keys" → `anon` `public` |
   | **service_role key** | Under "Project API keys" → `service_role` `secret` (keep this private!) |

### 1.3 Run the database migration

**Option A — Using the SQL Editor (recommended for beginners):**

1. In the Supabase dashboard, go to **SQL Editor**.
2. Click **New query**.
3. Paste the contents of `supabase/migrations/001_create_portfolio_items.sql` from this repository.
4. Click **Run**.

**Option B — Using the Supabase CLI:**

```bash
# Install the Supabase CLI (https://supabase.com/docs/guides/cli)
npm install -g supabase

# Link to your remote project
supabase link --project-ref <your-project-ref>

# Push migrations
supabase db push
```

This creates:
- The `portfolio_items` table with appropriate indexes
- Row Level Security policies (public read, service_role write)
- An `updated_at` auto-update trigger

---

## 2. Vercel Setup (Hosting & Deployment)

This project is configured for zero-config deployment on Vercel using the Python serverless runtime.

### 2.1 Connect your repository to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with your GitHub account.
2. Click **Add New… → Project**.
3. Import the GitHub repository containing this code.
4. Vercel will automatically detect `vercel.json` — no framework or build settings changes are needed.

### 2.2 Add environment variables

Before deploying, add the following environment variables in **Settings → Environment Variables**:

| Variable | Required | Value |
|----------|----------|-------|
| `SECRET_KEY` | Yes | A strong random string (generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `SUPABASE_URL` | Yes | Your Supabase project URL from step 1.2 |
| `SUPABASE_KEY` | Yes | Your Supabase anon (public) key from step 1.2 |
| `SUPABASE_SERVICE_ROLE_KEY` | No | Service role key (only if write operations are needed) |

### 2.3 Deploy

1. Click **Deploy**. Vercel will build and deploy your app automatically.
2. Once deployed, you'll receive a URL (e.g. `https://your-project.vercel.app`).
3. Visit `<your-url>/health` to verify the app is connected to Supabase.

### 2.4 Automatic deployments

Every push to the `main` branch will trigger a new production deployment. Pull requests get preview deployments automatically.

### How it works

- `vercel.json` routes all incoming requests to a single serverless function (`api/index.py`).
- `api/index.py` exposes the Flask WSGI `app` object, which Vercel's Python runtime invokes per-request.
- Static files are served through the Flask app (Vercel's Python runtime handles this efficiently for moderate traffic).

---

## 3. GitHub Classroom Setup (For Instructors)

Use GitHub Classroom to distribute this template as a student assignment.

### 3.1 Create a GitHub Classroom

1. Go to [classroom.github.com](https://classroom.github.com) and sign in.
2. Click **New classroom**.
3. Select a GitHub organization to host the classroom (create one if needed).
4. Name the classroom (e.g. `Web Development Fall 2026`) and invite any TAs.

### 3.2 Create an assignment from this template

1. In your classroom, click **New assignment**.
2. Give the assignment a title (e.g. `Portfolio App`).
3. Set the deadline and visibility (private recommended so students can't copy each other).
4. Under **Starter code**, select this repository as the template repository.
5. Choose whether it's an **individual** or **group** assignment.
6. (Optional) Enable autograding by adding test commands:
   - Add a test: **Run command** → `python -m unittest discover -s tests -v`
   - This will run the existing test suite on each student push.
7. Click **Create assignment**.

### 3.3 Distribute to students

1. GitHub Classroom generates an **invitation link** for the assignment.
2. Share this link with students (via LMS, email, etc.).
3. When a student accepts the invitation, GitHub automatically:
   - Creates a private copy of this repository for the student (or group).
   - Grants the student push access to their copy.

### 3.4 Student workflow (share with students)

Each student should:

1. **Accept the assignment** via the invitation link.
2. **Clone their repository** locally:
   ```bash
   git clone https://github.com/<org>/<assignment-repo>.git
   cd <assignment-repo>
   ```
3. **Set up their own Supabase project** (see Section 1 above).
4. **Deploy to Vercel** (see Section 2 above) — each student deploys their own instance.
5. **Configure local development:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with their Supabase credentials
   ```
6. **Run locally:**
   ```bash
   flask --app run run
   ```
7. **Run tests:**
   ```bash
   python -m unittest discover -s tests -v
   ```
8. **Push changes** — autograding (if enabled) runs automatically on each push.

### 3.5 Instructor tips

- **Monitoring progress:** Use the GitHub Classroom dashboard to see student repositories, commit activity, and autograding results.
- **Providing feedback:** Use GitHub pull requests or issues on student repos to give feedback.
- **Shared Supabase vs. individual:** For simplicity, each student should create their own Supabase project. Alternatively, you can provision a shared project and distribute read-only credentials, but this adds complexity.

---

## Local Development

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
# Edit .env with your Supabase project URL and keys
```

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Your Supabase project URL (e.g. `https://abc123.supabase.co`) |
| `SUPABASE_KEY` | Yes | Anon (public) key — safe for client-side reads |
| `SUPABASE_SERVICE_ROLE_KEY` | No | Service role key — use only in trusted server contexts |
| `SECRET_KEY` | Yes | Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `SUPABASE_TIMEOUT` | No | PostgREST request timeout in seconds (default: 10) |
| `SUPABASE_MAX_RETRIES` | No | Client initialization retry attempts (default: 3) |

### Run the app

```bash
flask --app run run
```

### Run tests

```bash
python -m unittest discover -s tests -v
```

## Health Check

The `/health` endpoint returns JSON indicating service status:

```json
{"status": "healthy", "supabase": "connected"}
```

Returns HTTP 503 when Supabase connectivity is degraded.

## Security Best Practices

1. **Never expose `SUPABASE_SERVICE_ROLE_KEY` to the client.** It bypasses RLS.
2. **Use the anon key** (`SUPABASE_KEY`) for this read-only portfolio app.
3. **Enable RLS** on every table (the migration does this automatically).
4. **Rotate keys** periodically via the Supabase dashboard.
5. **Keep `.env` out of version control** (already in `.gitignore`).

## Placeholder Behavior

- If Supabase credentials are not configured, the app serves placeholder student portfolio content.
- Home page: `/`
- Student detail page: `/students/placeholder-project`
