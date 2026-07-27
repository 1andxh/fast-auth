## Session

Represents an authenticated device or client.

A user may have multiple active sessions.

---

## Refresh Token Family

A chain of refresh tokens created through rotation.

Replay attacks revoke the entire family.

---

## Repository

A persistence boundary responsible for retrieving and storing domain objects.

Repositories expose domain language rather than CRUD.

---

## Service

Coordinates business workflows and enforces authentication policies.

---

## Transaction Boundary

The point where changes are committed to persistent storage.

Repositories flush.

Services commit.