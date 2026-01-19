# Just Write — AI Writing Tutor 📚✍️

## Overview 💡
**Just Write** is an AI-powered writing tutor that helps elementary students (Grades 3–5) improve their writing through a scaffolded set of phases: *I Do, We Do, You Do*. The system provides grade-aware writing prompts, teacher lesson videos, an interactive Socratic chat coach, and an automated evaluator that returns analytic feedback aligned to PSSA-style rubrics.

This README documents the problem statement, user requirements, system architecture, AI models used, data schema, API surface, front-end components, developer setup, security guidance, and known issues / next steps. Use it as the source material for a deeper narrative or technical design doc.

---

## Problem Statement & Users 🎯
- Problem: Many students need tailored, scaffolded writing practice. Teachers need scalable, immediate feedback & coach-like guidance to support student development.
- Primary Users:
  - **Students (Grades 3–5)**: select prompts, watch a short lesson (I Do), practice with guided questions (We Do), then write independently (You Do).
  - **Teachers**: create/curate prompts & lessons, review auto-evaluations, monitor student progress.

User requirements summary:
- Grade-specific prompts and lessons
- Fast, interactive chat tutoring for coaching
- Automated, standard-aligned evaluation (scores + feedback)
- Simple registration & JWT-based authentication
- Offline-friendly local development and seeded content for evaluation/test

---

## High-Level Architecture 🏗️
- **Frontend**: Next.js 15 (React 19) + Tailwind CSS, Axios for HTTP.
- **Backend**: FastAPI (Python) with SQLAlchemy ORM, Pydantic schema models.
- **Database**: PostgreSQL (local dev, configured via `DATABASE_URL`).
- **AI**: Google Gemini (via Pydantic-AI / google-generativeai wrappers). The agents are built with `pydantic_ai.Agent` using model `gemini-2.0-flash`.
- **Auth**: JSON Web Tokens (JWT) with `python-jose` and hashed passwords (Passlib pbkdf2_sha256).

Component diagram (quick):
Frontend (Next.js) ↔ Backend (FastAPI) ↔ PostgreSQL
Backend ↔ Google GenAI (Gemini) via Pydantic-AI/`google-generativeai`

---

## Key Files & Locations (File Map) 📁
Backend
- `backend/app/main.py` — FastAPI app bootstrap, CORS, router include, DB create_all.
- `backend/app/database.py` — SQLAlchemy engine & session setup.
- `backend/app/models.py` — SQLAlchemy table models (`User`, `Prompt`, `LessonContent`, `StudentScore`, `WritingProject`).
- `backend/app/schemas/schemas.py` — Pydantic request/response schema models.
- `backend/app/api/auth.py` — `/auth/register`, `/auth/login`, `/auth/me` endpoints and `get_current_user` dependency.
- `backend/app/api/tutor.py` — `/tutor/prompts`, `/tutor/lesson`, `/tutor/chat`, `/tutor/evaluate` endpoints.
- `backend/app/core/ai_agents.py` — Pydantic-AI `Agent` setup, picks `gemini-2.0-flash` by default.
- `backend/app/core/system_prompt.py` — System prompt templates for Socratic/Evaluator roles.
- `backend/scripts/seed_prompts.py`, `seed_lessons_v2.py` — Seed DB with prompts and lessons.
- `fix_db_schema.py` — helper script used to add missing schema fields (one-time migration aid).

Frontend
- `frontend/src/app/page.tsx` — landing/dashboard and phase navigation.
- `frontend/src/components/PhaseTabs.tsx` — central UI for I/We/You phases.
- `frontend/src/components/SocraticChat.tsx` — chat UI + history handling.
- `frontend/src/context/AuthContext.tsx` — user/token handling and auth fetch logic (timeouts added).
- `frontend/src/utils/api.ts` — centralized API base URL detection (uses same host as the browser to avoid CORS mismatch).

Scripts & Utilities
- `scripts/check_db_v2.py` — DB connectivity check.
- `scripts/init_db.py` — initialization helpers.
- `scripts/test_chat.py` — test harness for chat/eval flow.

---

## AI Implementation Details 🤖
### Models
- **Gemini model**: `gemini-2.0-flash` (invoked via `GoogleModel` in `pydantic_ai.models.google`). The code sets the `GOOGLE_API_KEY` in the environment and returns `GoogleModel('gemini-2.0-flash')` to `Agent`.

### Agent Roles
- **Socratic Agent (We Do)**: Interactive question/answer stream to scaffold student thinking. Implemented as `we_do_agent` using `SYSTEM_PROMPT_WE_DO`.
- **Evaluation Agent (You Do)**: Accepts student writing and returns structured feedback (JSON). Implemented as `evaluation_agent` using `SYSTEM_PROMPT_YOU_DO`.

### Prompts & Output
- The evaluator tries to parse JSON returned by the model. If the model returns JSON in triple-backticks (```json ... ```), the backend extracts that JSON using regex and returns parsed JSON to the frontend.
- A fallback returns raw text if parsing fails — appropriate guards added to avoid crashes.

### Packages
- `pydantic-ai` — agent and typed response helpers.
- `google-generativeai` — underlying genai client.

Notes on reproducibility: set `GOOGLE_API_KEY` in `.env` for local testing; rotate secrets if leaked.

---

