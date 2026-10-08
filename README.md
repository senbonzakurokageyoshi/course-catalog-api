# Course Catalog API
A standalone backend project on FastAPI for the course catalog.

## How to run
1. Create and activate a virtual environment:
   - Mac/Linux: `python3 -m venv .venv` and `source .venv/bin/activate`
   - Windows: `python -m venv .venv` and `.venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `fastapi dev main.py`

## What was verified
- `GET /` returns a welcome message.
- `GET /courses` returns 6 courses, with `ai-integration` first by default (sorted by popularity).
- `GET /courses?is_elective=true` returns exactly 2 courses.
- `GET /courses?is_elective=false` returns exactly 4 courses.
- `GET /courses?sort=title` returns 6 courses alphabetically by title.
- `GET /courses?page=2&page_size=2` returns `web-security` and `backend-fastapi`.
- `GET /courses/web-security` returns the web security course.
- `GET /courses/nope` returns a 404 error with the detail "Course not found".