# ADR-003

# Context
Services were accumulating persistence responsibilities.

# Decison
Move persistence concerns into repositories.

# Consequences
Services focus on business policy; repositories own SQLAlchemy interactions.