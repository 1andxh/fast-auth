# ADR-004

# Context
A reused refresh token indicates token compromise.

# Decision
Revoke the entire refresh token family and the associated session when reuse is detected.

# Consequence
Improves security by preventing continued use of compromised credentials, at the cost of forcing the user to authenticate again.