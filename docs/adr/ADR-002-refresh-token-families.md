# ADR -002

# Context
Refresh token replay attacks need to invalidate an entire chain.

# Decison
Track a family ID across rotated refresh tokens.

# Consequences
Replay attacks invalidate every descendant token.