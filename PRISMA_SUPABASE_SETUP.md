# Trainlytics - Prisma + Supabase Setup Guide

## 🗄️ Database Architecture

Trainlytics uses **Prisma** as the ORM with **Supabase PostgreSQL** for database management.

### Why Prisma + Supabase?

- ✅ **Type-safe database access** with Python async support
- ✅ **Auto-generated migrations** from schema changes
- ✅ **Supabase** provides managed PostgreSQL with built-in features
- ✅ **Real-time capabilities** with Supabase subscriptions
- ✅ **Built-in authentication** and row-level security

---

## 📋 Prerequisites

1. **Supabase Account**: Sign up at https://supabase.com
2. **Python 3.11+** installed
3. **Node.js 16+** (for Prisma CLI)

---

## 🚀 Step 1: Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Click "New Project"
3. Fill in project details:
   - **Name**: `trainlytics`
   - **Database Password**: (save this securely!)
   - **Region**: Choose closest to your users
4. Wait for project to be created (~2 minutes)

5. Get your **Database Connection String**:
   - Go to Project Settings → Database
   - Copy the **Connection string** (URI mode)
   - It looks like: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

---

## 🔧 Step 2: Configure Environment

1. **Update backend/.env**:

```bash
# Database (Supabase PostgreSQL)
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"

# Prisma
PRISMA_TELEMETRY_DISABLED=1

# App configuration
SECRET_KEY="your-secret-key-here"
ENVIRONMENT="development"

# External connectors
STRAVA_CLIENT_ID="your-strava-client-id"
STRAVA_CLIENT_SECRET="your-strava-client-secret"
STRAVA_CALLBACK_URL="http://localhost:8000/api/v1/connectors/strava/callback"

GARMIN_CONSUMER_KEY="your-garmin-key"
GARMIN_CONSUMER_SECRET="your-garmin-secret"

POLAR_CLIENT_ID="your-polar-client-id"
POLAR_CLIENT_SECRET="your-polar-client-secret"

COROS_API_KEY="your-coros-key"
COROS_API_SECRET="your-coros-secret"

# Redis
REDIS_URL="redis://localhost:6379/0"

# Celery
CELERY_BROKER_URL="redis://localhost:6379/1"
```

2. **Update .env values**:
   - Replace `[YOUR-PASSWORD]` with your Supabase database password
   - Replace `[PROJECT-REF]` with your Supabase project reference
   - Generate a strong `SECRET_KEY`: `openssl rand -hex 32`

---

## 📦 Step 3: Install Dependencies

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install Prisma CLI globally (optional, for convenience)
npm install -g prisma

# Generate Prisma Client
prisma generate --schema=./prisma/schema.prisma
```

---

## 🏗️ Step 4: Run Migrations

### Option A: Create and Apply Migration

```bash
cd backend

# Create a new migration
prisma migrate dev --name init --schema=./prisma/schema.prisma

# This will:
# 1. Create migration SQL files
# 2. Apply migration to your database
# 3. Generate Prisma Client
```

### Option B: Push Schema (Development Only)

For rapid development without migrations:

```bash
prisma db push --schema=./prisma/schema.prisma
```

⚠️ **Warning**: `db push` doesn't create migration history. Use for prototyping only!

---

## 🔍 Step 5: Verify Database

### Check Tables in Supabase Dashboard

1. Go to Supabase Dashboard → Table Editor
2. You should see all tables:
   - `users`
   - `activities`
   - `workouts`
   - `training_plans`
   - `connected_accounts`
   - `coach_profiles`
   - `athlete_coaches`
   - `comments`
   - `notifications`
   - `user_metrics`

### Or Check via Prisma Studio

```bash
prisma studio --schema=./prisma/schema.prisma
```

Opens a visual database editor at `http://localhost:5555`

---

## 🐍 Step 6: Using Prisma in Python

### Import Prisma Client

```python
from prisma import Prisma

# Create async client
prisma = Prisma()

# Connect
await prisma.connect()

# Query
user = await prisma.user.find_unique(
    where={'email': 'user@example.com'}
)

# Create
new_user = await prisma.user.create(
    data={
        'email': 'newuser@example.com',
        'hashedPassword': '...',
        'name': 'New User',
        'role': 'ATHLETE'
    }
)

# Update
updated = await prisma.user.update(
    where={'id': user.id},
    data={'name': 'Updated Name'}
)

# Delete
await prisma.user.delete(
    where={'id': user.id}
)

# Disconnect when done
await prisma.disconnect()
```

### Common Queries

