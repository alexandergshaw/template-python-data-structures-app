# template-python-data-structures-app

A Flask-based **personal portfolio** template — designed for a single student
to show off their own work. Project data lives in a local JSON file, so there
is no external database to manage.

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
  domain/models.py            # domain entities (dataclasses)
  repositories/
    base.py                   # abstract repository interface
    portfolio_repository.py   # JSON-file-backed implementation
  services/                   # business logic layer
  web/
    routes.py                 # Flask blueprint/routes
    health.py                 # /health endpoint for monitoring
app/templates/
  base.html
  portfolio/index.html
  portfolio/detail.html
app/static/css/style.css
data/projects.json            # all worked projects (source of truth)
run.py                        # local entrypoint (loads .env)
api/index.py                  # Vercel serverless entrypoint
tests/test_app.py             # unit tests
```

## Key Design Decisions

| Concern | Approach |
|---------|----------|
| **Separation of concerns** | Abstract `PortfolioRepository` interface decouples services from the data source |
| **Simple data store** | Projects are listed in a local JSON file — easy to edit and version-controlled |
| **Graceful degradation** | App serves empty/placeholder content when the JSON file is missing or malformed |
| **Observability** | Structured logging + `/health` endpoint for monitoring |

## Projects JSON file

Every project shown on the portfolio is loaded from a single JSON file —
`data/projects.json` by default. The file looks like this:

```json
{
  "projects": [
    {
      "slug": "placeholder-project",
      "student_name": "Your Name",
      "title": "Your First Project",
      "summary": "Add a short description of this project here.",
      "project_url": "#"
    }
  ]
}
```

Add a new object to the `projects` list for each project you want to show.
Required fields per entry:

| Field | Description |
|-------|-------------|
| `slug` | Unique URL-friendly identifier used in `/students/<slug>` |
| `student_name` | Name credited for the project |
| `title` | Project title shown on cards and detail pages |
| `summary` | Short description shown in cards |
| `project_url` | Link to the live project or source code |

Override the file location by setting `PROJECTS_JSON_PATH` in your environment.

### How the JSON gets to where it needs to go

1. `app/__init__.py` reads `PROJECTS_JSON_PATH` from the app config.
2. It constructs a `JsonPortfolioRepository` pointed at that file.
3. The repository is injected into `PortfolioService`, which the routes use
   to render the home page and per-project detail pages.
4. The `/health` endpoint reports whether the JSON file is present.

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
# Edit .env to personalize the site
```

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask secret key (generate with `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `PROJECTS_JSON_PATH` | No | Path to the projects JSON file (default: `data/projects.json`) |

### Run the app

```bash
flask --app run run
```

### Run tests

```bash
pytest
```

## Deploying to Vercel

This project is configured for zero-config deployment on Vercel using the
Python serverless runtime.

1. Sign in at [vercel.com](https://vercel.com) with your GitHub account.
2. Click **Add New… → Project** and import this repository.
3. Vercel auto-detects `vercel.json` — no extra build settings are required.
4. Add `SECRET_KEY` (and optionally `PROJECTS_JSON_PATH`) under
   **Settings → Environment Variables**.
5. Click **Deploy**. Every push to `main` will trigger a new deployment.

### How it works

- `vercel.json` routes all incoming requests to a single serverless function (`api/index.py`).
- `api/index.py` exposes the Flask WSGI `app` object, which Vercel's Python runtime invokes per-request.
- Static files are served through the Flask app.

## Health Check

The `/health` endpoint returns JSON indicating service status:

```json
{"status": "healthy", "projects": "available"}
```

Returns HTTP 503 when the projects JSON file cannot be located.

## Placeholder Behavior

- If the projects JSON file is missing, the app serves a single placeholder
  project so the templates always have something to render.
- Home page: `/`
- Student detail page: `/students/placeholder-project`

### Data-structure powered features

The home and project pages expose visitor-facing portfolio features (project
search, a guided tour, recommendations, "you are here" indicators, an editor's
pick, and more). Each feature is powered by **exactly one** data structure from
`data_structures/assignment1`–`assignment10`. Until a data structure is
implemented, its feature stays visible but shows a "work in progress"
placeholder; as soon as the assignment is complete, the feature comes online
automatically. The full feature ↔ data-structure mapping is documented in
`app/services/portfolio_service.py`.
