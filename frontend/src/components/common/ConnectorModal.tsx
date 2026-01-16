import { X, CheckCircle, Loader2, AlertCircle } from 'lucide-react'
import { useState } from 'react'

interface ConnectorModalProps {
  isOpen: boolean
  onClose: () => void
  connector: {
    name: string
    logo?: string
    color: string
    description: string
    features: string[]
  }
}

export default function ConnectorModal({ isOpen, onClose, connector }: ConnectorModalProps) {
  const [status, setStatus] = useState<'idle' | 'connecting' | 'success' | 'error'>('idle')

  if (!isOpen) return null

  const handleConnect = async () => {
    setStatus('connecting')

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000))

      // In production, redirect to OAuth URL
      // window.location.href = authUrl

      setStatus('success')

      setTimeout(() => {
        onClose()
        setStatus('idle')
      }, 2000)
    } catch (error) {
      setStatus('error')
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full mx-4 overflow-hidden">
        {/* Header */}
        <div className={`bg-gradient-to-r ${connector.color} p-6 text-white`}>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 hover:bg-white/10 rounded-lg transition"
          >
            <X className="h-5 w-5" />
          </button>

          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center">
              <span className="text-3xl font-bold bg-gradient-to-r ${connector.color} text-transparent bg-clip-text">
                {connector.name[0]}
              </span>
            </div>

            <div>
              <h2 className="text-2xl font-bold">Connect {connector.name}</h2>
              <p className="text-white/80 text-sm">{connector.description}</p>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {status === 'success' ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Successfully Connected!
              </h3>
              <p className="text-gray-600">
                Your {connector.name} account is now synced with Trainlytics
              </p>
            </div>
          ) : status === 'error' ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <AlertCircle className="h-8 w-8 text-red-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Connection Failed
              </h3>
              <p className="text-gray-600 mb-4">
                Unable to connect to {connector.name}. Please try again.
              </p>
              <button
                onClick={() => setStatus('idle')}
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Try Again
              </button>
            </div>
          ) : (
            <>
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-3">
                  What you'll get:
                </h3>
                <ul className="space-y-2">
                  {connector.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
                <p className="text-sm text-blue-900">
                  <strong>Privacy:</strong> We only access your activity data. We never post on your behalf or access personal information.
                </p>
              </div>

              <button
                onClick={handleConnect}
                disabled={status === 'connecting'}
                className={`w-full bg-gradient-to-r ${connector.color} text-white px-6 py-3 rounded-xl font-semibold hover:opacity-90 transition flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {status === 'connecting' ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    <span>Connecting...</span>
                  </>
                ) : (
                  <span>Connect {connector.name}</span>
                )}
              </button>

              <p className="text-xs text-gray-500 text-center mt-4">
                By connecting, you agree to share your activity data with Trainlytics
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
