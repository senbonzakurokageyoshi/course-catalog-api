# Course Catalog API

A standalone backend project on FastAPI for the course catalog.

## How to run

1. Create and activate a virtual environment:
   - Mac/Linux: `python3 -m venv .venv` and `source .venv/bin/activate`
   - Windows: `python -m venv .venv` and `.venv\Scripts\Activate.ps1`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `fastapi dev main.py`

## What changed in Lab 5

### CORS

`CORSMiddleware` is attached with `allow_origins=["http://localhost:3000"]`. This is the exact origin (scheme + host + port, no trailing slash) of the Next.js dev server. Requests from any other origin will not receive `Access-Control-Allow-Origin` in the response, so the browser will block JavaScript from reading them. The `/courses` page (Server Component) works without CORS because the request is made by the Next.js server, not the browser.

### camelCase JSON

All models inherit from `CamelModel`, which uses `alias_generator=to_camel`. Python keeps `snake_case` field names; Pydantic produces `camelCase` in JSON automatically. `validate_by_name=True` is required so that `data.py` can still create objects using `is_elective=True` (field name), not `isElective=True` (alias).

### New routes

`POST /courses/{course_id}/like` — increments the like counter and returns the updated course.

```json
{ "id": "web-security", "title": "Web Security Essentials", ..., "likes": 22 }
```

`POST /enrollments` — accepts a JSON body `{ "courseId": "...", "studentName": "..." }`, validates that the course exists and the name is at least 2 characters, and returns `201` with the created record including an `id`.

```json
{ "courseId": "web-security", "studentName": "Aigerim", "id": 1 }
```

`GET /enrollments` — returns all enrollments stored in memory (reset on every server restart).

## What was verified

- `GET /` returns a welcome message.
- `GET /courses` returns 6 courses in camelCase, `ai-integration` first.
- `GET /courses?is_elective=true` returns exactly 2 courses.
- `GET /courses?sort=title` returns 6 courses alphabetically.
- `GET /courses?page=2&page_size=2` returns `web-security` and `backend-fastapi`.
- `GET /courses/web-security` returns the web security course.
- `GET /courses/nope` returns 404 `Course not found`.
- `POST /courses/web-security/like` returns 200, likes incremented.
- `POST /courses/nope/like` returns 404.
- `POST /enrollments` with valid body returns 201 with `id`.
- `POST /enrollments` with `studentName: "A"` returns 422.
- `POST /enrollments` with unknown `courseId` returns 404.
- Preflight `OPTIONS /enrollments` with correct headers returns 200.
