# template-python-database-app

A best-practice Flask + Supabase portfolio template for showcasing student work.

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

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

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

### 3. Set up the database

Run the migration in your Supabase SQL Editor or via the [Supabase CLI](https://supabase.com/docs/guides/cli):

```bash
# Using Supabase CLI
supabase db push
```

Or paste the contents of `supabase/migrations/001_create_portfolio_items.sql` into the SQL Editor.

This creates:
- The `portfolio_items` table with appropriate indexes
- Row Level Security policies (public read, service_role write)
- An `updated_at` auto-update trigger

### 4. Run the app

```bash
flask --app run run
```

### 5. Run tests

```bash
python -m unittest discover -s tests -v
```

## Deploying to Vercel

This project is configured for zero-config deployment on [Vercel](https://vercel.com) using the Python serverless runtime.

### Steps

1. Push this repository to GitHub (or connect it directly in the Vercel dashboard).
2. Import the project in the [Vercel Dashboard](https://vercel.com/new).
3. Add the following **Environment Variables** in your Vercel project settings:

   | Variable        | Description                          |
   | --------------- | ------------------------------------ |
   | `SECRET_KEY`    | A strong random secret key           |
   | `SUPABASE_URL`  | Your Supabase project URL            |
   | `SUPABASE_KEY`  | Your Supabase anon key               |

4. Deploy. Vercel will automatically detect `vercel.json` and build the serverless function from `api/index.py`.

### How it works

- `vercel.json` routes all incoming requests to a single serverless function (`api/index.py`).
- `api/index.py` exposes the Flask WSGI `app` object, which Vercel's Python runtime invokes per-request.
- Static files are served through the Flask app (Vercel's Python runtime handles this efficiently for moderate traffic).

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