## Data Model Summary (selected) 🗄️
`User`:
- `id`, `email`, `username`, `hashed_password`, `grade_level`, `created_at`

`Prompt`:
- `id`, `topic`, `grade_level`, `prompt_text`, `assignment_type` (`we-do` / `you-do`).

`LessonContent` (`lesson_contents`):
- `id`, `grade_level`, `topic`, `phase`, `video_url`, `content_html`.

`StudentScore` and `WritingProject` hold evaluations & writing content.

---

## API Endpoints (important ones) 🔌
- POST `/auth/register` — Register a user. Req: `email, username, password, grade_level` → returns `UserResponse`.
- POST `/auth/login` — Login. Req: `email, password` → returns `access_token` (JWT).
- GET `/auth/me` — Get current user (JWT required).

- GET `/tutor/prompts` — Query params: `topic`, `assignment_type` (we-do/you-do). Requires auth; returns prompts filtered by `current_user.grade_level`.
- GET `/tutor/lesson` — Query params: `topic`, `phase`. Requires auth; returns `LessonContent` (falls back to grade 3 if missing).
- POST `/tutor/chat` — Chat with Socratic agent; accepts `message`, `history`, `topic`, `prompt`.
- POST `/tutor/evaluate` — Send writing text for evaluation; backend uses model and tries to parse JSON feedback.

Example curl (register):
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"test","password":"pass","grade_level":3}'
```

---

## Frontend UX Flow & Components 🧭
- `PhaseTabs` presents three sub-phases (`i-do`, `we-do`, `you-do`). It fetches lesson content (I Do) or prompts (We/You Do) depending on sub-phase and `user`. Axios calls include the JWT from `localStorage` and use `API_BASE_URL` from `src/utils/api.ts`.
- `SocraticChat` manages chat messages and posts to `/tutor/chat`.
- `AuthContext` fetches `/auth/me` on load (15s timeout) and provides `user` & `token` to the app; it handles 401 responses by clearing local session.

Important client-side behavior:
- Uses `127.0.0.1`/`localhost` detection to avoid Windows IPv6 issues.
- Added defensive timeout (15s) for `/auth/me` to avoid indefinite spinner during backend cold starts.

---

## Running Locally (development) 🛠️
1. Clone & install (assumes native Python & Node installed):
```bash
# clone
git clone https://github.com/milind-kopikar/just_write.git
cd just_write

# Python env
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows (PowerShell)
pip install -r backend/requirements.txt

# Frontend
cd frontend
npm ci
cd ..
```
2. Create `.env` (example) at `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@127.0.0.1:5432/just_write
GOOGLE_API_KEY=REPLACE_ME
SECRET_KEY=REPLACE_ME
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
> **DO NOT** commit `.env`. Use `.env.example` as a template.

3. Start backend & frontend:
```bash
# from project root
npm run start:backend    # starts uvicorn for FastAPI
npm run dev --prefix frontend   # starts Next.js dev server
```

4. Seed DB (optional):
```bash
.\.venv\Scripts\python.exe scripts/seed_prompts.py
.\.venv\Scripts\python.exe scripts/seed_lessons_v2.py
```

---

## Secrets & Security 🔒
- **Important**: `backend/.env` was previously committed and has been removed and purged from history. **Rotate any secrets** (Google API key, DB password, SECRET_KEY) immediately. If Google flags a key as leaked it will return permission errors (403) that lead to 503 responses from the backend. The server logs these errors with messages such as "Your API key was reported as leaked. Please use another API key." — rotate keys and re-deploy.
- Add secrets to GitHub Actions / CI secrets — never commit to repo.
- Use `.gitignore` to prevent `node_modules`, `.next`, `.env`, and `.venv` from being tracked.
- Use tools such as `git-secrets` or `truffleHog` in CI to detect leaks.

---

## Troubleshooting & Known Issues ⚠️
- Windows `localhost` vs `127.0.0.1` can cause CORS or resolution anomalies; the app detects host and uses same host for API calls.
- Large files generated by frontend builds (e.g., Next SWC binary) should not be committed — `.gitignore` added; remove them from history if present.
- The evaluator expects JSON returned by the model; if model returns free text, backend falls back to `raw_text` response.

---

## Testing & QA 🧪
- Use `scripts/test_chat.py` to simulate chat/evaluate flows (example scripts exist in `scripts/`).
- Manual tests: register a demo user, log in, switch topics, verify prompts load for your `grade_level`, and run a chat + evaluate cycle.

---

## Future Work & TODOs 🚧
- Persist evaluation results (`StudentScore` relations) and writing drafts for reporting.
- Teacher-facing admin UI for custom prompt/lesson creation and student progress management.
- Add unit/integration tests for chat/evaluation endpoints and model-parsing logic.
- Improve model prompt templates & response validation for higher parsing reliability.

---

## Contribution & Contact ✉️
- Repo: https://github.com/milind-kopikar/just_write
- Author / Owner: Milind Kopikare

If you want a formatted technical whitepaper built from this README (10-page narrative), I can produce an expanded document with sections crafted for non-technical stakeholders and a separate technical appendix for AI engineers.

---

Thank you — this README is intended to be both a developer quick start and a basis for the narrative you want to write. If you want, I can now:
1. Expand this into a multi-page design doc (Word/Markdown) targeted at educational stakeholders, or
2. Generate a 10-page narrative draft directly from this material.

Which would you prefer next? ✨