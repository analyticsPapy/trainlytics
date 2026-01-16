import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import AthleteDashboard from './pages/athlete/Dashboard'
import DashboardNew from './pages/athlete/DashboardNew'
import CoachDashboard from './pages/coach/Dashboard'
import Activities from './pages/athlete/Activities'
import Workouts from './pages/athlete/Workouts'
import Connections from './pages/athlete/Connections'

function App() {
  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/athlete/dashboard" element={<DashboardNew />} />
        <Route path="/athlete/dashboard-old" element={<AthleteDashboard />} />
        <Route path="/athlete/activities" element={<Activities />} />
        <Route path="/athlete/workouts" element={<Workouts />} />
        <Route path="/athlete/connections" element={<Connections />} />
        <Route path="/coach/dashboard" element={<CoachDashboard />} />
      </Routes>
    </div>
  )
}

export default App
