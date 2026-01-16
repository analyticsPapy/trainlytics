import { Routes, Route } from 'react-router-dom'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import AthleteDashboard from './pages/athlete/Dashboard'
import CoachDashboard from './pages/coach/Dashboard'
import Activities from './pages/athlete/Activities'
import Workouts from './pages/athlete/Workouts'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/athlete/dashboard" element={<AthleteDashboard />} />
        <Route path="/athlete/activities" element={<Activities />} />
        <Route path="/athlete/workouts" element={<Workouts />} />
        <Route path="/coach/dashboard" element={<CoachDashboard />} />
        <Route path="/" element={<Login />} />
      </Routes>
    </div>
  )
}

export default App
