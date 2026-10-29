# Support Desk Ticketing System

A simple backend ticketing system (support desk / issue tracker), built with FastAPI and SQLModel. Users can create tickets and track their own, while admins manage all tickets and update their status.

## Live demo

Deployed on Render: https://support-desk-ticketing.onrender.com/docs

Note: the free Render instance spins down after periods of inactivity, so the first request after idle time may take up to ~50 seconds.

## Features
- User registration and login (JWT authentication)
- Password hashing (pwdlib)
- Two user roles: user and admin
- CRUD operations for tickets
- Ownership logic — regular users can only see and modify their own tickets, admins can see and manage all tickets
- Pagination on the ticket list (skip, limit)
- Database powered by SQLModel/PostgreSQL, with a User ↔ Ticket relationship (foreign key)
- Database schema version tracking via Alembic migrations
- Middleware that measures and returns the processing time of each request (X-Process-Time header)
- Seed script for creating the first admin account
- Dockerized app and database, orchestrated with Docker Compose
- Pytest test suite covering auth, CRUD, ownership/permission logic, and validation edge cases
- Deployed to Render (Web Service + managed PostgreSQL)

## Tech stack
- Python 3.13
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- PostgreSQL
- Alembic (database migrations)
- JWT (PyJWT) + OAuth2 password flow
- pwdlib (password hashing)
- Docker & Docker Compose
- Pytest
- Render (deployment)

[... ostatak fajla do "Possible extensions" ostaje isti ...]

## Possible extensions (phase 2)
- A dedicated Comment table instead of a single resolution field