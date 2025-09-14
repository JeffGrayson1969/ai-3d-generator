import React from 'react'
import { Clock, Loader, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

const StatusIndicator = ({ status, progress, message }) => {
  const getStatusConfig = (status) => {
    switch (status) {
      case 'queued':
        return {
          icon: Clock,
          className: 'status-queued',
          text: 'Queued'
        }
      case 'processing':
        return {
          icon: Loader,
          className: 'status-processing',
          text: 'Processing'
        }
      case 'completed':
        return {
          icon: CheckCircle,
          className: 'status-completed',
          text: 'Completed'
        }
      case 'failed':
        return {
          icon: XCircle,
          className: 'status-failed',
          text: 'Failed'
        }
      case 'cancelled':
        return {
          icon: AlertCircle,
          className: 'status-failed',
          text: 'Cancelled'
        }
      default:
        return {
          icon: Clock,
          className: 'status-queued',
          text: 'Unknown'
        }
    }
  }

  const config = getStatusConfig(status)
  const Icon = config.icon

  return (
    <div className="space-y-4">
      {/* Status Badge */}
      <div className="flex items-center justify-between">
        <div className={`status-indicator ${config.className}`}>
          <Icon
            size={16}
            className={status === 'processing' ? 'animate-spin' : ''}
          />
          <span>{config.text}</span>
        </div>

        {/* Progress Percentage */}
        {(status === 'processing' || status === 'completed') && (
          <div className="text-white font-mono text-sm">
            {progress}%
          </div>
        )}
      </div>

      {/* Progress Bar */}
      {(status === 'processing' || progress > 0) && (
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* Status Message */}
      {message && (
        <div className="text-white/70 text-sm bg-white/5 rounded-lg p-3">
          {message}
        </div>
      )}

      {/* Additional Info Based on Status */}
      {status === 'queued' && (
        <div className="text-white/50 text-xs">
          Your request is in the queue. Generation will start shortly.
        </div>
      )}

      {status === 'processing' && (
        <div className="text-white/50 text-xs">
          AI is generating your 3D model. This may take a few moments.
        </div>
      )}

      {status === 'completed' && (
        <div className="text-green-400 text-xs">
          🎉 Success! Your 3D model is ready for download.
        </div>
      )}

      {status === 'failed' && (
        <div className="text-red-400 text-xs">
          Generation failed. Please try again with a different prompt.
        </div>
      )}
    </div>
  )
}

export default StatusIndicator