# Trainlytics

A comprehensive training platform for coaches and athletes, featuring activity tracking, workout planning, and performance analytics.

## Overview

Trainlytics is a full-stack web application that connects coaches with athletes, allowing seamless training management, activity synchronization from multiple fitness platforms, and detailed performance analysis.

## Features

### For Athletes
- 🏃 **Activity Tracking**: Sync activities from Strava, Garmin, Polar, and Coros
- 📅 **Workout Calendar**: View and manage scheduled workouts
- 📊 **Performance Analytics**: Track progress with detailed metrics and visualizations
- 💬 **Coach Communication**: Share activities and receive feedback from coaches
- 🎯 **Training Plans**: Follow personalized training plans created by coaches

### For Coaches
- 👥 **Athlete Management**: Manage multiple athletes and their training
- 📝 **Workout Builder**: Create structured workouts with specific targets
- 📋 **Training Plans**: Design comprehensive training plans with periodization
- 📊 **Analytics Dashboard**: Monitor athlete progress and performance trends
- 💬 **Feedback System**: Comment on activities and provide guidance

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Task Queue**: Celery + Redis
- **Authentication**: JWT (python-jose)
- **API Client**: httpx (async)

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **State Management**: Redux Toolkit
- **UI Components**: TailwindCSS + Radix UI
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Monitoring**: Sentry
- **Email**: SendGrid
- **Storage**: S3/Minio

## Documentation

- [**Architecture Documentation**](./ARCHITECTURE.md) - Comprehensive technical architecture guide
  - System architecture overview
  - Database schema and models
  - API endpoints and communication
  - External integrations (Strava, Garmin, Polar, Coros)
  - Security and authentication
  - Deployment guide

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/trainlytics.git
cd trainlytics
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start services with Docker Compose**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- Celery Flower: http://localhost:5555

## Project Structure

```
trainlytics/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── workers/      # Celery tasks
│   │   └── ...
│   └── alembic/          # Database migrations
│
├── frontend/             # React TypeScript frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── store/        # Redux store
│   │   └── ...
│   └── public/
│
├── docker-compose.yml    # Docker services configuration
├── ARCHITECTURE.md       # Detailed architecture documentation
└── README.md            # This file
```

## Development Workflow

### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements-dev.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Celery Workers

```bash
# Start Celery worker
celery -A app.workers.celery_app worker --loglevel=info

# Start Celery beat (scheduler)
celery -A app.workers.celery_app beat --loglevel=info

# Monitor with Flower
celery -A app.workers.celery_app flower
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token

### Activities
- `GET /api/v1/activities` - List activities
- `GET /api/v1/activities/{id}` - Get activity details
- `POST /api/v1/activities` - Create manual activity
- `PUT /api/v1/activities/{id}` - Update activity
- `DELETE /api/v1/activities/{id}` - Delete activity

### Workouts
- `GET /api/v1/workouts` - List workouts
- `GET /api/v1/workouts/{id}` - Get workout details
- `POST /api/v1/workouts` - Create workout
- `PUT /api/v1/workouts/{id}` - Update workout
- `DELETE /api/v1/workouts/{id}` - Delete workout

### Connectors
- `GET /api/v1/connectors/strava/connect` - Initiate Strava OAuth
- `GET /api/v1/connectors/strava/callback` - Strava OAuth callback
- `POST /api/v1/connectors/strava/sync` - Trigger manual sync
- `DELETE /api/v1/connectors/strava/disconnect` - Disconnect Strava

For complete API documentation, visit `/api/docs` when running the backend.

## External Integrations

### Strava
1. Create a Strava API application at https://www.strava.com/settings/api
2. Configure callback URL: `http://localhost:8000/api/v1/connectors/strava/callback`
3. Add credentials to `.env`:
```
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
```

### Garmin
1. Register for Garmin Health API access
2. Add credentials to `.env`

### Polar
1. Register for Polar AccessLink API
2. Add credentials to `.env`

### Coros
1. Contact Coros for API access
2. Add credentials to `.env`

## Deployment

### Production Deployment with Docker

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

### Environment Variables

Key environment variables for production:

```env
# Application
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@host:5432/trainlytics

# Redis
REDIS_URL=redis://host:6379/0

# External Services
STRAVA_CLIENT_ID=...
STRAVA_CLIENT_SECRET=...
SENTRY_DSN=...
```

See `.env.example` for complete configuration.

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support:
- Email: support@trainlytics.com
- Documentation: [ARCHITECTURE.md](./ARCHITECTURE.md)
- Issues: GitHub Issues

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced analytics (ML-based insights)
- [ ] Social features (athlete community)
- [ ] Integration with more fitness platforms
- [ ] Real-time collaboration features
- [ ] Video analysis tools

## Acknowledgments

- FastAPI for the amazing Python web framework
- Strava, Garmin, Polar, and Coros for their APIs
- The open-source community for the excellent tools and libraries