```python
# Find many with filters
activities = await prisma.activity.find_many(
    where={
        'userId': user_id,
        'activityType': 'RUN',
        'startDate': {
            'gte': start_date,
            'lte': end_date
        }
    },
    order_by={'startDate': 'desc'},
    take=50
)

# Relations
user_with_activities = await prisma.user.find_unique(
    where={'id': user_id},
    include={
        'activities': True,
        'workouts': True
    }
)

# Aggregations
stats = await prisma.activity.aggregate(
    where={'userId': user_id},
    _sum={'distanceMeters': True},
    _avg={'avgHeartRate': True},
    _count=True
)
```

---

## 🔄 Step 7: Schema Changes

When you modify `prisma/schema.prisma`:

### 1. Update Schema File

Edit `backend/prisma/schema.prisma`

### 2. Create Migration

```bash
prisma migrate dev --name descriptive_name --schema=./prisma/schema.prisma
```

Example:
```bash
prisma migrate dev --name add_workout_notes --schema=./prisma/schema.prisma
```

### 3. Generate Client

```bash
prisma generate --schema=./prisma/schema.prisma
```

### 4. Apply in Production

```bash
prisma migrate deploy --schema=./prisma/schema.prisma
```

---

## 🧪 Testing with Prisma

### Setup Test Database

Create a separate test database in Supabase or use a local PostgreSQL:

```bash
# .env.test
DATABASE_URL="postgresql://postgres:password@localhost:5432/trainlytics_test"
```

### Run Tests

```bash
# Run with test environment
pytest app/tests/ --env=test

# With coverage
pytest app/tests/ --cov=app --cov-report=html
```

### Test Fixtures

```python
# conftest.py
import pytest
from prisma import Prisma

@pytest.fixture
async def prisma_client():
    """Provide a Prisma client for tests."""
    client = Prisma()
    await client.connect()

    yield client

    # Cleanup
    await client.user.delete_many()
    await client.disconnect()

@pytest.fixture
async def test_user(prisma_client):
    """Create a test user."""
    user = await prisma_client.user.create(
        data={
            'email': 'test@example.com',
            'hashedPassword': 'hashed_password',
            'name': 'Test User',
            'role': 'ATHLETE'
        }
    )
    return user
```

---

## 🔐 Supabase Security

### Row Level Security (RLS)

Enable RLS in Supabase Dashboard:

```sql
-- Enable RLS on activities table
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own activities
CREATE POLICY "Users can view own activities"
ON activities
FOR SELECT
USING (auth.uid()::text = user_id);

-- Policy: Users can insert their own activities
CREATE POLICY "Users can insert own activities"
ON activities
FOR INSERT
WITH CHECK (auth.uid()::text = user_id);
```

### Database Backups

Supabase automatically backs up your database:
- **Point-in-time recovery**: Available for Pro plans
- **Manual backups**: Project Settings → Database → Backups

---

## 📊 Supabase Features

### Real-time Subscriptions

```python
# Listen to activity changes (future feature)
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Subscribe to activity inserts
subscription = supabase.table('activities') \
    .on('INSERT', lambda payload: print(payload)) \
    .subscribe()
```

### Storage

Store activity files (GPX, FIT files):

```python
# Upload activity file
supabase.storage.from_('activity-files').upload(
    f'users/{user_id}/activity_{activity_id}.gpx',
    gpx_file
)

# Get public URL
url = supabase.storage.from_('activity-files').get_public_url(
    f'users/{user_id}/activity_{activity_id}.gpx'
)
```

---

## 🐛 Troubleshooting

### Error: "Can't reach database server"

✅ **Check**:
- Database URL is correct
- Supabase project is active
- IP is allowed (Supabase allows all by default)

### Error: "Prisma Client not generated"

✅ **Fix**:
```bash
prisma generate --schema=./prisma/schema.prisma
```

### Error: "Migration failed"

✅ **Fix**:
```bash
# Reset database (⚠️ deletes all data!)
prisma migrate reset --schema=./prisma/schema.prisma

# Or resolve conflicts manually
prisma migrate resolve --rolled-back [migration_name]
```

### Error: "Connection pool timeout"

✅ **Fix**: Increase connection pool size in Supabase Dashboard:
- Settings → Database → Connection Pooling
- Increase max connections

---

## 🚀 Production Checklist

- [ ] Enable SSL mode in DATABASE_URL: `?sslmode=require`
- [ ] Set connection pooling in Supabase
- [ ] Enable Row Level Security (RLS)
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Use connection pooler (PgBouncer)
- [ ] Optimize queries with indexes
- [ ] Enable query logging for slow queries

---

## 📚 Resources

- **Prisma Docs**: https://www.prisma.io/docs
- **Prisma Python**: https://prisma-client-py.readthedocs.io/
- **Supabase Docs**: https://supabase.com/docs
- **Supabase Python**: https://supabase.com/docs/reference/python

---

## 🆘 Need Help?

- **Prisma Discord**: https://discord.gg/prisma
- **Supabase Discord**: https://discord.supabase.com
- **GitHub Issues**: https://github.com/analyticsPapy/trainlytics/issues
