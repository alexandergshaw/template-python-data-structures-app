# template-python-database-app

A blank, best-practice Flask + Supabase portfolio template for showcasing student work.

## Architecture

```text
app/
  __init__.py                 # app factory and dependency wiring
  config.py                   # environment-aware config objects
  extensions.py               # external client initialization (Supabase)
  domain/models.py            # domain entities
  repositories/               # data access layer
  services/                   # business logic layer
  web/routes.py               # Flask blueprint/routes
app/templates/
  base.html
  portfolio/index.html
  portfolio/detail.html
app/static/css/style.css
run.py                        # local entrypoint
tests/test_app.py             # focused route/app tests
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment placeholders and set values:

```bash
cp .env.example .env
```

4. Run the app:

```bash
flask --app run run
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
   | `SUPABASE_KEY`  | Your Supabase anon or service key    |

4. Deploy. Vercel will automatically detect `vercel.json` and build the serverless function from `api/index.py`.

### How it works

- `vercel.json` routes all incoming requests to a single serverless function (`api/index.py`).
- `api/index.py` exposes the Flask WSGI `app` object, which Vercel's Python runtime invokes per-request.
- Static files are served through the Flask app (Vercel's Python runtime handles this efficiently for moderate traffic).

## Placeholder Behavior

- If Supabase credentials are not configured, the app serves placeholder student portfolio content.
- Home page: `/`
- Student detail page: `/students/placeholder-project`
