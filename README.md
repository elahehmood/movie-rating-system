
# Movie Rating System (Phase 1 – Back-End)

A FastAPI + PostgreSQL backend for managing movies and submitting ratings.  
Movie responses include aggregated rating info: `average_rating` and `ratings_count`.

---

## Tech Stack
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL (Docker Compose)
- Poetry

---

## Quick Start (Docker – Recommended)

### 1) Build & run
```bash
docker compose up -d --build
````

### 2) Open Swagger UI

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Run Locally (Poetry)

### 1) Install dependencies

```bash
poetry install
```

### 2) Configure environment

Create `.env` from `.env.example`.

**Important DB note (common 500 fix):**
If you run FastAPI locally (e.g., `--port 8001`), `DB_HOST=db` will fail because `db` is only resolvable inside the Docker network.
For local runs, use:

* `DB_HOST=localhost`
* `DB_PORT=5433` (or whatever port you mapped in `docker-compose.yml`)

### 3) Run migrations

```bash
poetry run alembic upgrade head
```

### 4) Start the server

```bash
poetry run uvicorn app.main:app --reload --port 8001
```

Swagger UI:

* [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## Base Path

All endpoints are mounted under:

```
/api/v1
```

---

## Endpoints

### Movies

#### GET `/api/v1/movies`

Paginated list with optional filters.

Query params:

* `page` (default: 1)
* `page_size` (default: 10)
* `title` (optional)
* `release_year` (optional)
* `genre` (optional)

Response structure:

* `status`
* `data.page`, `data.page_size`, `data.total_items`, `data.items[]`

Each movie item includes:

* `id`, `title`, `release_year`, `cast`
* `director` (id, name)
* `genres` (list of names)
* `average_rating`
* `ratings_count`

#### GET `/api/v1/movies/{movie_id}`

Returns a single movie with relations and rating aggregation.

#### POST `/api/v1/movies`

Creates a movie and associates genres.

Example body:

```json
{
  "title": "The Godfather",
  "director_id": 3,
  "release_year": 1972,
  "cast": "Marlon Brando, Al Pacino",
  "genres": [1, 2]
}
```

#### PATCH `/api/v1/movies/{movie_id}`

Updates movie fields and (optionally) replaces the genre list.

#### DELETE `/api/v1/movies/{movie_id}`

Deletes the movie and dependent records (ratings + association table rows).
Returns `204 No Content` on success.

---

### Ratings

#### POST `/api/v1/movies/{movie_id}/ratings`

Adds a rating to a movie.

Body:

```json
{ "score": 8 }
```

Rules:

* `score` must be between 1 and 10
* invalid score → 422
* movie not found → 404

---

## Response Format

### Success

```json
{ "status": "success", "data": {} }
```

### Failure

```json
{
  "status": "failure",
  "error": { "code": 422, "message": "..." }
}
```

---

## Common Error: `could not translate host name "db"`

This happens when running the API locally while `DB_HOST=db` is set.

Fix:

* Local run: set `DB_HOST=localhost` (and use your mapped DB port, e.g., `5433`)
* Docker run: `DB_HOST=db` is correct

```
::contentReference[oaicite:0]{index=0}
```
