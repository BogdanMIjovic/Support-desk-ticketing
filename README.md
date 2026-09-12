Support Desk Ticketing System

A simple backend ticketing system (support desk / issue tracker), built with FastAPI and SQLModel. Users can create tickets and track their own, while admins manage all tickets and update their status.

Features
User registration and login (JWT authentication)
Password hashing (pwdlib)
Two user roles: user and admin
CRUD operations for tickets
Ownership logic — regular users can only see and modify their own tickets, admins can see and manage all tickets
Pagination on the ticket list (skip, limit)
Database powered by SQLModel/SQLite, with a User ↔ Ticket relationship (foreign key)
Database schema version tracking via Alembic migrations
Middleware that measures and returns the processing time of each request (X-Process-Time header)
Seed script for creating the first admin account
Test suite covering auth, ticket ownership logic, and validation edge cases (pytest)
Tech stack
Python 3.13
FastAPI
SQLModel (SQLAlchemy + Pydantic)
SQLite
Alembic (database migrations)
JWT (PyJWT) + OAuth2 password flow
pwdlib (password hashing)
pytest + httpx (testing)
Project structure
main.py
create_admin.py
.env
conftest.py
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
test/
├── test_dummy.py
├── test_auth.py
└── test_tickets.py
Data models

User

id, username (unique), full_name, email (unique)
role: USER or ADMIN
is_active
hashed_password

Ticket

id, title, description
status: OPEN, IN_PROGRESS, SOLVED
priority: LOW, MEDIUM, HIGH
created_at
resolution (optional, set by admin)
owner_id (foreign key to User)
Authentication and roles

Authentication uses JWT tokens (OAuth2 password flow). After logging in, the token is sent in the Authorization: Bearer <token> header for all protected routes.

user — can create tickets, and can only see/modify their own tickets (cannot change status or resolution)
admin — can see and modify all tickets, including changing status and setting the resolution
API routes
Method	Route	Description	Access
POST	/register	Register a new user	Public
POST	/token	Log in, returns a JWT token	Public
GET	/ticket	List tickets (paginated)	Logged-in user (user sees their own, admin sees all)
GET	/ticket/{ticket_id}	Get a single ticket	Owner or admin
POST	/ticket	Create a new ticket	Logged-in user
PATCH	/ticket/{ticket_id}	Update a ticket	Owner (limited) or admin (full)
DELETE	/ticket/{ticket_id}	Delete a ticket	Owner or admin
Getting started
Clone the repository and enter the project folder
Create and activate a virtual environment
   python -m venv .venv
   .venv\Scripts\activate
Install dependencies
   pip install -r requirements.txt
Create a .env file in the project root with the following content
   SECRET_KEY=your_secret_key_here
Apply the database migrations
   alembic upgrade head
Run the server
   uvicorn main:app --reload
API documentation (Swagger UI) is available at
   http://127.0.0.1:8000/docs
Creating an admin user

The first admin account is created manually via the seed script (there is no public route for granting the admin role):

python create_admin.py

The script asks for a username, password, and optionally an email/full name, and creates a user with the ADMIN role directly in the database.

Database migrations

This project uses Alembic to track changes to the database schema. After every change to the models in app/models.py:

alembic revision --autogenerate -m "description of the change"
alembic upgrade head
Testing

The project has a pytest test suite covering authentication, ticket CRUD, ownership/permission logic, and a few validation edge cases. Tests run against a separate on-disk SQLite database (test.db), isolated from the app's own database via a get_session dependency override.

Install test dependencies (already included in requirements.txt):

pip install pytest httpx

Run the full test suite:

pytest

Run a specific test file:

pytest test/test_auth.py
pytest test/test_tickets.py

What's covered:

Auth (test/test_auth.py) — registration, duplicate username handling, login (success/failure), access to a protected route with a valid token
Tickets (test/test_tickets.py) — CRUD operations, ownership logic (users can only see/modify their own tickets), admin overrides (status/resolution updates, viewing all tickets), 403/404 handling, and validation edge cases (e.g. missing required fields)
Possible extensions (phase 2)
A dedicated Comment table instead of a single resolution field
Docker support and deployment
