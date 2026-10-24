# colony

The application layer of a distributed system, organized like an ant colony.

## Why this exists

`reliable-redis` is the worker ants — jobs get queued, retried, and tracked. `colony`
is everything around that: the guard ants checking who's allowed in (auth), the
chambers that will eventually hold persistent state (a database), and the division
of labor as the system grows into separate services. This repo is that layer,
built the same way as `reliable-redis` — naive first, fix the specific gap observed.

## API reference

Run the server, then see `/docs` (Swagger UI) or `/redoc` (ReDoc) for the full list
of endpoints, request/response shapes, and descriptions — generated straight from
the code, so it never goes stale.

## Not built yet

- **Per-user identity** — one shared API key for everyone right now, not per-caller
  credentials. Real auth (sessions or tokens) comes once multiple callers actually
  need to be told apart.
- **Persistence** — no database yet; nothing here outlives Redis.
- **Service split** — single app for now; splitting happens once a real reason to
  split shows up, not preemptively.

## Requirements

- Python 3.14, managed with `uv`
- A running Redis server
- A `.env` file — copy `.env.example` to `.env` and fill in your own key

## Quickstart

Clone and install:

```bash
git clone https://github.com/Gagan-Polukonda/colony.git
cd colony
uv sync
```

Copy `.env.example` to `.env` and fill in a key (see Requirements for how to generate one).

Install Redis if you don't have it:

```bash
docker run -d --name redis -p 6379:6379 redis   # any OS, incl. Windows via Docker Desktop
# or: brew install redis && brew services start redis   (macOS)
# or: sudo apt install redis-server                      (Linux)
```

Native Windows without Docker: use [Memurai](https://www.memurai.com/) (Redis's official
Windows-compatible partner) instead.

Start Redis:

```bash
redis-server --daemonize yes
```

Run the server:

```bash
uv run uvicorn main:app --reload
```

Optional — only if you want the server to auto-restart when `.env` changes (already covered
by this repo's `uvicorn[standard]` dependency, nothing extra to install):

```bash
uv run uvicorn main:app --reload --reload-include ".env"
```

Then open `http://127.0.0.1:8000/docs`.