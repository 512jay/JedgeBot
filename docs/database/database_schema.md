# 📂 Modular Business Database Schema (ERD)

---

## 💾 `auth` — User Identity & Access

| Table | Field | Notes |
|-------|-------|-------|
| **users** | id | PK |
|  | email | unique |
|  | password_hash |  |
|  | role | enum(`client`, `manager`, `enterprise`) |
|  | status | enum(`active`, `grace`, `downgraded`, `banned`) |
|  | created_at | datetime |

---

## 🏢 `org` — Organizational Structure

| Table | Field | Notes |
|-------|-------|-------|
| **enterprises** | id | PK |
|  | user_id | FK → `users.id` |
|  | company_name |  |
|  | subscription_plan |  |
|  | reassignment_policy |  |

| **enterprise_managers** | id | PK |
|  | enterprise_id | FK → `enterprises.id` |
|  | manager_id | FK → `users.id` |

| **clients** | id | PK |
|  | user_id | FK → `users.id` |
|  | default_manager_id | FK → `users.id` |

| **client_manager_assignments** | id | PK |
|  | client_id | FK → `users.id` |
|  | manager_id | FK → `users.id` |
|  | approved | bool |
|  | access_type | enum(`view`, `trade`) |
|  | assigned_by | FK → `users.id` |
|  | assigned_at | datetime |
|  | expires_at | datetime (nullable) |

---

## 💼 `brokerage` — Account Management & Access Control

| Table | Field | Notes |
|-------|-------|-------|
| **brokerage_accounts** | id | PK |
|  | client_id | FK → `users.id` |
|  | broker_name |  |
|  | account_number |  |
|  | balance | int |
|  | verification_status | enum(`pending_email`, `verified`, `disputed`) |
|  | created_by | FK → `users.id` |
|  | created_at | datetime |

| **brokerage_account_permissions** | id | PK |
|  | brokerage_account_id | FK → `brokerage_accounts.id` |
|  | user_id | FK → `users.id` |
|  | access_type | enum(`view`, `trade`) |
|  | granted_by | FK → `users.id` |
|  | granted_at | datetime |

---

## 📜 `audit` — Action Logs & Compliance

| Table | Field | Notes |
|-------|-------|-------|
| **audit_logs** | id | PK |
|  | user_id | FK → `users.id` |
|  | action_type | e.g. `grant_view`, `upgrade_plan` |
|  | target_id | account ID, user ID, or assignment ID |
|  | timestamp | datetime |

