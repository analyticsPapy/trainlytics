# Trainlytics - Architecture Documentation

## Table des matières

1. [Vue d'ensemble de l'architecture](#1-vue-densemble-de-larchitecture)
2. [Stack technique Python/React](#2-stack-technique-pythonreact)
   - [Backend Stack](#backend-stack)
   - [Frontend Stack](#frontend-stack)
3. [Architecture des services](#3-architecture-des-services)
   - [Schéma de microservices légers](#schéma-de-microservices-légers)
4. [Base de données et relations](#4-base-de-données-et-relations)
   - [Schéma ERD complet](#schéma-erd-complet)
   - [Modèles SQLAlchemy](#modèles-sqlalchemy)
5. [API et Communication](#5-api-et-communication)
   - [FastAPI Main Application](#fastapi-main-application)
   - [Configuration avec Pydantic](#configuration-avec-pydantic)
   - [Exemple d'endpoint avec dépendances](#exemple-dendpoint-avec-dépendances)
   - [Dependencies (Auth, DB, etc.)](#dependencies-auth-db-etc)
6. [Gestion des connexions externes](#6-gestion-des-connexions-externes)
   - [Architecture des connecteurs](#architecture-des-connecteurs)
   - [Base Connector (Classe abstraite)](#base-connector-classe-abstraite)
   - [Strava Connector Implementation](#strava-connector-implementation)
   - [API Endpoint pour Strava](#api-endpoint-pour-strava)
7. [Sécurité et authentification](#7-sécurité-et-authentification)
   - [JWT Authentication avec FastAPI](#jwt-authentication-avec-fastapi)
   - [Encryption des tokens OAuth](#encryption-des-tokens-oauth)
   - [Rate Limiting](#rate-limiting)
   - [Middleware de sécurité](#middleware-de-sécurité)
8. [Structure des fichiers](#8-structure-des-fichiers-complète)
9. [Déploiement](#9-déploiement)
   - [Docker Setup](#docker-setup)
   - [Backend Dockerfile](#backend-dockerfile)
   - [Frontend Dockerfile (Development)](#frontend-dockerfile-development)
   - [Frontend Dockerfile (Production)](#frontend-dockerfile-production)
   - [Nginx Configuration](#nginx-configuration)
   - [Celery Configuration](#celery-configuration)
   - [Celery Tasks Example](#celery-tasks-example)
   - [Commandes de déploiement](#commandes-de-déploiement)
   - [Production Deployment](#production-deployment-exemple-sur-railwayrender)
10. [Résumé de l'architecture](#résumé-de-larchitecture)
    - [Points clés](#points-clés)
    - [Ordre d'implémentation recommandé](#ordre-dimplémentation-recommandé)

---

## 1. Vue d'ensemble de l'architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        TRAINLYTICS                             │
│                  Python Backend + React Frontend               │
└────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│                      React + TypeScript                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Athlete    │  │     Coach    │  │    Marketing │           │
│  │    Portal    │  │    Portal    │  │     Pages    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                 │
│  State Management: Redux Toolkit / Zustand                      │
│  UI Components: TailwindCSS + shadcn/ui                         │
│  Routing: React Router v6                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/REST + WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                         API GATEWAY                             │
│                      FastAPI + Nginx                            │
│                                                                 │
│  ├─ REST API (FastAPI)                                          │
│  ├─ WebSocket (real-time notifications)                         │
│  ├─ Rate Limiting (SlowAPI)                                     │
│  └─ CORS + Authentication Middleware                            │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                         │
│                     Python 3.11+ Services                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Core Services                         │   │
│  │  ├─ Auth Service (JWT + OAuth2)                          │   │
│  │  ├─ User Service                                         │   │
│  │  ├─ Activity Service                                     │   │
│  │  ├─ Workout Service                                      │   │
│  │  ├─ Plan Service                                         │   │
│  │  ├─ Analytics Service                                    │   │
│  │  ├─ Notification Service                                 │   │
│  │  └─ Comment Service                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 Integration Services                     │   │
│  │  ├─ Strava Connector (httpx async)                       │   │
│  │  ├─ Garmin Connector                                     │   │
│  │  ├─ Polar Connector                                      │   │
│  │  ├─ Coros Connector                                      │   │
│  │  └─ Sync Orchestrator                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  Background Workers                      │   │
│  │  ├─ Celery Workers (async tasks)                         │   │
│  │  ├─ Activity Sync Jobs                                   │   │
│  │  ├─ Metrics Calculation Jobs                             │   │
│  │  ├─ Email Sending Jobs                                   │   │
│  │  └─ Webhook Processing Jobs                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  PostgreSQL  │  │    Redis     │  │   S3/Minio   │           │
│  │              │  │              │  │              │           │
│  │ - Users      │  │ - Sessions   │  │ - Files      │           │
│  │ - Activities │  │ - Cache      │  │ - Exports    │           │
│  │ - Workouts   │  │ - Job Queue  │  │ - Avatars    │           │
│  │ - Plans      │  │ - Pub/Sub    │  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Strava     │  │    Garmin    │  │    Polar     │           │
│  │     API      │  │     API      │  │     API      │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   SendGrid   │  │    Sentry    │  │  Stripe API  │           │
│  │   (Email)    │  │ (Monitoring) │  │  (Payments)  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Stack technique Python/React

### Backend Stack

```python
# Core Framework
fastapi==0.109.0              # API framework
uvicorn[standard]==0.27.0     # ASGI server
pydantic==2.5.0              # Data validation
pydantic-settings==2.1.0     # Settings management

# Database
sqlalchemy==2.0.25           # ORM
alembic==1.13.1              # Migrations
asyncpg==0.29.0              # Async PostgreSQL driver
psycopg2-binary==2.9.9       # PostgreSQL adapter

# Authentication
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4            # Password hashing
python-multipart==0.0.6           # OAuth2

# HTTP Client
httpx==0.26.0                # Async HTTP client (pour APIs externes)
aiohttp==3.9.1               # Alternative async HTTP

# Background Tasks
celery==5.3.4                # Task queue
redis==5.0.1                 # Cache & message broker
flower==2.0.1                # Celery monitoring

# Utilities
python-dotenv==1.0.0         # Environment variables
pytz==2023.3                 # Timezone handling
python-dateutil==2.8.2       # Date utilities
pydantic-extra-types==2.3.0  # Extra Pydantic types

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx[test]==0.26.0

# Monitoring & Logging
sentry-sdk==1.39.2           # Error tracking
structlog==23.3.0            # Structured logging

# Security
cryptography==41.0.7         # Encryption
slowapi==0.1.9               # Rate limiting

# Email
python-mailgun3==1.2.0       # Email service
jinja2==3.1.2                # Email templates

# Data Processing
pandas==2.1.4                # Data analysis
numpy==1.26.2                # Numerical computing
```

### Frontend Stack

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",

    "// State Management": "",
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",

    "// API Client": "",
    "axios": "^1.6.5",
    "swr": "^2.2.4",

    "// UI Components": "",
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-toast": "^1.1.5",
    "lucide-react": "^0.307.0",

    "// Forms": "",
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.4",

    "// Charts": "",
    "recharts": "^2.10.3",

    "// Date": "",
    "date-fns": "^3.0.6",

    "// Utils": "",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.47",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.3.3",
    "vite": "^5.0.11",
    "eslint": "^8.56.0",
    "prettier": "^3.1.1"
  }
}
```

---

## 3. Architecture des services

### Schéma de microservices légers

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONOLITH MODULAIRE                           │
│                    (Single FastAPI App)                         │
└─────────────────────────────────────────────────────────────────┘
```

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Point d'entrée FastAPI
│   │
│   ├── api/                       # API Endpoints
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependencies (auth, db, etc.)
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # POST /login, /register
│   │   │   ├── users.py           # CRUD users
│   │   │   ├── activities.py      # CRUD activities
│   │   │   ├── workouts.py        # CRUD workouts
│   │   │   ├── plans.py           # CRUD training plans
│   │   │   ├── comments.py        # CRUD comments
│   │   │   ├── notifications.py   # Notifications
│   │   │   ├── analytics.py       # Analytics endpoints
│   │   │   └── connectors/
│   │   │       ├── strava.py      # Strava OAuth + webhook
│   │   │       ├── garmin.py
│   │   │       ├── polar.py
│   │   │       └── coros.py
│   │   └── websockets/
│   │       └── notifications.py   # WebSocket for real-time
│   │
│   ├── core/                      # Configuration globale
│   │   ├── __init__.py
│   │   ├── config.py              # Settings (Pydantic)
│   │   ├── security.py            # JWT, password hashing
│   │   └── logging.py             # Logging config
│   │
│   ├── db/                        # Database
│   │   ├── __init__.py
│   │   ├── base.py                # Base SQLAlchemy
│   │   ├── session.py             # DB session management
│   │   └── init_db.py             # DB initialization
│   │
│   ├── models/                    # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── activity.py
│   │   ├── workout.py
│   │   ├── plan.py
│   │   ├── comment.py
│   │   ├── notification.py
│   │   ├── connected_account.py
│   │   ├── athlete_coach.py
│   │   └── sync_log.py
│   │
│   ├── schemas/                   # Pydantic Schemas (DTO)
│   │   ├── __init__.py
│   │   ├── user.py                # UserCreate, UserRead, UserUpdate
│   │   ├── activity.py
│   │   ├── workout.py
│   │   ├── plan.py
│   │   ├── comment.py
│   │   ├── notification.py
│   │   └── token.py
│   │
│   ├── services/                  # Business Logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── activity_service.py
│   │   ├── workout_service.py
│   │   ├── plan_service.py
│   │   ├── comment_service.py
│   │   ├── notification_service.py
│   │   ├── analytics_service.py
│   │   ├── permission_service.py
│   │   └── connectors/
│   │       ├── base_connector.py
│   │       ├── strava_connector.py
│   │       ├── garmin_connector.py
│   │       ├── polar_connector.py
│   │       ├── coros_connector.py
│   │       └── sync_orchestrator.py
│   │
│   ├── workers/                   # Celery Tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py          # Celery configuration
│   │   ├── activity_sync.py       # Sync tasks
│   │   ├── metrics_calculation.py # Analytics tasks
│   │   ├── email_tasks.py         # Email sending
│   │   └── webhook_tasks.py       # Webhook processing
│   │
│   ├── utils/                     # Utilities
│   │   ├── __init__.py
│   │   ├── email.py               # Email helpers
│   │   ├── encryption.py          # Token encryption
│   │   ├── validators.py          # Custom validators
│   │   └── formatters.py          # Data formatters
│   │
│   └── tests/                     # Tests
│       ├── __init__.py
│       ├── conftest.py            # Pytest fixtures
│       ├── test_auth.py
│       ├── test_activities.py
│       └── test_connectors.py
│
├── alembic/                       # Database Migrations
│   ├── versions/
│   └── env.py
│
├── .env.example
├── .env
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml                 # Poetry config (alternative)
├── pytest.ini
└── README.md
```

---

## 4. Base de données et relations

### Schéma ERD complet

```
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│       users          │
├──────────────────────┤
│ id (PK)             │◄──────────────┐
│ email               │               │
│ hashed_password     │               │
│ name                │               │
│ avatar_url          │               │
│ role (enum)         │               │
│ timezone            │               │
│ created_at          │               │
│ updated_at          │               │
└──────────────────────┘               │
         │                             │
         │ 1:1                         │ 1:N
         ▼                             │
┌──────────────────────┐               │
│   coach_profiles     │               │
├──────────────────────┤               │
│ id (PK)             │               │
│ user_id (FK) UNIQUE │               │
│ bio                 │               │
│ specialties         │               │
│ max_athletes        │               │
│ accepting_new       │               │
└──────────────────────┘               │
                                       │
┌──────────────────────┐               │
│  athlete_coaches     │               │
├──────────────────────┤               │
│ id (PK)             │               │
│ athlete_id (FK) ────┼───────────────┘
│ coach_id (FK) ──────┼───────────────┐
│ status (enum)       │               │
│ permissions (JSONB) │               │
│ start_date          │               │
│ end_date            │               │
│ created_at          │               │
└──────────────────────┘               │
                                       │
                                       │
┌──────────────────────┐               │
│ connected_accounts   │               │
├──────────────────────┤               │
│ id (PK)             │               │
│ user_id (FK) ───────┼───────────────┘
│ provider (enum)     │
│ provider_user_id    │
│ access_token        │  ← Encrypted
│ refresh_token       │  ← Encrypted
│ token_expires_at    │
│ sync_enabled        │
│ last_sync_at        │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│     activities       │
├──────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ connected_account_id│
│ provider            │
│ provider_activity_id│
│ name                │
│ activity_type       │
│ start_date          │
│ duration_seconds    │
│ distance_meters     │
│ elevation_gain      │
│ avg_heart_rate      │
│ avg_power           │
│ avg_speed_mps       │
│ calories            │
│ raw_data (JSONB)    │
│ available_metrics   │
│ created_at          │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│  activity_streams    │
├──────────────────────┤
│ id (PK)             │
│ activity_id (FK)    │
│ stream_type (enum)  │
│ data (JSONB)        │
│ resolution          │
└──────────────────────┘


┌──────────────────────┐
│   training_plans     │
├──────────────────────┤
│ id (PK)             │
│ created_by (FK)     │
│ athlete_id (FK)     │
│ name                │
│ description         │
│ start_date          │
│ end_date            │
│ weeks_count         │
│ is_template         │
│ status (enum)       │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│      workouts        │
├──────────────────────┤
│ id (PK)             │
│ training_plan_id(FK)│
│ created_by (FK)     │
│ athlete_id (FK)     │
│ title               │
│ workout_type        │
│ scheduled_date      │
│ target_duration     │
│ target_distance     │
│ target_heart_rate   │
│ structure (JSONB)   │
│ status (enum)       │
│ activity_id (FK)    │ ← Lien vers activité réelle
│ completed_at        │
└──────────────────────┘
         │
         │ 1:N
         ▼
┌──────────────────────┐
│      comments        │
├──────────────────────┤
│ id (PK)             │
│ author_id (FK)      │
│ target_id (FK)      │
│ workout_id (FK)     │
│ activity_id (FK)    │
│ content             │
│ created_at          │
└──────────────────────┘


┌──────────────────────┐
│   notifications      │
├──────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ type (enum)         │
│ title               │
│ message             │
│ action_url          │
│ is_read             │
│ created_at          │
└──────────────────────┘


┌──────────────────────┐
│    user_metrics      │
├──────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ date                │
│ period_type (enum)  │
│ total_distance      │
│ total_duration      │
│ activity_count      │
│ fitness_level (CTL) │
│ fatigue_level (ATL) │
│ form (TSB)          │
│ calculated_at       │
└──────────────────────┘
```

### Modèles SQLAlchemy

#### backend/app/models/user.py

```python
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class UserRole(str, enum.Enum):
    ATHLETE = "athlete"
    COACH = "coach"
    BOTH = "both"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    avatar_url = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.ATHLETE)
    timezone = Column(String, default="UTC")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)

    # Relationships
    coach_profile = relationship("CoachProfile", back_populates="user", uselist=False)
    connected_accounts = relationship("ConnectedAccount", back_populates="user")
    activities = relationship("Activity", back_populates="user")

    # Coaching relationships
    coaching_as_athlete = relationship(
        "AthleteCoach",
        foreign_keys="AthleteCoach.athlete_id",
        back_populates="athlete"
    )
    coaching_as_coach = relationship(
        "AthleteCoach",
        foreign_keys="AthleteCoach.coach_id",
        back_populates="coach"
    )

    # Plans
    plans_created = relationship(
        "TrainingPlan",
        foreign_keys="TrainingPlan.created_by",
        back_populates="creator"
    )
    plans_assigned = relationship(
        "TrainingPlan",
        foreign_keys="TrainingPlan.athlete_id",
        back_populates="athlete"
    )

    # Workouts
    workouts_created = relationship(
        "Workout",
        foreign_keys="Workout.created_by",
        back_populates="creator"
    )
    workouts_assigned = relationship(
        "Workout",
        foreign_keys="Workout.athlete_id",
        back_populates="athlete"
    )
```

#### backend/app/models/activity.py

```python
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Enum as SQLEnum, JSON, Index
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class ActivityType(str, enum.Enum):
    RUN = "run"
    RIDE = "ride"
    SWIM = "swim"
    WORKOUT = "workout"
    WALK = "walk"
    HIKE = "hike"
    OTHER = "other"

class Provider(str, enum.Enum):
    STRAVA = "strava"
    GARMIN = "garmin"
    POLAR = "polar"
    COROS = "coros"
    MANUAL = "manual"

class DataQuality(str, enum.Enum):
    FULL = "full"
    PARTIAL = "partial"
    MINIMAL = "minimal"

class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    connected_account_id = Column(String, ForeignKey("connected_accounts.id"))

    # Source tracking
    provider = Column(SQLEnum(Provider), nullable=False)
    provider_activity_id = Column(String, nullable=False)
    data_quality = Column(SQLEnum(DataQuality), default=DataQuality.FULL)

    # Basic metadata
    name = Column(String, nullable=False)
    description = Column(String)
    activity_type = Column(SQLEnum(ActivityType), nullable=False, index=True)
    sport_type = Column(String)

    # Date & Time
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime)
    timezone = Column(String)

    # Core metrics
    duration_seconds = Column(Integer)
    distance_meters = Column(Float)
    moving_time_seconds = Column(Integer)

    # Elevation
    elevation_gain_meters = Column(Float)
    elevation_loss_meters = Column(Float)

    # Heart Rate
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)

    # Power
    avg_power = Column(Float)
    max_power = Column(Float)
    normalized_power = Column(Float)

    # Speed
    avg_speed_mps = Column(Float)
    max_speed_mps = Column(Float)

    # Other
    avg_cadence = Column(Float)
    avg_temperature = Column(Float)
    calories = Column(Integer)

    # GPS
    start_latlng = Column(JSON)
    end_latlng = Column(JSON)

    # Flags
    is_manual = Column(Boolean, default=False)
    shared_with_coach = Column(Boolean, default=True)

    # Data
    available_metrics = Column(JSON, default={})
    raw_data = Column(JSON, nullable=False)
    processed_data = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="activities")
    connected_account = relationship("ConnectedAccount", back_populates="activities")
    streams = relationship("ActivityStream", back_populates="activity", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="activity")
    workout = relationship("Workout", back_populates="activity", uselist=False)

    __table_args__ = (
        Index('idx_user_provider_activity', 'user_id', 'provider_activity_id', unique=True),
    )
```

#### backend/app/models/workout.py

```python
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class WorkoutStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    POSTPONED = "postponed"

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(String, primary_key=True, index=True)
    training_plan_id = Column(String, ForeignKey("training_plans.id"))
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    athlete_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Workout info
    title = Column(String, nullable=False)
    description = Column(String)
    workout_type = Column(String, nullable=False)

    # Scheduling
    scheduled_date = Column(DateTime, nullable=False, index=True)
    scheduled_time = Column(String)

    # Target metrics
    target_duration = Column(Integer)
    target_distance = Column(Float)
    target_pace = Column(Float)
    target_heart_rate = Column(Integer)
    target_power = Column(Float)

    # Structured workout
    structure = Column(JSON)

    # Completion
    status = Column(SQLEnum(WorkoutStatus), default=WorkoutStatus.PLANNED, index=True)
    completed_at = Column(DateTime)
    activity_id = Column(String, ForeignKey("activities.id"), unique=True)

    # Feedback
    athlete_notes = Column(String)
    coach_feedback = Column(String)
    rpe = Column(Integer)  # Rate of Perceived Exertion (1-10)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    training_plan = relationship("TrainingPlan", back_populates="workouts")
    creator = relationship("User", foreign_keys=[created_by], back_populates="workouts_created")
    athlete = relationship("User", foreign_keys=[athlete_id], back_populates="workouts_assigned")
    activity = relationship("Activity", back_populates="workout")
    comments = relationship("Comment", back_populates="workout")
```

---

## 5. API et Communication

### FastAPI Main Application

#### backend/app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import sentry_sdk

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import auth, users, activities, workouts, plans, comments, notifications, analytics
from app.api.v1.connectors import strava, garmin, polar, coros

# Initialize Sentry
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.1,
        environment=settings.ENVIRONMENT
    )

# Setup logging
setup_logging()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Trainlytics API",
    description="API for Trainlytics - Coach & Athlete Training Platform",
    version="1.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
app.include_router(workouts.router, prefix="/api/v1/workouts", tags=["workouts"])
app.include_router(plans.router, prefix="/api/v1/plans", tags=["plans"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

# Connectors
app.include_router(strava.router, prefix="/api/v1/connectors/strava", tags=["strava"])
app.include_router(garmin.router, prefix="/api/v1/connectors/garmin", tags=["garmin"])
app.include_router(polar.router, prefix="/api/v1/connectors/polar", tags=["polar"])
app.include_router(coros.router, prefix="/api/v1/connectors/coros", tags=["coros"])

@app.get("/")
async def root():
    return {
        "message": "Trainlytics API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Configuration avec Pydantic

#### backend/app/core/config.py

```python
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Trainlytics"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # OAuth Providers
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    STRAVA_CALLBACK_URL: str

    GARMIN_CONSUMER_KEY: str
    GARMIN_CONSUMER_SECRET: str

    POLAR_CLIENT_ID: str
    POLAR_CLIENT_SECRET: str

    COROS_API_KEY: str
    COROS_API_SECRET: str

    # Email
    SMTP_HOST: str = "smtp.sendgrid.net"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    FROM_EMAIL: str

    # File Storage (S3/Minio)
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "trainlytics"

    # Monitoring
    SENTRY_DSN: str = ""

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Exemple d'endpoint avec dépendances

#### backend/app/api/v1/activities.py

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.activity import Activity, ActivityType, Provider
from app.schemas.activity import ActivityRead, ActivityCreate, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter()

@router.get("/", response_model=List[ActivityRead])
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    activity_type: Optional[ActivityType] = None,
    provider: Optional[Provider] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer les activités de l'utilisateur
    """
    service = ActivityService(db)

    activities = service.get_user_activities(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        activity_type=activity_type,
        provider=provider,
        start_date=start_date,
        end_date=end_date
    )

    return activities

@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer une activité spécifique
    """
    service = ActivityService(db)

    activity = service.get_activity(activity_id)

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Vérifier les permissions
    if activity.user_id != current_user.id:
        # Si c'est un coach, vérifier la relation
        if not service.coach_can_view_activity(current_user.id, activity):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this activity"
            )

    return activity

@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_manual_activity(
    activity_in: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Créer une activité manuelle
    """
    service = ActivityService(db)

    activity = service.create_manual_activity(
        user_id=current_user.id,
        activity_data=activity_in
    )

    return activity
```

### Dependencies (Auth, DB, etc.)

#### backend/app/api/deps.py

```python
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

def get_db() -> Generator:
    """
    Dependency pour obtenir une session DB
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency pour obtenir l'utilisateur courant depuis le JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()

    if user is None:
        raise credentials_exception

    return user

async def get_current_coach(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Vérifier que l'utilisateur est un coach
    """
    if current_user.role not in ["coach", "both"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a coach"
        )
    return current_user
```

---

## 6. Gestion des connexions externes

### Architecture des connecteurs

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONNECTOR ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   Base Connector     │  ← Classe abstraite
│   (ABC Protocol)     │
├──────────────────────┤
│ + authenticate()     │
│ + refresh_token()    │
│ + get_activities()   │
│ + get_activity()     │
│ + normalize_activity│
│ + handle_webhook()   │
└──────────────────────┘
          ▲
          │ implements
          │
    ┌─────┴─────┬─────────┬──────────┐
    │           │         │          │
┌───┴───┐  ┌───┴───┐ ┌──┴────┐ ┌───┴────┐
│Strava │  │Garmin │ │Polar  │ │ Coros  │
│Conn.  │  │Conn.  │ │Conn.  │ │ Conn.  │
└───────┘  └───────┘ └───────┘ └────────┘
```

**Flow de synchronisation:**

1. User connects → OAuth flow → Store tokens (encrypted)
2. Initial sync → Fetch last 90 days
3. Register webhook → Real-time updates
4. Background sync → Celery task every hour
5. Normalize data → Common format → Store in DB

### Base Connector (Classe abstraite)

See the full implementation in the architecture document above (Section 6).

### Strava Connector Implementation

See the full implementation in the architecture document above (Section 6).

### API Endpoint pour Strava

See the full implementation in the architecture document above (Section 6).

---

## 7. Sécurité et authentification

### JWT Authentication avec FastAPI

#### backend/app/core/security.py

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hasher un mot de passe"""
    return pwd_context.hash(password)

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Créer un JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt
```

### Encryption des tokens OAuth

#### backend/app/utils/encryption.py

```python
from cryptography.fernet import Fernet
from app.core.config import settings
import base64

def get_cipher():
    """Obtenir le cipher Fernet"""
    key = settings.SECRET_KEY[:32].encode()
    key_base64 = base64.urlsafe_b64encode(key)
    return Fernet(key_base64)

def encrypt_token(token: str) -> str:
    """Chiffrer un token OAuth"""
    cipher = get_cipher()
    encrypted = cipher.encrypt(token.encode())
    return encrypted.decode()

def decrypt_token(encrypted_token: str) -> str:
    """Déchiffrer un token OAuth"""
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_token.encode())
    return decrypted.decode()
```

### Rate Limiting

See rate limiting examples in Section 5 (API and Communication).

### Middleware de sécurité

#### backend/app/middleware/security.py

```python
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Ajouter des headers de sécurité"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response
```

---

## 8. Structure des fichiers complète

```
trainlytics/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── activities.py
│   │   │       ├── workouts.py
│   │   │       ├── plans.py
│   │   │       └── connectors/
│   │   │           ├── strava.py
│   │   │           ├── garmin.py
│   │   │           ├── polar.py
│   │   │           └── coros.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── activity.py
│   │   │   ├── workout.py
│   │   │   └── ...
│   │   ├── schemas/
│   │   ├── services/
│   │   │   └── connectors/
│   │   ├── workers/
│   │   │   ├── celery_app.py
│   │   │   ├── activity_sync.py
│   │   │   └── ...
│   │   ├── utils/
│   │   ├── middleware/
│   │   └── tests/
│   │
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── layout/
│   │   │   ├── athlete/
│   │   │   └── coach/
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   ├── athlete/
│   │   │   └── coach/
│   │   ├── services/
│   │   ├── store/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── hooks/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 9. Déploiement

### Docker Setup

#### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: trainlytics
      POSTGRES_USER: trainlytics_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://trainlytics_user:${DB_PASSWORD}@postgres:5432/trainlytics
      - REDIS_URL=redis://redis:6379/0

  celery_worker:
    build:
      context: ./backend
    command: celery -A app.workers.celery_app worker --loglevel=info

  frontend:
    build:
      context: ./frontend
    ports:
      - "5173:5173"

volumes:
  postgres_data:
  redis_data:
```

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (Development)

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### Frontend Dockerfile (Production)

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration

```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://frontend;
    }

    location /api {
        proxy_pass http://backend;
    }
}
```

### Celery Configuration

#### backend/app/workers/celery_app.py

```python
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "trainlytics",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.beat_schedule = {
    'sync-all-active-accounts': {
        'task': 'app.workers.activity_sync.sync_all_active_accounts',
        'schedule': crontab(minute='0', hour='*/1'),
    },
}
```

### Celery Tasks Example

See Section 9 for complete Celery task examples.

### Commandes de déploiement

```bash
# Développement local
docker-compose up -d

# Exécuter les migrations
docker-compose exec backend alembic upgrade head

# Accéder à la DB
docker-compose exec postgres psql -U trainlytics_user -d trainlytics

# Arrêter tout
docker-compose down
```

### Production Deployment (exemple sur Railway/Render)

See Section 9 for production deployment configuration examples.

---

## Résumé de l'architecture

### Points clés

1. **Backend Python/FastAPI**
   - Architecture modulaire et maintenable
   - Async/await pour performance
   - Celery pour tâches asynchrones
   - SQLAlchemy pour ORM robuste

2. **Frontend React**
   - TypeScript pour type safety
   - Redux Toolkit pour state management
   - Vite pour build rapide
   - TailwindCSS pour styling

3. **Database PostgreSQL**
   - Relations complexes bien gérées
   - JSONB pour données flexibles
   - Indexes optimisés

4. **Redis**
   - Cache
   - Session storage
   - Celery broker
   - Pub/Sub pour WebSocket

5. **Sécurité**
   - JWT authentication
   - Token encryption
   - Rate limiting
   - CORS configuré

6. **Scalabilité**
   - Microservices pattern (modulaire)
   - Background workers
   - Caching strategy
   - Horizontal scaling ready

### Ordre d'implémentation recommandé

**Semaine 1-2: Base**
- Setup projet (backend + frontend)
- Database + migrations
- Auth (JWT)
- CRUD Users

**Semaine 3-4: Core features**
- Strava connector
- Activities CRUD
- Celery setup
- Basic sync

**Semaine 5-6: Coach features**
- Coach/Athlete relationships
- Workouts
- Invitations

**Semaine 7-8: Advanced**
- Plans d'entraînement
- Notifications
- Analytics
- Permissions

**Semaine 9-10: Polish**
- Multi-providers (Garmin, Polar)
- WebSocket real-time
- Tests
- Déploiement
