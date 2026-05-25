from src.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
