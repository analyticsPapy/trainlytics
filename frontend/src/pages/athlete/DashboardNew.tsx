import { useState } from 'react'
import {
  Activity,
  TrendingUp,
  Clock,
  MapPin,
  Heart,
  Zap,
  Calendar,
  BarChart3,
  Plus,
  ChevronRight,
  Trophy,
  Target
} from 'lucide-react'

export default function DashboardNew() {
  const [selectedPeriod, setSelectedPeriod] = useState('week')

  const stats = [
    {
      label: 'Total Distance',
      value: '124.8 km',
      change: '+12.5%',
      icon: MapPin,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-500/10',
      borderColor: 'border-blue-500/20'
    },
    {
      label: 'Training Time',
      value: '12h 34m',
      change: '+8.2%',
      icon: Clock,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-500/10',
      borderColor: 'border-purple-500/20'
    },
    {
      label: 'Avg Heart Rate',
      value: '145 bpm',
      change: '-2.1%',
      icon: Heart,
      color: 'from-red-500 to-red-600',
      bgColor: 'bg-red-500/10',
      borderColor: 'border-red-500/20'
    },
    {
      label: 'Fitness Score',
      value: '87',
      change: '+5.3%',
      icon: Zap,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-500/10',
      borderColor: 'border-orange-500/20'
    }
  ]

  const recentActivities = [
    {
      id: 1,
      type: 'run',
      name: 'Morning Run',
      distance: '10.5 km',
      duration: '52:34',
      pace: '5:00 /km',
      elevation: '+125m',
      time: '2 hours ago',
      heartRate: 145,
      calories: 550,
      color: 'blue'
    },
    {
      id: 2,
      type: 'ride',
      name: 'Evening Ride',
      distance: '45.2 km',
      duration: '1:45:22',
      pace: '25.8 km/h',
      elevation: '+450m',
      time: '1 day ago',
      heartRate: 138,
      calories: 980,
      color: 'green'
    },
    {
      id: 3,
      type: 'run',
      name: 'Interval Training',
      distance: '8.0 km',
      duration: '35:12',
      pace: '4:24 /km',
      elevation: '+45m',
      time: '2 days ago',
      heartRate: 162,
      calories: 450,
      color: 'purple'
    }
  ]

  const upcomingWorkouts = [
    {
      id: 1,
      title: 'Long Run',
      type: 'Endurance',
      date: 'Tomorrow',
      duration: '90 min',
      distance: '18 km',
      notes: 'Easy pace, focus on form'
    },
    {
      id: 2,
      title: 'Tempo Run',
      type: 'Speed',
      date: 'Wednesday',
      duration: '60 min',
      distance: '12 km',
      notes: 'Maintain 85% max HR'
    },
    {
      id: 3,
      title: 'Recovery Ride',
      type: 'Recovery',
      date: 'Friday',
      duration: '45 min',
      distance: '20 km',
      notes: 'Keep it easy'
    }
  ]

  const weeklyProgress = [
    { day: 'Mon', distance: 12, duration: 60 },
    { day: 'Tue', distance: 8, duration: 35 },
    { day: 'Wed', distance: 15, duration: 75 },
    { day: 'Thu', distance: 0, duration: 0 },
    { day: 'Fri', distance: 20, duration: 90 },
    { day: 'Sat', distance: 45, duration: 150 },
    { day: 'Sun', distance: 25, duration: 110 }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Welcome back, John!</h1>
              <p className="text-gray-600 mt-1">Here's your training overview for this week</p>
            </div>

            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition">
                <Plus className="h-4 w-4" />
                <span>Log Activity</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Period Selector */}
        <div className="flex space-x-2 mb-8">
          {['week', 'month', 'year'].map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                selectedPeriod === period
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              {period.charAt(0).toUpperCase() + period.slice(1)}
            </button>
          ))}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, idx) => (
            <div
              key={idx}
              className={`bg-white rounded-2xl p-6 border ${stat.borderColor} hover:shadow-lg transition-all duration-300 group`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`${stat.bgColor} p-3 rounded-xl group-hover:scale-110 transition`}>
                  <stat.icon className={`h-6 w-6 bg-gradient-to-br ${stat.color} text-transparent`} style={{ WebkitTextFillColor: 'transparent', backgroundClip: 'text' }} />
                </div>
                <span className={`text-sm font-semibold ${
                  stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.change}
                </span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Weekly Progress Chart */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">Weekly Progress</h2>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  View Details →
                </button>
              </div>

              <div className="flex items-end justify-between h-64 space-x-4">
                {weeklyProgress.map((day, idx) => {
                  const maxDistance = Math.max(...weeklyProgress.map(d => d.distance))
                  const height = (day.distance / maxDistance) * 100

                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center">
                      <div className="w-full flex flex-col items-center">
                        <div className="relative w-full h-52 flex items-end justify-center">
                          <div
                            className={`w-full bg-gradient-to-t rounded-t-xl transition-all duration-500 ${
                              day.distance > 0
                                ? 'from-blue-500 to-blue-400 hover:from-blue-600 hover:to-blue-500'
                                : 'from-gray-200 to-gray-100'
                            }`}
                            style={{ height: `${height}%` }}
                          >
                            {day.distance > 0 && (
                              <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition whitespace-nowrap">
                                {day.distance}km • {day.duration}min
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="text-sm font-medium text-gray-600 mt-2">{day.day}</div>
                      </div>
                    </div>
                  )
                })}
              </div>

              <div className="mt-6 flex items-center justify-between text-sm">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-blue-500 rounded"></div>
                    <span className="text-gray-600">Distance (km)</span>
                  </div>
                </div>
                <div className="text-gray-500">Target: 100km/week</div>
              </div>
            </div>

            {/* Recent Activities */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">Recent Activities</h2>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  View All →
                </button>
              </div>

              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div
                    key={activity.id}
                    className="group border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 flex-1">
                        <div className={`bg-${activity.color}-100 p-3 rounded-xl`}>
                          <Activity className={`h-6 w-6 text-${activity.color}-600`} />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center space-x-2">
                            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition">
                              {activity.name}
                            </h3>
                            <span className="text-xs text-gray-500">{activity.time}</span>
                          </div>

                          <div className="flex items-center space-x-6 mt-2 text-sm text-gray-600">
                            <div className="flex items-center space-x-1">
                              <MapPin className="h-4 w-4" />
                              <span>{activity.distance}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Clock className="h-4 w-4" />
                              <span>{activity.duration}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Heart className="h-4 w-4" />
                              <span>{activity.heartRate} bpm</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Zap className="h-4 w-4" />
                              <span>{activity.calories} kcal</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Goals */}
            <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-6 text-white shadow-lg">
              <div className="flex items-center space-x-2 mb-4">
                <Trophy className="h-6 w-6" />
                <h2 className="text-lg font-bold">Weekly Goal</h2>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span>Progress</span>
                  <span className="font-semibold">78%</span>
                </div>
                <div className="w-full bg-white/20 rounded-full h-3">
                  <div className="bg-white rounded-full h-3 transition-all duration-500" style={{ width: '78%' }}></div>
                </div>
              </div>

              <div className="text-sm opacity-90">
                You're 22km away from your 100km goal! Keep it up! 🎯
              </div>
            </div>

            {/* Upcoming Workouts */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <div className="flex items-center space-x-2 mb-6">
                <Calendar className="h-5 w-5 text-gray-600" />
                <h2 className="text-lg font-bold text-gray-900">Upcoming Workouts</h2>
              </div>

              <div className="space-y-4">
                {upcomingWorkouts.map((workout) => (
                  <div
                    key={workout.id}
                    className="border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer group"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition">
                          {workout.title}
                        </h3>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                            {workout.type}
                          </span>
                          <span className="text-xs text-gray-500">{workout.date}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4" />
                        <span>{workout.duration}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MapPin className="h-4 w-4" />
                        <span>{workout.distance}</span>
                      </div>
                    </div>

                    <p className="text-xs text-gray-500">{workout.notes}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h2 className="text-lg font-bold text-gray-900 mb-6">Quick Stats</h2>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Activities this month</span>
                  <span className="text-lg font-bold text-gray-900">24</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Longest run</span>
                  <span className="text-lg font-bold text-gray-900">21.1 km</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Total elevation</span>
                  <span className="text-lg font-bold text-gray-900">3,450 m</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Calories burned</span>
                  <span className="text-lg font-bold text-gray-900">12,450</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
