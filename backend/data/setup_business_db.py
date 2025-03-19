from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Numeric,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from datetime import datetime

# Load environment variables
BUSINESS_DATABASE_URL = os.getenv(
    "BUSINESS_DATABASE_URL",
    "postgresql://jedgebot_admin:password@localhost:5433/jedgebot_business",
)

engine = create_engine(BUSINESS_DATABASE_URL)
Base = declarative_base()


# Users table (links to auth_db.users)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    auth_user_id = Column(
        Integer, nullable=False, unique=True
    )  # Links to auth_db.users
    created_at = Column(DateTime, default=datetime.utcnow)


# Roles table
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # e.g., manager, client, admin


# User Roles Mapping
class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)


# Subscription Plans
class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String, nullable=False)  # "free", "client", "manager"
    active_until = Column(DateTime, nullable=True)


# Broker Accounts
class BrokerAccount(Base):
    __tablename__ = "broker_accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    broker_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)


# Transactions (for payments and trading logs)
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    status = Column(String, nullable=False)  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)


# Clients Table (if managers oversee multiple clients)
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    active = Column(Boolean, default=True)


# Create tables
def init_business_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_business_db()
    print("Business database setup complete.")
