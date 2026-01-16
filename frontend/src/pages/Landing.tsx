import { Link } from 'react-router-dom'
import { Activity, BarChart3, Users, Zap, CheckCircle, ArrowRight, Play } from 'lucide-react'

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation */}
      <nav className="border-b border-white/10 bg-black/20 backdrop-blur-lg fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Activity className="h-8 w-8 text-blue-400" />
              <span className="text-2xl font-bold text-white">Trainlytics</span>
            </div>

            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-300 hover:text-white transition">Features</a>
              <a href="#pricing" className="text-gray-300 hover:text-white transition">Pricing</a>
              <a href="#about" className="text-gray-300 hover:text-white transition">About</a>
            </div>

            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-300 hover:text-white transition"
              >
                Log In
              </Link>
              <Link
                to="/register"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 mb-6">
                <Zap className="h-4 w-4 text-blue-400" />
                <span className="text-sm text-blue-400 font-medium">All-in-One Training Platform</span>
              </div>

              <h1 className="text-5xl lg:text-7xl font-bold text-white mb-6 leading-tight">
                Train Smarter,
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400"> Not Harder</span>
              </h1>

              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Connect your fitness devices, analyze your performance, and collaborate with coaches.
                All your training data in one powerful platform.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/register"
                  className="group bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-semibold transition flex items-center justify-center space-x-2"
                >
                  <span>Start Free Trial</span>
                  <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition" />
                </Link>

                <button className="group bg-white/10 hover:bg-white/20 text-white px-8 py-4 rounded-lg font-semibold transition backdrop-blur-sm border border-white/10 flex items-center justify-center space-x-2">
                  <Play className="h-5 w-5" />
                  <span>Watch Demo</span>
                </button>
              </div>

              <div className="flex items-center space-x-8 mt-12 text-gray-400">
                <div>
                  <div className="text-3xl font-bold text-white">10K+</div>
                  <div className="text-sm">Active Athletes</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">500+</div>
                  <div className="text-sm">Coaches</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-white">2M+</div>
                  <div className="text-sm">Activities Tracked</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-3xl blur-3xl opacity-20"></div>
              <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 p-8 rounded-3xl border border-white/10 shadow-2xl">
                {/* Mock Dashboard Preview */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full"></div>
                      <div>
                        <div className="font-semibold text-white">John Athlete</div>
                        <div className="text-sm text-gray-400">Morning Run - 10.5 km</div>
                      </div>
                    </div>
                    <div className="text-green-400 text-sm font-medium">+2.5%</div>
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { label: 'Distance', value: '125 km', color: 'from-blue-500 to-blue-600' },
                      { label: 'Time', value: '12h 30m', color: 'from-purple-500 to-purple-600' },
                      { label: 'Elevation', value: '2,450 m', color: 'from-orange-500 to-orange-600' }
                    ].map((stat, idx) => (
                      <div key={idx} className="bg-slate-800/50 p-4 rounded-xl border border-white/5">
                        <div className={`text-2xl font-bold bg-gradient-to-r ${stat.color} text-transparent bg-clip-text`}>
                          {stat.value}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">{stat.label}</div>
                      </div>
                    ))}
                  </div>

                  <div className="h-32 bg-slate-800/50 rounded-xl border border-white/5 p-4">
                    <div className="flex items-end justify-between h-full">
                      {[40, 65, 45, 80, 60, 90, 75].map((height, idx) => (
                        <div
                          key={idx}
                          className="w-8 bg-gradient-to-t from-blue-500 to-cyan-400 rounded-t-lg transition-all hover:from-blue-400 hover:to-cyan-300"
                          style={{ height: `${height}%` }}
                        ></div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-black/20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold text-white mb-4">
              Everything You Need to Excel
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Powerful features designed for athletes and coaches to track, analyze, and optimize training.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Activity,
                title: 'Multi-Platform Sync',
                description: 'Connect Strava, Garmin, Polar, and Coros. All your activities in one place.',
                color: 'from-blue-500 to-cyan-500'
              },
              {
                icon: BarChart3,
                title: 'Advanced Analytics',
                description: 'Deep insights into your performance with AI-powered analysis and trends.',
                color: 'from-purple-500 to-pink-500'
              },
              {
                icon: Users,
                title: 'Coach Collaboration',
                description: 'Seamless communication between athletes and coaches with shared workouts.',
                color: 'from-orange-500 to-red-500'
              },
              {
                icon: CheckCircle,
                title: 'Training Plans',
                description: 'Create and follow structured training plans tailored to your goals.',
                color: 'from-green-500 to-emerald-500'
              },
              {
                icon: Zap,
                title: 'Real-time Updates',
                description: 'Instant notifications when activities sync or coaches leave feedback.',
                color: 'from-yellow-500 to-orange-500'
              },
              {
                icon: BarChart3,
                title: 'Performance Metrics',
                description: 'Track fitness, fatigue, and form with scientific training load metrics.',
                color: 'from-indigo-500 to-purple-500'
              }
            ].map((feature, idx) => (
              <div
                key={idx}
                className="group bg-slate-800/30 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-slate-800/50 hover:border-white/20 transition-all duration-300"
              >
                <div className={`w-14 h-14 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition`}>
                  <feature.icon className="h-7 w-7 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-400 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Integrations */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Connect Your Favorite Platforms
          </h2>
          <p className="text-xl text-gray-400 mb-12">
            Sync activities automatically from all major fitness platforms
          </p>

          <div className="flex flex-wrap justify-center items-center gap-8">
            {['Strava', 'Garmin', 'Polar', 'Coros'].map((platform) => (
              <div
                key={platform}
                className="bg-slate-800/50 backdrop-blur-sm border border-white/10 rounded-2xl px-12 py-6 hover:border-white/20 hover:bg-slate-800/70 transition"
              >
                <div className="text-2xl font-bold text-white">{platform}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12 text-center">
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Transform Your Training?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of athletes and coaches using Trainlytics
            </p>
            <Link
              to="/register"
              className="inline-flex items-center space-x-2 bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition"
            >
              <span>Start Your Free Trial</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <Activity className="h-6 w-6 text-blue-400" />
                <span className="text-xl font-bold text-white">Trainlytics</span>
              </div>
              <p className="text-gray-400 text-sm">
                The ultimate training analytics platform for athletes and coaches.
              </p>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white transition">Features</a></li>
                <li><a href="#" className="hover:text-white transition">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition">Integrations</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white transition">About</a></li>
                <li><a href="#" className="hover:text-white transition">Blog</a></li>
                <li><a href="#" className="hover:text-white transition">Careers</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-white font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white transition">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition">Contact</a></li>
                <li><a href="#" className="hover:text-white transition">Privacy</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-white/10 mt-12 pt-8 text-center text-gray-400 text-sm">
            © 2024 Trainlytics. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
