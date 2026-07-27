# ADR-001 

## Context

JWT-only authentication made session management difficult.

## Decision

Introduce a Session aggregate between the User and tokens.

## Consequences

Supports device management, revocation, audit trails, OAuth reuse, and MFA.