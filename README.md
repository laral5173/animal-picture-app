# Animal Picture App

A small microservice that fetches random pictures of cats, dogs, and bears
from public APIs, saves them, and serves them back via REST endpoints.

Built for the Camunda TAM Tech Challenge.

## Tech stack

- **Python 3.12 + FastAPI** — REST API framework
- **SQLite** — embedded database (no external DB server required; ships
  inside the container, nothing to install locally)
- **httpx** — async HTTP client used to fetch images from the external APIs
- **Docker / docker-compose** — fully containerized, portable build

## How to run it

### Option A — with Docker (recommended, zero local setup)

```bash
docker-compose up --build
```

The app will be available at **http://localhost:8000**

The SQLite database and downloaded images are persisted in local
`./data` and `./images` folders (created automatically) via Docker volumes,
so your data survives container restarts.

### Option B — without Docker (local Python)

Requires Python 3.12+.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The app will be available at **http://localhost:8000**

## API Endpoints

### 1. Fetch & save pictures

```
POST /animals/fetch
Content-Type: application/json

{
  "animal_type": "dog",
  "count": 3
}
```

`animal_type` accepts: `cat`, `dog`, `bear`
`count`: how many pictures to fetch (1–10)

Returns the list of saved picture records (id, source URL, local file path).

### 2. Get the latest saved picture (metadata)

```
GET /animals/{animal_type}/latest
```

Example: `GET /animals/dog/latest`

Returns the most recently saved record for that animal type.

### 3. Get the latest saved picture (actual image file) — bonus

```
GET /animals/{animal_type}/latest/image
```

Returns the actual image file, so you can open it directly in a browser.

### 4. Simple web UI — bonus

Open **http://localhost:8000** in your browser. Pick an animal, click
"Fetch new picture", and the image appears on the page.

### Interactive API docs

FastAPI auto-generates interactive docs at **http://localhost:8000/docs**
— useful for trying out the endpoints manually without curl/Postman.

## Running the tests (bonus)

### Without Docker

```bash
pip install -r requirements.txt
pytest tests/ -v
```

### With Docker

```bash
docker-compose up --build -d
docker exec -it animal-picture-app-animal-picture-app-1 pytest tests/ -v
```

7 automated tests cover both endpoints: successful fetch (single and
multiple images), invalid animal type handling, input validation,
404 handling when no pictures exist yet, and retrieval of the most
recent record. External API calls are mocked so tests run instantly
and don't depend on network access.

## User guide

A non-technical guide for end users is available in [`USER_GUIDE.md`](USER_GUIDE.md).
It explains how to use the app from a browser, what to expect, and includes
optional command-line examples.

## Design decisions

- **SQLite over a heavier DB**: the challenge asks for something
  "shipped" without assuming local setup. SQLite is a single file —
  no separate database server/container needed, which keeps the
  docker-compose setup minimal while still being a real, queryable
  database.
- **Images saved to disk, not just URLs in the DB**: storing the actual
  file (not just the source URL) makes the "get the last picture"
  endpoint self-contained — it doesn't depend on the external API
  still being available or the image still existing there later.
- **Sequential fetching for multiple images**: kept simple and
  readable for this exercise; could be parallelized with
  `asyncio.gather` if throughput became a concern at larger scale.
- **cataas.com instead of placekitten.com for cats**: the challenge
  originally suggested `https://placekitten.com/` for cat pictures,
  but at the time of development that API was not responding reliably.
  Per the challenge instructions ("feel free to pick an alternative"),
  `https://cataas.com/cat` was chosen as a drop-in replacement that
  returns random cat images in the same way.

## What I'd add with more time

- Switch from sequential to concurrent fetching (`asyncio.gather`) when
  `count > 1`, for faster multi-image requests.
- Add pagination to a "list all pictures" endpoint.
- Add structured logging and basic request metrics.
- Move from SQLite to Postgres for a production deployment that needs
  concurrent writes at scale.
