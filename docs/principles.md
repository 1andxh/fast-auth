# Engineering Principles

FastAuth is built around a number of engineering principles that guide architectural decisions.

## Understand before implementing

Architecture is designed before code is written.

## Business policy over infrastructure

Business rules should not depend on frameworks or databases.

## Services orchestrate

Services coordinate workflows and enforce business rules.

## Repositories persist

Repositories own database access and persistence concerns.

## Explicit over implicit

Code should favour readability and predictability over hidden behaviour.

## Security by design

Security is considered part of the architecture rather than an afterthought.

## Evolution over premature abstraction

Abstractions are introduced when justified by the system, not by convention.