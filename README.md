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

## Placeholder Behavior

- If Supabase credentials are not configured, the app serves placeholder student portfolio content.
- Home page: `/`
- Student detail page: `/students/placeholder-project`
