import { useState } from 'react'
import { Link, RefreshCw, Unlink, CheckCircle, AlertCircle, Clock } from 'lucide-react'
import ConnectorModal from '../../components/common/ConnectorModal'

export default function Connections() {
  const [selectedConnector, setSelectedConnector] = useState<any>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const connectors = [
    {
      id: 'strava',
      name: 'Strava',
      color: 'from-orange-500 to-orange-600',
      description: 'The social network for athletes',
      status: 'connected',
      lastSync: '2 minutes ago',
      activitiesCount: 156,
      features: [
        'Automatic activity sync',
        'GPS routes and maps',
        'Heart rate and power data',
        'Segment analysis',
        'Real-time updates via webhooks'
      ]
    },
    {
      id: 'garmin',
      name: 'Garmin',
      color: 'from-blue-600 to-blue-700',
      description: 'Connect your Garmin devices',
      status: 'disconnected',
      lastSync: null,
      activitiesCount: 0,
      features: [
        'All Garmin device support',
        'Detailed metrics and data',
        'Training load and recovery',
        'Sleep and wellness tracking',
        'Historical data import'
      ]
    },
    {
      id: 'polar',
      name: 'Polar',
      color: 'from-red-500 to-red-600',
      description: 'Polar Flow integration',
      status: 'connected',
      lastSync: '1 hour ago',
      activitiesCount: 89,
      features: [
        'Training Load Pro',
        'Running Index',
        'Recovery tracking',
        'Heart rate zones',
        'Automatic sync'
      ]
    },
    {
      id: 'coros',
      name: 'Coros',
      color: 'from-green-500 to-green-600',
      description: 'Connect your Coros watch',
      status: 'error',
      lastSync: '2 days ago',
      activitiesCount: 45,
      features: [
        'Training metrics',
        'GPS tracking',
        'Heart rate data',
        'Battery-efficient sync',
        'Race predictions'
      ]
    }
  ]

  const handleConnect = (connector: any) => {
    setSelectedConnector(connector)
    setIsModalOpen(true)
  }

  const handleDisconnect = async (connectorId: string) => {
    // In production, call API to disconnect
    console.log('Disconnecting:', connectorId)
  }

  const handleSync = async (connectorId: string) => {
    // In production, trigger sync
    console.log('Syncing:', connectorId)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Connected Platforms</h1>
          <p className="text-gray-600">
            Connect your fitness platforms to automatically sync your activities to Trainlytics
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-600 mb-1">Connected Platforms</div>
                <div className="text-3xl font-bold text-gray-900">
                  {connectors.filter(c => c.status === 'connected').length}
                </div>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <Link className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-600 mb-1">Total Activities</div>
                <div className="text-3xl font-bold text-gray-900">
                  {connectors.reduce((sum, c) => sum + c.activitiesCount, 0)}
                </div>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                <RefreshCw className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-gray-600 mb-1">Last Sync</div>
                <div className="text-xl font-semibold text-gray-900">
                  {connectors.find(c => c.status === 'connected')?.lastSync || 'Never'}
                </div>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Connectors Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {connectors.map((connector) => (
            <div
              key={connector.id}
              className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-300"
            >
              {/* Header */}
              <div className={`bg-gradient-to-r ${connector.color} p-6 text-white`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center">
                      <span className="text-2xl font-bold bg-gradient-to-r ${connector.color} text-transparent bg-clip-text">
                        {connector.name[0]}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{connector.name}</h3>
                      <p className="text-white/80 text-sm">{connector.description}</p>
                    </div>
                  </div>

                  <div>
                    {connector.status === 'connected' && (
                      <div className="bg-white/20 rounded-full px-3 py-1 flex items-center space-x-1">
                        <CheckCircle className="h-4 w-4" />
                        <span className="text-sm font-medium">Connected</span>
                      </div>
                    )}
                    {connector.status === 'error' && (
                      <div className="bg-red-500/20 rounded-full px-3 py-1 flex items-center space-x-1">
                        <AlertCircle className="h-4 w-4" />
                        <span className="text-sm font-medium">Error</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                {connector.status === 'connected' ? (
                  <>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div>
                        <div className="text-sm text-gray-600 mb-1">Activities Synced</div>
                        <div className="text-2xl font-bold text-gray-900">
                          {connector.activitiesCount}
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-600 mb-1">Last Sync</div>
                        <div className="text-sm font-semibold text-gray-900">
                          {connector.lastSync}
                        </div>
                      </div>
                    </div>

                    <div className="flex space-x-3">
                      <button
                        onClick={() => handleSync(connector.id)}
                        className="flex-1 bg-blue-50 text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-100 transition flex items-center justify-center space-x-2"
                      >
                        <RefreshCw className="h-4 w-4" />
                        <span>Sync Now</span>
                      </button>

                      <button
                        onClick={() => handleDisconnect(connector.id)}
                        className="flex-1 bg-red-50 text-red-600 px-4 py-2 rounded-lg font-medium hover:bg-red-100 transition flex items-center justify-center space-x-2"
                      >
                        <Unlink className="h-4 w-4" />
                        <span>Disconnect</span>
                      </button>
                    </div>
                  </>
                ) : connector.status === 'error' ? (
                  <>
                    <div className="bg-red-50 border border-red-200 rounded-xl p-4 mb-4">
                      <p className="text-sm text-red-900">
                        <strong>Connection Error:</strong> Unable to sync activities. Please reconnect your account.
                      </p>
                    </div>

                    <button
                      onClick={() => handleConnect(connector)}
                      className={`w-full bg-gradient-to-r ${connector.color} text-white px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition`}
                    >
                      Reconnect {connector.name}
                    </button>
                  </>
                ) : (
                  <>
                    <div className="mb-6">
                      <div className="text-sm font-semibold text-gray-900 mb-3">
                        Available Features:
                      </div>
                      <ul className="space-y-2">
                        {connector.features.slice(0, 3).map((feature, idx) => (
                          <li key={idx} className="flex items-center space-x-2 text-sm text-gray-700">
                            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                            <span>{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <button
                      onClick={() => handleConnect(connector)}
                      className={`w-full bg-gradient-to-r ${connector.color} text-white px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition`}
                    >
                      Connect {connector.name}
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Help Section */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-2xl p-8 border border-blue-100">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Need Help?</h2>
          <p className="text-gray-700 mb-4">
            Having trouble connecting your platforms? Check out our detailed guides:
          </p>
          <div className="flex flex-wrap gap-3">
            <a href="#" className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition">
              Connection Guide
            </a>
            <a href="#" className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition">
              Troubleshooting
            </a>
            <a href="#" className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition">
              Contact Support
            </a>
          </div>
        </div>
      </div>

      {/* Connector Modal */}
      {selectedConnector && (
        <ConnectorModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false)
            setSelectedConnector(null)
          }}
          connector={selectedConnector}
        />
      )}
    </div>
  )
}
