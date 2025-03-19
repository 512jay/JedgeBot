from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime

# Load environment variables
BUSINESS_DATABASE_URL = os.getenv(
    "BUSINESS_DATABASE_URL",
    "postgresql://jedgebot_admin:password@localhost:5433/jedgebot_business",
)

engine = create_engine(BUSINESS_DATABASE_URL)
Base = declarative_base()


# User Roles (manager, client)
class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    auth_user_id = Column(Integer, nullable=False)  # Links to auth_db.users
    role = Column(String, nullable=False)  # "manager", "client"


# Managers & Clients Mapping
class ManagerClient(Base):
    __tablename__ = "managers_clients"
    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, nullable=False)  # Links to auth_db.users
    client_id = Column(Integer, nullable=False)  # Links to auth_db.users
    active = Column(Boolean, default=True)


# Subscription Plans
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True)
    auth_user_id = Column(Integer, nullable=False)  # Links to auth_db.users
    plan_type = Column(String, nullable=False)  # "free", "client", "manager"
    active_until = Column(DateTime, nullable=True)


# Broker Accounts
class BrokerAccount(Base):
    __tablename__ = "broker_accounts"
    id = Column(Integer, primary_key=True)
    auth_user_id = Column(Integer, nullable=False)  # Links to auth_db.users
    broker_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)


# Create tables
def init_business_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_business_db()
    print("Business database setup complete.")
