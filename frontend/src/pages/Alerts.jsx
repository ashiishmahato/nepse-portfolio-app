import React, { useState, useEffect } from 'react'
import { Layout, Header } from '../components/Layout'
import { AlertBadge, LoadingSpinner, EmptyState } from '../components/common'
import { alertsAPI } from '../services/api'
import { Filter, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

export const Alerts = () => {
  const [alerts, setAlerts] = useState([])
  const [filteredAlerts, setFilteredAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeOnly, setActiveOnly] = useState(true)
  const [filterType, setFilterType] = useState('all')
  
  useEffect(() => {
    loadAlerts()
    // Refresh every 30 seconds
    const interval = setInterval(loadAlerts, 30000)
    return () => clearInterval(interval)
  }, [])
  
  useEffect(() => {
    filterAlerts()
  }, [alerts, activeOnly, filterType])
  
  const loadAlerts = async () => {
    try {
      setLoading(true)
      const res = await alertsAPI.getAll(activeOnly, 100)
      setAlerts(res.data)
    } catch (error) {
      console.error('Error loading alerts:', error)
      toast.error('Failed to load alerts')
    } finally {
      setLoading(false)
    }
  }
  
  const filterAlerts = () => {
    let filtered = alerts
    
    if (filterType !== 'all') {
      filtered = filtered.filter(alert => alert.alert_type === filterType)
    }
    
    filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    setFilteredAlerts(filtered)
  }
  
  const handleMarkAsRead = async (id) => {
    try {
      await alertsAPI.markAsRead(id)
      toast.success('Alert marked as read')
      loadAlerts()
    } catch (error) {
      toast.error('Failed to mark alert as read')
    }
  }
  
  const handleDeactivate = async (id) => {
    try {
      await alertsAPI.deactivate(id)
      toast.success('Alert deactivated')
      loadAlerts()
    } catch (error) {
      toast.error('Failed to deactivate alert')
    }
  }
  
  const handleGenerateAlerts = async () => {
    try {
      setLoading(true)
      await alertsAPI.generate()
      toast.success('Alerts generated!')
      loadAlerts()
    } catch (error) {
      toast.error('Failed to generate alerts')
    } finally {
      setLoading(false)
    }
  }
  
  const alertTypes = [
    { value: 'all', label: 'All Alerts' },
    { value: 'sell_target', label: '🎯 Sell Target' },
    { value: 'buy_dip', label: '💰 Buy Dip' },
    { value: 'stop_loss', label: '⛔ Stop Loss' },
    { value: 'rsi_signal', label: '📊 RSI Signal' },
  ]
  
  if (loading && alerts.length === 0) return <Layout><LoadingSpinner /></Layout>
  
  return (
    <Layout>
      <Header
        title="Alerts"
        subtitle="Real-time stock alerts and signals"
        action={
          <button
            onClick={handleGenerateAlerts}
            className="flex items-center gap-2 bg-primary hover:bg-primary/80 px-4 py-2 rounded-lg font-medium"
          >
            <RefreshCw size={20} />
            Generate Now
          </button>
        }
      />
      
      {/* Filters */}
      <div className="glass rounded-lg p-4 mb-6">
        <div className="flex flex-wrap items-center gap-4">
          <button
            onClick={() => setActiveOnly(!activeOnly)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeOnly
                ? 'bg-primary text-white'
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            Active Only
          </button>
          
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-white/10 border border-white/20 rounded px-3 py-2"
          >
            {alertTypes.map(type => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
          
          <div className="ml-auto text-sm text-gray-400">
            {filteredAlerts.length} alert{filteredAlerts.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>
      
      {/* Alerts List */}
      {filteredAlerts.length > 0 ? (
        <div className="space-y-4">
          {filteredAlerts.map(alert => (
            <div key={alert.id} className="relative">
              <AlertBadge alert={alert} />
              <div className="flex gap-2 mt-2">
                {!alert.is_notified && (
                  <button
                    onClick={() => handleMarkAsRead(alert.id)}
                    className="text-xs bg-blue-900/20 text-blue-300 hover:bg-blue-900/30 px-3 py-1 rounded"
                  >
                    Mark as Read
                  </button>
                )}
                <button
                  onClick={() => handleDeactivate(alert.id)}
                  className="text-xs bg-gray-900/20 text-gray-300 hover:bg-gray-900/30 px-3 py-1 rounded"
                >
                  Dismiss
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No Alerts"
          description={activeOnly ? 'No active alerts at the moment' : 'No alerts found'}
        />
      )}
    </Layout>
  )
}
