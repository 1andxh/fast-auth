# FastAuth

FastAuth is a production-grade authentication service built with FastAPI, SQLAlchemy 2.0, PostgreSQL and JWT.

Unlike tutorial projects, FastAuth is designed around software engineering principles rather than framework features. The project emphasises clear architectural boundaries, maintainability, and security.

## Goals

- Production-ready authentication
- Session-centric architecture
- Refresh token rotation
- Replay attack detection
- Repository pattern
- Structured logging
- Comprehensive testing
- Extensible identity platform

## Current Features

- User registration
- Login
- JWT access tokens
- Refresh token rotation
- Session management
- Rate limiting
- Structured exception handling
- Integration tests

## Architecture

FastAuth follows a layered architecture.

HTTP Request
→ Routes
→ Dependency Injection
→ Services
→ Repositories
→ SQLAlchemy
→ PostgreSQL

Further documentation can be found in the `docs/` directory.