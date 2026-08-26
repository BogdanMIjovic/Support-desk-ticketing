# Support Desk Ticketing System

A simple backend ticketing system (support desk / issue tracker), built with **FastAPI** and **SQLModel**. Users can create tickets and track their own, while admins manage all tickets and update their status.

## Features

- User registration and login (JWT authentication)
- Password hashing (pwdlib)
- Two user roles: `user` and `admin`
- CRUD operations for tickets
- Ownership logic — regular users can only see and modify their own tickets, admins can see and manage all tickets
- Pagination on the ticket list (`skip`, `limit`)
- Database powered by SQLModel/SQLite, with a User ↔ Ticket relationship (foreign key)
- Database schema version tracking via Alembic migrations
- Middleware that measures and returns the processing time of each request (`X-Process-Time` header)
- Seed script for creating the first admin account

## Tech stack

- Python 3.13
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- Alembic (database migrations)
- JWT (PyJWT) + OAuth2 password flow
- pwdlib (password hashing)

## Project structure

```
main.py
create_admin.py
.env
alembic/
├── env.py
└── versions/
app/
├── models.py          (SQLModel tables: User, Ticket)
├── database.py        (engine, get_session)
├── schemas.py         (Pydantic: Create/Update/Out models, Token)
├── auth.py            (JWT, hashing, route protection)
├── routes/
│   ├── auth_routes.py
│   └── ticket_routes.py
└── middleware/
    └── timer.py
```

## Data models

**User**
- `id`, `username` (unique), `full_name`, `email` (unique)
- `role`: `USER` or `ADMIN`
- `is_active`
- `hashed_password`

**Ticket**
- `id`, `title`, `description`
- `status`: `OPEN`, `IN_PROGRESS`, `SOLVED`
- `priority`: `LOW`, `MEDIUM`, `HIGH`
- `created_at`
- `resolution` (optional, set by admin)
- `owner_id` (foreign key to `User`)

## Authentication and roles

Authentication uses JWT tokens (OAuth2 password flow). After logging in, the token is sent in the `Authorization: Bearer <token>` header for all protected routes.

- **user** — can create tickets, and can only see/modify their own tickets (cannot change `status` or `resolution`)
- **admin** — can see and modify all tickets, including changing status and setting the resolution

## API routes

| Method | Route | Description | Access |
|---|---|---|---|
| POST | `/register` | Register a new user | Public |
| POST | `/token` | Log in, returns a JWT token | Public |
| GET | `/ticket` | List tickets (paginated) | Logged-in user (user sees their own, admin sees all) |
| GET | `/ticket/{ticket_id}` | Get a single ticket | Owner or admin |
| POST | `/ticket` | Create a new ticket | Logged-in user |
| PATCH | `/ticket/{ticket_id}` | Update a ticket | Owner (limited) or admin (full) |
| DELETE | `/ticket/{ticket_id}` | Delete a ticket | Owner or admin |

## Getting started

1. Clone the repository and enter the project folder

2. Create and activate a virtual environment
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content
   ```
   SECRET_KEY=your_secret_key_here
   ```

5. Apply the database migrations
   ```
   alembic upgrade head
   ```

6. Run the server
   ```
   uvicorn main:app --reload
   ```

7. API documentation (Swagger UI) is available at
   ```
   http://127.0.0.1:8000/docs
   ```

## Creating an admin user

The first admin account is created manually via the seed script (there is no public route for granting the admin role):

```
python create_admin.py
```

The script asks for a username, password, and optionally an email/full name, and creates a user with the `ADMIN` role directly in the database.

## Database migrations

This project uses Alembic to track changes to the database schema. After every change to the models in `app/models.py`:

```
alembic revision --autogenerate -m "description of the change"
alembic upgrade head
```

## Possible extensions (phase 2)

- A dedicated `Comment` table instead of a single `resolution` field
- Docker support and deployment
- Tests (pytest)
