# Trainlytics Frontend

React + TypeScript frontend for the Trainlytics training platform.

## Quick Start

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Run the development server:
```bash
npm run dev
```

The app will be available at http://localhost:5173

### With Docker

```bash
cd ..
docker-compose up frontend
```

## Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── services/     # API services
│   ├── store/        # Redux store
│   ├── types/        # TypeScript types
│   ├── utils/        # Utility functions
│   ├── App.tsx       # Main app component
│   └── main.tsx      # Entry point
└── public/           # Static assets
```

## Features

- ⚡️ Vite for fast development
- ⚛️ React 18 with TypeScript
- 🎨 TailwindCSS for styling
- 🔄 Redux Toolkit for state management
- 📡 Axios for API calls
- 🎯 React Router for navigation
